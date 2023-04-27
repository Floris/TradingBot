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
        self.strategies = strategies
        self.config = config

    def initialize_strategies(self) -> None:
        """Initializes the strategies."""

        for strategy in self.strategies:
            strategy.initialize(self.config)

    def generate_signals(self, df: pandas.DataFrame) -> list[Signal]:
        """
        Generates signals from the strategies.

        args:
            df: pandas.DataFrame
        returns:
            list[Signal]
        """

        signals = []
        for strategy in self.strategies:
            if trade_signal := strategy.analyze(df):
                signals.append(trade_signal)
        return signals
