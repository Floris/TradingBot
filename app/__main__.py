from bot.trading_bot import TRADING_BOT


def main() -> None:
    TRADING_BOT.run()

    # config = MainConfig(
    #     symbol="BTCUSDT",
    #     polling_interval=0.5,
    #     market_data_config=MarketDataConfig(interval="15m", limit=1000),
    #     trading_config=TradingConfig(
    #         notional=Decimal("100"),
    #         stop_loss_percentage=Decimal("0.95"),
    #         take_profit_percentage=Decimal("1.10"),
    #     ),
    # )

    # BacktestEngine(
    #     strategies=[MACDStrategy()],
    #     config=config,
    #     market_data=BinanceMarketData(),
    # ).run()

    return


if __name__ == "__main__":
    main()
