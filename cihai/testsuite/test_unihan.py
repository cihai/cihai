# -*- coding: utf-8 -*-
"""Tests for cihai.

cihai.testsuite.test_unihan
~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import tempfile
import random
import logging

import sqlalchemy

from .helpers import unittest, TestCase, CihaiTestCase
from .._compat import PY2, text_type
from ..unihan import get_datafile, get_table, UnihanReader, \
    UNIHAN_FILENAMES, get_metadata, table_exists, install_raw_csv, \
    engine, create_table
from ..conversion import ucn_to_unicode

log = logging.getLogger(__name__)


class UnihanData(TestCase):

    def test_zip(self):
        self.assertEqual(2, 2)

    def test_files(self):
        """Test unihan text file data."""
        pass


class UnihanTable(CihaiTestCase):

    def test_returns_instance_table(self):
        table = get_table('Unihan_NumericValues')

        self.assertIsInstance(table, sqlalchemy.Table)

    def test_returns_metadata_has_csv_tables(self):
        for filename in UNIHAN_FILENAMES:
            tablename = filename.split('.')[0]
            self.assertIn(tablename, [table for table in get_metadata().tables])


class UnihanDataCSV(TestCase):

    @unittest.skip('Wait until helper TestCase is implemented.')
    def test_print_top(self):
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
                rowlines = []
                for key in row.keys():
                    if key == 'field' and not isinstance(row[key], text_type):
                        # import cchardet as chardet
                        # log.error(chardet.detect(row[key]))
                        # codec = chardet.detect(row[key])['encoding']
                        #row[key] = row[key].decode(codec)
                        self.assertIsInstance(row[key], text_type)
                    elif key == 'value':
                        # import chardet
                        # log.error(chardet.detect(row[key]))
                        # codec = chardet.detect(row[key])['encoding']
                        # #row[key] = row[key].decode(codec)
                        # self.assertIsInstance(row[key], text_type)
                        pass

                    rowlines.append(row[key])
                try:
                    rowline = '\t'.join(rowlines)
                except UnicodeDecodeError as e:
                    log.info('row: %s (%s) gives:\n%s' % (row, row['char'], e))

                print('%s' % rowline)


class UnihanMethods(CihaiTestCase):

    def test_returns_table(self):
        csv_filename = random.choice(UNIHAN_FILENAMES)
        self.assertRegexpMatches(csv_filename, 'Unihan')
        table = install_raw_csv(get_datafile(csv_filename))
        self.assertIsInstance(table, sqlalchemy.schema.Table)

    def test_table_exists(self):
        metadata = get_metadata()
        for table_name in metadata.tables:
            self.assertTrue(table_exists(table_name))
            self.assertIsInstance(table_name, text_type)

    def test_get_metadata(self):
        metadata = get_metadata()

        self.assertIsInstance(metadata, sqlalchemy.MetaData)

    def test_get_table(self):
        metadata = get_metadata()
        # pick a random table name.
        table = get_table(random.choice(list(metadata.tables)))
        self.assertIsInstance(table, sqlalchemy.Table)

    def test_get_datafile(self):
        # file installed on installation.
        csv_filename = random.choice(UNIHAN_FILENAMES)

        csv_abspath = get_datafile(csv_filename)
        self.assertNotEqual(csv_filename, csv_abspath)
        self.assertIsInstance(csv_abspath, text_type)

    def test_create_table(self):
        table_name = 'testTable_%s' % random.randint(1, 1337)

        table = create_table(table_name, engine)

        self.assertIsInstance(table, sqlalchemy.Table)
        self.assertTrue(table.exists())

        table.drop()

        self.assertFalse(table.exists())


class UnihanReadings(CihaiTestCase):

    def test_kMandarin(self):
        table = get_table('Unihan_Readings')

        rows = table.select().where(table.c.field == 'kMandarin').limit(4).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kDefinition(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kDefinition
        Major definitions are separated by semicolons, and minor definitions by
        commas. Any valid Unicode character (except for tab, double-quote, and
        any line break character) may be used within the definition field.
        """

        rows = table.select().where(table.c.field == 'kDefinition').limit(4).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kCantonese(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kCantonese
        A full description of jyutping can be found at
        <http://www.lshk.org/cantonese.php>. The main differences between
        jyutping and the Yale romanization previously used are:
        """

        rows = table.select().where(table.c.field == 'kCantonese').limit(4).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kHangul(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kHangul

        """

        rows = table.select().where(table.c.field == 'kHangul').limit(4).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kHanyuPinlu(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kHanyuPinlu

        """

        rows = table.select().where(table.c.field == 'kHanyuPinlu').limit(4).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kHanyuPinyin(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kHanyuPinyin

        """

        rows = table.select().where(table.c.field == 'kHanyuPinyin').limit(4).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kJapaneseKun(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kJapaneseKun

        """

        rows = table.select().where(table.c.field == 'kJapaneseKun').limit(4).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kJapaneseOn(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kJapaneseKun

        """

        rows = table.select().where(table.c.field == 'kJapaneseOn').limit(4).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kKorean(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kKorean

        """

        rows = table.select().where(table.c.field == 'kKorean').limit(4).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kTang(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kTang

        """

        rows = table.select().where(table.c.field == 'kTang').limit(4).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kVietnamese(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kVietnamese

        """

        rows = table.select().where(table.c.field == 'kVietnamese').limit(4).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kXHC1983(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kVietnamese

        """

        rows = table.select().where(table.c.field == 'kXHC1983').limit(4).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_searchByChar(self):
        pass
