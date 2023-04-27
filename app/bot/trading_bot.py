from decimal import Decimal

from binance_exchange.market_data import BinanceMarketData
from config import MainConfig, MarketDataConfig, TradingConfig
from signals.signal_engine import SignalEngine
from signals.signal_processor import SignalProcessor
from strategies.macd_strategy import MACDStrategy
from strategies.rsi_strategy import SimpleRsiStrategy

config = MainConfig(
    symbol="BTCUSDT",
    polling_interval=0.5,
    market_data_config=MarketDataConfig(interval="15m", limit=1000),
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

TRADING_BOT = SignalProcessor(
    signal_engine=engine,
    config=config,
    market_data=BinanceMarketData(),
    signal_handler=lambda x: print(x.dict()),
)
