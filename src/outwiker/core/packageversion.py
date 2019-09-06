# -*- coding: utf-8 -*-

VERSION_OK = 0
OUTWIKER_MUST_BE_UPGRADED = 1
PLUGIN_MUST_BE_UPGRADED = 2


def _checkSingleVersion(package_version, required_version):
    if package_version[0] > required_version[0]:
        return PLUGIN_MUST_BE_UPGRADED

    if package_version[0] < required_version[0]:
        return OUTWIKER_MUST_BE_UPGRADED

    if package_version[1] < required_version[1]:
        return OUTWIKER_MUST_BE_UPGRADED

    return VERSION_OK


def checkVersion(package_version, requiredlist):
    '''
    package_version - current package version.
    requiredlist - list of the supported versions.
    '''
    if requiredlist is None or len(requiredlist) == 0:
        return VERSION_OK

    for required in requiredlist:
        result = _checkSingleVersion(package_version, required)
        if result == VERSION_OK:
            return result

    return result
