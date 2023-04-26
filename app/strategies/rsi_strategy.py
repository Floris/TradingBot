import time
from decimal import Decimal

import pandas
from config import TradingBotConfig
from enums import OrderSide
from schemas import Signal
from ta.momentum import rsi


class SimpleRsiStrategy:
    def initialize(
        self,
        config: TradingBotConfig,
    ) -> None:
        """
        Initialize the Simple RSI Strategy with the given configuration.
        """
        self.config = config
        self.name = "Simple RSI Strategy"
        self.last_signal_timestamp = {OrderSide.BUY: 0, OrderSide.SELL: 0}
        self.min_interval_seconds = 300
        self.overbought: int = 70
        self.oversold: int = 30
        self.window: int = 14

    def _create_signal(
        self,
        action: OrderSide,
        reason: str,
        current_price: Decimal,
        stop_price: Decimal | None = None,
        take_profit_price: Decimal | None = None,
    ) -> Signal:
        """
        Create a signal object for the given action and current price.

        :param action: The order side (OrderSide.BUY or OrderSide.SELL)
        :param current_price: The current price of the asset
        :return: A Signal object
        """

        if stop_price:
            stop_price = round(stop_price, 2)

        if take_profit_price:
            take_profit_price = round(take_profit_price, 2)

        return Signal(
            name=self.name,
            reason=reason,
            action=action,
            symbol=self.config.symbol,
            price=round(current_price, 2),
            stop_price=stop_price,
            take_profit_price=take_profit_price,
        )

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

        current_time = int(time.time())
        current_rsi = rsi(close=df["close"], window=self.window, fillna=False).iloc[-1]
        current_price = Decimal(df["close"].iloc[-1])

        if (
            current_rsi < self.oversold
            and current_time - self.last_signal_timestamp[OrderSide.BUY]
        ):
            self.last_signal_timestamp[OrderSide.BUY] = current_time
            return self._create_signal(
                action=OrderSide.BUY,
                reason="RSI value is below the oversold threshold",
                current_price=current_price,
                stop_price=Decimal(
                    current_price * self.config.trading_config.stop_loss_percentage
                ),
                take_profit_price=Decimal(
                    current_price * self.config.trading_config.take_profit_percentage
                ),
            )

        elif (
            current_rsi > self.overbought
            and current_time - self.last_signal_timestamp[OrderSide.SELL]
            > self.min_interval_seconds
        ):
            self.last_signal_timestamp[OrderSide.SELL] = current_time
            return self._create_signal(
                action=OrderSide.SELL,
                reason="RSI value is above the overbought threshold",
                current_price=current_price,
            )

        return None
