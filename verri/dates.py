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

    :return: The current date and time in UTC, timezone-aware.
    """
    return dt.datetime.now(tz=dt.timezone.utc)


def midnight(ts: dt.datetime | None = None) -> dt.datetime:
    """
    Midnight of the current or a specified date, in UTC.

    :param ts: A specific date to turn into midnight (defaults to the current date). *Note that this needs to be a
        timezone **aware** datetime, a naive one will be rejected.*
    :return: A `datetime` at UTC midnight.
    """
    ts = ts or now()
    if not ts.tzinfo:
        raise ValueError('a timezone aware datetime is required')

    return ts.replace(hour=0, minute=0, second=0, microsecond=0)


def from_ts(ts: int | float) -> dt.datetime:
    """
    Creates a `datetime` instance of *ts*.

    :param ts: A point in time, measured in seconds since the UNIX epoch.
    :return: A `datetime` instance in UTC.
    """
    return dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc)
