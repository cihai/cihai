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
import re
import tempfile
import random
import logging

import sqlalchemy

from .. import conversion

from .helpers import unittest, TestCase, CihaiTestCase
from .._compat import PY2, text_type, configparser
from ..util import get_datafile
from ..unihan import UNIHAN_FILENAMES, Unihan, RawReader
from ..conversion import ucn_to_unicode
from ..cihai import cihai_db, cihai_config

log = logging.getLogger(__name__)


class UnihanTestCase(TestCase):

    unihan = None

    def setUp(self):
        if not self.unihan:
            self.unihan = Unihan()


class UnihanRawImportCase(object):

    """Dump the Raw Unihan CSV's into SQLite database."""
    csv_filename = None
    table_name = None

    def test_verify_csv_sqlite_integrity(self):
        if self.csv_filename:
            self.csv_to_db(self.csv_filename)

    def csv_to_db(self, csv_filename):
        config = configparser.ConfigParser()
        config.read(cihai_config)  # Re-read, csv_to_table edits conf.

        # store a key in unihan.conf to prevent re-running (saves 3+ seconds)
        if config.has_section(csv_filename) and config.has_option(csv_filename, 'csv_verified'):
            if config.getboolean(csv_filename, 'csv_verified'):
                self.skipTest('%s already tested. Skipping.' % csv_filename)

        with open(get_datafile(csv_filename), 'r') as csv_file:
            # filter out comments
            csv_data = filter(lambda row: row[0] != '#', csv_file)

            # pick random lines *before* passing into RawReader.
            csv_lines = list(csv_data)
            csv_random = [random.choice(csv_lines) for i in range(10)]

            delim = b'\t' if PY2 else '\t'
            random_items = RawReader(
                csv_random,
                fieldnames=['char', 'field', 'value'],
                delimiter=delim
            )

            table = self.unihan.install_raw_csv(csv_filename)
            config.read(cihai_config)  # Re-read since csv import updates conf.
            b = sqlalchemy.inspect(table)

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
                sql_item = sqlalchemy.select([
                    table.c.char, table.c.field, table.c.value
                ]).where(sqlalchemy.and_(
                    table.c.char == csv_item['char'],
                    table.c.field == csv_item['field']
                )).execute().fetchone()
                self.assertEqual(
                    sql_item,
                    tuple([csv_item['char'], csv_item['field'], csv_item['value']])
                )

            config.set(csv_filename, 'csv_verified', text_type(True))
            config_file = open(cihai_config, 'w+')
            config.write(config_file)
            config_file.close()


class UnihanTable(UnihanTestCase):

    def setUp(self):
        super(UnihanTable, self).setUp()
        self.unihan.install_raw_csv('Unihan_NumericValues.txt')

    def test_returns_instance_table(self):
        table = self.unihan.get_table('Unihan_NumericValues')

        self.assertIsInstance(table, sqlalchemy.Table)

    def test_returns_metadata_has_csv_tables(self):
        """CSV files should install their filename with .txt truncated.

        Unihan_NumericValues.txt is table Unihan_NumericValues.

        """

        self.assertIn('Unihan_NumericValues', [f.split('.')[0] for f in UNIHAN_FILENAMES])


class UnihanMethods(UnihanTestCase):

    def setUp(self):
        super(UnihanMethods, self).setUp()

        # Assures at least one table is installed before testing.
        self.unihan.install_raw_csv('Unihan_NumericValues.txt')

    def test_returns_table(self):
        csv_filename = random.choice(UNIHAN_FILENAMES)
        self.assertRegexpMatches(csv_filename, 'Unihan')
        table = self.unihan.install_raw_csv(csv_filename)
        self.assertIsInstance(table, sqlalchemy.schema.Table)

    def test_create_table(self):
        table_name = 'testTable_%s' % random.randint(1, 1337)

        table = self.unihan.create_table(table_name)

        self.assertIsInstance(table, sqlalchemy.Table)
        self.assertTrue(table.exists())

        self.unihan.metadata.drop_all(tables=[table])

        self.assertFalse(table.exists())


