from typing import Protocol

import pandas
from config import TradingBotConfig
from schemas import CreateOrderSchema, Signal


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
