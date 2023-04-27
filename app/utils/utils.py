from datetime import datetime, timezone


def timestamp_to_datetime(timestamp: int) -> str:
    dt = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def datetime_to_timestamp(value: datetime) -> int:
    return int(value.timestamp() * 1000)


def y_m_d_to_datetime(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
