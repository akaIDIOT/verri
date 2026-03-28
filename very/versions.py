import datetime as dt

from very import git, version


@version
def date(ts=None):
    match ts:
        case int() | float():
            ts = dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc)
        case None:
            ts = dt.datetime.now(tz=dt.timezone.utc)

    return f'{ts.year}.{ts.month}.{ts.day}'


@version
def commit_date(ref='HEAD'):
    return date(ts=git.commit_ts(ref))
