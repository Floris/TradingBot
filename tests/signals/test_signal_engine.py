import pandas as pd

from app.schemas import OrderSide
from app.signals.signal_engine import SignalEngine


def test_initialize_strategies(signal_engine: SignalEngine) -> None:
    """
    Test that the `initialize_strategies` method correctly initializes the strategies.
    """
    signal_engine.initialize_strategies()
    # No exception raised, test passes


def test_generate_signals(signal_engine: SignalEngine) -> None:
    """
    Test that the `generate_signals` method generates signals from the strategies.
    """
    df = pd.DataFrame(
        {
            "open": [9000, 9500, 10000, 11000, 10500],
            "high": [9500, 10000, 11000, 11500, 11000],
            "low": [9000, 9500, 10000, 10500, 10000],
            "close": [9500, 10000, 11000, 10500, 11000],
            "volume": [100, 200, 300, 400, 500],
        }
    )

    signals = signal_engine.generate_signals(df)

    # Check the signals generated
    for signal in signals:
        print(signal)

    assert len(signals) == 1
    assert signals[0].action == OrderSide.BUY
