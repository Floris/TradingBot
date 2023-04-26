from datetime import datetime
from typing import Protocol

import pandas
from config import TradingBotConfig
from enums import INTERVALS
from schemas import CreateOrderSchema, Signal


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


class CryptoExchangeProtocol(Protocol):
    def create_order(self, payload: CreateOrderSchema) -> dict:
        ...

    def get_order_by_id(self, order_id: str) -> dict:
        ...

    def get_all_orders(self) -> list[dict]:
        ...

    def cancel_order_by_id(self, order_id: str) -> None:
        ...

    def get_account(self) -> dict:
        ...


class StrategyProtocol(Protocol):
    def initialize(
        self,
        config: TradingBotConfig,
    ) -> None:
        ...

    def analyze(self, df: pandas.DataFrame) -> Signal | None:
        ...
