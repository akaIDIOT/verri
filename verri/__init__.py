import warnings
from textwrap import dedent

from packaging.version import parse


_FALLBACK_VERSION = '0.0+unable.to.determine.version'


def version(func):
    def validate(*args, **kwargs):
        try:
            value = func(*args, **kwargs)
        except Exception as e:
            warnings.warn(
                dedent(
                    f"""
                    WARNING: {__name__} failed to determine version during build:
                    
                        {e!r}
                    
                    Falling back to version "{_FALLBACK_VERSION}".
                    """
                ).strip(),
                UserWarning,
                stacklevel=2,
            )
            value = _FALLBACK_VERSION

        return str(parse(value))

    return validate
