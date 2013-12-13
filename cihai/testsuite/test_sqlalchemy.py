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

from sqlalchemy import create_engine, MetaData, Table, Column, \
    inspect, and_, select

from .helpers import unittest, TestCase, CihaiTestCase
from .._compat import PY2, text_type, configparser
from ..unihan import get_datafile, UnihanReader, RawReader, UNIHAN_FILENAMES, \
    table_exists, install_raw_csv, unihan_config, sqlite_db

log = logging.getLogger(__name__)


class UnihanInstallRaw(CihaiTestCase):

    """Dump the Raw Unihan CSV's into SQLite database."""
    csv_filename = None
    table_name = None

    def test_verify_csv_sqlite_integrity(self):
        if self.csv_filename:
            self.csv_to_db(self.csv_filename)

    def csv_to_db(self, csv_filename):
        config = configparser.ConfigParser()
        config.read(unihan_config)  # Re-read, csv_to_table edits conf.

        if config.has_section(csv_filename) and config.has_option(csv_filename, 'csv_verified'):
            if config.getboolean(csv_filename, 'csv_verified'):
                self.skipTest('%s already tested. Skipping.' % csv_filename)

        with open(get_datafile(csv_filename), 'r') as csv_file:
            csv_data = filter(lambda row: row[0] != '#', csv_file)

            csv_lines = list(csv_data)
            csv_random = [random.choice(csv_lines) for i in range(10)]
            delim = b'\t' if PY2 else '\t'
            random_items = RawReader(
                csv_random,
                fieldnames=['char', 'field', 'value'],
                delimiter=delim
            )

            table = install_raw_csv(csv_filename)
            config.read(unihan_config)  # Re-read, csv_to_table edits conf.
            b = inspect(table)

            self.assertTrue(config.has_section(csv_filename))
            self.assertTrue(config.has_option(csv_filename, 'csv_rowcount'))
            self.assertTrue(config.has_option(csv_filename, 'csv_md5'))

            csv_rowcount = config.getint(csv_filename, 'csv_rowcount')

            self.assertEqual(len(b.columns), 4)
            self.assertEqual(
                [c.name for c in b.columns], ['id', 'char', 'field', 'value']
            )

            self.assertEqual(
                table.select().count().execute().scalar(),
                csv_rowcount
            )

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

            config.set(csv_filename, 'csv_verified', True)
            config_file = open(unihan_config, 'w+')
            config.write(config_file)
            config_file.close()


class Unihan_DictionaryIndices(UnihanInstallRaw):
    csv_filename = 'Unihan_DictionaryIndices.txt'
    table_name = 'Unihan_DictionaryIndices'


class Unihan_DicionaryLikeData(UnihanInstallRaw):
    csv_filename = 'Unihan_DictionaryLikeData.txt'
    table_name = 'Unihan_DictionaryLikeData'


class Unihan_IRGSources(UnihanInstallRaw):
    csv_filename = 'Unihan_IRGSources.txt'
    table_name = 'Unihan_IRGSources'


class Unihan_NumericValues(UnihanInstallRaw):
    csv_filename = 'Unihan_NumericValues.txt'
    table_name = 'Unihan_NumericValues'


class Unihan_OtherMappings(UnihanInstallRaw):
    csv_filename = 'Unihan_OtherMappings.txt'
    table_name = 'Unihan_OtherMappings'


class Unihan_RadicalStrokeCounts(UnihanInstallRaw):
    csv_filename = 'Unihan_RadicalStrokeCounts.txt'
    table_name = 'Unihan_RadicalStrokeCounts'


class Unihan_Readings(UnihanInstallRaw):
    csv_filename = 'Unihan_Readings.txt'
    table_name = 'Unihan_Readings'


class Unihan_Variants(UnihanInstallRaw):
    csv_filename = 'Unihan_Variants.txt'
    table_name = 'Unihan_Variants'

