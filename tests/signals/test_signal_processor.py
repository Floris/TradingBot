from decimal import Decimal

import pandas as pd

from app.config.config import MainConfig
from app.position_manager.position_manager import PositionManager
from app.schemas import OrderSide, Signal
from app.signals.signal_engine import SignalEngine
from app.signals.signal_processor import SignalProcessor
from tests.mocked_data import MockMarketData


def test_signal_processor_constructor(signal_processor: SignalProcessor) -> None:
    """
    Test that the SignalProcessor constructor correctly initializes its attributes.
    """
    assert isinstance(signal_processor.config, MainConfig)
    assert isinstance(signal_processor.signal_engine, SignalEngine)
    assert isinstance(signal_processor.market_data, MockMarketData)
    assert isinstance(signal_processor.position_manager, PositionManager)


def test_signal_processor_get_df(signal_processor: SignalProcessor) -> None:
    """
    Test that the `_get_df` method retrieves the klines data from the market data object.
    """
    df = signal_processor._get_df()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_signal_processor_handle_signals(signal_processor: SignalProcessor) -> None:
    """
    Test that the `_handle_signals` method correctly passes signals to the position manager.
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

    signals = [signal]

    initial_open_positions = signal_processor.position_manager.open_positions
    signal_processor._handle_signals(signals)
    assert (
        signal_processor.position_manager.open_positions == initial_open_positions + 1
    )


def test_signal_processor_print_stats(
    signal_processor: SignalProcessor, capsys
) -> None:
    """
    Test that the `_print_stats` method prints the last kline's statistics.
    """
    df = pd.DataFrame(
        {
            "open_time": [1609459200000],
            "open": [9000],
            "close": [9500],
            "high": [9500],
            "low": [9000],
            "volume": [100],
        }
    )
    signal_processor._print_stats(df)
    captured = capsys.readouterr()

    assert "Open Time:  2021-01-01 00:00:00" in captured.out
    assert "Open:  9000" in captured.out
    assert "Close:  9500" in captured.out
    assert "High:  9500" in captured.out
    assert "Low:  9000" in captured.out
    assert "Volume:  100" in captured.out


def test_signal_processor_run(signal_processor: SignalProcessor) -> None:
    """
    Test that the `run` method processes signals and updates the position manager's open positions.
    """
    initial_open_positions = signal_processor.position_manager.open_positions
    signal_processor.config.backtest = True
    signal_processor.run()
    assert signal_processor.position_manager.open_positions > initial_open_positions
