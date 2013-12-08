# -*- coding: utf8 - *-
"""For accessing vcspull as a package.

libunihan.unihan
~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, with_statement

import os
import zipfile
import csv

from . import conversion

UNIHAN_FILES = [
    'Unihan_DictionaryIndices.txt',
    'Unihan_DictionaryLikeData.txt',
    'Unihan_IRGSources.txt',
    'Unihan_NumericValues.txt',
    'Unihan_OtherMappings.txt',
    'Unihan_RadicalStrokeCounts.txt',
    'Unihan_Readings.txt',
    'Unihan_Variants.txt'
]


def get_datafile(file_):
    """Return absolute path to libunihan data file.

    :param file_: file name relative to ``./data``.
    :type file_: string
    :returns: Absolute path to data file.
    :rtype: string

    """
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/', file_)


class UnihanReader(csv.DictReader):
    """Read from Unihan CSV resource."""
    def __init__(self, *args, **kwargs):
        csv.DictReader.__init__(self, *args, **kwargs)

    def next(self):
        row = csv.DictReader.next(self)

        if row['char'].startswith('U+'):
            row['char'] = conversion.ucn_to_python(row['char'])

        if (
            row['field'] == 'kDefinition' or
            row['field'] == 'kMandarin'
        ):
            row['value'] = row['value'].decode('utf-8')

        return row

#  _neilg | borneo: you should be able to use regular expressions to convert
#  U+([a-f0-9]+)\b to \U[a-f0-9]{8}


def main():
    print('test')
