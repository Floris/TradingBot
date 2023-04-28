from datetime import datetime

import pandas as pd

from app.config.config import MainConfig
from app.enums import INTERVALS
from app.interfaces import MarketDataProtocol


class MockMarketData(MarketDataProtocol):
    def __init__(self, config: MainConfig) -> None:
        self.config = config

    def get_klines(
        self,
        symbol: str,
        interval: INTERVALS,
        limit: int,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> pd.DataFrame:
        """
        Get klines from the exchange.

        Args:
            symbol (str): The symbol to get klines for.
            interval (INTERVALS): The interval to get klines for.
            limit (int): The maximum number of klines to return.
            start_time (datetime | None): The start time for the klines. If None, will use the earliest available time.
            end_time (datetime | None): The end time for the klines. If None, will use the latest available time.

        Returns:
            pandas.DataFrame: A DataFrame containing klines data.
        """
        data = {
            "open_time": [1209459200000, 1409459200000, 1509459201000, 1609459201000],
            "open": [5324, 9000.12, 9100.00, 9600.12],
            "close": [7545, 9500, 9000, 10500],
            "high": [7233.3, 9500.61, 9600.12, 10500],
            "low": [0.12312, 9000.22, 9100.34, 9500],
            "volume": [23, 100.16, 200.77, 31.43],
        }

        return pd.DataFrame(data).sort_values(by="open_time", ascending=True)
