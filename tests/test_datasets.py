# -*- coding: utf-8 -*-
"""Tests for cihai datasets

tests.datasets
~~~~~~~~~~~~~~

These tests will be tested against a fixture of :class:`Cihai` which uses the
settings found in ``test_config.yml``.

"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import logging
import random
import unittest

import sqlalchemy
from sqlalchemy import MetaData

from cihai import conversion
from cihai._compat import unichr
from cihai.test import TestCase

log = logging.getLogger(__name__)

cjk_ranges = {
    'CJK Unified Ideographs': range(0x4E00, 0x9FFF + 1),
    'CJK Unified Ideographs Extension A': range(0x3400, 0x4DBF + 1),
    'CJK Unified Ideographs Extension B': range(0x20000, 0x2A6DF + 1),
    'CJK Unified Ideographs Extension C': range(0x2A700, 0x2B73F + 1),
    'CJK Unified Ideographs Extension D': range(0x2B840, 0x2B81F + 1),
    'CJK Compatibility Ideographs': range(0xF900, 0xFAFF + 1),
    'CJK Radicals Supplement': range(0x2E80, 0x2EFF + 1),
    'CJK Symbols and Punctuation': range(0x3000, 0x303F + 1),
    'CJK Strokes': range(0x31C0, 0x31EF + 1),
    'Ideographic Description Characters': range(0x2FF0, 0x2FFF + 1),
    'Kangxi Radicals': range(0x2F00, 0x2FDF + 1),
    'Enclosed CJK Letters and Months': range(0x3200, 0x32FF + 1),
    'CJK Compatibility': range(0x3300, 0x33FF + 1),
    'CJK Compatibility Ideographs': range(0xF900, 0xFAFF + 1),
    'CJK Compatibility Ideographs Supplement': range(0x2F800, 0x2FA1F + 1),
    'CJK Compatibility Forms': range(0xFE30, 0xFE4F + 1),
    'Yijing Hexagram Symbols': range(0x4DC0, 0x4DFF + 1)
}


class BootstrapUnicode(TestCase):

    def test_generate_unicode(self):
        from cihai import conversion

        totalCharacters = 0
        for block_name, urange in cjk_ranges.items():
            for c in urange:
                char = unichr(int(c))
                ucn = conversion.python_to_ucn(char)

            totalCharacters += len(urange)

        print('Total characters: %s' % totalCharacters)


engine = sqlalchemy.create_engine('sqlite:///')
metadata = MetaData(bind=engine)

unicode_table = sqlalchemy.Table(
    'cjk',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer(), primary_key=True),
    sqlalchemy.Column('char', sqlalchemy.Unicode()),
    sqlalchemy.Column('ucn', sqlalchemy.String()),
)

sample_table = sqlalchemy.Table(
    'sample_table',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer(), primary_key=True),
    sqlalchemy.Column('char_id', sqlalchemy.ForeignKey('cjk.id')),
    sqlalchemy.Column('value', sqlalchemy.Unicode()),
)

metadata.create_all()


def get_char_fk(char):
    return unicode_table.select(unicode_table.c.id) \
        .where(unicode_table.c.char == char).limit(1) \
        .execute().fetchone().id


def get_char_fk_multiple(*args):
    """Retrieve the Rows

    """

    where_opts = []

    for arg in args:
        where_opts.append(unicode_table.c.char == arg)

    where_opts = sqlalchemy.or_(*where_opts)

    results = unicode_table.select() \
        .where(where_opts) \
        .execute()

    return results


class TableInsertFK(TestCase):

    @classmethod
    def setUpClass(cls):
        chars = []

        while len(chars) < 3:
            c = 0x4E00 + random.randint(1, 333)
            char = {
                'hex': c,
                'char': unichr(int(c)),
                'ucn': conversion.python_to_ucn(unichr(int(c)))
            }
            if char not in chars:
                chars.append(char)

            metadata.bind.execute(unicode_table.insert(), chars)

        cls.chars = chars

    def test_insert_row(self):

        cjkchar = self.chars[0]

        c = cjkchar['hex']
        char = cjkchar['char']
        ucn = cjkchar['ucn']

        row = unicode_table.select().limit(1) \
            .execute().fetchone()

        self.assertEqual(row.char, cjkchar['char'])

    def test_insert_bad_fk(self):
        wat = sample_table.insert().values(
            value='',
            char_id='wat'
        ).execute()

        print(wat)

    def test_insert_on_foreign_key(self):

        cjkchar = self.chars[0]
        hex = cjkchar['hex']
        char = cjkchar['char']
        ucn = cjkchar['ucn']

        sample_table.insert().values(
            char_id=get_char_fk(char),
            value='hey'
        ).execute()

        select_char = unicode_table.select().where(unicode_table.c.char == char).limit(1)
        row = select_char.execute().fetchone()

        self.assertIsNotNone(row)

    def test_get_char_foreign_key_multiple(self):
        char_fk_multiple = get_char_fk_multiple(*[c['char'] for c in self.chars])

        for char in char_fk_multiple:

            print(char['char'])


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BootstrapUnicode))
    suite.addTest(unittest.makeSuite(TableInsertFK))
    return suite
