# -*- coding: utf8 - *-
"""Utility and helper methods for cihai.

cihai.util
~~~~~~~~~~

"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import collections
import csv
import os
import pkgutil
import sys

from ._compat import PY2, reraise, string_types, text_type


def get_datafile(filename):
    """Return absolute path to cihai data file.

    :param filename: file name relative to ``./data``.
    :type filename: string
    :returns: Absolute path to data file.
    :rtype: string

    """

    abspath = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'data/', filename)
    return abspath


class UnicodeReader(csv.DictReader):
    """Read from Unihan CSV into Unicode."""
    def __init__(self, *args, **kwargs):
        csv.DictReader.__init__(self, *args, **kwargs)

    def __next__(self):
        row = csv.DictReader.__next__(self)

        return self.row(row)

    def next(self):
        row = csv.DictReader.next(self)

        return self.row(row)

    def row(self, row):
        for key in row.keys():
            if not isinstance(row[key], text_type):
                row[key] = text_type(row[key].decode('utf-8'))

        return row


def _dl_progress(count, block_size, total_size, out=sys.stdout):
    """
    MIT License: https://github.com/okfn/dpm-old/blob/master/dpm/util.py

    Modification for testing: http://stackoverflow.com/a/4220278

    """
    def format_size(bytes):
        if bytes > 1000 * 1000:
            return '%.1fMb' % (bytes / 1000.0 / 1000)
        elif bytes > 10 * 1000:
            return '%iKb' % (bytes / 1000)
        elif bytes > 1000:
            return '%.1fKb' % (bytes / 1000.0)
        else:
            return '%ib' % bytes

    if not count:
        print('Total size: %s' % format_size(total_size))
    last_percent = int((count - 1) * block_size * 100 / total_size)
    # may have downloaded less if count*block_size > total_size
    maxdownloaded = count * block_size
    percent = min(int(maxdownloaded * 100 / total_size), 100)
    if percent > last_percent:
        # TODO: is this acceptable? Do we want to do something nicer?
        out.write(
            '%3d%% [%s>%s]\r' % (
                percent,
                int(percent / 2) * '=',
                int(50 - percent / 2) * ' '
            )
        )
        out.flush()
    if maxdownloaded >= total_size:
        print('\n')


# Code from https://github.com/pypa/warehouse
# Copyright 2013 Donald Stufft
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class AttributeDict(dict):

    def __getattr__(self, name):
        if name not in self:
            raise AttributeError("'{}' object has no attribute '{}'".format(
                self.__class__,
                name,
            ))

        return self[name]


def merge_dict(base, additional):
    if base is None:
        return additional

    if additional is None:
        return base

    if not (isinstance(base, collections.Mapping)
            and isinstance(additional, collections.Mapping)):
        return additional

    merged = base
    for key, value in additional.items():
        if isinstance(value, collections.Mapping):
            merged[key] = merge_dict(merged.get(key), value)
        else:
            merged[key] = value

    return merged


def convert_to_attr_dict(dictionary):
    output = {}
    for key, value in dictionary.items():
        if isinstance(value, collections.Mapping):
            output[key] = convert_to_attr_dict(value)
        else:
            output[key] = value
    return AttributeDict(output)

# Code from https://github.com/mitsuhiko/werkzeug
# Copyright 2013 Werkzeug Team.
# LICENSE: https://github.com/mitsuhiko/werkzeug/blob/master/LICENSE


class ImportStringError(ImportError):
    """Provides information about a failed :func:`import_string` attempt."""

    #: String in dotted notation that failed to be imported.
    import_name = None
    #: Wrapped exception.
    exception = None

    def __init__(self, import_name, exception):
        self.import_name = import_name
        self.exception = exception

        msg = (
            'import_string() failed for %r. Possible reasons are:\n\n'
            '- missing __init__.py in a package;\n'
            '- package or module path not included in sys.path;\n'
            '- duplicated package or module name taking precedence in '
            'sys.path;\n'
            '- missing module, class, function or variable;\n\n'
            'Debugged import:\n\n%s\n\n'
            'Original exception:\n\n%s: %s')

        name = ''
        tracked = []
        for part in import_name.replace(':', '.').split('.'):
            name += (name and '.') + part
            imported = import_string(name, silent=True)
            if imported:
                tracked.append((name, getattr(imported, '__file__', None)))
            else:
                track = ['- %r found in %r.' % (n, i) for n, i in tracked]
                track.append('- %r not found.' % name)
                msg = msg % (import_name, '\n'.join(track),
                             exception.__class__.__name__, str(exception))
                break

        ImportError.__init__(self, msg)

    def __repr__(self):
        return '<%s(%r, %r)>' % (self.__class__.__name__, self.import_name,
                                 self.exception)


def import_string(import_name, silent=False):
    """Imports an object based on a string.  This is useful if you want to
    use import paths as endpoints or something similar.  An import path can
    be specified either in dotted notation (``xml.sax.saxutils.escape``)
    or with a colon as object delimiter (``xml.sax.saxutils:escape``).

    If `silent` is True the return value will be `None` if the import fails.

    :param import_name: the dotted name for the object to import.
    :param silent: if set to `True` import errors are ignored and
                   `None` is returned instead.
    :return: imported object
    """
    # XXX: py3 review needed
    assert isinstance(import_name, string_types)
    # force the import name to automatically convert to strings
    import_name = str(import_name)
    try:
        if ':' in import_name:
            module, obj = import_name.split(':', 1)
        elif '.' in import_name:
            module, obj = import_name.rsplit('.', 1)
        else:
            return __import__(import_name)
        # __import__ is not able to handle unicode strings in the fromlist
        # if the module is a package
        if PY2 and isinstance(obj, unicode):
            obj = obj.encode('utf-8')
        try:
            return getattr(__import__(module, None, None, [obj]), obj)
        except (ImportError, AttributeError):
            # support importing modules not yet set up by the parent module
            # (or package for that matter)
            modname = module + '.' + obj
            __import__(modname)
            return sys.modules[modname]
    except ImportError as e:
        if not silent:
            reraise(
                ImportStringError,
                ImportStringError(import_name, e),
                sys.exc_info()[2])


def find_modules(import_path, include_packages=False, recursive=False):
    """Find all the modules below a package.  This can be useful to
    automatically import all views / controllers so that their metaclasses /
    function decorators have a chance to register themselves on the
    application.

    Packages are not returned unless `include_packages` is `True`.  This can
    also recursively list modules but in that case it will import all the
    packages to get the correct load path of that module.

    :param import_name: the dotted name for the package to find child modules.
    :param include_packages: set to `True` if packages should be returned, too.
    :param recursive: set to `True` if recursion should happen.
    :return: generator
    """
    module = import_string(import_path)
    path = getattr(module, '__path__', None)
    if path is None:
        raise ValueError('%r is not a package' % import_path)
    basename = module.__name__ + '.'
    for importer, modname, ispkg in pkgutil.iter_modules(path):
        modname = basename + modname
        if ispkg:
            if include_packages:
                yield modname
            if recursive:
                for item in find_modules(modname, include_packages, True):
                    yield item
        else:
            yield modname


def supports_wide():
    """Return if python interpreter supports wide characters.

    :returns: Returns `True` if python supports wide character sets.
    :rtype: bool
    """
    return sys.maxunicode > 0xffff
