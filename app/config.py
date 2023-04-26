from datetime import datetime
from decimal import Decimal

from enums import INTERVALS
from pydantic import BaseModel


class MarketDataConfig(BaseModel):
    interval: INTERVALS  # interval of the candles
    limit: int  # number of candles to fetch
    start_time: datetime | None = None  # start time of the candles
    end_time: datetime | None = None  # end time of the candles


class TradingConfig(BaseModel):
    notional: Decimal  # how much money to trade with
    stop_loss_percentage: Decimal = Decimal("0.95")  # stop loss percentage
    take_profit_percentage: Decimal = Decimal("1.10")  # take profit percentage


class TradingBotConfig(BaseModel):
    symbol: str  # symbol to trade
    polling_interval: float  # how often to poll for new data

    market_data_config: MarketDataConfig  # market data config
    trading_config: TradingConfig  # trading config
