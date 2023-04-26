import pandas as pd
import pytest

from app.strategies.macd_strategy import MACDStrategy
from tests.sample_data import SAMPLE_DATA_NO_SIGNAL


@pytest.fixture
def macd_strategy(trading_bot_config) -> MACDStrategy:
    config = trading_bot_config
    strategy = MACDStrategy()
    strategy.initialize(config)
    return strategy


def test_macd_strategy_analyze_no_signal(macd_strategy):

    df = pd.DataFrame(SAMPLE_DATA_NO_SIGNAL)

    signal = macd_strategy.analyze(df)

    assert signal is None
