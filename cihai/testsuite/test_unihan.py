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
from .._compat import PY2, text_type
from ..util import get_datafile
from ..unihan import UNIHAN_FILENAMES, engine, Unihan, UnihanReader
from ..conversion import ucn_to_unicode

log = logging.getLogger(__name__)


class UnihanTestCase(TestCase):

    unihan = None

    def setUp(self):
        if not self.unihan:
            self.unihan = Unihan()

    # @classmethod
    # def setUpClass(cls):
        # install_raw_csv()


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

        for tablename in [table for table in self.unihan.metadata.tables]:
            self.assertIn(tablename, [f.split('.')[0] for f in UNIHAN_FILENAMES])


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

    def test_table_exists(self):
        for table_name in self.unihan.metadata.tables:
            self.assertTrue(self.unihan.table_exists(table_name))
            self.assertIsInstance(table_name, text_type)

    def test_get_table(self):
        # pick a random table name.
        table = self.unihan.get_table(random.choice(list(self.unihan.metadata.tables)))
        self.assertIsInstance(table, sqlalchemy.Table)

    def test_get_datafile(self):
        # file installed on installation.
        csv_filename = random.choice(UNIHAN_FILENAMES)

        csv_abspath = get_datafile(csv_filename)
        self.assertNotEqual(csv_filename, csv_abspath)
        self.assertIsInstance(csv_abspath, text_type)

    def test_create_table(self):
        table_name = 'testTable_%s' % random.randint(1, 1337)

        table = self.unihan.create_table(table_name, engine)

        self.assertIsInstance(table, sqlalchemy.Table)
        self.assertTrue(table.exists())

        table.drop()

        self.assertFalse(table.exists())


class UnihanReadings(UnihanTestCase):

    def setUp(self):
        super(UnihanReadings, self).setUp()

        # Assures at least one table is installed before testing.
        self.unihan.install_raw_csv('Unihan_Readings.txt')

    def test_kMandarin(self):
        table = self.unihan.get_table('Unihan_Readings')

        rows = table.select().where(table.c.field == 'kMandarin').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kDefinition(self):
        table = self.unihan.get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kDefinition
        Major definitions are separated by semicolons, and minor definitions by
        commas. Any valid Unicode character (except for tab, double-quote, and
        any line break character) may be used within the definition field.
        """

        rows = table.select().where(table.c.field == 'kDefinition').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kCantonese(self):
        table = self.unihan.get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kCantonese
        A full description of jyutping can be found at
        <http://www.lshk.org/cantonese.php>. The main differences between
        jyutping and the Yale romanization previously used are:
        """

        rows = table.select().where(table.c.field == 'kCantonese').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kHangul(self):
        table = self.unihan.get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kHangul

        """

        rows = table.select().where(table.c.field == 'kHangul').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kHanyuPinlu(self):
        table = self.unihan.get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kHanyuPinlu

        """

        rows = table.select().where(table.c.field == 'kHanyuPinlu').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kHanyuPinyin(self):
        table = self.unihan.get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kHanyuPinyin

        """

        rows = table.select().where(table.c.field == 'kHanyuPinyin').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kJapaneseKun(self):
        table = self.unihan.get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kJapaneseKun

        """

        rows = table.select().where(table.c.field == 'kJapaneseKun').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kJapaneseOn(self):
        table = self.unihan.get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kJapaneseKun

        """

        rows = table.select().where(table.c.field == 'kJapaneseOn').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kKorean(self):
        table = self.unihan.get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kKorean

        """

        rows = table.select().where(table.c.field == 'kKorean').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kTang(self):
        table = self.unihan.get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kTang

        """

        rows = table.select().where(table.c.field == 'kTang').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kVietnamese(self):
        table = self.unihan.get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kVietnamese

        """

        rows = table.select().where(table.c.field == 'kVietnamese').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kXHC1983(self):
        table = self.unihan.get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kXHC1983

        """

        rows = table.select().where(table.c.field == 'kXHC1983').limit(1).execute()

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

    def test_table_exists(self):
        self.assertTrue(self.unihan.table_exists('Unihan_RadicalStrokeCounts'))

    def test_kRSAdobe_Japan1_6(self):
        table = self.unihan.get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSAdobe_Japan1_6

        """

        rows = table.select().where(table.c.field == 'kRSAdobe_Japan1_6').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kRSJapanese(self):
        table = self.unihan.get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSJapanese

        """

        rows = table.select().where(table.c.field == 'kRSJapanese').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kRSKangXi(self):
        table = self.unihan.get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSKangXi

        """

        rows = table.select().where(table.c.field == 'kRSKangXi').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kRSKanWa(self):
        table = self.unihan.get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSKanWa

        """

        rows = table.select().where(table.c.field == 'kRSKanWa').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kRSKorean(self):
        table = self.unihan.get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSKorean

        """

        rows = table.select().where(table.c.field == 'kRSKorean').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kRSUnicode(self):
        table = self.unihan.get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSUnicode

        """

        rows = table.select().where(table.c.field == 'kRSUnicode').limit(1).execute()

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
        table = self.unihan.get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kAccountingNumeric

        """

        rows = table.select().where(table.c.field == 'kAccountingNumeric').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kOtherNumeric(self):
        table = self.unihan.get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kOtherNumeric

        """

        rows = table.select().where(table.c.field == 'kOtherNumeric').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kPrimaryNumeric(self):
        table = self.unihan.get_table('Unihan_Variants')

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

    def test_like(self):
        table = self.unihan.get_table('Unihan_Readings')

        def selectkDefinition(char=None):
            select = table.select().where(table.c.field == 'kDefinition')

            if char:
                select = select.where(table.c.char == conversion.python_to_ucn(char))

            return select

        self.assertNotIn('LIKE', selectkDefinition().compile().__str__())

        kDefinitionQuery = selectkDefinition().where(
            table.c.value.like('%(same as%')
        )

        self.assertIn('LIKE', kDefinitionQuery.compile().__str__())
        rows = kDefinitionQuery.execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)
            self.assertTrue(re.search('\(same as', r.value))

        self.assertGreaterEqual(1, selectkDefinition(char='好').execute().rowcount)
