from decimal import Decimal

import pytest

from app.config import MainConfig, MarketDataConfig, TradingConfig


@pytest.fixture()
def trading_bot_config() -> MainConfig:
    return MainConfig(
        symbol="BTCUSDT",
        polling_interval=0.5,
        market_data_config=MarketDataConfig(interval="15m", limit=1000),
        trading_config=TradingConfig(
            starting_balance=Decimal("10000"),
            notional=Decimal("100"),
            stop_loss_percentage=Decimal("0.95"),
            take_profit_percentage=Decimal("1.10"),
        ),
    )
