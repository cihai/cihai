# -*- coding: utf8 - *-
"""Utility and helper methods for cihai.

cihai.util
~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import csv

from ._compat import text_type


def get_datafile(filename):
    """Return absolute path to cihai data file.

    :param filename: file name relative to ``./data``.
    :type filename: string
    :returns: Absolute path to data file.
    :rtype: string

    """

    abspath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/', filename)
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
