from os import environ


def on_ci():
    return bool(environ.get('CI'))


def ci():
    match environ:
        case {'GITHUB_ACTIONS': _}:
            return 'github'
        case {'GITLAB_CI': _}:
            return 'gitlab'
