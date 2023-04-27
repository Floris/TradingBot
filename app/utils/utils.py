from datetime import datetime, timezone

from enums import INTERVALS


def timestamp_to_datetime(timestamp: int) -> str:
    dt = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def datetime_to_timestamp(value: datetime) -> int:
    return int(value.timestamp() * 1000)


def y_m_d_to_datetime(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)


def interval_to_seconds(interval: INTERVALS) -> int:
    intervals = {
        "1s": 1,
        "1m": 60,
        "3m": 180,
        "5m": 300,
        "15m": 900,
        "30m": 1800,
        "1h": 3600,
        "2h": 7200,
        "4h": 14400,
        "6h": 21600,
        "8h": 28800,
        "12h": 43200,
        "1d": 86400,
        "3d": 259200,
        "1w": 604800,
        "1M": 2592000,
    }
    return intervals[interval]
