import os
from decimal import Decimal

from binance_exchange.exchange import BinanceExchange
from binance_exchange.market_data import BinanceMarketData
from bot.trading_bot_builder import trading_bot_builder
from config.config_builder import config_builder
from dotenv import load_dotenv
from utils.utils import get_instance_from_mapping, get_strategy_instances

load_dotenv()


CRYPTO_EXCHANGE_MAPPING = {
    "BinanceExchange": BinanceExchange,
    # Extra crypto exchanges can be added here...
}


MARKET_DATA_PROVIDER_MAPPING = {
    "BinanceMarketData": BinanceMarketData,
    # Extra market data providers can be added here...
}


def main() -> None:
    strategies = get_strategy_instances()

    crypto_exchange_instances = get_instance_from_mapping(
        CRYPTO_EXCHANGE_MAPPING, "CRYPTO_EXCHANGE"
    )
    market_data_provider_instances = get_instance_from_mapping(
        MARKET_DATA_PROVIDER_MAPPING, "MARKET_DATA_PROVIDER"
    )

    config = config_builder(
        symbol=os.getenv("SYMBOL", "BTCUSDT"),
        interval=os.getenv("INTERVAL", "4h"),
        limit=int(os.getenv("LIMIT", "1000")),
        starting_balance=os.getenv("STARTING_BALANCE", "0"),
        notional=os.getenv("NOTIONAL", "0"),
        max_amount_open_positions=int(os.getenv("MAX_OPEN_POSITIONS", "4")),
        backtest=os.getenv("BACKTEST", "True").lower() == "true",
        polling_interval_weight=float(os.getenv("POLLING_INTERVAL_WEIGHT", "1")),
        start_date=os.getenv("START_DATE", None),
        end_date=os.getenv("END_DATE", None),
    )
    trading_bot = trading_bot_builder(
        config=config,
        strategies=strategies,
        crypto_exchange=crypto_exchange_instances,
        market_data_provider=market_data_provider_instances,
    )

    trading_bot.run()
    trading_bot.position_manager.print_stats(
        close_price=Decimal(trading_bot.df["close"].iloc[-1])
    )


if __name__ == "__main__":
    main()
