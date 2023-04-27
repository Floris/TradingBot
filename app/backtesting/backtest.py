from collections import defaultdict
from decimal import Decimal

from binance_exchange.market_data import BinanceMarketData
from config import MainConfig, MarketDataConfig, TradingConfig
from enums import OrderSide
from schemas import Signal
from signals.signal_engine import SignalEngine
from signals.signal_processor import SignalProcessor
from strategies.macd_strategy import MACDStrategy
from strategies.rsi_strategy import SimpleRsiStrategy
from utils.utils import y_m_d_to_datetime

config = MainConfig(
    symbol="BTCUSDT",
    polling_interval=0.5,
    market_data_config=MarketDataConfig(
        interval="1d",
        limit=1000,
        start_time=y_m_d_to_datetime("2020-01-01"),
        end_time=y_m_d_to_datetime("2023-01-01"),
    ),
    trading_config=TradingConfig(
        notional=Decimal("100"),
        stop_loss_percentage=Decimal("0.95"),
        take_profit_percentage=Decimal("1.10"),
    ),
)

engine = SignalEngine(
    strategies=[SimpleRsiStrategy(), MACDStrategy()],
    config=config,
)

portfolio: dict[str, Decimal] = defaultdict(Decimal)
initial_balance = Decimal(10000)
balance = initial_balance
trade_count = 0
total_profit = Decimal(0)
total_sell_signal_count = 0
total_buy_signal_count = 0


def backtest_logic(signal: Signal) -> None:
    global balance, trade_count, total_profit, total_sell_signal_count, total_buy_signal_count
    print(signal.name)
    print(signal.reason)
    print(signal.action)
    print(signal.symbol)
    print(signal.price)
    print(signal.stop_price)
    print(signal.take_profit_price)

    if signal.action == OrderSide.BUY:
        total_buy_signal_count = total_buy_signal_count + 1

        # Calculate the quantity to buy
        quantity = balance / signal.price
        # Update the portfolio
        portfolio[signal.symbol] += quantity
        # Update the balance
        balance -= quantity * signal.price

    elif signal.action == OrderSide.SELL and portfolio[signal.symbol] > 0:
        total_sell_signal_count = total_sell_signal_count + 1

        # Calculate the sell value
        sell_value = portfolio[signal.symbol] * signal.price
        # Update the balance
        balance += sell_value
        # Reset the portfolio for the symbol
        portfolio[signal.symbol] = Decimal(0)

        # Calculate the profit for this trade
        profit = sell_value - (initial_balance / trade_count)
        total_profit += profit
        print(f"Profit for this trade: {profit}")

    trade_count += 1

    print(f"Current balance: {balance}")
    print(f"Total profit: {total_profit}")
    return


def run_backtest() -> None:
    SignalProcessor(
        signal_engine=engine,
        config=config,
        market_data=BinanceMarketData(),
        signal_handler=backtest_logic,
    ).run(backtest=True)

    print(f"Final balance: {balance}")
    print(f"Total profit: {total_profit}")
    print(f"Total trades: {trade_count}")
    print(f"Total buy signals: {total_buy_signal_count}")
    print(f"Total sell signals: {total_sell_signal_count}")

    if trade_count > 0 and total_profit:
        print(f"Profit per trade: {total_profit / trade_count}")
        print(f"Profit percentage: {total_profit / initial_balance}")
