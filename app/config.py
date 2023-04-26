from datetime import datetime
from decimal import Decimal

from enums import INTERVALS
from pydantic import BaseModel


class MarketDataConfig(BaseModel):
    interval: INTERVALS
    limit: int
    start_time: datetime | None = None
    end_time: datetime | None = None


class TradingConfig(BaseModel):
    notional: Decimal
    stop_loss_percentage: Decimal = Decimal("0.95")
    take_profit_percentage: Decimal = Decimal("1.10")


class TradingBotConfig(BaseModel):
    symbol: str
    polling_interval: float

    market_data_config: MarketDataConfig
    trading_config: TradingConfig
