#!/usr/bin/python
# -*- coding: utf-8 -*-

import builtins
import os
import os.path
import glob
import sys
import shutil
import re
from typing import List, Tuple, Callable, TextIO
from pathlib import Path

from fabric.api import local, lcd, settings, task

from buildtools.utilites import (getPython,
                                 execute,
                                 tobool,
                                 print_info,
                                 windows_only,
                                 linux_only
                                 )
from buildtools.defines import DEB_BINARY_BUILD_DIR, COVERAGE_PARAMS
from buildtools.builders import (BuilderWindows,
                                 BuilderSources,
                                 BuilderPlugins,
                                 BuilderLinuxBinary,
                                 BuilderDebBinaryFactory,
                                 BuilderAppImage,
                                 BuilderSnap,
                                 )
from buildtools.versionstools import (display_version,
                                      InitUpdater,
                                      VersionsXmlUpdater)


@task
def plugins(updatedonly=False):
    '''
    Create an archive with plugins (7z required)
    '''
    updatedonly = tobool(updatedonly)
    builder = BuilderPlugins(updatedOnly=updatedonly)
    builder.build()


@task
def plugins_clear():
    '''
    Remove an archive with plugins (7z required)
    '''
    builder = BuilderPlugins()
    builder.clear()


@task
def sources(is_stable=False):
    '''
    Create the sources archives
    '''
    is_stable = tobool(is_stable)
    builder = BuilderSources(is_stable=tobool(is_stable))
    builder.build()


@task
def sources_clear():
    '''
    Remove the sources archives.
    '''
    builder = BuilderSources()
    builder.clear()


@task
@windows_only
def win(is_stable=False, skiparchives=False, skipinstaller=False):
    '''
    Build OutWiker for Windows
    '''
    builder = BuilderWindows(is_stable=tobool(is_stable),
                             create_archives=not tobool(skiparchives),
                             create_installer=not tobool(skipinstaller)
                             )
    builder.build()


@task
@windows_only
def win_clear():
    '''
    Remove assemblies under Windows
    '''
    builder = BuilderWindows()
    builder.clear()


@task
@linux_only
def linux_binary(is_stable=False, skiparchives=False):
    '''
    Assemble binary builds for Linux
    '''
    builder = BuilderLinuxBinary(is_stable=tobool(is_stable),
                                 create_archive=not tobool(skiparchives)
                                 )
    builder.build()


@task
@linux_only
def linux_clear():
    '''
    Remove binary builds for Linux
    '''
    builder = BuilderLinuxBinary()
    builder.clear()


@task
def run(args=u''):
    '''
    Run OutWiker from sources
    '''
    with lcd("src"):
        execute(u'{} runoutwiker.py {}'.format(getPython(), args))


@task
def test(*args):
    '''
    Run the unit tests
    '''
    command = getPython() if args else 'coverage run {}'.format(COVERAGE_PARAMS)

    local('{command} runtests.py {args}'.format(
        command=command, args=' '.join(args)))


def _runTests(testdir, prefix, section=u'', *args):
    files = [fname[len(testdir) + 1:]
             for fname
             in glob.glob(u'{path}/{prefix}*.py'.format(path=testdir,
                                                        prefix=prefix))]
    files.sort()

    with lcd(testdir):
        if section:
            execute("{python} {prefix}{section}.py {params}".format(
                python=getPython(),
                prefix=prefix,
                section=section,
                params=u' '.join(args))
            )
        else:
            with settings(warn_only=True):
                for fname in files:
                    execute("{python} {fname} {params}".format(
                        python=getPython(),
                        fname=fname,
                        params=u' '.join(args))
                    )


@task
@linux_only
def deb_binary(is_stable=False):
    '''
    Create binary deb package
    '''
    is_stable = tobool(is_stable)
    builder = BuilderDebBinaryFactory.get_default(DEB_BINARY_BUILD_DIR,
                                                  is_stable)
    builder.build()
    print_info('Deb created: {}'.format(builder.get_deb_files()))


@task
@linux_only
def deb_binary_clear():
    '''
    Remove binary deb package
    '''
    builder = BuilderDebBinaryFactory.get_default()
    builder.clear()


@task
def clear():
    '''
    Remove artifacts after all assemblies
    '''
    plugins_clear()
    sources_clear()

    if sys.platform.startswith('linux'):
        linux_clear()
        # deb_clear()
        deb_binary_clear()
    elif sys.platform.startswith('win32'):
        win_clear()


@task
def create_tree(maxlevel, nsiblings, path):
    '''
    Create wiki tree for the tests
    '''
    from outwiker.core.tree import WikiDocument

    builtins._ = _empty
    wikiroot = WikiDocument.create(path)
    _create_tree(1, int(maxlevel), int(nsiblings), wikiroot)


def _empty(param):
    return param


