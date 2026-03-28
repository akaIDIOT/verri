from very import dates


def test_midnight_zeroes():
    ts = dates.midnight()
    assert ts.hour == ts.minute == ts.second == ts.microsecond == 0
