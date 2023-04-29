import os
from datetime import datetime

import pandas
from binance import spot
from enums import INTERVALS
from ta.utils import dropna
from utils.utils import datetime_to_timestamp

client = spot.Spot(
    api_key=os.getenv("BINANCE_API_KEY", None),
    api_secret=os.getenv("BINANCE_SECRET", None),
)

BINANCE_KLINE_COLUMNS = [
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "quote_asset_volume",
    "number_of_trades",
    "taker_buy_base_asset_volume",
    "taker_buy_quote_asset_volume",
    "ignore",
]


class BinanceMarketData:
    def get_klines(
        self,
        symbol: str,
        interval: INTERVALS,
        limit: int,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> pandas.DataFrame:

        binance_start_time = None
        if start_time:
            binance_start_time = datetime_to_timestamp(start_time)

        binance_end_time = None
        if end_time:
            binance_end_time = datetime_to_timestamp(end_time)

        klines = client.klines(
            symbol=symbol,
            interval=interval,
            startTime=binance_start_time,
            endTime=binance_end_time,
            limit=limit,
        )

        df = pandas.DataFrame(
            klines,
            columns=BINANCE_KLINE_COLUMNS,
        )

        # Convert values to float
        df = df.astype(
            {
                "open": float,
                "high": float,
                "low": float,
                "close": float,
                "volume": float,
                "quote_asset_volume": float,
                "taker_buy_base_asset_volume": float,
                "taker_buy_quote_asset_volume": float,
            }
        )

        return dropna(df)
