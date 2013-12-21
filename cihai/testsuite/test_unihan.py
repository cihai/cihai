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
import cProfile
from pstats import Stats

import sqlalchemy

from profilehooks import profile, coverage

from .. import conversion

from .helpers import unittest, TestCase, CihaiTestCase
from .._compat import PY2, text_type, configparser
from ..util import get_datafile, UnicodeReader
from ..datasets.unihan import UNIHAN_DATASETS, Unihan
from ..conversion import ucn_to_unicode
from ..cihai import cihai_db, cihai_config, Cihai

log = logging.getLogger(__name__)


class UnihanTest(Unihan):

    _engine = sqlalchemy.create_engine('sqlite:///:memory:')


class UnihanTestCase(TestCase):

    unihan = None

    def setUp(self):
        if not self.unihan:
            self.unihan = Unihan()


class UnihanInstall(TestCase):

    """Dump the Raw Unihan CSV's into SQLite database.

    1. default install dict
    2. open file, strip #'s
    3. count total entries
    4. concatenate csv files
    5. import to csv2dict
    6. count entries
    7. insert all into db
    8. verify counts of fields with db

    """

    # def setUp(self):
        # super(UnihanInstall, self).setUp()

    def setUp(self):
        """init each test"""
        super(UnihanInstall, self).setUp()
        # self.pr = cProfile.Profile()
        # self.pr.enable()
        # print("\n<<<---")

    def tearDown(self):
        """finish any test"""
        # p = Stats(self.pr)
        # p.strip_dirs()
        # p.sort_stats('cumtime')
        # p.print_stats()
        # print("\n--->>>")

    def test_datasets_schema(self):
        """UNIHAN_DATASETS schema is { 'FILENAME': ['fields'] }."""
        self.assertTrue(UNIHAN_DATASETS)
        self.assertIsInstance(UNIHAN_DATASETS, dict)

        for _file, fields in UNIHAN_DATASETS.items():
            self.assertIsInstance(_file, text_type)
            self.assertIsInstance(fields, list)
            for field in fields:
                self.assertIsInstance(field, text_type)

    @profile
    def test_get_csv_rows(self):
        unihan = Unihan()
        #unihan._metadata = sqlalchemy.MetaData(bind='sqlite://')
        data = unihan.get_csv_rows()

        newt = unihan.to_db(data)

        what = newt.select().count().execute()
        print(what)
        print(what.scalar())

    def test_strip_comments(self):
        pass

    def test_count_total_entries(self):
        pass

    def test_count_insert_all_into_db(self):
        pass

    def test_verify_count_of_fields_in_db(self):
        pass

    def test_saves_to_config(self):
        pass

# class UnihanTable(UnihanTestCase):

    # def setUp(self):
        # super(UnihanTable, self).setUp()
        # self.unihan.install('Unihan_NumericValues.txt')

    # def test_returns_instance_table(self):
        # table = self.unihan.get_table('Unihan')

        # self.assertIsInstance(table, sqlalchemy.Table)

    # def test_returns_metadata_has_csv_tables(self):
        # """CSV files should install their filename with .txt truncated.

        # Unihan_NumericValues.txt is table Unihan_NumericValues.

        # """

        # self.assertIn('Unihan_NumericValues', [f.split('.')[0] for f in UNIHAN_FILENAMES])


# class UnihanMethods(UnihanTestCase):

    # def setUp(self):
        # super(UnihanMethods, self).setUp()

        # # Assures at least one table is installed before testing.
        # self.unihan.install('Unihan_NumericValues.txt')

    # def test_returns_table(self):
        # csv_filename = random.choice(UNIHAN_FILENAMES)
        # self.assertRegexpMatches(csv_filename, 'Unihan')
        # table = self.unihan.install(csv_filename)
        # self.assertIsInstance(table, sqlalchemy.schema.Table)

    # def test__create_table(self):
        # table_name = 'testTable_%s' % random.randint(1, 1337)

        # table = self.unihan._create_table(table_name)

        # self.assertIsInstance(table, sqlalchemy.Table)
        # self.assertTrue(table.exists())

        # self.unihan.metadata.drop_all(tables=[table])

        # self.assertFalse(table.exists())


# class UnihanMiddleware(CihaiTestCase, UnihanTestCase):

    # def test_get(self):
        # c = Cihai()
        # c.use(Unihan)
        # results = c.get('你', fields=['kDefinition'])

        # #self.assertTrue(results)  # returns something
        # self.assertIsInstance(results, dict)
        # from pprint import pprint
        # pprint(results)

    # def test_reverse(self):

        # c = Cihai()
        # c.use(Unihan)
        # results = c.reverse(r'%first%', fields=['kDefinition'])
        # from pprint import pprint
        # pprint(results)


