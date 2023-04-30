from decimal import Decimal

import pandas
from config.config import MainConfig
from enums import OrderSide
from schemas import Signal
from strategies.base_strategy import BaseStrategy
from ta.momentum import rsi


class SimpleRsiStrategy(BaseStrategy):
    def initialize(
        self,
        config: MainConfig,
    ) -> None:
        """
        Initialize the Simple RSI Strategy with the given configuration.
        """
        super().initialize(config)
        self.name = "Simple RSI Strategy"

        self.overbought: int = 70
        self.oversold: int = 30
        self.window: int = 14

    def analyze(self, df: pandas.DataFrame) -> Signal | None:
        """
        Analyze the given dataframe and generate buy or sell signals based on the RSI strategy.

        A buy signal is created when the RSI value is below the oversold threshold,
        indicating that the asset is potentially undervalued and it's a good time to buy.

        A sell signal is created when the RSI value is above the overbought threshold,
        indicating that the asset is potentially overvalued and it's a good time to sell.

        :param df: A pandas DataFrame containing the asset's historical data
        :return: A Signal object if a buy or sell signal is generated, None otherwise
        """

        current_rsi = rsi(close=df["close"], window=self.window, fillna=False).iloc[-1]
        current_price = Decimal(df["close"].iloc[-1])

        if current_rsi < self.oversold:
            return self._create_signal(
                action=OrderSide.BUY,
                reason="RSI value is below the oversold threshold",
                current_price=current_price,
            )

        elif current_rsi > self.overbought:
            return self._create_signal(
                action=OrderSide.SELL,
                reason="RSI value is above the overbought threshold",
                current_price=current_price,
            )

        return None
