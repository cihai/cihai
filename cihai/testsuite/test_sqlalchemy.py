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

TestCase will then be able to pull from UnihanRaw data via SQLAlchemy.

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import tempfile
import logging
import csv
import random

import sqlalchemy

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, \
    String, Index, inspect, and_, select

from .helpers import TestCase, unittest
from .._compat import PY2, text_type
from ..unihan import get_datafile, UnihanReader, RawReader

log = logging.getLogger(__name__)

sqlite_db = get_datafile('unihan.db')


def get_table(table_name, fields, engine):
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

    return table


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

    table = get_table(table_name, fields, engine)

    with open(csv_file, 'r') as csvfile:

        csvfile = filter(lambda row: row[0] != '#', csvfile)
        delim = b'\t' if PY2 else '\t'

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

    """Dump the Raw Unihan CSV's into SQLite database.

    Should have decorator not to run if unihan.db exists.
    """
    def setUp(self):
        self.engine = create_engine('sqlite:///%s' % sqlite_db, echo=False)
        self.metadata = MetaData(bind=self.engine)
        try:
            self.table = Table('Unihan', self.metadata, autoload=True)
        except sqlalchemy.exc.NoSuchTableError as e:
            self.table = Table('Unihan', self.metadata)

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

    def test_sqlite3_matches_csv(self):
        """Test that sqlite3 data matches rows in CSV."""

        # pick out random rows in csv, check.
        # check by total rows in csv and sql table
        csvfile = open(get_datafile('Unihan_Readings.txt'), 'r')
        csvfile = filter(lambda row: row[0] != '#', csvfile)
        delim = b'\t' if PY2 else '\t'
        r = RawReader(
            csvfile,
            fieldnames=['char', 'field', 'value'],
            delimiter=delim
        )

        b = inspect(self.table)

        self.assertEqual(len(b.columns), 4)
        self.assertEqual(
            [c.name for c in b.columns], ['id', 'char', 'field', 'value']
        )

        csv_lines = list(r)
        csv_rowcount = len(csv_lines)

        self.assertEqual(
            self.table.select().count().execute().scalar(),
            csv_rowcount
        )

        random_items = [random.choice(csv_lines) for i in range(10)]

        for csv_item in random_items:
            sql_item = select([
                self.table.c.char, self.table.c.field, self.table.c.value
            ]).where(and_(
                self.table.c.char == csv_item['char'],
                self.table.c.field == csv_item['field']
            )).execute().fetchone()

            self.assertEqual(sql_item, tuple(csv_item.values()))

    def test_unihan_ini(self):
        """data/unihan.ini exists, has csv item counts and md5 of imported db.

        """

        engine = create_engine('sqlite:///%s' % sqlite_db, echo=False)

        pass
