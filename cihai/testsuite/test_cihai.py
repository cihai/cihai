# -*- coding: utf-8 -*-
"""Tests for cihai.

cihai.testsuite.test_cihai
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import tempfile
import logging

import sqlalchemy

from sqlalchemy import Table, MetaData

from .helpers import TestCase, get_datafile
from .._compat import PY2, text_type, string_types
from ..util import get_datafile
from .. import conversion

log = logging.getLogger(__name__)

"""Cihai

1. Create a table for unicode characters.
2. Create query to provide ID value for unicode character. Establish
fk.
3. Test expression from 2 can be used in a new query.

Note: Don't get test full integration.

"""


class Cihai(object):

    """the Cihai object."""

    def __init__(self):
        pass


class FixturesTest(TestCase):

    def test_unihan_csv_exist(self):
        pass


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


class InitialUnicode(TestCase):

    def test_generate_unicode(self):
        from .. import conversion

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
    sqlalchemy.Column('value', sqlalchemy.Unicode())
)

metadata.create_all()


def get_char_fk(char):
    return unicode_table.select() \
        .where(unicode_table.c.char == char).limit(1) \
        .execute().fetchone().id


def get_char_fk_multiple(*args):

    where_opts = []
    print(args)
    for arg in args:
        print(arg)
        where_opts.append(unicode_table.c.char == arg)

    where_opts = sqlalchemy.or_(*where_opts)

    return unicode_table.select() \
        .where(where_opts) \
        .execute()


class TableInsertFK(TestCase):

    def test_insert_row(self):

        c = 0x4E00
        char = unichr(int(c))
        ucn = conversion.python_to_ucn(char)

        unicode_table.insert().values(
            char=char,
            ucn=ucn
        ).execute()

        row = unicode_table.select().limit(1) \
            .execute().fetchone()
        self.assertEqual(row.char, '一')

    def test_insert_on_foreign_key(self):

        for c in range(0x4E00, 0x4E00 + 2):
            char = unichr(int(c))
            ucn = conversion.python_to_ucn(char)

            unicode_table.insert().values(
                char=char,
                ucn=ucn
            ).execute()

            sample_table.insert().values(
                char_id=get_char_fk(char),
                value='hey'
            ).execute()

            select_char = unicode_table.select().where(unicode_table.c.char == char).limit(1)
            row = select_char.execute().fetchone()

            print(row)

    def test_insert_on_foreign_key_multiple(self):
        chars = get_char_fk_multiple('一', '丁')
