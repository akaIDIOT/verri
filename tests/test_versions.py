from contextlib import nullcontext

import pytest
from freezegun import freeze_time
from packaging.version import parse

from verri import _FALLBACK_VERSION
from verri.tasty import cherry, mango, strawberry


def test_ultimate_fallback_is_valid():
    assert str(parse(_FALLBACK_VERSION)) == _FALLBACK_VERSION


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
        ('00-no-repository.tar.gz', pytest.warns(UserWarning, match='fallback version'), '2001.2.3+vcs.missing'),
        ('01-init-no-commits.tar.gz', pytest.warns(UserWarning, match='fallback version'), '2001.2.3+vcs.missing'),
        ('02-initial-commit.tar.gz', nullcontext(), '2026.4.27.0'),
        ('03-two-commits.tar.gz', nullcontext(), '2026.4.27.1'),
        ('04-feature-branch.tar.gz', nullcontext(), '2026.4.27.2'),
        ('05-feature-branch-two-commits.tar.gz', nullcontext(), '2026.4.27.3'),
        ('06-merge-feature-branch.tar.gz', nullcontext(), '2026.4.27.2'),
        ('07-dirty.tar.gz', nullcontext(), '2026.4.27.2+dirty'),
        ('08-authored-2001.tar.gz', nullcontext(), '2026.4.27.3'),
    ],
)
@freeze_time('2001-02-03T12:34:56.789+00:00')
def test_strawberry_flavour(inside_repo, repo, context, version):
    with inside_repo(repo), context:
        assert strawberry() == version
