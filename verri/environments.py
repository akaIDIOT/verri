"""
Utility functions related to the current environment.
"""

from os import environ


def on_ci():
    """
    Whether the current environment is a CI/CD environment.

    :return: `True` if a `CI` environment variable is set and truthy, `False` otherwise.
    """
    return bool(environ.get('CI'))


def ci():
    """
    The name of the CI/CD environment the current environment is running in, if any.

    :return: The name of the CI/CD environment; `'github'` or `'gitlab'`, `None` when not running in a supported CI/CD
        environment.
    """
    match environ:
        case {'GITHUB_ACTIONS': _}:
            return 'github'
        case {'GITLAB_CI': _}:
            return 'gitlab'


def ci_default_branch():
    """
    The name of the default branch of the repository being built, when running in a CI/CD environment.

    Currently only available on GitLab CI/CD, through the `CI_DEFAULT_BRANCH` environment variable.

    :return: The name of the default branch, `None` when not available.
    """
    match environ:
        # TODO: does github expose this information somewhere accessible?
        case {'GITLAB_CI': _, 'CI_DEFAULT_BRANCH': default_branch}:
            return default_branch.strip()


def ci_current_branch():
    """
    The name of the branch being built, if running in a CI/CD environment.

    :return: The name of the currently checked out branch, `None` when not available.
    """
    match environ:
        case {'GITHUB_ACTIONS': _, 'GITHUB_REF_TYPE': 'branch', 'GITHUB_REF': branch}:
            return branch.strip()
        case {'GITLAB_CI': _, 'CI_COMMIT_BRANCH': branch}:
            return branch.strip()
