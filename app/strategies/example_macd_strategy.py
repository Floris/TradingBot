from decimal import Decimal

import pandas as pd
from config.config import MainConfig
from enums import OrderSide
from schemas import Signal
from strategies.base_strategy import BaseStrategy
from ta.trend import MACD


class MACDStrategy(BaseStrategy):
    def initialize(self, config: MainConfig) -> None:
        """
        Initialize the MACD Strategy with the given configuration.
        """
        super().initialize(config)
        self.name = "MACD Strategy"

        self.n_fast: int = 12
        self.n_slow: int = 26
        self.n_sign: int = 9

    def analyze(self, df: pd.DataFrame) -> Signal | None:
        """
        Analyze the given dataframe and generate buy or sell signals based on the MACD strategy.

        A buy signal is created when the MACD line crosses above the signal line,
        indicating that the asset's price may start to rise and it's a good time to buy.

        A sell signal is created when the MACD line crosses below the signal line,
        indicating that the asset's price may start to fall and it's a good time to sell.

        :param df: A pandas DataFrame containing the asset's historical data
        :return: A Signal object if a buy or sell signal is generated, None otherwise
        """

        macd = MACD(
            close=df["close"],
            window_fast=self.n_fast,
            window_slow=self.n_slow,
            window_sign=self.n_sign,
            fillna=False,
        )

        macd_line = macd.macd()
        if len(macd_line) < 2:
            return None

        signal_line = macd.macd_signal()

        current_macd = macd_line.iloc[-1]
        previous_macd = macd_line.iloc[-2]
        current_signal = signal_line.iloc[-1]
        previous_signal = signal_line.iloc[-2]

        current_price = Decimal(df["close"].iloc[-1])

        if current_macd > current_signal and previous_macd <= previous_signal:
            return self._create_signal(
                action=OrderSide.BUY,
                reason="MACD line crossed above signal line",
                current_price=current_price,
            )

        elif current_macd < current_signal and previous_macd >= previous_signal:
            return self._create_signal(
                action=OrderSide.SELL,
                reason="MACD line crossed below signal line",
                current_price=current_price,
            )

        return None
