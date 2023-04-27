from datetime import datetime, timezone

from app.utils.utils import (
    datetime_to_timestamp,
    timestamp_to_datetime,
    y_m_d_to_datetime,
)


def test_timestamp_to_datetime() -> None:
    assert timestamp_to_datetime(1619712123000) == "2021-04-29 16:02:03"
    assert timestamp_to_datetime(1630034444000) == "2021-08-27 03:20:44"


def test_datetime_to_timestamp() -> None:
    assert (
        datetime_to_timestamp(datetime(2021, 4, 29, 2, 2, 3, tzinfo=timezone.utc))
        == 1619661723000
    )
    assert (
        datetime_to_timestamp(datetime(2021, 8, 27, 17, 14, 4, tzinfo=timezone.utc))
        == 1630084444000
    )


def test_y_m_d_to_datetime() -> None:
    assert y_m_d_to_datetime("2021-04-29") == datetime(2021, 4, 29, tzinfo=timezone.utc)
    assert y_m_d_to_datetime("2022-12-31") == datetime(
        2022, 12, 31, tzinfo=timezone.utc
    )
