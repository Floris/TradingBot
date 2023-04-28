from binance_exchange.exchange import BinanceExchange
from binance_exchange.market_data import BinanceMarketData
from bot.trading_bot_builder import trading_bot_builder
from config.config_builder import config_builder
from strategies.macd_strategy import MACDStrategy
from strategies.rsi_strategy import SimpleRsiStrategy


def main() -> None:
    config = config_builder(
        symbol="BTCUSDT",
        interval="1h",
        limit=1000,
        start_date="2020-01-01",
        end_date="2023-01-01",
        starting_balance="10000",
        notional="100",
        max_amount_open_positions=10,
        backtest=True,
        polling_interval_weight=0.5,
    )
    trading_bot = trading_bot_builder(
        config=config,
        strategies=[SimpleRsiStrategy(), MACDStrategy()],
        crypto_exchange=BinanceExchange(),
        market_data_provider=BinanceMarketData(),
    )
    trading_bot.run()
    trading_bot.position_manager.print_stats(close_price=trading_bot.last_price)


if __name__ == "__main__":
    main()
