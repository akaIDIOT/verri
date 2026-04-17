class CommandNotFound(FileNotFoundError):
    version_local = 'vcs.error'


class NoRepository(ValueError):
    version_local = 'vcs.missing'
