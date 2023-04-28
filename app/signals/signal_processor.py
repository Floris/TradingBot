from decimal import Decimal
from time import sleep

import pandas
from config.config import MainConfig
from interfaces import MarketDataProtocol
from position_manager.position_manager import PositionManager
from schemas import Signal
from signals.signal_engine import SignalEngine
from utils.utils import interval_to_seconds, timestamp_to_datetime


class SignalProcessor:
    def __init__(
        self,
        config: MainConfig,
        signal_engine: SignalEngine,
        market_data: MarketDataProtocol,
        position_manager: PositionManager,
    ) -> None:
        """
        Constructor for the SignalProcessor class.

        Args:
            config (MainConfig): An instance of MainConfig class.
            signal_engine (SignalEngine): An instance of SignalEngine class.
            market_data (MarketDataProtocol): An object implementing the MarketDataProtocol interface.
            position_manager (PositionManager): An object implementing the PositionManager
        """
        self.config = config
        self.signal_engine = signal_engine
        self.market_data = market_data
        self.position_manager = position_manager
        self.last_price: Decimal = Decimal(0)

    def _print_stats(self, df: pandas.DataFrame) -> None:
        """
        Prints the statistics of the last kline in the given DataFrame.

        Args:
            df (pandas.DataFrame): A DataFrame containing klines data.
        """
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

        Args:
            signals (list[Signal]): A list of Signal objects.
        """
        for signal in signals:
            self.position_manager.handle_signal(signal)

    def _get_df(self) -> pandas.DataFrame:
        """
        Gets the klines from the market data.

        Returns:
            pandas.DataFrame: A DataFrame containing klines data.
        """
        return self.market_data.get_klines(
            symbol=self.config.symbol,
            interval=self.config.market_data_config.interval,
            limit=self.config.market_data_config.limit,
            start_time=self.config.market_data_config.start_time,
            end_time=self.config.market_data_config.end_time,
        )

    def run(self) -> None:
        """
        Runs the SignalProcessor in either backtest or standard mode.

        Args:
            backtest (bool | None): A boolean indicating whether to run in backtest mode or not. Default is False.
                If None, the function will not run in backtest mode and will run in standard mode.
        Returns:
            pandas.Series: A Series containing the last kline data.

        Backtest mode:
            With backtest mode enabled, the signal processor will loop through the klines returned by the market data.
            This way, we can test our strategies on historical data.

        Standard mode:
            With backtest mode disabled, the signal processor will loop indefinitely, polling the market data for new klines.
            This way, we can test our strategies on live data.
        """
        self.signal_engine.initialize_strategies()

        interval = self.config.polling_interval_weight * interval_to_seconds(
            self.config.market_data_config.interval
        )

        if self.config.backtest:
            df = self._get_df()
            for index in range(1, len(df)):
                df_slice = df.iloc[:index]
                self._handle_signals(self.signal_engine.generate_signals(df_slice))
                self._print_stats(df_slice)

            self.last_price = Decimal(df["close"].iloc[-1])
            return

        while True:
            df = self._get_df()
            self._handle_signals(self.signal_engine.generate_signals(df))
            self._print_stats(df)
            sleep(interval)
