import subprocess
from pathlib import Path

from verri import dates, environments
from verri.errors import CommandNotFound, NoRepository


def commit_ts(ref='HEAD'):
    commit = resolve(ref)
    return dates.from_ts(int(git('show', '--quiet', '--format=%cd', '--date=unix', commit)))


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


def shallow_refs():
    git_dir = git('rev-parse', '--git-dir')
    if (shallow := Path(git_dir) / 'shallow').exists():
        # .git/shallow exists, listing refs that are treated as shallow
        return set(shallow.read_text().splitlines(keepends=False))
    else:
        return None


def git(*args):
    try:
        return subprocess.check_output(('git', *args), stderr=subprocess.PIPE, text=True).strip()
    except FileNotFoundError as e:
        raise CommandNotFound('git') from e
    except subprocess.CalledProcessError as e:
        if e.returncode == 128:
            # specific return code for "fatal: not a git repository"
            raise NoRepository(e.stderr.strip() if e.stderr else None) from e
        else:
            raise
