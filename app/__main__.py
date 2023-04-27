from bot.trading_bot import TRADING_BOT


def main() -> None:
    TRADING_BOT.run()
    TRADING_BOT.position_manager.print_stats(close_price=TRADING_BOT.last_price)


if __name__ == "__main__":
    main()
