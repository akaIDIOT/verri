import datetime as dt
from zoneinfo import ZoneInfo

import pytest

from verri import dates


@pytest.fixture
def tz_eu_ams():
    # NB: Europe/Amsterdam is never at offset 0
    return ZoneInfo('Europe/Amsterdam')


def test_midnight_zeroes():
    ts = dates.midnight()

    assert ts.hour == ts.minute == ts.second == ts.microsecond == 0
    assert ts.tzinfo == dt.timezone.utc


def test_midnight_specific_date(tz_eu_ams):
    ts = dt.datetime(2001, 2, 3, 4, 5, 6, 789, tzinfo=tz_eu_ams)
    midnight = dates.midnight(ts)

    assert ts.date() == midnight.date()
    assert midnight.hour == midnight.minute == midnight.second == midnight.microsecond == 0


def test_timezone_roundtrip(tz_eu_ams):
    now_ams = dates.now().astimezone(tz_eu_ams)
    ts = dates.from_ts(now_ams.timestamp())

    assert ts.tzinfo != now_ams.tzinfo
    assert ts == now_ams
