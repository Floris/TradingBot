import pandas
from config.config import MainConfig
from interfaces import StrategyProtocol
from schemas import Signal


class SignalEngine:
    def __init__(
        self,
        config: MainConfig,
        strategies: list[StrategyProtocol],
    ) -> None:
        """
        Constructor for the SignalEngine class.

        Args:
            config (MainConfig): An instance of MainConfig class.
            strategies (list[StrategyProtocol]): A list of StrategyProtocol objects.
        """
        self.config = config
        self.strategies = strategies

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
