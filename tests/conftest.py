from decimal import Decimal

import pytest

from app.config.config import MainConfig, MarketDataConfig, TradingConfig
from app.position_manager.position_manager import PositionManager
from app.position_manager.trade_executor import TradeExecutor


@pytest.fixture()
def trading_bot_config() -> MainConfig:
    return MainConfig(
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
