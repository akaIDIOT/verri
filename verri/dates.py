"""
Utility functions related to dates and times.

!!! note

    All date-related values used by Verri use UTC as a timezone to ensure independence of the timezone when creating a
    version.
"""

import datetime as dt


def now() -> dt.datetime:
    """
    The current timezone-aware date and time, in UTC.

    :return:
    """
    return dt.datetime.now(tz=dt.timezone.utc)


def midnight(ts=None) -> dt.datetime:
    """

    :param ts:
    :return:
    """
    ts = ts or now()
    if not ts.tzinfo:
        raise ValueError('a timezone aware datetime is required')

    return ts.replace(hour=0, minute=0, second=0, microsecond=0)


def from_ts(ts) -> dt.datetime:
    """

    :param ts: A point in time, measured in seconds since the UNIX epoch.
    :return:
    """
    return dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc)
