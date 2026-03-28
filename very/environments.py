from os import environ


def on_ci():
    return bool(environ.get('CI'))
