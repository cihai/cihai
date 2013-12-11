# -*- coding: utf-8 -*-
"""Tests for cihai.

cihai.testsuite.test_sqlalchemy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

Raw CSV Import
--------------

To aid in developing, CSV's will be dumped into a sqlite file for speed.

To properly test the unihan.db created is accurate, raw CSV's will md5'd, lines
counted and info stored to data/unihan_info.ini.

Then dumped raw into sqlite databases.

Tests are made to verify the RawCSVImporter:

- Retrieves the total number of items from CSV (excluding comments).
- Retrieves MD5 sum of file
- Saves both to data/unihan_info.ini
- All rows are added, the CSV row count matches with the table count.
- Data is consistent, untouched from CSV format (no encoding/decoding).

TestCase Helper
---------------

The CSV row count will be checked against the unihan.db row count to verify
integrity.

If no unihan.db or unihan_info.ini exist, unihan.db will be repopulated.

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import tempfile
import logging
import csv

import sqlalchemy

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, \
    String, Index

from .helpers import TestCase, unittest
from .._compat import PY2, text_type
from ..unihan import get_datafile, UnihanReader, RawReader

log = logging.getLogger(__name__)

sqlite_db = get_datafile('unihan.db')


def csv_to_table(engine, csv_file, table_name, fields):
    """Create table from CSV.

    :param engine: sqlalchemy engine
    :type engine: :sqlalchemy:class:`sqlalchemy.engine.Engine`
    :param csv_file: csv file
    :type csv_file: string
    :param table_name: name of table
    :type table_name: string
    :param fields: csv / table fields and sqlalchemy type.
        from ``sqlalchemy.types``.
    :type fields: tuple

    """

    metadata = MetaData(bind=engine)

    table = Table(table_name, metadata)

    col = Column('id', Integer, primary_key=True)
    table.append_column(col)

    field_names = [field for (field, t) in fields]
    field_types = {
        'string': String(256)
    }

    for (field, type_) in fields:
        col = Column(field, field_types[type_])
        table.append_column(col)

    Index('unique', table.c.char, table.c.field, table.c.value, unique=True)

    if os.path.exists(sqlite_db):
        print('db exists: %s' % sqlite_db)
    try:
        if table.exists():
            pass
        if not table.exists():
            table.create()

            pass
    except Exception as e:
        print(e)
        table.create()

    with open(csv_file, 'r') as csvfile:

        delim = b'\t' if PY2 else '\t'
        csvfile = filter(lambda row: row[0] != '#', csvfile)

        r = RawReader(
            csvfile,
            fieldnames=['char', 'field', 'value'],
            delimiter=delim
        )

        r = list(r)

        if table.select().count().execute().scalar() != len(r):
            try:
                results = engine.execute(table.insert(), r)
            except sqlalchemy.exc.IntegrityError as e:
                raise(e)
            except Exception as e:
                raise(e)
        else:
            print('rows populated, all is well!')

        print(
            "csv count: %s    row count: %s" % (
                len(r),
                table.select().count().execute().scalar()
            )
        )


class UnihanSQLAlchemyRaw(TestCase):

    """Dump the Raw Unihan CSV's into SQLite database."""

    # @unittest.skip('Postpone until CSV reader decodes and returns Unicode.')
    def test_create_data(self):

        if not os.path.exists(sqlite_db):
            pass

        engine = create_engine('sqlite:///%s' % sqlite_db, echo=False)
        csv_to_table(
            engine=engine,
            csv_file=get_datafile('Unihan_Readings.txt'),
            table_name='Unihan',
            fields=[
                ('char', 'string'),
                ('field', 'string'),
                ('value', 'string')
            ]
        )

        with open(get_datafile('Unihan_Readings.txt'), 'r') as csvfile:
            # py3.3 regression http://bugs.python.org/issue18829
            delim = b'\t' if PY2 else '\t'
            csvfile = filter(lambda row: row[0] != '#', csvfile)
            r = RawReader(
                csvfile,
                fieldnames=['char', 'field', 'value'],
                delimiter=delim
            )

            r = list(r)[:5]
            print('\n')

            for row in r:
                print('%s' % row)
