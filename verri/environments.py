from os import environ


def on_ci():
    return bool(environ.get('CI'))


def ci():
    match environ:
        case {'GITHUB_ACTIONS': _}:
            return 'github'
        case {'GITLAB_CI': _}:
            return 'gitlab'


def ci_default_branch():
    match environ:
        # TODO: does github expose this information somewhere accessible?
        case {'GITLAB_CI': _, 'CI_DEFAULT_BRANCH': default_branch}:
            return default_branch.strip()


def ci_current_branch():
    match environ:
        case {'GITHUB_ACTIONS': _, 'GITHUB_REF_TYPE': 'branch', 'GITHUB_REF': branch}:
            return branch.strip()
        case {'GITLAB_CI': _, 'CI_COMMIT_BRANCH': branch}:
            return branch.strip()
