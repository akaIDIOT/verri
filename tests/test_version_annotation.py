import pytest
from packaging.version import parse

from verri import _FALLBACK_VERSION, version


def test_ultimate_fallback_is_valid():
    assert str(parse(_FALLBACK_VERSION)) == _FALLBACK_VERSION


def test_simple_function():
    @version
    def one():
        return '1'

    assert one() == '1'


def test_broken_function():
    @version
    def broken():
        raise ValueError('something went wrong')

    with pytest.warns(UserWarning, match='fallback version'):
        assert broken() == _FALLBACK_VERSION


def test_simple_fallback():
    @version(fallback='1.0')
    def broken():
        raise ValueError('whoopsiedaisy')

    with pytest.warns(UserWarning, match='fallback version'):
        assert broken() == '1.0'


def test_simple_fallback_override_local():
    class OopsError(Exception):
        version_local = 'oops-i-did-it-again'

    @version(fallback='1.0')
    def broken():
        raise OopsError('rights were sold')

    with pytest.warns(UserWarning, match='fallback version'):
        assert broken() == '1.0+oops.i.did.it.again'


def test_invalid_fallback():
    @version(fallback=1)
    def broken():
        raise ValueError('Houston, we have a problem')

    with pytest.raises(TypeError, match='invalid fallback'):
        broken()


def test_wrapper_has_original_meta():
    @version
    def name1():
        return '1.0'

    @version()
    def name2():
        """docstring"""
        return '2.0'

    @version(fallback='3.0')
    def name3():
        return '3.0'

    assert name1.__name__ == 'name1'
    assert name2.__name__ == 'name2'
    assert name2.__doc__ == 'docstring'
    assert name3.__name__ == 'name3'
