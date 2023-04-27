from collections.abc import Callable
from time import sleep

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

    def handle_signal(self, signal: Signal) -> None:
        print(signal.dict())
        self.signal_handler(signal)

    def run_backtest(self) -> None:
        """
        Runs with historical data. Iterates through the historical data.
        Executes the strategies and handle the signals based on historical data.
        """
        self.signal_engine.initialize_strategies()

        df = self.market_data.get_klines(
            symbol=self.config.symbol,
            interval=self.config.market_data_config.interval,
            limit=self.config.market_data_config.limit,
            start_time=self.config.market_data_config.start_time,
            end_time=self.config.market_data_config.end_time,
        )

        for index in range(1, len(df)):
            df_slice = df.iloc[:index]
            signals = self.signal_engine.generate_signals(df_slice)

            for signal in signals:
                self.signal_handler(signal)

            print("-" * 50)
            print("Open Time: ", timestamp_to_datetime(df_slice["open_time"].iloc[-1]))
            print("Open: ", df_slice["open"].iloc[-1])
            print("Close: ", df_slice["close"].iloc[-1])
            print("High: ", df_slice["high"].iloc[-1])
            print("Low: ", df_slice["low"].iloc[-1])
            print("Volume: ", df_slice["volume"].iloc[-1])
            print("-" * 50)

    def run(self) -> None:
        """
        Runs the Signal Processor.
        Executes the strategies and handles the signals.
        """

        self.signal_engine.initialize_strategies()

        while True:
            df = self.market_data.get_klines(
                symbol=self.config.symbol,
                interval=self.config.market_data_config.interval,
                limit=self.config.market_data_config.limit,
                start_time=self.config.market_data_config.start_time,
                end_time=self.config.market_data_config.end_time,
            )

            signals = self.signal_engine.generate_signals(df)

            for signal in signals:
                self.handle_signal(signal)

            print("-" * 50)
            print("Open Time: ", timestamp_to_datetime(df["open_time"].iloc[-1]))
            print("Open: ", df["open"].iloc[-1])
            print("High: ", df["high"].iloc[-1])
            print("Low: ", df["low"].iloc[-1])
            print("Volume: ", df["volume"].iloc[-1])
            print("-" * 50)
            sleep(self.config.polling_interval)
