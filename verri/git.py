"""
Utility functions related to git repositories.
"""

import subprocess
from pathlib import Path

from verri import dates, environments
from verri.errors import CommandError, NoRepository, RepositoryTooShallow


def commit_ts(ref='HEAD'):
    """
    The commit date of *ref*, in UTC.

    :param ref: The ref to get the commit date of (defaults to `HEAD`).
    :return: The commit date in UTC, timezone-aware.
    """
    commit = resolve(ref)
    return dates.from_ts(int(git('show', '--quiet', '--format=%cd', '--date=unix', commit)))


def num_commits_since(ts):
    """
    The number of first parent commits since *ts*.

    :param ts: The point in time to count the number of commits since.
    :return: The number of first parent commits since *ts*.
    :raise RepositoryTooShallow: If the repository is a shallow clone and the commit count is uncertain.
    """
    commits = git('log', '--first-parent', f'--since={int(ts.timestamp())}', '--format=%H', '--date=unix').splitlines(
        keepends=False
    )

    if commits and (shallow := shallow_refs()) and commits[-1] in shallow:
        # oldest commit that is included with the --since filter is shallow, unable to check whether there *should* be
        # more commits that would match the --since filter, refuse an unclear commit count
        raise RepositoryTooShallow(commits[-1])

    return len(commits)


def clean():
    """
    Whether the working directory is clean, i.e., no tracked files have been changed.

    :return: `True` if the repository is clean, `False` otherwise.
    """
    return not git('status', '--porcelain', '--untracked-files=no')


def branch():
    """
    The name of the current branch, falling back to the branch reported by the CI/CD environment if there is none.

    :return: The name of the current branch, `None` if there is none.
    """
    return git('branch', '--show-current') or environments.ci_current_branch()


def resolve(ref='HEAD'):
    """
    Resolves *ref* to the commit it points to.

    :param ref: The ref to resolve (defaults to `HEAD`).
    :return: The full commit hash that *ref* points to.
    """
    return git('rev-parse', ref)


def _is_commit(ref):
    """
    Whether *ref* is a full commit hash.
    """
    try:
        return len(bytes.fromhex(ref)) in {20, 32}
    except ValueError:
        return False


def short(ref='HEAD'):
    """
    A short commit hash of *ref*, truncated to 7 characters.

    :param ref: The ref to shorten (defaults to `HEAD`).
    :return: A 7 character commit hash of *ref*.
    """
    if _is_commit(ref):
        return ref[:7]
    else:
        return short(resolve(ref))


def shallow_refs():
    """
    The commit hashes at which the repository is shallow.

    :return: The commit hashes at which the repository is shallow, `None` if the repository is not shallow.
    """
    git_dir = git('rev-parse', '--git-dir')
    if (shallow := Path(git_dir) / 'shallow').exists():
        # .git/shallow exists, listing refs that are treated as shallow
        return set(shallow.read_text().splitlines(keepends=False))
    else:
        return None


def git(*args):
    """
    Runs the `git` command line, returning its output.

    :param args: The arguments to pass on to the `git` command line.
    :return: The output of the `git` command line.
    :raise NoRepository: The working directory is not a git repository.
    :raise CommandError: The `git` command has failed with a fatal git error.
    :raise subprocess.CalledProcessError: The `git` command failed for another reason.
    """
    try:
        return subprocess.check_output(('git', *args), stderr=subprocess.PIPE, text=True).strip()
    except FileNotFoundError as e:
        raise CommandError('git') from e
    except subprocess.CalledProcessError as e:
        error = e.stderr.strip() if e.stderr else None
        if e.returncode == 128 and error:
            # 128 signals a fatal error from git
            if 'not a git repository' in error:
                raise NoRepository(error) from e
            raise CommandError(error) from e
        # git might have failed for another reason, continue original error
        raise
