from collections import defaultdict
from decimal import Decimal
from typing import TypedDict
from uuid import uuid4

from config.config import MainConfig
from enums import OrderSide
from position_manager.trade_executor import TradeExecutor
from schemas import OrderSchema, Signal


class Position(TypedDict):
    symbol: str
    entry_price: Decimal
    stop_loss_price: Decimal
    take_profit_price: Decimal
    quantity: Decimal
    order_id: str


class PositionManager:
    def __init__(self, config: MainConfig, trade_executor: TradeExecutor):
        """
        Initializes a new PositionManager instance.

        Args:
        - config: MainConfig instance, containing the main configuration.
        - trade_executor: TradeExecutor instance, which is responsible for executing trades.
        """
        self.config = config
        self.trade_executor = trade_executor

        self.active_positions: dict[str, Position] = defaultdict()
        self.portfolio: dict[str, Decimal] = defaultdict(Decimal)
        self.balance = self.config.trading_config.starting_balance

        self.total_sell_signal_count: int = 0
        self.total_sell_orders_count: int = 0
        self.total_buy_signal_count: int = 0
        self.total_buy_orders_count: int = 0

        self.open_positions: int = 0

    def _close_position(self, position_id: str, signal: Signal) -> None:
        """
        Closes an active position.

        Args:
        - position_id: str, the ID of the position to be closed.
        - signal: Signal instance, the signal that triggered the closing of the position.
        """
        if position_id not in self.active_positions:
            return

        position = self.active_positions[position_id]

        sell_order = self.trade_executor.submit_order(
            symbol=position["symbol"],
            side=OrderSide.SELL,
            quantity=position["quantity"],
            price=signal.price,
        )

        self._update_balance_and_portfolio(position, sell_order)
        self.open_positions -= 1
        del self.active_positions[position_id]

    def _update_balance_and_portfolio(
        self, position: Position, sell_order: OrderSchema
    ) -> None:
        """
        Updates the balance and the portfolio of the PositionManager.

        Args:
        - position: dict, the position data.
        - sell_order: Any, the sell order data.
        """
        sell_value = sell_order.executed_qty * sell_order.price
        self.balance += sell_value
        self.portfolio[position["symbol"]] -= position["quantity"]

    def generate_position_id(self) -> str:
        """
        Generates a new position ID.

        Returns:
        - A string representing a new UUID.
        """
        return str(uuid4())

    def _manage_counters(self, signal: Signal) -> None:
        """
        Manages the counters for the PositionManager.

        Args:
        - signal: Signal instance, the signal that triggered the counter update.
        """
        if signal.action == OrderSide.BUY:
            self.total_buy_signal_count += 1
            return

        self.total_sell_signal_count += 1

    def handle_signal(self, signal: Signal) -> None:
        """
        Handles a new signal.

        Args:
        - signal: Signal instance, the signal to be handled.
        """
        self._manage_counters(signal)

        notional = self.config.trading_config.notional

        if signal.action == OrderSide.BUY:
            self._handle_buy_signal(signal, notional)
        elif signal.action == OrderSide.SELL:
            self._handle_sell_signal(signal)

        print(f"Current balance: {self.balance}")

    def _handle_buy_signal(self, signal: Signal, notional: Decimal) -> None:
        """
        Handles a new buy signal.

        Args:
        - signal: Signal instance, the buy signal to be handled.
        - notional: Decimal, the notional value for the trade.
        """
        if self.open_positions > self.config.trading_config.max_amount_open_positions:
            return

        self.open_positions += 1

        # Calculate the quantity to buy
        quantity = notional / signal.price

        buy_order = self.trade_executor.submit_order(
            symbol=signal.symbol,
            side=OrderSide.BUY,
            quantity=quantity,
            price=signal.price,
        )

        # Update the portfolio
        self.portfolio[signal.symbol] += quantity

        # Update the balance
        self.balance -= notional

        # Add the position to active_positions
        self.active_positions[self.generate_position_id()] = {
            "symbol": signal.symbol,
            "entry_price": signal.price,
            "stop_loss_price": signal.stop_price,
            "take_profit_price": signal.take_profit_price,
            "quantity": quantity,
            "order_id": buy_order.order_id,
        }

        self.total_buy_orders_count += 1

    def _handle_sell_signal(self, signal: Signal) -> None:
        """
        Handles a new sell signal.

        Args:
        - signal: Signal instance, the sell signal to be handled.
        """
        if len(self.active_positions.keys()) == 0:
            return

        positions_for_symbol = [
            (position_id, position_data)
            for position_id, position_data in self.active_positions.items()
            if position_data["symbol"] == signal.symbol
        ]

        if positions_for_symbol:
            oldest_position_id, _ = positions_for_symbol[0]
            self._close_position(position_id=oldest_position_id, signal=signal)
            self.total_sell_orders_count += 1

    def print_stats(
        self,
        close_price: Decimal,
    ) -> None:
        """
        Prints the statistics for the PositionManager.

        Args:
        - close_price: Decimal, the closing price of the asset.
        """
        final_portfolio_value = sum(
            position["quantity"] * close_price
            for position in self.active_positions.values()
        )
        balance_plus_portfolio_value = self.balance + final_portfolio_value
        total_profit = (
            balance_plus_portfolio_value - self.config.trading_config.starting_balance
        )

        print(f"Sum open positions Value: {round(final_portfolio_value,2)}")
        print(f"Open positions count: {self.open_positions}")

        print(f"Final cash balance: {self.balance}")
        print(
            f"Final cash balance + sum open positions value: {round(balance_plus_portfolio_value,2)}"
        )

        print(f"Total profit: {round(total_profit,2)}")

        print(f"Total buy signals: {self.total_buy_signal_count}")
        print(f"Total executed buy orders: {self.total_buy_orders_count}")

        print(f"Total sell signals: {self.total_sell_signal_count}")
        print(f"Total executed sell orders: {self.total_sell_orders_count}")
