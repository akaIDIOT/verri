import datetime as dt
from contextlib import nullcontext
from subprocess import CalledProcessError
from unittest.mock import patch

import pytest

from verri import dates, git
from verri.errors import CommandError, NoRepository, RepositoryTooShallow


def identify_repo(repo, *values):
    # a regular pytest param, identified by its first argument
    return pytest.param(repo, *values, id=repo)


def test_commit_ts(inside_repo):
    with inside_repo('06-merge-feature-branch.tar.gz'):
        ts = dt.datetime(2026, 4, 27, 16, 45, 56, tzinfo=dt.UTC)
        assert git.commit_ts('HEAD') == git.commit_ts('main') == git.commit_ts('f586083') == ts


def test_commit_ts_mismatching_author_date(inside_repo):
    with inside_repo('08-authored-2001.tar.gz'):
        ts = dt.datetime(2026, 4, 27, 17, 54, 44, tzinfo=dt.UTC)
        # NB: using --format=%ad for author date, as opposed to --format=%cd for commit date
        assert dates.from_ts(int(git.git('show', '--quiet', '--format=%ad', '--date=unix', 'HEAD'))) != ts
        assert git.commit_ts() == ts


@pytest.mark.parametrize(
    ('repo', 'expected_feedback', 'num_commits'),
    [
        identify_repo('02-initial-commit.tar.gz', nullcontext(), 1),
        identify_repo('03-two-commits.tar.gz', nullcontext(), 2),
        # commits on the current branch count as normal
        identify_repo('04-feature-branch.tar.gz', nullcontext(), 3),
        identify_repo('05-feature-branch-two-commits.tar.gz', nullcontext(), 4),
        # commits are counted along the 'first-parent' path; commits on main in this case
        identify_repo('06-merge-feature-branch.tar.gz', nullcontext(), 3),
        # whether the repository is clean does not matter when counting commits
        identify_repo('07-dirty.tar.gz', nullcontext(), 3),
        # author date should not matter, commit was made on the same day
        identify_repo('08-authored-2001.tar.gz', nullcontext(), 4),
        identify_repo('09-new-commit-date.tar.gz', nullcontext(), 1),
        # clone depth 1 will report the single commit on that day as shallow, should raise
        identify_repo('10-clone-depth-1.tar.gz', pytest.raises(RepositoryTooShallow, match='f5a0194'), None),
        # still shallow, but the only commit on the commit date is not shallow, should be fine
        identify_repo('11-clone-depth-3.tar.gz', nullcontext(), 1),
    ],
)
def test_num_commits_since(inside_repo, repo, expected_feedback, num_commits):
    with inside_repo(repo), expected_feedback:
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
        identify_repo('02-initial-commit.tar.gz', 'main'),
        identify_repo('04-feature-branch.tar.gz', 'feature/branch'),
        identify_repo('06-merge-feature-branch.tar.gz', 'main'),
        identify_repo('07-dirty.tar.gz', 'main'),
    ],
)
def test_branch(inside_repo, repo, branch):
    with inside_repo(repo):
        assert git.branch() == branch


@pytest.mark.parametrize(
    ('repo', 'expected_feedback', 'commit'),
    [
        identify_repo('00-no-repository.tar.gz', pytest.raises(NoRepository, match='not a git repository'), None),
        identify_repo('01-init-no-commits.tar.gz', pytest.raises(CommandError, match='ambiguous argument'), None),
        identify_repo('02-initial-commit.tar.gz', nullcontext(), '2de5e2d'),
        identify_repo('04-feature-branch.tar.gz', nullcontext(), 'd1a9df9'),
        identify_repo('07-dirty.tar.gz', nullcontext(), 'f586083'),
    ],
)
def test_resolve_short(inside_repo, repo, expected_feedback, commit):
    with inside_repo(repo), expected_feedback:
        assert git.resolve('HEAD').startswith(commit)
        assert git.short() == commit


@pytest.mark.parametrize(
    ('repo', 'expected_refs'),
    [
        identify_repo('09-new-commit-date.tar.gz', None),
        identify_repo('10-clone-depth-1.tar.gz', {'f5a01947a265449f7da7b6a472a39e2cb1364248'}),
        identify_repo('11-clone-depth-3.tar.gz', {'f586083f8852be4c8bef296bf97c0956f719abbd'}),
    ],
)
def test_shallow_refs(inside_repo, repo, expected_refs):
    with inside_repo(repo):
        assert git.shallow_refs() == expected_refs


def test_no_git():
    with patch.object(git.subprocess, 'check_output', autospec=True) as check_output:
        check_output.side_effect = FileNotFoundError('/usr/bin/git')
        with pytest.raises(CommandError, match='git'):
            git.git('--version')


def test_git_generic_error():
    with patch.object(git.subprocess, 'check_output', autospec=True) as check_output:
        error = CalledProcessError(cmd='git --version', returncode=123)
        check_output.side_effect = error
        with pytest.raises(CalledProcessError) as raised:
            git.git('--version')

    assert raised.value is error
