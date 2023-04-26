from time import sleep

from config import TradingBotConfig
from enums import OrderType, TimeInForce
from interfaces import CryptoExchangeProtocol, MarketDataProtocol, StrategyProtocol
from schemas import CreateOrderSchema, Signal
from utils.utils import timestamp_to_datetime


class TradingBot:
    def __init__(
        self,
        strategies: list[StrategyProtocol],
        config: TradingBotConfig,
        market_data: MarketDataProtocol,
        trade_execution_engine: CryptoExchangeProtocol,
    ) -> None:
        self.strategies = strategies
        self.config = config
        self.market_data = market_data
        self.trade_execution_engine = trade_execution_engine

    def handle_signal(self, signal: Signal) -> None:
        print(signal.dict())

        quantity = round(self.config.trading_config.notional / signal.price, 8)

        self.trade_execution_engine.create_order(
            payload=CreateOrderSchema(
                symbol=signal.symbol,
                side=signal.action,
                quantity=quantity,
                price=signal.price,
                type=OrderType.LIMIT,
                time_in_force=TimeInForce.GTC,
                client_order_id=None,
                stop_price=signal.stop_price,
                trailing_delta=None,
            )
        )

    def run(self) -> None:
        """
        Runs the trading bot.
        Executes the strategies and handle the signals.
        """

        for strategy in self.strategies:
            strategy.initialize(self.config)

        while True:

            df = self.market_data.get_klines(
                symbol=self.config.symbol,
                interval=self.config.market_data_config.interval,
                limit=self.config.market_data_config.limit,
                start_time=self.config.market_data_config.start_time,
                end_time=self.config.market_data_config.end_time,
            )

            for strategy in self.strategies:
                if trade_signal := strategy.analyze(df):
                    self.handle_signal(trade_signal)

            print("-" * 50)
            print("Open Time: ", timestamp_to_datetime(df["open_time"].iloc[-1]))
            print("Open: ", df["open"].iloc[-1])
            print("High: ", df["high"].iloc[-1])
            print("Low: ", df["low"].iloc[-1])
            print("Volume: ", df["volume"].iloc[-1])
            print("-" * 50)
            sleep(self.config.polling_interval)
