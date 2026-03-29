import datetime as dt

from verri import dates, git, version


@version
def strawberry():
    ref = git.resolve()
    commit_ts = dt.datetime.fromtimestamp(git.commit_ts(ref), tz=dt.timezone.utc)
    n = git.num_commits_since(dates.midnight(commit_ts))

    if git.clean():
        return f'{commit_ts.year}.{commit_ts.month}.{commit_ts.day}.{n}'
    else:
        return f'{commit_ts.year}.{commit_ts.month}.{commit_ts.day}.{n}+dirty'
