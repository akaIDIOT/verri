import sys
import tarfile
from contextlib import contextmanager
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


@pytest.fixture
def inside_repo(pytestconfig, monkeypatch, tmp_path_factory):
    @contextmanager
    def extract_and_cd(repo_name):
        repo_dir = tmp_path_factory.mktemp('git-repository')
        with tarfile.open(pytestconfig.rootpath / 'tests' / 'repos' / repo_name) as repo:
            # extract the test repository (omitting the filter argument raises warnings in 3.14+, but it's only
            # available on 3.12+)
            if sys.version_info < (3, 12):
                repo.extractall(repo_dir)
            else:
                repo.extractall(repo_dir, filter='tar')
        # cd into the extracted repository for the duration of the test
        with monkeypatch.context() as mp:
            mp.chdir(repo_dir)
            yield

    return extract_and_cd
