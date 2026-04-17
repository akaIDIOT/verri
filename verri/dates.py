import datetime as dt


def now():
    return dt.datetime.now(tz=dt.timezone.utc)


def midnight(ts=None):
    ts = ts or now()
    # TODO: should midnight force UTC?
    return ts.replace(hour=0, minute=0, second=0, microsecond=0)


def from_ts(ts):
    return dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc)
