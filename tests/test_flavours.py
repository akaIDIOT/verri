import inspect
from contextlib import nullcontext

import pytest
from freezegun import freeze_time

from verri import tasty
from verri.tasty import cherry, mango, pineapple, strawberry


def identify_repo(repo, *values):
    # a regular pytest param, identified by its first argument
    return pytest.param(repo, *values, id=repo)


@pytest.mark.parametrize(
    ('time', 'version'),
    [
        ('2001-02-03T12:34:56.789+00:00', '2001.2.3'),
        ('2001-02-03T00:12:34.456+02:00', '2001.2.2'),  # date rollover, date-based versioning enforces using UTC
    ],
)
def test_mango_flavour(time, version):
    with freeze_time(time):
        assert mango() == version


@pytest.mark.parametrize(
    ('time', 'version'),
    [
        ('2001-02-03T12:34:56.789+00:00', '2001.2.3.45296'),
        ('2001-02-03T00:12:34.456+02:00', '2001.2.2.79954'),
    ],
)
def test_cherry_flavour(time, version):
    with freeze_time(time):
        assert cherry() == version


@pytest.mark.parametrize(
    ('repo', 'context', 'version'),
    [
        identify_repo(
            '00-no-repository.tar.gz', pytest.warns(UserWarning, match='fallback version'), '2001.2.3+vcs.missing'
        ),
        identify_repo(
            '01-init-no-commits.tar.gz', pytest.warns(UserWarning, match='fallback version'), '2001.2.3+vcs.error'
        ),
        identify_repo('02-initial-commit.tar.gz', nullcontext(), '2026.4.27.0'),
        identify_repo('03-two-commits.tar.gz', nullcontext(), '2026.4.27.1'),
        identify_repo('04-feature-branch.tar.gz', nullcontext(), '2026.4.27.2'),
        identify_repo('05-feature-branch-two-commits.tar.gz', nullcontext(), '2026.4.27.3'),
        identify_repo('06-merge-feature-branch.tar.gz', nullcontext(), '2026.4.27.2'),
        identify_repo('07-dirty.tar.gz', nullcontext(), '2026.4.27.2+dirty'),
        identify_repo('08-authored-2001.tar.gz', nullcontext(), '2026.4.27.3'),
        identify_repo('09-new-commit-date.tar.gz', nullcontext(), '2026.6.10.0'),
        identify_repo(
            '10-clone-depth-1.tar.gz', pytest.warns(UserWarning, match='fallback version'), '2001.2.3+vcs.too.shallow'
        ),
        identify_repo('11-clone-depth-3.tar.gz', nullcontext(), '2026.6.10.0'),
    ],
)
@freeze_time('2001-02-03T12:34:56.789+00:00')
def test_strawberry_flavour(inside_repo, repo, context, version):
    with inside_repo(repo), context:
        assert strawberry() == version


@pytest.mark.parametrize(
    ('repo', 'expected_feedback', 'version'),
    [
        identify_repo(
            '00-no-repository.tar.gz', pytest.warns(UserWarning, match='fallback version'), '2001.2.3+vcs.missing'
        ),
        identify_repo(
            '01-init-no-commits.tar.gz', pytest.warns(UserWarning, match='fallback version'), '2001.2.3+vcs.error'
        ),
        identify_repo('02-initial-commit.tar.gz', nullcontext(), '2026.4.27.dev1+2de5e2d'),
        identify_repo('03-two-commits.tar.gz', nullcontext(), '2026.4.27.dev2+eb9a1ee'),
        identify_repo('04-feature-branch.tar.gz', nullcontext(), '2026.4.27.dev3+d1a9df9'),
        identify_repo('05-feature-branch-two-commits.tar.gz', nullcontext(), '2026.4.27.dev4+07319e1'),
        identify_repo('06-merge-feature-branch.tar.gz', nullcontext(), '2026.4.27.dev3+f586083'),
        identify_repo('07-dirty.tar.gz', nullcontext(), '2026.4.27.dev3+dirty'),
        identify_repo('08-authored-2001.tar.gz', nullcontext(), '2026.4.27.dev4+8ffcba0'),
        identify_repo('09-new-commit-date.tar.gz', nullcontext(), '2026.6.10.dev1+f5a0194'),
        identify_repo(
            '10-clone-depth-1.tar.gz', pytest.warns(UserWarning, match='fallback version'), '2001.2.3+vcs.too.shallow'
        ),
        identify_repo('11-clone-depth-3.tar.gz', nullcontext(), '2026.6.10.dev1+f5a0194'),
    ],
)
@freeze_time('2001-02-03T12:34:56.789+00:00')
def test_pineapple_flavour_empty_environment(empty_environment, inside_repo, repo, expected_feedback, version):
    with inside_repo(repo), expected_feedback:
        assert pineapple() == version


@pytest.mark.parametrize(
    ('repo', 'expected_feedback', 'version'),
    [
        identify_repo(
            '00-no-repository.tar.gz', pytest.warns(UserWarning, match='fallback version'), '2001.2.3+vcs.missing'
        ),
        identify_repo(
            '01-init-no-commits.tar.gz', pytest.warns(UserWarning, match='fallback version'), '2001.2.3+vcs.error'
        ),
        identify_repo('02-initial-commit.tar.gz', nullcontext(), '2026.4.27'),
        identify_repo('03-two-commits.tar.gz', nullcontext(), '2026.4.27.1'),
        identify_repo('04-feature-branch.tar.gz', nullcontext(), '2026.4.27.dev3+d1a9df9'),
        identify_repo('05-feature-branch-two-commits.tar.gz', nullcontext(), '2026.4.27.dev4+07319e1'),
        identify_repo('06-merge-feature-branch.tar.gz', nullcontext(), '2026.4.27.2'),
        identify_repo('07-dirty.tar.gz', nullcontext(), '2026.4.27.dev3+dirty'),
        identify_repo('08-authored-2001.tar.gz', nullcontext(), '2026.4.27.3'),
    ],
)
@freeze_time('2001-02-03T12:34:56.789+00:00')
def test_pineapple_flavour_on_ci(on_github_actions, inside_repo, repo, expected_feedback, version):
    with inside_repo(repo), expected_feedback:
        assert pineapple() == version


def test_flavours_registered_to_all():
    def is_tasty_function(obj):
        return inspect.isfunction(obj) and obj.__module__ == 'verri.tasty'

    names = {name for name, _ in inspect.getmembers(tasty, predicate=is_tasty_function)}

    assert set(tasty.__all__) == names
    assert tasty.__all__ == sorted(names)
