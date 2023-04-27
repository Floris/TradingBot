from datetime import datetime


def timestamp_to_datetime(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S")


def datetime_to_timestamp(value: datetime) -> int:
    return int(value.timestamp() * 1000)


def y_m_d_to_datetime(value: str) -> datetime:
    """
    y_m_d string to datetime
    """

    return datetime.strptime(value, "%Y-%m-%d")
