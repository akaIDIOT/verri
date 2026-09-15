import warnings
from collections.abc import Callable
from functools import partial, update_wrapper
from textwrap import dedent

from packaging.version import parse


# a hard coded valid but meaningless version for when nothing has worked
_FALLBACK_VERSION = '0.0+unable.to.determine.version'


def version(func=None, /, *, fallback=None):
    """
    Decorator that will validate a resulting version is PEP-440 compliant, optionally resorting to a fallback value.

    :param func: The function to decorate.
    :param fallback: A fallback version, either a `str` value or a `Callable` that returns a `str`.
    :return: A PEP-440 compliant version.
    """

    def validate(*args, **kwargs):
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
                    raise TypeError(f'invalid fallback for version "{func.__name__}": {fallback!r}')

            value = parse(value)
            if local := getattr(e, 'version_local', None):
                # the error type provided a specific value for the local version component
                # TODO: use copy.replace() when requires-python reaches >=3.13
                value = value.__replace__(local=local)

            warnings.warn(
                dedent(
                    f"""
                    WARNING: {__name__} failed to determine {func.__name__} version during build:
                    
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