# class UnihanReadings(UnihanTestCase):
    # def setUp(self):
        # super(UnihanReadings, self).setUp()

        # # Assures at least one table is installed before testing.
        # self.unihan.install('Unihan_Readings.txt')
        # self.table = self.unihan.get_table('Unihan')

    # def test_kMandarin(self):
        # rows = self.table.select().where(self.table.c.field == 'kMandarin').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kDefinition(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kDefinition
        # Major definitions are separated by semicolons, and minor definitions by
        # commas. Any valid Unicode character (except for tab, double-quote, and
        # any line break character) may be used within the definition field.
        # """

        # rows = self.table.select().where(self.table.c.field == 'kDefinition').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kCantonese(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kCantonese
        # A full description of jyutping can be found at
        # <http://www.lshk.org/cantonese.php>. The main differences between
        # jyutping and the Yale romanization previously used are:
        # """

        # rows = self.table.select().where(self.table.c.field == 'kCantonese').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kHangul(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kHangul

        # """

        # rows = self.table.select().where(self.table.c.field == 'kHangul').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kHanyuPinlu(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kHanyuPinlu

        # """

        # rows = self.table.select().where(self.table.c.field == 'kHanyuPinlu').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kHanyuPinyin(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kHanyuPinyin

        # """

        # rows = self.table.select().where(self.table.c.field == 'kHanyuPinyin').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kJapaneseKun(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kJapaneseKun

        # """

        # rows = self.table.select().where(self.table.c.field == 'kJapaneseKun').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kJapaneseOn(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kJapaneseKun

        # """

        # rows = self.table.select().where(self.table.c.field == 'kJapaneseOn').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kKorean(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kKorean

        # """

        # rows = self.table.select().where(self.table.c.field == 'kKorean').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kTang(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kTang

        # """

        # rows = self.table.select().where(self.table.c.field == 'kTang').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kVietnamese(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kVietnamese

        # """

        # rows = self.table.select().where(self.table.c.field == 'kVietnamese').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kXHC1983(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kXHC1983

        # """

        # rows = self.table.select().where(self.table.c.field == 'kXHC1983').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # # def test_table_exists(self):
        # # self.assertTrue(self.unihan.table_exists('Unihan_Readings'))


# class UnihanVariants(UnihanTestCase):

    # def setUp(self):
        # super(UnihanVariants, self).setUp()

        # # Assures at least one table is installed before testing.
        # self.unihan.install('Unihan_Variants.txt')
        # self.table = self.unihan.get_table('Unihan')

    # # def test_table_exists(self):
        # # self.assertTrue(self.unihan.table_exists('Unihan_Variants'))

    # def test_kSemanticVariant(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kSemanticVariant

        # """

        # rows = self.table.select().where(self.table.c.field == 'kSemanticVariant').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kTraditionalVariant(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kTraditionalVariant

        # """

        # rows = self.table.select().where(self.table.c.field == 'kTraditionalVariant').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kSpecializedSemanticVariant(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kSpecializedSemanticVariant

        # """

        # rows = self.table.select().where(self.table.c.field == 'kSpecializedSemanticVariant').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kSimplifiedVariant(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kSimplifiedVariant

        # """

        # rows = self.table.select().where(self.table.c.field == 'kSimplifiedVariant').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kCompatibilityVariant(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kCompatibilityVariant

        # """

        # rows = self.table.select().where(self.table.c.field == 'kCompatibilityVariant').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)


# class UnihanRadicalStrokeCounts(UnihanTestCase):

    # def setUp(self):
        # super(UnihanRadicalStrokeCounts, self).setUp()

        # # Assures at least one table is installed before testing.
        # self.unihan.install('Unihan_RadicalStrokeCounts.txt')
        # self.table = self.unihan.get_table('Unihan')

    # # def test_table_exists(self):
        # # self.assertTrue(self.unihan.table_exists('Unihan_RadicalStrokeCounts'))

    # def test_kRSAdobe_Japan1_6(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kRSAdobe_Japan1_6

        # """

        # rows = self.table.select().where(self.table.c.field == 'kRSAdobe_Japan1_6').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kRSJapanese(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kRSJapanese

        # """

        # rows = self.table.select().where(self.table.c.field == 'kRSJapanese').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kRSKangXi(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kRSKangXi

        # """

        # rows = self.table.select().where(self.table.c.field == 'kRSKangXi').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kRSKanWa(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kRSKanWa

        # """

        # rows = self.table.select().where(self.table.c.field == 'kRSKanWa').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kRSKorean(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kRSKorean

        # """

        # rows = self.table.select().where(self.table.c.field == 'kRSKorean').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kRSUnicode(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kRSUnicode

        # """

        # rows = self.table.select().where(self.table.c.field == 'kRSUnicode').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)


# class UnihanNumericValues(UnihanTestCase):

    # def setUp(self):
        # super(UnihanNumericValues, self).setUp()

        # # Assures at least one table is installed before testing.
        # self.unihan.install('Unihan_NumericValues.txt')

    # # def test_table_exists(self):
        # # self.assertTrue(self.unihan.table_exists('Unihan_NumericValues'))

    # def test_kAccountingNumeric(self):
        # table = self.unihan.get_table('Unihan')

        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kAccountingNumeric

        # """

        # rows = table.select().where(table.c.field == 'kAccountingNumeric').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kOtherNumeric(self):
        # table = self.unihan.get_table('Unihan')

        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kOtherNumeric

        # """

        # rows = table.select().where(table.c.field == 'kOtherNumeric').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kPrimaryNumeric(self):
        # table = self.unihan.get_table('Unihan')

        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kPrimaryNumeric

        # """

        # rows = table.select().where(table.c.field == 'kPrimaryNumeric').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)


