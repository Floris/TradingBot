from decimal import Decimal

from config.config import MainConfig, MarketDataConfig, TradingConfig
from enums import INTERVALS
from utils.utils import y_m_d_to_datetime


def config_builder(
    symbol: str = "BTCUSDT",
    interval: INTERVALS = "1h",
    limit: int = 1000,
    starting_balance: str = "10000",
    notional: str = "100",
    max_amount_open_positions: int = 10,
    backtest: bool = True,
    polling_interval_weight: float = 0.5,
    start_date: str | None = None,
    end_date: str | None = None,
) -> MainConfig:
    market_data_config = MarketDataConfig(
        interval=interval,
        limit=limit,
        start_time=y_m_d_to_datetime(start_date) if start_date else None,
        end_time=y_m_d_to_datetime(end_date) if end_date else None,
    )

    trading_config = TradingConfig(
        starting_balance=Decimal(starting_balance),
        notional=Decimal(notional),
        max_amount_open_positions=max_amount_open_positions,
    )

    return MainConfig(
        backtest=backtest,
        symbol=symbol,
        polling_interval_weight=polling_interval_weight,
        market_data_config=market_data_config,
        trading_config=trading_config,
    )
