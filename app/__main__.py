from bot.trading_bot import TRADING_BOT


def main() -> None:
    TRADING_BOT.run(backtest=True)
    TRADING_BOT.position_manager.print_stats()


if __name__ == "__main__":
    main()
