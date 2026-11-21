class CommandError(RuntimeError):
    """
    Raised when an external command (e.g. `git`) failed or crashed.
    """

    version_local = 'vcs.error'


class NoRepository(ValueError):
    """
    Raised when `verri` requires a repository to determine a version, but was unable to find it.
    """

    version_local = 'vcs.missing'


class RepositoryTooShallow(ValueError):
    """
    Raised when the repository required to determine a version is too [shallow](https://git-scm.com/docs/shallow).
    """

    version_local = 'vcs.too.shallow'
