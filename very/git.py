import subprocess
from functools import cache


def commit_ts(ref='HEAD'):
    commit = resolve(ref)
    return int(git('show', '--quiet', '--format=%cd', '--date=unix', commit))


@cache
def resolve(ref='HEAD'):
    return git('rev-parse', ref)


def git(*args):
    return subprocess.check_output(('git', *args), stderr=subprocess.DEVNULL, text=True).strip()
