import datetime as dt

from verri import dates, environments, git, version


@version
def strawberry():
    ref = git.resolve()
    commit_ts = dt.datetime.fromtimestamp(git.commit_ts(ref), tz=dt.timezone.utc)
    n = git.num_commits_since(dates.midnight(commit_ts))

    if git.clean():
        return f'{commit_ts.year}.{commit_ts.month}.{commit_ts.day}.{max(0, n - 1)}'
    else:
        return f'{commit_ts.year}.{commit_ts.month}.{commit_ts.day}.{max(0, n - 1)}+dirty'


@version
def pineapple():
    ref = git.resolve()
    commit_ts = dt.datetime.fromtimestamp(git.commit_ts(ref), tz=dt.timezone.utc)
    commit_version = f'{commit_ts.year}.{commit_ts.month}.{commit_ts.day}'
    n = git.num_commits_since(dates.midnight(commit_ts))
    # combine all requirements for the version under construction to be considered a releasable pineapple
    release = all(
        (
            environments.on_ci(),
            git.clean(),
            branch := git.branch(),
            # local git typically has no concept of a default branch, assume it'll be either 'main' or 'master'
            branch == environments.ci_default_branch() or branch in {'main', 'master'},
        )
    )

    match release, n:
        case True, 1 | 0:
            return commit_version
        case True, n if n > 1:
            return f'{commit_version}.{n - 1}'
        case _:
            return f'{commit_version}.dev{n}+{git.short(ref) if git.clean() else "dirty"}'
