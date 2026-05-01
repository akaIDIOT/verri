from verri import environments


def test_emtpy_environ(empty_environment):
    assert environments.on_ci() is False
    assert environments.ci() is None
    assert environments.ci_current_branch() is None
    assert environments.ci_default_branch() is None


def test_on_github_actions(on_github_actions):
    assert environments.on_ci()
    assert environments.ci() == 'github'
    assert environments.ci_current_branch() == 'current-branch'
    assert environments.ci_default_branch() is None


def test_on_gitlab_cicd(on_gitlab_cicd):
    assert environments.on_ci()
    assert environments.ci() == 'gitlab'
    assert environments.ci_current_branch() == 'current-branch'
    assert environments.ci_default_branch() == 'default-branch'
