import datetime as dt
from contextlib import nullcontext
from subprocess import CalledProcessError
from unittest.mock import patch

import pytest

from verri import dates, git
from verri.errors import CommandNotFound, NoRepository


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


@pytest.mark.parametrize(
    ('repo', 'num_commits'),
    [
        # NB: all commits in the repositories used here were made on the same day, 2026-04-27 (see repos/README.md)
        ('02-initial-commit.tar.gz', 1),
        ('03-two-commits.tar.gz', 2),
        # commits on the current branch count as normal
        ('04-feature-branch.tar.gz', 3),
        ('05-feature-branch-two-commits.tar.gz', 4),
        # commits are counted along the 'first-parent' path; commits on main in this case
        ('06-merge-feature-branch.tar.gz', 3),
        # whether the repository is clean does not matter when counting commits
        ('07-dirty.tar.gz', 3),
        # author date should not matter, commit was made on the same day
        ('08-authored-2001.tar.gz', 4),
    ],
)
def test_num_commits_since(inside_repo, repo, num_commits):
    with inside_repo(repo):
        commit_day = dates.midnight(git.commit_ts())
        assert git.num_commits_since(commit_day) == num_commits


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


def test_no_git():
    with patch.object(git.subprocess, 'check_output') as check_output:
        check_output.side_effect = FileNotFoundError('/usr/bin/git')
        with pytest.raises(CommandNotFound, match='git'):
            git.git('--version')


def test_git_generic_error():
    with patch.object(git.subprocess, 'check_output') as check_output:
        error = CalledProcessError(cmd='git --version', returncode=123)
        check_output.side_effect = error
        with pytest.raises(CalledProcessError) as e:
            git.git('--version')

    assert e.value is error
