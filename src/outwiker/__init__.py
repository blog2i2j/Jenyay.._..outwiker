__version__ = (3, 0, 0, 868)
__status__ = 'dev'
__api_version__ = (3, 868)


def getVersionStr() -> str:
    return '.'.join([str(item) for item in __version__]) + ' ' + __status__
