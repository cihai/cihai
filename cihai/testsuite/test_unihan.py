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
from ..unihan import get_datafile, get_table, UnihanReader, \
    UNIHAN_FILENAMES, get_metadata, table_exists, install_raw_csv, \
    engine, create_table, table_exists
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
            self.assertIn(tablename, [table for table in self.c.metadata.tables])


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
        for table_name in self.c.metadata.tables:
            self.assertTrue(table_exists(table_name))
            self.assertIsInstance(table_name, text_type)

    def test_get_metadata(self):
        self.assertIsInstance(self.c.metadata, sqlalchemy.MetaData)

    def test_get_table(self):
        # pick a random table name.
        table = get_table(random.choice(list(self.c.metadata.tables)))
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

        rows = table.select().where(table.c.field == 'kMandarin').limit(1).execute()

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

        rows = table.select().where(table.c.field == 'kDefinition').limit(1).execute()

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

        rows = table.select().where(table.c.field == 'kCantonese').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kHangul(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kHangul

        """

        rows = table.select().where(table.c.field == 'kHangul').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kHanyuPinlu(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kHanyuPinlu

        """

        rows = table.select().where(table.c.field == 'kHanyuPinlu').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kHanyuPinyin(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kHanyuPinyin

        """

        rows = table.select().where(table.c.field == 'kHanyuPinyin').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kJapaneseKun(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kJapaneseKun

        """

        rows = table.select().where(table.c.field == 'kJapaneseKun').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kJapaneseOn(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kJapaneseKun

        """

        rows = table.select().where(table.c.field == 'kJapaneseOn').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kKorean(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kKorean

        """

        rows = table.select().where(table.c.field == 'kKorean').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kTang(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kTang

        """

        rows = table.select().where(table.c.field == 'kTang').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kVietnamese(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kVietnamese

        """

        rows = table.select().where(table.c.field == 'kVietnamese').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kXHC1983(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kXHC1983

        """

        rows = table.select().where(table.c.field == 'kXHC1983').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_table_exists(self):
        self.assertTrue(table_exists('Unihan_Readings'))


class UnihanVariants(CihaiTestCase):

    def test_table_exists(self):
        self.assertTrue(table_exists('Unihan_Variants'))

    def test_kSemanticVariant(self):
        table = get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kSemanticVariant

        """

        rows = table.select().where(table.c.field == 'kSemanticVariant').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kTraditionalVariant(self):
        table = get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kTraditionalVariant

        """

        rows = table.select().where(table.c.field == 'kTraditionalVariant').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kSpecializedSemanticVariant(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kSpecializedSemanticVariant

        """

        rows = table.select().where(table.c.field == 'kSpecializedSemanticVariant').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kSimplifiedVariant(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kSimplifiedVariant

        """

        rows = table.select().where(table.c.field == 'kSimplifiedVariant').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kCompatibilityVariant(self):
        table = get_table('Unihan_Readings')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kCompatibilityVariant

        """

        rows = table.select().where(table.c.field == 'kCompatibilityVariant').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)


class UnihanRadicalStrokeCounts(CihaiTestCase):

    def test_table_exists(self):
        self.assertTrue(table_exists('Unihan_RadicalStrokeCounts'))

    def test_kRSAdobe_Japan1_6(self):
        table = get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSAdobe_Japan1_6

        """

        rows = table.select().where(table.c.field == 'kRSAdobe_Japan1_6').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kRSJapanese(self):
        table = get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSJapanese

        """

        rows = table.select().where(table.c.field == 'kRSJapanese').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kRSKangXi(self):
        table = get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSKangXi

        """

        rows = table.select().where(table.c.field == 'kRSKangXi').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kRSKanWa(self):
        table = get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSKanWa

        """

        rows = table.select().where(table.c.field == 'kRSKanWa').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kRSKorean(self):
        table = get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSKorean

        """

        rows = table.select().where(table.c.field == 'kRSKorean').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kRSUnicode(self):
        table = get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kRSUnicode

        """

        rows = table.select().where(table.c.field == 'kRSUnicode').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)


class UnihanNumericValues(CihaiTestCase):

    def test_table_exists(self):
        self.assertTrue(table_exists('Unihan_NumericValues'))

    def test_kAccountingNumeric(self):
        table = get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kAccountingNumeric

        """

        rows = table.select().where(table.c.field == 'kAccountingNumeric').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kOtherNumeric(self):
        table = get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kOtherNumeric

        """

        rows = table.select().where(table.c.field == 'kOtherNumeric').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kPrimaryNumeric(self):
        table = get_table('Unihan_Variants')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kPrimaryNumeric

        """

        rows = table.select().where(table.c.field == 'kPrimaryNumeric').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)


class UnihanDictionaryLikeData(CihaiTestCase):

    def test_table_exists(self):
        self.assertTrue(table_exists('Unihan_DictionaryLikeData'))

    def test_kFrequency(self):
        table = get_table('Unihan_DictionaryLikeData')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kFrequency

        """

        rows = table.select().where(table.c.field == 'kFrequency').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kPhonetic(self):
        table = get_table('Unihan_DictionaryLikeData')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kPhonetic

        """

        rows = table.select().where(table.c.field == 'kPhonetic').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kTotalStrokes(self):
        table = get_table('Unihan_DictionaryLikeData')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kTotalStrokes

        """

        rows = table.select().where(table.c.field == 'kTotalStrokes').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)

    def test_kGradeLevel(self):
        table = get_table('Unihan_DictionaryLikeData')

        """
        http://www.unicode.org/reports/tr38/tr38-15.html#kGradeLevel

        """

        rows = table.select().where(table.c.field == 'kGradeLevel').limit(1).execute()

        for r in rows:
            self.assertIsInstance(ucn_to_unicode(r['char']), text_type)


class kDefinition(CihaiTestCase):

    """
    http://www.unicode.org/reports/tr38/tr38-15.html#kDefinition
    Major definitions are separated by semicolons, and minor definitions by
    commas. Any valid Unicode character (except for tab, double-quote, and
    any line break character) may be used within the definition field.
    """

    def test_like(self):
        table = get_table('Unihan_Readings')

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
