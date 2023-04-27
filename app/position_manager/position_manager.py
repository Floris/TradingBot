from collections import defaultdict
from decimal import Decimal
from typing import Any
from uuid import uuid4

from config import MainConfig
from enums import OrderSide
from schemas import Signal


class PositionManager:
    def __init__(self, config: MainConfig):
        self.config = config
        self.active_positions: dict[str, dict[str, Any]] = defaultdict(dict)
        self.portfolio: dict[str, Decimal] = defaultdict(Decimal)
        self.balance = self.config.trading_config.starting_balance
        self.trade_count = 0
        self.total_profit = Decimal("0")
        self.total_sell_signal_count = 0
        self.total_buy_signal_count = 0

    def generate_position_id(self) -> str:
        return str(uuid4())

    def update_position(self, position_id: str, updated_values: dict) -> None:
        if position_id in self.active_positions:
            self.active_positions[position_id].update(updated_values)

    def handle_signal(self, signal: Signal) -> None:

        print(signal.name)
        print(signal.reason)
        print(signal.action)
        print(signal.symbol)
        print(signal.price)
        print(signal.stop_price)
        print(signal.take_profit_price)

        notional = self.config.trading_config.notional

        if signal.action == OrderSide.BUY:
            self.trade_count += 1
            self.total_buy_signal_count = self.total_buy_signal_count + 1

            # Calculate the quantity to buy
            quantity = notional / signal.price

            # Update the portfolio
            self.portfolio[signal.symbol] += quantity

            # Update the balance
            self.balance -= notional

            # Add the position to active_positions
            position_id = self.generate_position_id()
            self.active_positions[position_id] = {
                "symbol": signal.symbol,
                "entry_price": signal.price,
                "stop_loss_price": signal.stop_price,
                "take_profit_price": signal.take_profit_price,
                "quantity": quantity,
            }

        elif signal.action == OrderSide.SELL and self.portfolio[signal.symbol] > 0:
            self.trade_count += 1
            self.total_sell_signal_count = self.total_sell_signal_count + 1

            # Calculate the sell value
            sell_value = self.portfolio[signal.symbol] * signal.price

            # Update the balance
            self.balance += sell_value

            # Reset the portfolio for the symbol
            self.portfolio[signal.symbol] = Decimal(0)

            # Remove the position from active_positions
            for position_id in list(self.active_positions):
                if self.active_positions[position_id]["symbol"] == signal.symbol:
                    del self.active_positions[position_id]

            # Calculate the profit for this trade
            profit = sell_value - notional
            self.total_profit += profit
            print(f"Profit for this trade: {profit}")

        print(f"Current balance: {self.balance}")
        print(f"Total profit: {self.total_profit}")
        return

    def print_stats(self) -> None:
        # Calculate the final portfolio value
        final_portfolio_value = Decimal(0)
        for position in self.active_positions.values():
            final_portfolio_value += position["quantity"] * position["entry_price"]

        print(f"Open positions Value: {round(final_portfolio_value,2)}")
        print(f"Final balance: {self.balance}")
        print(f"Total profit: {self.total_profit}")
        print(f"Total trades: {self.trade_count}")
        print(f"Total buy signals: {self.total_buy_signal_count}")
        print(f"Total sell signals: {self.total_sell_signal_count}")

        if self.trade_count > 0 and self.total_profit:
            print(f"Profit per trade: {self.total_profit / self.trade_count}")
            print(
                f"Profit percentage: {self.total_profit / self.config.trading_config.starting_balance * 100}"
            )
