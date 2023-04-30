from abc import ABC, abstractmethod
from decimal import Decimal

import pandas
from config.config import MainConfig
from enums import OrderSide
from schemas import Signal


class BaseStrategy(ABC):
    def initialize(self, config: MainConfig) -> None:
        self.config = config

    @abstractmethod
    def analyze(self, df: pandas.DataFrame) -> Signal | None:
        pass

    def _create_signal(
        self, action: OrderSide, reason: str, current_price: Decimal
    ) -> Signal:
        return Signal(
            name=self.__class__.__name__,
            reason=reason,
            action=action,
            symbol=self.config.symbol,
            price=round(current_price, 2),
        )
