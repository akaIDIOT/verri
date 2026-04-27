import subprocess

from verri import dates, environments
from verri.errors import CommandNotFound, NoRepository


def commit_ts(ref='HEAD'):
    commit = resolve(ref)
    return dates.from_ts(int(git('show', '--quiet', '--format=%cd', '--date=unix', commit)))


def num_commits_today(ts=None):
    return num_commits_since(ts=dates.midnight(ts=ts))


def num_commits_since(ts):
    return len(
        git('log', '--first-parent', f'--since={int(ts.timestamp())}', '--format=%cd', '--date=unix').splitlines(
            keepends=False
        )
    )


def clean():
    return not git('status', '--porcelain', '--untracked-files=no')


def branch():
    return git('branch', '--show-current') or environments.ci_current_branch()


def resolve(ref='HEAD'):
    return git('rev-parse', ref)


def _is_commit(ref):
    try:
        return len(bytes.fromhex(ref)) in {20, 32}
    except ValueError:
        return False


def short(ref='HEAD'):
    if _is_commit(ref):
        return ref[:7]
    else:
        return short(resolve(ref))


def git(*args):
    try:
        return subprocess.check_output(('git', *args), stderr=subprocess.PIPE, text=True).strip()
    except FileNotFoundError as e:
        raise CommandNotFound('git') from e
    except subprocess.CalledProcessError as e:
        if e.returncode == 128:
            # specific return code for "fatal: not a git repository"
            raise NoRepository(e.stderr.strip()) from e
        else:
            raise
