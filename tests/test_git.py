import datetime as dt
from contextlib import nullcontext

import pytest

from verri import dates, git
from verri.errors import NoRepository


def test_commit_ts(inside_repo):
    with inside_repo('06-merge-feature-branch.tar.gz'):
        ts = dt.datetime(2026, 4, 27, 16, 45, 56, tzinfo=dt.timezone.utc)
        assert git.commit_ts('HEAD') == git.commit_ts('main') == git.commit_ts('f586083') == ts


def test_commit_ts_mismatching_author_date(inside_repo):
    with inside_repo('08-authored-2001.tar.gz'):
        ts = dt.datetime(2026, 4, 27, 17, 54, 44, tzinfo=dt.timezone.utc)
        # NB: using --format=%ad for author date, as opposed to --format=%cd for commit date
        assert dates.from_ts(int(git.git('show', '--quiet', '--format=%ad', '--date=unix', 'HEAD'))) != ts
        assert git.commit_ts() == ts


def test_clean(inside_repo):
    with inside_repo('06-merge-feature-branch.tar.gz'):
        assert git.clean()
    with inside_repo('07-dirty.tar.gz'):
        assert not git.clean()


@pytest.mark.parametrize(
    ('repo', 'branch'),
    [
        ('02-initial-commit.tar.gz', 'main'),
        ('04-feature-branch.tar.gz', 'feature/branch'),
        ('06-merge-feature-branch.tar.gz', 'main'),
        ('07-dirty.tar.gz', 'main'),
    ],
)
def test_branch(inside_repo, repo, branch):
    with inside_repo(repo):
        assert git.branch() == branch


@pytest.mark.parametrize(
    ('repo', 'context', 'commit'),
    [
        ('00-no-repository.tar.gz', pytest.raises(NoRepository, match='not a git repository'), None),
        ('01-init-no-commits.tar.gz', pytest.raises(NoRepository, match='ambiguous argument'), None),
        ('02-initial-commit.tar.gz', nullcontext(), '2de5e2d'),
        ('04-feature-branch.tar.gz', nullcontext(), 'd1a9df9'),
        ('07-dirty.tar.gz', nullcontext(), 'f586083'),
    ],
)
def test_resolve_short(inside_repo, repo, context, commit):
    with inside_repo(repo), context:
        assert git.resolve('HEAD').startswith(commit)
        assert git.short() == commit
