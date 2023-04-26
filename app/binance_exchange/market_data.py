from datetime import datetime

import pandas
from binance import spot
from enums import INTERVALS
from ta.utils import dropna

from settings import settings

client = spot.Spot(api_key=settings.BINANCE_API_KEY, api_secret=settings.BINANCE_SECRET)

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
        klines = client.klines(
            symbol=symbol,
            interval=interval,
            startTime=start_time,
            endTime=end_time,
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