class UnihanReadings(UnihanTestCase):
    def setUp(self):
        super(UnihanReadings, self).setUp()

        # Assures at least one table is installed before testing.
        self.unihan.install_raw_csv('Unihan_Readings.txt')
        self.table = self.unihan.get_table('Unihan_Readings')

    def test_kMandarin(self):
        rows = self.table.select().where(self.table.c.field == 'kMandarin').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kDefinition(self):
        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kDefinition
        Major definitions are separated by semicolons, and minor definitions by
        commas. Any valid Unicode character (except for tab, double-quote, and
        any line break character) may be used within the definition field.
        """

        rows = self.table.select().where(self.table.c.field == 'kDefinition').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kCantonese(self):
        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kCantonese
        A full description of jyutping can be found at
        <http://www.lshk.org/cantonese.php>. The main differences between
        jyutping and the Yale romanization previously used are:
        """

        rows = self.table.select().where(self.table.c.field == 'kCantonese').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kHangul(self):
        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kHangul

        """

        rows = self.table.select().where(self.table.c.field == 'kHangul').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kHanyuPinlu(self):
        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kHanyuPinlu

        """

        rows = self.table.select().where(self.table.c.field == 'kHanyuPinlu').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kHanyuPinyin(self):
        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kHanyuPinyin

        """

        rows = self.table.select().where(self.table.c.field == 'kHanyuPinyin').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kJapaneseKun(self):
        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kJapaneseKun

        """

        rows = self.table.select().where(self.table.c.field == 'kJapaneseKun').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kJapaneseOn(self):
        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kJapaneseKun

        """

        rows = self.table.select().where(self.table.c.field == 'kJapaneseOn').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kKorean(self):
        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kKorean

        """

        rows = self.table.select().where(self.table.c.field == 'kKorean').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kTang(self):
        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kTang

        """

        rows = self.table.select().where(self.table.c.field == 'kTang').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kVietnamese(self):
        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kVietnamese

        """

        rows = self.table.select().where(self.table.c.field == 'kVietnamese').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kXHC1983(self):
        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kXHC1983

        """

        rows = self.table.select().where(self.table.c.field == 'kXHC1983').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_table_exists(self):
        self.assertTrue(self.unihan.table_exists('Unihan_Readings'))


class UnihanVariants(UnihanTestCase):

    def setUp(self):
        super(UnihanVariants, self).setUp()

        # Assures at least one table is installed before testing.
        self.unihan.install_raw_csv('Unihan_Variants.txt')

    def test_table_exists(self):
        self.assertTrue(self.unihan.table_exists('Unihan_Variants'))

    def test_kSemanticVariant(self):
        table = self.unihan.get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kSemanticVariant

        """

        rows = table.select().where(table.c.field == 'kSemanticVariant').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kTraditionalVariant(self):
        table = self.unihan.get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kTraditionalVariant

        """

        rows = table.select().where(table.c.field == 'kTraditionalVariant').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kSpecializedSemanticVariant(self):
        table = self.unihan.get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kSpecializedSemanticVariant

        """

        rows = table.select().where(table.c.field == 'kSpecializedSemanticVariant').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kSimplifiedVariant(self):
        table = self.unihan.get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kSimplifiedVariant

        """

        rows = table.select().where(table.c.field == 'kSimplifiedVariant').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kCompatibilityVariant(self):
        table = self.unihan.get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kCompatibilityVariant

        """

        rows = table.select().where(table.c.field == 'kCompatibilityVariant').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)


class UnihanRadicalStrokeCounts(UnihanTestCase):

    def setUp(self):
        super(UnihanRadicalStrokeCounts, self).setUp()

        # Assures at least one table is installed before testing.
        self.unihan.install_raw_csv('Unihan_RadicalStrokeCounts.txt')
        self.table = self.unihan.get_table('Unihan_RadicalStrokeCounts')

    def test_table_exists(self):
        self.assertTrue(self.unihan.table_exists('Unihan_RadicalStrokeCounts'))

    def test_kRSAdobe_Japan1_6(self):
        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSAdobe_Japan1_6

        """

        rows = self.table.select().where(self.table.c.field == 'kRSAdobe_Japan1_6').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kRSJapanese(self):
        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSJapanese

        """

        rows = self.table.select().where(self.table.c.field == 'kRSJapanese').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kRSKangXi(self):
        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSKangXi

        """

        rows = self.table.select().where(self.table.c.field == 'kRSKangXi').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kRSKanWa(self):
        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSKanWa

        """

        rows = self.table.select().where(self.table.c.field == 'kRSKanWa').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kRSKorean(self):
        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSKorean

        """

        rows = self.table.select().where(self.table.c.field == 'kRSKorean').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kRSUnicode(self):
        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSUnicode

        """

        rows = self.table.select().where(self.table.c.field == 'kRSUnicode').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)