# class UnihanDictionaryLikeData(UnihanTestCase):

    # def setUp(self):
        # super(UnihanDictionaryLikeData, self).setUp()

        # # Assures at least one table is installed before testing.
        # self.unihan.install('Unihan_DictionaryLikeData.txt')
        # self.table = self.unihan.get_table('Unihan')

    # # def test_table_exists(self):
        # #self.assertTrue(self.unihan.table_exists('Unihan_DictionaryLikeData'))

    # def test_kFrequency(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kFrequency

        # """

        # rows = self.table.select().where(self.table.c.field == 'kFrequency').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kPhonetic(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kPhonetic

        # """

        # rows = self.table.select().where(self.table.c.field == 'kPhonetic').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kTotalStrokes(self):
        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kTotalStrokes

        # """

        # rows = self.table.select().where(self.table.c.field == 'kTotalStrokes').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    # def test_kGradeLevel(self):

        # """
        # http://www.unicode.org/reports/tr38/tr38-15.html#kGradeLevel

        # """

        # rows = self.table.select().where(self.table.c.field == 'kGradeLevel').limit(1).execute()

        # for r in rows:
            # self.assertIsInstance(ucn_to_unicode(r['char']), text_type)


# class Unihan_DictionaryIndices(UnihanTestCase, UnihanRawImportCase):
    # csv_filename = 'Unihan_DictionaryIndices.txt'
    # #table_name = 'Unihan_DictionaryIndices'
    # table_name='Unihan'

    # def setUp(self):
        # super(Unihan_DictionaryIndices, self).setUp()

        # # Assures at least one table is installed before testing.
        # self.unihan.install(self.csv_filename)


# class Unihan_DictionaryLikeData(UnihanTestCase, UnihanRawImportCase):
    # csv_filename = 'Unihan_DictionaryLikeData.txt'
    # #table_name = 'Unihan_DictionaryLikeData'
    # table_name='Unihan'

    # def setUp(self):
        # super(Unihan_DictionaryLikeData, self).setUp()

        # # Assures at least one table is installed before testing.
        # self.unihan.install(self.csv_filename)


# class Unihan_IRGSources(UnihanTestCase, UnihanRawImportCase):
    # csv_filename = 'Unihan_IRGSources.txt'
    # #table_name = 'Unihan_IRGSources'
    # table_name='Unihan'

    # def setUp(self):
        # super(Unihan_IRGSources, self).setUp()

        # # Assures at least one table is installed before testing.
        # self.unihan.install(self.csv_filename)


# class Unihan_NumericValues(UnihanTestCase, UnihanRawImportCase):
    # csv_filename = 'Unihan_NumericValues.txt'
    # #table_name = 'Unihan_NumericValues'
    # table_name='Unihan'

    # def setUp(self):
        # super(Unihan_NumericValues, self).setUp()

        # # Assures at least one table is installed before testing.
        # self.unihan.install(self.csv_filename)


# class Unihan_OtherMappings(UnihanTestCase, UnihanRawImportCase):
    # csv_filename = 'Unihan_OtherMappings.txt'
    # #table_name = 'Unihan_OtherMappings'
    # table_name='Unihan'

    # def setUp(self):
        # super(Unihan_OtherMappings, self).setUp()

        # # Assures at least one table is installed before testing.
        # self.unihan.install(self.csv_filename)


# class Unihan_RadicalStrokeCounts(UnihanTestCase, UnihanRawImportCase):
    # csv_filename = 'Unihan_RadicalStrokeCounts.txt'
    # #table_name = 'Unihan_RadicalStrokeCounts'
    # table_name='Unihan'

    # def setUp(self):
        # super(Unihan_RadicalStrokeCounts, self).setUp()

        # # Assures at least one table is installed before testing.
        # self.unihan.install(self.csv_filename)


# class Unihan_Readings(UnihanRawImportCase):
    # csv_filename = 'Unihan_Readings.txt'
    # #table_name = 'Unihan_Readings'
    # table_name='Unihan'

    # def setUp(self):
        # super(Unihan_Readings, self).setUp()

        # # Assures at least one table is installed before testing.
        # self.unihan.install(self.csv_filename)


# class Unihan_Variants(UnihanRawImportCase):
    # csv_filename = 'Unihan_Variants.txt'
    # #table_name = 'Unihan_Variants'
    # table_name='Unihan'

    # def setUp(self):
        # super(Unihan_Variants, self).setUp()

        # # Assures at least one table is installed before testing.
        # self.unihan.install(self.csv_filename)