def _create_tree(level, maxlevel, nsiblings, parent):
    from outwiker.pages.wiki.wikipage import WikiPageFactory

    if level <= maxlevel:
        for n in range(nsiblings):
            pagename = u'page_{:03g}_{:03g}'.format(level, n)
            print(u'Create page {}'.format(pagename))

            newpage = WikiPageFactory().create(parent, pagename, [])
            newpage.content = u'Абырвалг'
            newpage.icon = u'images/outwiker_16.png'
            _create_tree(level + 1, maxlevel, nsiblings, newpage)


@task
def build(is_stable=False):
    '''
    Create artifacts for current version.
    '''
    is_stable = tobool(is_stable)

    if is_stable:
        build(False)

    sources(is_stable)
    plugins(True)

    if sys.platform.startswith('win32'):
        win(is_stable)


@task
def doc():
    '''
    Build documentation
    '''
    doc_path = u'doc/_build'
    if os.path.exists(doc_path):
        shutil.rmtree(doc_path)

    with lcd('doc'):
        local('make html')


@task(alias='linux_appimage')
@linux_only
def appimage(is_stable=0):
    '''
    Build AppImage package
    '''
    builder = BuilderAppImage(is_stable=tobool(is_stable))
    builder.build()
    print_info('AppImage created: {}'.format(builder.get_appimage_files()))


@task
def coverage():
    '''
    Create test coverage statistics
    '''
    local('coverage report {} -i'.format(COVERAGE_PARAMS))
    local('coverage html {} -i'.format(COVERAGE_PARAMS))


@task
@linux_only
def docker_build_create():
    '''
    Create a Docker image to build process
    '''
    with lcd('need_for_build/build_docker'):
        local('docker build -t outwiker/build_linux .')


@task
@linux_only
def docker_build(*args):
    '''
    Run the build process inside the Docker container
    '''
    docker_build_create()

    tasks_str = ' '.join(args)
    current_dir = os.path.abspath('.')
    command = 'docker run -v "{path}:/home/user/project" --user $(id -u):$(id -g) -i -t outwiker/build_linux {tasks}'.format(
        path=current_dir,
        tasks=tasks_str
    )
    local(command)


@task(alias='linux_snap')
@linux_only
def snap(*params):
    '''
    Build clean snap package
    '''
    builder = BuilderSnap(*params)
    builder.build()


@task(alias='update_version')
def set_version(version_str: str = ''):
    """Set new OutWiker version for all files with versions"""
    if not version_str.strip():
        display_version()
        version_str = input(
            'Enter new OutWiker version in the format: "x.x.x.xxx [status]": ')

    version, status = _parse_version(version_str)
    update_info = [
        (Path('src', 'outwiker', '__init__.py'), InitUpdater()),
        (Path('need_for_build', 'versions.xml'), VersionsXmlUpdater()),
    ]

    for fname, updater in update_info:
        _update_version_for_file(fname, updater.set_version, version, status)


@task(alias='add_version')
def add_new_version(version_str: str = ''):
    """Append new version information to all files with versions"""
    if not version_str.strip():
        display_version()
        version_str = input(
            'Enter new OutWiker version in the format: "x.x.x.xxx [status]": ')

    version, status = _parse_version(version_str)
    update_info = [
        (Path('src', 'outwiker', '__init__.py'), InitUpdater()),
        (Path('need_for_build', 'versions.xml'), VersionsXmlUpdater()),
    ]

    for fname, updater in update_info:
        _update_version_for_file(fname, updater.add_version, version, status)


@task(alias='set_date')
def set_release_date(date: str = ''):
    """Set release date for current version"""
    if not date.strip():
        display_version()
        date = input('Enter OutWiker release date: ')

    update_info = [
        (Path('src', 'outwiker', '__init__.py'), InitUpdater()),
        (Path('need_for_build', 'versions.xml'), VersionsXmlUpdater()),
    ]

    for fname, updater in update_info:
        _set_release_date_for_file(fname, updater, date)


def _parse_version(version_str: str) -> Tuple[List[int], str]:
    regexp = re.compile(r'(?P<numbers>(\d+)(\.\d+)*)(?P<status>\s+.*)?')
    match = regexp.match(version_str)
    numbers = [int(number) for number in match.group('numbers').split('.')]
    status = match.group('status')
    if status is None:
        status = ''
    return (numbers, status.strip())


def _update_version_for_file(path: str,
                             updater_func: Callable[[TextIO, List[int], str], str],
                             version: List[int],
                             status: str):
    with open(path) as fp_in:
        content_new = updater_func(fp_in, version, status)

    with open(path, 'w') as fp_out:
        fp_out.write(content_new)


def _set_release_date_for_file(path: str, updater, date_str: str):
    with open(path) as fp_in:
        content_new = updater.set_release_date(fp_in, date_str)

    with open(path, 'w') as fp_out:
        fp_out.write(content_new)
