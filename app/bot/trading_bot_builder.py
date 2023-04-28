from config.config import MainConfig
from interfaces import CryptoExchangeProtocol, MarketDataProtocol, StrategyProtocol
from position_manager.position_manager import PositionManager
from position_manager.trade_executor import TradeExecutor
from signals.signal_engine import SignalEngine
from signals.signal_processor import SignalProcessor


def trading_bot_builder(
    config: MainConfig,
    strategies: list[StrategyProtocol],
    market_data_provider: MarketDataProtocol,
    crypto_exchange: CryptoExchangeProtocol | None = None,
) -> SignalProcessor:
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