class UnihanNumericValues(UnihanTestCase):

    def setUp(self):
        super(UnihanNumericValues, self).setUp()

        # Assures at least one table is installed before testing.
        self.unihan.install_raw_csv('Unihan_NumericValues.txt')

    def test_table_exists(self):
        self.assertTrue(self.unihan.table_exists('Unihan_NumericValues'))

    def test_kAccountingNumeric(self):
        table = self.unihan.get_table('Unihan_NumericValues')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kAccountingNumeric

        """

        rows = table.select().where(table.c.field == 'kAccountingNumeric').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kOtherNumeric(self):
        table = self.unihan.get_table('Unihan_NumericValues')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kOtherNumeric

        """

        rows = table.select().where(table.c.field == 'kOtherNumeric').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kPrimaryNumeric(self):
        table = self.unihan.get_table('Unihan_NumericValues')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kPrimaryNumeric

        """

        rows = table.select().where(table.c.field == 'kPrimaryNumeric').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)


class UnihanDictionaryLikeData(UnihanTestCase):

    def setUp(self):
        super(UnihanDictionaryLikeData, self).setUp()

        # Assures at least one table is installed before testing.
        self.unihan.install_raw_csv('Unihan_DictionaryLikeData.txt')

    def test_table_exists(self):
        self.assertTrue(self.unihan.table_exists('Unihan_DictionaryLikeData'))

    def test_kFrequency(self):
        table = self.unihan.get_table('Unihan_DictionaryLikeData')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kFrequency

        """

        rows = table.select().where(table.c.field == 'kFrequency').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kPhonetic(self):
        table = self.unihan.get_table('Unihan_DictionaryLikeData')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kPhonetic

        """

        rows = table.select().where(table.c.field == 'kPhonetic').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kTotalStrokes(self):
        table = self.unihan.get_table('Unihan_DictionaryLikeData')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kTotalStrokes

        """

        rows = table.select().where(table.c.field == 'kTotalStrokes').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kGradeLevel(self):
        table = self.unihan.get_table('Unihan_DictionaryLikeData')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kGradeLevel

        """

        rows = table.select().where(table.c.field == 'kGradeLevel').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)


class kDefinition(UnihanTestCase):

    """
    http://www.unicode.org/reports/tr38/tr38-15.html#kDefinition
    Major definitions are separated by semicolons, and minor definitions by
    commas. Any valid Unicode character (except for tab, double-quote, and
    any line break character) may be used within the definition field.
    """

    def setUp(self):
        super(kDefinition, self).setUp()

        # Assures at least one table is installed before testing.
        self.unihan.install_raw_csv('Unihan_Readings.txt')
        self.table = self.unihan.get_table('Unihan_Readings')

    def test_like(self):
        def selectkDefinition(char=None):
            select = self.table.select().where(self.table.c.field == 'kDefinition')

            if char:
                select = select.where(self.table.c.char == conversion.python_to_ucn(char))

            return select

        self.assertNotIn('LIKE', selectkDefinition().compile().__str__())

        kDefinitionQuery = selectkDefinition().where(
            self.table.c.value.like('%(same as%')
        )

        self.assertIn('LIKE', kDefinitionQuery.compile().__str__())
        rows = kDefinitionQuery.execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)
            self.assertTrue(re.search('\(same as', r.value))

        self.assertGreaterEqual(1, selectkDefinition(char='好').execute().rowcount)


class Unihan_DictionaryIndices(UnihanTestCase, UnihanRawImportCase):
    csv_filename = 'Unihan_DictionaryIndices.txt'
    table_name = 'Unihan_DictionaryIndices'

    def setUp(self):
        super(Unihan_DictionaryIndices, self).setUp()

        # Assures at least one table is installed before testing.
        self.unihan.install_raw_csv(self.csv_filename)


class Unihan_DictionaryLikeData(UnihanTestCase, UnihanRawImportCase):
    csv_filename = 'Unihan_DictionaryLikeData.txt'
    table_name = 'Unihan_DictionaryLikeData'

    def setUp(self):
        super(Unihan_DictionaryLikeData, self).setUp()

        # Assures at least one table is installed before testing.
        self.unihan.install_raw_csv(self.csv_filename)


class Unihan_IRGSources(UnihanTestCase, UnihanRawImportCase):
    csv_filename = 'Unihan_IRGSources.txt'
    table_name = 'Unihan_IRGSources'

    def setUp(self):
        super(Unihan_IRGSources, self).setUp()

        # Assures at least one table is installed before testing.
        self.unihan.install_raw_csv(self.csv_filename)


class Unihan_NumericValues(UnihanTestCase, UnihanRawImportCase):
    csv_filename = 'Unihan_NumericValues.txt'
    table_name = 'Unihan_NumericValues'

    def setUp(self):
        super(Unihan_NumericValues, self).setUp()

        # Assures at least one table is installed before testing.
        self.unihan.install_raw_csv(self.csv_filename)


class Unihan_OtherMappings(UnihanTestCase, UnihanRawImportCase):
    csv_filename = 'Unihan_OtherMappings.txt'
    table_name = 'Unihan_OtherMappings'

    def setUp(self):
        super(Unihan_OtherMappings, self).setUp()

        # Assures at least one table is installed before testing.
        self.unihan.install_raw_csv(self.csv_filename)


class Unihan_RadicalStrokeCounts(UnihanTestCase, UnihanRawImportCase):
    csv_filename = 'Unihan_RadicalStrokeCounts.txt'
    table_name = 'Unihan_RadicalStrokeCounts'

    def setUp(self):
        super(Unihan_RadicalStrokeCounts, self).setUp()

        # Assures at least one table is installed before testing.
        self.unihan.install_raw_csv(self.csv_filename)


class Unihan_Readings(UnihanRawImportCase):
    csv_filename = 'Unihan_Readings.txt'
    table_name = 'Unihan_Readings'

    def setUp(self):
        super(Unihan_Readings, self).setUp()

        # Assures at least one table is installed before testing.
        self.unihan.install_raw_csv(self.csv_filename)


class Unihan_Variants(UnihanRawImportCase):
    csv_filename = 'Unihan_Variants.txt'
    table_name = 'Unihan_Variants'

    def setUp(self):
        super(Unihan_Variants, self).setUp()

        # Assures at least one table is installed before testing.
        self.unihan.install_raw_csv(self.csv_filename)
