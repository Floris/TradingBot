from decimal import Decimal

from binance_exchange.exchange import BinanceExchange
from binance_exchange.market_data import BinanceMarketData
from config import MainConfig, MarketDataConfig, TradingConfig
from position_manager.position_manager import PositionManager
from position_manager.trade_executor import TradeExecutor
from signals.signal_engine import SignalEngine
from signals.signal_processor import SignalProcessor
from strategies.macd_strategy import MACDStrategy
from strategies.rsi_strategy import SimpleRsiStrategy
from utils.utils import y_m_d_to_datetime

config = MainConfig(
    backtest=True,
    symbol="BTCUSDT",
    polling_interval_weight=0.5,
    market_data_config=MarketDataConfig(
        interval="1h",
        limit=1000,
        start_time=y_m_d_to_datetime("2020-01-01"),
        end_time=y_m_d_to_datetime("2023-01-01"),
    ),
    trading_config=TradingConfig(
        starting_balance=Decimal("10000"),
        notional=Decimal("100"),
        max_amount_open_positions=10,
    ),
)

engine = SignalEngine(
    config=config,
    strategies=[SimpleRsiStrategy(), MACDStrategy()],
)

position_manager = PositionManager(
    config=config,
    trade_executor=TradeExecutor(config=config, crypto_exchange=BinanceExchange()),
)


TRADING_BOT = SignalProcessor(
    config=config,
    signal_engine=engine,
    market_data=BinanceMarketData(),
    position_manager=position_manager,
)
