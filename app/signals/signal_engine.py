import pandas
from config import MainConfig
from interfaces import StrategyProtocol
from schemas import Signal


class SignalEngine:
    def __init__(
        self,
        strategies: list[StrategyProtocol],
        config: MainConfig,
    ) -> None:
        """
        Constructor for the SignalEngine class.

        Args:
            strategies (list[StrategyProtocol]): A list of StrategyProtocol objects.
            config (MainConfig): An instance of MainConfig class.
        """
        self.strategies = strategies
        self.config = config

    def initialize_strategies(self) -> None:
        """Initializes the strategies."""

        for strategy in self.strategies:
            strategy.initialize(self.config)

    def generate_signals(self, df: pandas.DataFrame) -> list[Signal]:
        """
        Generates signals from the strategies.

        Args:
            df (pandas.DataFrame): A DataFrame containing klines data.

        Returns:
            list[Signal]: A list of Signal objects.
        """

        signals = []
        for strategy in self.strategies:
            if trade_signal := strategy.analyze(df):
                signals.append(trade_signal)
        return signals
