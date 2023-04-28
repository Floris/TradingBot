from decimal import Decimal

import pandas as pd
import pytest

from app.config.config import MainConfig, MarketDataConfig, TradingConfig
from app.interfaces import StrategyProtocol
from app.position_manager.position_manager import PositionManager
from app.position_manager.trade_executor import TradeExecutor
from app.schemas import OrderSide, Signal
from app.signals.signal_engine import SignalEngine
from app.signals.signal_processor import SignalProcessor
from tests.mocked_data import MockMarketData


@pytest.fixture()
def trading_bot_config() -> MainConfig:
    return MainConfig(
        backtest=True,
        symbol="BTCUSDT",
        polling_interval_weight=0.5,
        market_data_config=MarketDataConfig(interval="15m", limit=1000),
        trading_config=TradingConfig(
            max_amount_open_positions=3,
            starting_balance=Decimal("10000"),
            notional=Decimal("100"),
            stop_loss_percentage=Decimal("0.95"),
            take_profit_percentage=Decimal("1.10"),
        ),
    )


@pytest.fixture
def position_manager(trading_bot_config: MainConfig) -> PositionManager:
    trade_executor = TradeExecutor(config=trading_bot_config, crypto_exchange=None)
    return PositionManager(config=trading_bot_config, trade_executor=trade_executor)


class MockStrategy(StrategyProtocol):
    def initialize(self, config: MainConfig) -> None:
        pass

    def analyze(self, df: pd.DataFrame) -> Signal | None:
        if df.iloc[-1]["close"] > 10000:
            return Signal(
                name="mock_strategy",
                reason="price_above_10000",
                symbol="BTCUSDT",
                action=OrderSide.BUY,
                price=df.iloc[-1]["close"],
                stop_price=None,
                take_profit_price=None,
            )
        return None


@pytest.fixture
def signal_engine(trading_bot_config: MainConfig) -> SignalEngine:
    strategies = [MockStrategy()]
    return SignalEngine(config=trading_bot_config, strategies=strategies)


@pytest.fixture
def signal_processor(
    trading_bot_config: MainConfig, position_manager: PositionManager
) -> SignalProcessor:
    signal_engine = SignalEngine(config=trading_bot_config, strategies=[MockStrategy()])
    market_data = MockMarketData(trading_bot_config)
    return SignalProcessor(
        trading_bot_config, signal_engine, market_data, position_manager
    )
