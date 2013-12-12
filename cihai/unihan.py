# -*- coding: utf8 - *-
"""Unihan file parsing, importing and codec handling.

cihai.unihan
~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import zipfile
import csv
import logging

from sqlalchemy import create_engine, MetaData, Table

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


def get_datafile(filename):
    """Return absolute path to cihai data file.

    :param filename: file name relative to ``./data``.
    :type filename: string
    :returns: Absolute path to data file.
    :rtype: string

    """
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/', filename)


sqlite_db = get_datafile('unihan.db')
engine = create_engine('sqlite:///%s' % sqlite_db, echo=False)
metadata = MetaData(bind=engine)
metadata.reflect()


def get_metadata():
    metadata = MetaData(bind=engine)
    metadata.reflect()

    return metadata


def get_table(table_name):
    """Return :class:`~sqlalchemy.schema.Table`.

    :param table_name: name of sql table
    :type table_name: string
    :rtype: :class:`sqlalchemy.schema.Table`

    """

    metadata = MetaData(bind=engine)
    metadata.reflect()
    table = Table(table_name, metadata, autoload=True)

    return table


def table_exists(table_name):
    """la
    """

    table = Table(table_name, metadata)

    return table.exists()


class RawReader(csv.DictReader):
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
        for key in row.keys():
            if not isinstance(row[key], text_type):
                row[key] = text_type(row[key].decode('utf-8'))

        return row


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
            row['char'] = conversion.ucn_to_unicode(row['char'])

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
