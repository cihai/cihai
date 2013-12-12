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
import hashlib
import random

import sqlalchemy

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, \
    String, Index, inspect, and_, select

from .helpers import TestCase, unittest
from .._compat import PY2, text_type, configparser
from ..unihan import get_datafile, UnihanReader, RawReader, UNIHAN_FILES, \
    table_exists

log = logging.getLogger(__name__)

sqlite_db = get_datafile('unihan.db')
unihan_config = get_datafile('unihan.conf')


def create_table(table_name, fields, engine):
    """Create table and return  :sqlalchemy:class:`sqlalchemy.Table`.

    :param table_name: name of table to create
    :type table_name: string
    :param fields: name and type of column to create
    :type fields: dict
    :param engine: sqlalchemy engine
    :type engine: :sqlalchemy:`sqlalchemy.Engine`
    :returns: Newly created table with columns and index.
    :rtype: :class:`sqlalchemy.schema.Table`

    """
    metadata = MetaData(bind=engine)
    table = Table(table_name, metadata)

    col = Column('id', Integer, primary_key=True)
    table.append_column(col)

    field_names = [field for (field, t) in fields]

    for (field, type_) in fields:
        col = Column(field, type_)
        table.append_column(col)

    Index('%s_unique' % table_name, table.c.char, table.c.field, table.c.value, unique=True)

    if not table.exists():
        table.create()

    return table


def csv_to_table(engine, csv_filename, table_name, fields):
    """Create table from CSV.

    :param engine: sqlalchemy engine
    :type engine: :class:`sqlalchemy.engine.Engine`
    :param csv_filename: csv file name inside data, e.g. ``Unihan_Readings.txt``.
    :type csv_filename: string
    :param table_name: name of table
    :type table_name: string
    :param fields: csv / table fields and sqlalchemy type.
        e.g. :class:`sqlalchemy.types.Integer`.
    :type fields: tuple
    :rtype: :class:`sqlalchemy.schema.Table`

    """

    table = create_table(table_name, fields, engine)
    unihan_csv = get_datafile(csv_filename)

    with open(unihan_csv, 'r') as csv_file:
        csv_md5 = hashlib.sha256(unihan_csv.encode('utf-8')).hexdigest()
        csv_data = filter(lambda row: row[0] != '#', csv_file)
        delim = b'\t' if PY2 else '\t'

        config = configparser.ConfigParser()
        config.read(unihan_config)
        if not config.has_section(csv_filename):
            config.add_section(csv_filename)

        if (
            not os.path.exists(unihan_config) or
            not config.has_option(csv_filename, 'csv_rowcount') or
            (
                config.has_option(csv_filename, 'csv_rowcount') and
                table.select().count().execute().scalar() != config.getint(csv_filename, 'csv_rowcount')
            )
        ):

            r = RawReader(
                csv_data,
                fieldnames=['char', 'field', 'value'],
                delimiter=delim
            )
            r = list(r)

            try:
                results = engine.execute(table.insert(), r)
                config.set(csv_filename, 'csv_rowcount', text_type(len(r)))
            except sqlalchemy.exc.IntegrityError as e:
                raise(e)
            except Exception as e:
                raise(e)
        else:
            log.debug('Rows populated, all is well!')

        config.set(csv_filename, 'csv_md5', csv_md5)
        config_file = open(unihan_config, 'w+')
        config.write(config_file)
        config_file.close()
    return table


class UnihanImport(TestCase):

    """Dump the Raw Unihan CSV's into SQLite database.

    Should have decorator not to run if unihan.db exists.
    """
    csv_filename = None
    table_name = None

    def setUp(self):
        self.engine = create_engine('sqlite:///%s' % sqlite_db, echo=False)
        self.metadata = MetaData(bind=self.engine)

    def test_sqlite3_matches_csv(self):

        if not self.table_name:
            pass
        elif table_exists(self.table_name):
            self.skipTest('{!r} table exists, skipping.'.format(self.table_name))

        if self.csv_filename:
            self.csv_to_db(self.csv_filename)

    def csv_to_db(self, csv_filename):
        config = configparser.ConfigParser()

        with open(get_datafile(csv_filename), 'r') as csv_file:
            csv_data = filter(lambda row: row[0] != '#', csv_file)
            table_name = self.table_name
            delim = b'\t' if PY2 else '\t'
            r = RawReader(
                csv_data,
                fieldnames=['char', 'field', 'value'],
                delimiter=delim
            )
            table = csv_to_table(
                engine=self.engine,
                csv_filename=csv_filename,
                table_name=table_name,
                fields=[
                    ('char', String(256)),
                    ('field', String(256)),
                    ('value', String(256)),
                ]
            )

            config.read(unihan_config)  # Re-read, csv_to_table edits conf.

            self.assertTrue(config.has_section(csv_filename))
            self.assertTrue(config.has_option(csv_filename, 'csv_rowcount'))
            self.assertTrue(config.has_option(csv_filename, 'csv_md5'))

            csv_rowcount = config.getint(csv_filename, 'csv_rowcount')

            b = inspect(table)

            self.assertEqual(len(b.columns), 4)
            self.assertEqual(
                [c.name for c in b.columns], ['id', 'char', 'field', 'value']
            )

            csv_lines = list(r)  # try just 500

            self.assertEqual(
                table.select().count().execute().scalar(),
                csv_rowcount
            )

            random_items = [random.choice(csv_lines) for i in range(10)]

            for csv_item in random_items:
                sql_item = select([
                    table.c.char, table.c.field, table.c.value
                ]).where(and_(
                    table.c.char == csv_item['char'],
                    table.c.field == csv_item['field']
                )).execute().fetchone()
                self.assertEqual(
                    sql_item,
                    tuple([csv_item['char'], csv_item['field'], csv_item['value']])
                )


class Unihan_DictionaryIndices(UnihanImport):
    csv_filename = 'Unihan_DictionaryIndices.txt'
    table_name = 'Unihan_DictionaryIndices'


class Unihan_DicionaryLikeData(UnihanImport):
    csv_filename = 'Unihan_DictionaryLikeData.txt'
    table_name = 'Unihan_DictionaryLikeData'


class Unihan_IRGSources(UnihanImport):
    csv_filename = 'Unihan_IRGSources.txt'
    table_name = 'Unihan_IRGSources'


class Unihan_NumericValues(UnihanImport):
    csv_filename = 'Unihan_NumericValues.txt'
    table_name = 'Unihan_NumericValues'


class Unihan_OtherMappings(UnihanImport):
    csv_filename = 'Unihan_OtherMappings.txt'
    table_name = 'Unihan_OtherMappings'


class Unihan_RadicalStrokeCounts(UnihanImport):
    csv_filename = 'Unihan_RadicalStrokeCounts.txt'
    table_name = 'Unihan_RadicalStrokeCounts'


class Unihan_Readings(UnihanImport):
    csv_filename = 'Unihan_Readings.txt'
    table_name = 'Unihan_Readings'


class Unihan_Variants(UnihanImport):
    csv_filename = 'Unihan_Variants.txt'
    table_name = 'Unihan_Variants'

