import warnings
from collections.abc import Callable
from functools import partial, update_wrapper
from textwrap import dedent

from packaging.version import parse


# a hard coded valid but meaningless version for when nothing has worked
_FALLBACK_VERSION = '0.0+unable.to.determine.version'


def version(func=None, /, *, fallback=None):
    def validate(*args, **kwargs):
        name = func.__name__
        try:
            value = func(*args, **kwargs)
            return str(parse(value))
        except Exception as e:
            match fallback:
                case None:
                    value = _FALLBACK_VERSION
                case str():
                    value = fallback
                case Callable():
                    value = fallback()
                case _:
                    raise TypeError

            value = parse(value)
            warnings.warn(
                dedent(
                    f"""
                    WARNING: {__name__} failed to determine {name} version during build:
                    
                        {e!r}
                    
                    Using fallback version "{value}".
                    """
                ).strip(),
                UserWarning,
                stacklevel=2,
            )

            return str(value)

    if func:
        # form @version
        return update_wrapper(validate, func)
    else:
        # form @version(fallback=...)
        return partial(version, fallback=fallback)
