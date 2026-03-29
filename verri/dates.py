import datetime as dt


def midnight(ts=None):
    ts = ts or dt.datetime.now(tz=dt.timezone.utc)
    return ts.replace(hour=0, minute=0, second=0, microsecond=0)
