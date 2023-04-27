from collections.abc import Callable
from time import sleep

import pandas
from config import MainConfig
from interfaces import MarketDataProtocol
from schemas import Signal
from signals.signal_engine import SignalEngine
from utils.utils import timestamp_to_datetime


class SignalProcessor:
    def __init__(
        self,
        signal_engine: SignalEngine,
        config: MainConfig,
        market_data: MarketDataProtocol,
        signal_handler: Callable[[Signal], None],
    ) -> None:
        self.signal_engine = signal_engine
        self.config = config
        self.market_data = market_data
        self.signal_handler = signal_handler

    def _print_stats(self, df: pandas.DataFrame) -> None:
        print("-" * 50)
        print("Open Time: ", timestamp_to_datetime(df["open_time"].iloc[-1]))
        print("Open: ", df["open"].iloc[-1])
        print("Close: ", df["close"].iloc[-1])
        print("High: ", df["high"].iloc[-1])
        print("Low: ", df["low"].iloc[-1])
        print("Volume: ", df["volume"].iloc[-1])
        print("-" * 50)

    def _handle_signals(self, signals: list[Signal]) -> None:
        """
        Handles the signals.
        """
        for signal in signals:
            self.signal_handler(signal)

    def _get_df(self) -> pandas.DataFrame:
        """
        Gets the klines from the market data.
        """
        return self.market_data.get_klines(
            symbol=self.config.symbol,
            interval=self.config.market_data_config.interval,
            limit=self.config.market_data_config.limit,
            start_time=self.config.market_data_config.start_time,
            end_time=self.config.market_data_config.end_time,
        )

    def run(self, backtest: bool | None = False) -> None:
        self.signal_engine.initialize_strategies()

        if backtest:
            df = self._get_df()
            for index in range(1, len(df)):
                df_slice = df.iloc[:index]
                self._handle_signals(self.signal_engine.generate_signals(df_slice))
                self._print_stats(df_slice)
            return

        while True:
            df = self._get_df()
            self._handle_signals(self.signal_engine.generate_signals(df))
            self._print_stats(df)
            sleep(self.config.polling_interval)
