# -*- coding: utf8 - *-
"""For accessing vcspull as a package.

libunihan.unihan
~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import zipfile
import csv
import logging

from . import conversion
from ._compat import PY2, text_type

log = logging.getLogger(__name__)

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

    def __next__(self):
        row = csv.DictReader.__next__(self)

        return self.row(row)

    def next(self):
        row = csv.DictReader.next(self)

        return self.row(row)

    def row(self, row):
        if row['char'].startswith('U+'):
            row['char'] = conversion.ucn_to_python(row['char'])

        if (
            row['field'] == 'kDefinition' or
            row['field'] == 'kMandarin'
        ):
            row['value'] = row['value']

        if not isinstance(row['field'], text_type):
            try:
                row['field'] = text_type(row['field'])
            except UnicodeDecodeError as e:
                log.info(row['field'])
                raise e
        return row


def main():
    with open(get_datafile('Unihan_Readings.txt'), 'r') as csvfile:
        # py3.3 regression http://bugs.python.org/issue18829
        delim = b'\t' if PY2 else '\t'
        csvfile = filter(lambda row: row[0] != '#', csvfile)
        r = UnihanReader(
            csvfile,
            fieldnames=['char', 'field', 'value'],
            delimiter=delim
        )

        r = list(r)[:5]
        print('\n')

        for row in r:
            print(row)
            print(type(row['char']))
            rowlines = []
            for key in row.keys():
                rowlines.append(row[key])
            try:
                rowline = '\t'.join(rowlines)
            except UnicodeDecodeError as e:
                log.info('row: %s (%s) gives:\n%s' % (row, row['char'], e))

            print('%s' % rowline)
