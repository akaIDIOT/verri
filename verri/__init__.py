from packaging.version import parse


def version(func):
    def validate(*args, **kwargs):
        return str(parse(func(*args, **kwargs)))

    return validate
