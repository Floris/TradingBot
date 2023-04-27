from config import MainConfig
from interfaces import MarketDataProtocol, StrategyProtocol
from schemas import Signal


class BacktestEngine:
    def __init__(
        self,
        strategies: list[StrategyProtocol],
        config: MainConfig,
        market_data: MarketDataProtocol,
    ) -> None:
        self.strategies = strategies
        self.config = config
        self.market_data = market_data

    def run(self) -> None:
        """
        Runs the backtest engine.
        Executes the strategies and records the signals.
        """

        for strategy in self.strategies:
            strategy.initialize(self.config)

        df = self.market_data.get_klines(
            symbol=self.config.symbol,
            interval=self.config.market_data_config.interval,
            limit=self.config.market_data_config.limit,
            start_time=self.config.market_data_config.start_time,
            end_time=self.config.market_data_config.end_time,
        )

        # Store signals generated during the backtest
        signals: list[Signal] = []

        for index, row in df.iterrows():
            current_row_df = df.loc[:index]

            for strategy in self.strategies:
                if trade_signal := strategy.analyze(current_row_df):
                    signals.append(trade_signal)

        self.evaluate_performance(signals)

    def evaluate_performance(self, signals: list[Signal]) -> None:
        """
        Evaluate the performance of the strategies based on the generated signals.

        :param signals: A list of Signal objects generated during the backtest
        """
        # Calculate performance metrics based on the signals, such as profit, drawdown, win rate, etc.
        # You can use the performance evaluation methods from the Pyfolio, Backtrader or other libraries
        pass
