import datetime as dt

from very import version


@version
def date(ts=None):
    now = ts or dt.datetime.now(tz=dt.timezone.utc)
    return f'{now.year}.{now.month}.{now.day}'
