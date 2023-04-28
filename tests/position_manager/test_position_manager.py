from decimal import Decimal

from app.enums import OrderSide, OrderType, TimeInForce
from app.position_manager.position_manager import PositionManager
from app.schemas import OrderSchema, Signal


def test_handle_buy_signal(position_manager: PositionManager) -> None:
    """
    Test that the position manager correctly handles a buy signal by opening a position
    and updating the balance.
    """
    signal = Signal(
        name="signal",
        reason="reason",
        symbol="BTCUSDT",
        action=OrderSide.BUY,
        price=Decimal("10000.00"),
        stop_price=None,
        take_profit_price=None,
    )

    initial_balance = position_manager.balance
    position_manager.handle_signal(signal)

    assert position_manager.open_positions == 1
    assert position_manager.balance < initial_balance


def test_handle_sell_signal(position_manager: PositionManager) -> None:
    """
    Test that the position manager correctly handles a sell signal by closing an open position
    and updating the balance.
    """
    buy_signal = Signal(
        name="signal",
        reason="reason",
        symbol="BTCUSDT",
        action=OrderSide.BUY,
        price=Decimal("10000.00"),
        stop_price=None,
        take_profit_price=None,
    )

    sell_signal = Signal(
        name="signal",
        reason="reason",
        symbol="BTCUSDT",
        action=OrderSide.SELL,
        price=Decimal("11000.00"),
        stop_price=None,
        take_profit_price=None,
    )

    position_manager.handle_signal(buy_signal)
    initial_balance = position_manager.balance
    position_manager.handle_signal(sell_signal)

    assert position_manager.open_positions == 0
    assert position_manager.balance > initial_balance


def test_generate_position_id(position_manager: PositionManager) -> None:
    """
    Test that the position manager generates a valid position ID (a string).
    """
    position_id = position_manager.generate_position_id()
    assert isinstance(position_id, str)


def test_close_position(position_manager: PositionManager) -> None:
    """
    Test that the position manager correctly closes a position and updates the open_positions count.
    """
    buy_signal = Signal(
        name="signal",
        reason="reason",
        symbol="BTCUSDT",
        action=OrderSide.BUY,
        price=Decimal("10000.00"),
        stop_price=None,
        take_profit_price=None,
    )

    sell_signal = Signal(
        name="signal",
        reason="reason",
        symbol="BTCUSDT",
        action=OrderSide.SELL,
        price=Decimal("11000.00"),
        stop_price=None,
        take_profit_price=None,
    )

    position_manager.handle_signal(buy_signal)
    position_id = next(iter(position_manager.positions))
    position_manager._close_position(position_id, sell_signal)

    assert position_manager.open_positions == 0
    assert not position_manager.positions


def test_update_balance_and_portfolio(position_manager: PositionManager) -> None:
    """
    Test that the position manager correctly updates the balance and portfolio when a position is closed.
    """
    buy_signal = Signal(
        name="signal",
        reason="reason",
        symbol="BTCUSDT",
        action=OrderSide.BUY,
        price=Decimal("10000.00"),
        stop_price=None,
        take_profit_price=None,
    )

    sell_signal = Signal(
        name="signal",
        reason="reason",
        symbol="BTCUSDT",
        action=OrderSide.SELL,
        price=Decimal("11000.00"),
        stop_price=None,
        take_profit_price=None,
    )

    position_manager.handle_signal(buy_signal)
    position_id = next(iter(position_manager.positions))
    position = position_manager.positions[position_id]

    sell_order = OrderSchema(
        symbol="BTCUSDT",
        side=OrderSide.SELL,
        price=sell_signal.price,
        executed_qty=position.quantity,
        order_id="123456",
        client_order_id="123456",
        status="FILLED",
        type=OrderType.MARKET,
        time_in_force=TimeInForce.GTC,
        stop_price=None,
    )

    initial_balance = position_manager.balance
    position_manager._update_balance_and_portfolio(position, sell_order)

    assert position_manager.portfolio["BTCUSDT"] == 0
    assert position_manager.balance > initial_balance


def test_insufficient_balance(position_manager: PositionManager) -> None:
    """
    Test that the position manager does not open a position when there is an insufficient balance.
    """

    # Set the balance to 0, so we can't open any positions.
    position_manager.balance = Decimal("0.00")

    signal = Signal(
        name="signal",
        reason="reason",
        symbol="BTCUSDT",
        action=OrderSide.BUY,
        price=Decimal("100000000.00"),
        stop_price=None,
        take_profit_price=None,
    )

    position_manager.handle_signal(signal)

    assert position_manager.open_positions == 0
    assert position_manager.balance == Decimal("0.00")


def test_max_open_positions(position_manager: PositionManager) -> None:
    """
    Test that the position manager does not open more positions than the max amount of open positions
    specified in the config. The fixture config has set the max amount of open positions to 3.
    """

    signal = Signal(
        name="signal",
        reason="reason",
        symbol="BTCUSDT",
        action=OrderSide.BUY,
        price=Decimal("10000.00"),
        stop_price=None,
        take_profit_price=None,
    )

    # Here we make sure to open as many positions as the max amount of open positions, defined in the config.
    for _ in range(position_manager.config.trading_config.max_amount_open_positions):
        position_manager.handle_signal(signal)

    initial_open_positions = position_manager.open_positions

    # create a new signal, which should not be opened, since we already have the max amount of open positions.
    position_manager.handle_signal(signal)

    assert position_manager.open_positions == initial_open_positions
