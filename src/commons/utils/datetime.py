from datetime import datetime, timezone


def convert_datetime_iso_format(dt: datetime) -> str:
    return dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def utc_now():
    """Current UTC date and time with the microsecond value normalized to zero."""
    return datetime.now()
