from os import environ

import pytest


@pytest.fixture
def empty_environment(monkeypatch):
    for var in environ.keys():
        monkeypatch.delenv(var)


@pytest.fixture
def on_github_actions(empty_environment, monkeypatch):
    env = {
        'CI': '1',
        'GITHUB_ACTIONS': '1',
        'GITHUB_REF_TYPE': 'branch',
        'GITHUB_REF': 'current-branch',
    }
    for var, value in env.items():
        monkeypatch.setenv(var, value)


@pytest.fixture
def on_gitlab_cicd(empty_environment, monkeypatch):
    env = {
        'CI': '1',
        'CI_COMMIT_BRANCH': 'current-branch',
        'CI_DEFAULT_BRANCH': 'default-branch',
        'GITLAB_CI': '1',
    }
    for var, value in env.items():
        monkeypatch.setenv(var, value)
