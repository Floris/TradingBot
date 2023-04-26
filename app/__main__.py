from decimal import Decimal

from binance_exchange.exchange import BinanceExchange
from binance_exchange.market_data import BinanceMarketData
from bot.trading_bot import TradingBot
from config import MarketDataConfig, TradingBotConfig, TradingConfig
from strategies.macd_strategy import MACDStrategy
from strategies.rsi_strategy import SimpleRsiStrategy


def main() -> None:
    config = TradingBotConfig(
        symbol="BTCUSDT",
        polling_interval=0.5,
        market_data_config=MarketDataConfig(interval="15m", limit=1000),
        trading_config=TradingConfig(
            notional=Decimal("100"),
            stop_loss_percentage=Decimal("0.95"),
            take_profit_percentage=Decimal("1.10"),
        ),
    )

    TradingBot(
        strategies=[SimpleRsiStrategy(), MACDStrategy()],
        config=config,
        market_data=BinanceMarketData(),
        trade_execution_engine=BinanceExchange(),
    ).run()


if __name__ == "__main__":
    main()
