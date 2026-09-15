"""
A collection of tasty version flavours.
"""

from verri import dates, environments, git, version


@version
def mango():
    """
    A version flavour that represents the current date (see [`dates.midnight`][verri.dates.midnight]), formatted as
    `yyyy.mm.dd`, without leading zeroes.

    !!! warning

        This flavour takes nothing but the current date into account, potentially creating the same version number for
        multiple releases made on the same day.
    """
    today = dates.midnight()
    return f'{today.year}.{today.month}.{today.day}'


@version
def cherry():
    """
    A version flavour much like [mango], formatted as `yyyy.mm.dd.sss`, where `sss` is the number of seconds in the day
    since [midnight][verri.dates.midnight].

    !!! warning

        Depending on your build system, and the speed at which your project gets built, constructing different versions
        during the same build process can cause issues. Use with caution.
    """
    now = dates.now()
    today = dates.midnight(ts=now)
    seconds_today = int((now - today).total_seconds())
    return f'{today.year}.{today.month}.{today.day}.{seconds_today}'


@version(fallback=mango)
def strawberry():
    """
    A version flavour that uses the commit date of `HEAD` and the number of
    [first parent commits][verri.git.num_commits_since] since midnight on the commit date to construct a version
    formatted as `yyyy.mm.dd.n`, where `n` is the number of other first parent commits than `HEAD` on the same date.

    !!! fallback

        This flavour will fall back to [`mango`][verri.tasty.mango] flavour on error, see
        [error handling](caveats.md#error-handling).
    """
    ref = git.resolve()
    commit_ts = git.commit_ts(ref)
    n = git.num_commits_since(dates.midnight(commit_ts))

    if git.clean():
        return f'{commit_ts.year}.{commit_ts.month}.{commit_ts.day}.{max(0, n - 1)}'
    else:
        return f'{commit_ts.year}.{commit_ts.month}.{commit_ts.day}.{max(0, n - 1)}+dirty'


@version(fallback=mango)
def pineapple():
    """
    A version flavour that uses the commit date of `HEAD` and a number of components to construct a version:

    - the number of [first parent commits][verri.git.num_commits_since] since midnight on the commit date;
    - whether the version is being determined on a CI/CD environment;
    - whether the git checkout is clean;
    - the current git branch is the default branch.

    The resulting version is considered a "release" version if the checks above are all true. A pineapple flavoured
    release version is much like a [`strawberry`][verri.tasty.strawberry] flavour, although a trailing `.0` will be
    omitted.
    If not, a development version number will be created.

    !!! fallback

        This flavour will fall back to [`mango`][verri.tasty.mango] flavour on error, see
        [error handling](caveats.md#error-handling).
    """
    ref = git.resolve()
    commit_ts = git.commit_ts(ref)
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
