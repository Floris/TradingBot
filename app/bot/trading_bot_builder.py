from binance_exchange.market_data import BinanceMarketData
from config.config import MainConfig
from interfaces import CryptoExchangeProtocol, MarketDataProtocol, StrategyProtocol
from position_manager.position_manager import PositionManager
from position_manager.trade_executor import TradeExecutor
from signals.signal_engine import SignalEngine
from signals.signal_processor import SignalProcessor
from strategies.macd_strategy import MACDStrategy
from strategies.rsi_strategy import SimpleRsiStrategy


def trading_bot_builder(
    config: MainConfig,
    strategies: list[StrategyProtocol] | None = None,
    crypto_exchange: CryptoExchangeProtocol | None = None,
    market_data_provider: MarketDataProtocol | None = None,
) -> SignalProcessor:

    if strategies is None:
        strategies = [SimpleRsiStrategy(), MACDStrategy()]

    if market_data_provider is None:
        market_data_provider = BinanceMarketData()

    engine = SignalEngine(
        config=config,
        strategies=strategies,
    )

    position_manager = PositionManager(
        config=config,
        trade_executor=TradeExecutor(config=config, crypto_exchange=crypto_exchange),
    )

    return SignalProcessor(
        config=config,
        signal_engine=engine,
        market_data=market_data_provider,
        position_manager=position_manager,
    )
