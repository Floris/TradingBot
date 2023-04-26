from datetime import datetime
from typing import Protocol

import pandas
from enums import INTERVALS


class MarketDataProtocol(Protocol):
    def get_klines(
        self,
        symbol: str,
        interval: INTERVALS,
        limit: int,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> pandas.DataFrame:
        """Get klines from the exchange. Return a pandas DataFrame."""
        ...
