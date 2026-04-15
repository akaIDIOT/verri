import datetime as dt


def now():
    return dt.datetime.now(tz=dt.timezone.utc)


def midnight(ts=None):
    ts = ts or now()
    return ts.replace(hour=0, minute=0, second=0, microsecond=0)
