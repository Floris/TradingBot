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
    starting_balance: Decimal  # starting balance
    notional: Decimal  # how much money to trade with
    max_amount_open_positions: int = 1  # maximum number of open positions
    stop_loss_percentage: Decimal | None = None  # stop loss percentage
    take_profit_percentage: Decimal | None = None  # take profit percentage


class MainConfig(BaseModel):
    backtest: bool = False  # whether to run in backtest mode
    symbol: str  # symbol to trade
    polling_interval_weight: float = 1

    market_data_config: MarketDataConfig  # market data config
    trading_config: TradingConfig  # trading config
