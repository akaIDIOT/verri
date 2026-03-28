import datetime as dt

from very import dates, git, version


@version
def date(ts=None):
    match ts:
        case int() | float():
            ts = dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc)
        case None:
            ts = dates.midnight()

    return f'{ts.year}.{ts.month}.{ts.day}'


@version
def commit_date(ref='HEAD'):
    return date(ts=git.commit_ts(ref))


@version
def commit_date_n(ref='HEAD'):
    ref = git.resolve(ref)
    commit_ts = dt.datetime.fromtimestamp(git.commit_ts(ref), tz=dt.timezone.utc)
    n = git.num_commits_since(dates.midnight(commit_ts))

    return f'{commit_ts.year}.{commit_ts.month}.{commit_ts.day}.{n}'


@version
def commit_date_n_dev():
    ref = git.resolve()
    suffix = f'+{git.short(ref)}' if git.clean() else '+dirty'
    return f'{commit_date_n(ref)}{suffix}'


@version
def commit_date_n1(ref='HEAD'):
    ref = git.resolve(ref)
    commit_ts = dt.datetime.fromtimestamp(git.commit_ts(ref), tz=dt.timezone.utc)
    n = git.num_commits_since(dates.midnight(commit_ts))

    if n > 1:
        return f'{commit_ts.year}.{commit_ts.month}.{commit_ts.day}.{n - 1}'
    else:
        return f'{commit_ts.year}.{commit_ts.month}.{commit_ts.day}'


@version
def commit_date_n1_dev():
    ref = git.resolve()
    suffix = f'+{git.short(ref)}' if git.clean() else '+dirty'
    return f'{commit_date_n1(ref)}{suffix}'
