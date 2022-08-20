"""Tests for cihai datasets

tests.datasets
~~~~~~~~~~~~~~

These tests will be tested against a fixture of :class:`Cihai` which uses the
settings found in ``test_config.yml``.

"""
import random

import pytest

import sqlalchemy
from sqlalchemy import MetaData

from cihai import conversion

cjk_ranges = {  # http://www.unicode.org/reports/tr38/#BlockListing
    "CJK Unified Ideographs": range(0x4E00, 0x9FD5 + 1),
    "CJK Unified Ideographs Extension A": range(0x3400, 0x4DBF + 1),
    "CJK Unified Ideographs Extension B": range(0x20000, 0x2A6DF + 1),
    "CJK Unified Ideographs Extension C": range(0x2A700, 0x2B73F + 1),
    "CJK Unified Ideographs Extension D": range(0x2B840, 0x2B81F + 1),
    "CJK Unified Ideographs Extension E": range(0x2B820, 0x2CEAF + 1),
    "CJK Radicals Supplement": range(0x2E80, 0x2EFF + 1),
    "CJK Symbols and Punctuation": range(0x3000, 0x303F + 1),
    "CJK Strokes": range(0x31C0, 0x31EF + 1),
    "Ideographic Description Characters": range(0x2FF0, 0x2FFF + 1),
    "Kangxi Radicals": range(0x2F00, 0x2FDF + 1),
    "Enclosed CJK Letters and Months": range(0x3200, 0x32FF + 1),
    "CJK Compatibility": range(0x3300, 0x33FF + 1),
    "CJK Compatibility Ideographs": range(0xF900, 0xFAFF + 1),
    "CJK Compatibility Ideographs Supplement": range(0x2F800, 0x2FA1D + 1),
    "CJK Compatibility Forms": range(0xFE30, 0xFE4F + 1),
    "Yijing Hexagram Symbols": range(0x4DC0, 0x4DFF + 1),
}


engine = sqlalchemy.create_engine("sqlite:///")
metadata = MetaData(bind=engine)

unicode_table = sqlalchemy.Table(
    "cjk",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer(), primary_key=True),
    sqlalchemy.Column("char", sqlalchemy.Unicode()),
    sqlalchemy.Column("ucn", sqlalchemy.String()),
)

sample_table = sqlalchemy.Table(
    "sample_table",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer(), primary_key=True),
    sqlalchemy.Column("char_id", sqlalchemy.ForeignKey("cjk.id")),
    sqlalchemy.Column("value", sqlalchemy.Unicode()),
)

metadata.create_all()


def get_char_fk(char):
    return (
        unicode_table.select(unicode_table.c.id)
        .where(unicode_table.c.char == char)
        .limit(1)
        .execute()
        .fetchone()
        .id
    )


def get_char_fk_multiple(*args):
    """Retrieve the Rows"""

    where_opts = []

    for arg in args:
        where_opts.append(unicode_table.c.char == arg)

    where_opts = sqlalchemy.or_(*where_opts)

    results = unicode_table.select().where(where_opts).execute()

    return results


@pytest.fixture(scope="session")
def chars():
    chars = []

    while len(chars) < 3:
        c = 0x4E00 + random.randint(1, 333)
        char = {
            "hex": c,
            "char": chr(int(c)),
            "ucn": conversion.python_to_ucn(chr(int(c))),
        }
        if char not in chars:
            chars.append(char)

        metadata.bind.execute(unicode_table.insert(), chars)
    return chars


def test_insert_row(chars):

    cjkchar = chars[0]

    row = unicode_table.select().limit(1).execute().fetchone()

    assert row.char == cjkchar["char"]


def test_insert_bad_fk():
    wat = sample_table.insert().values(value="", char_id="wat").execute()

    assert wat


def test_insert_on_foreign_key(chars):

    cjkchar = chars[0]
    char = cjkchar["char"]

    sample_table.insert().values(char_id=get_char_fk(char), value="hey").execute()

    select_char = unicode_table.select().where(unicode_table.c.char == char).limit(1)
    row = select_char.execute().fetchone()

    assert row is not None


def test_get_char_foreign_key_multiple(chars):
    char_fk_multiple = get_char_fk_multiple(*[c["char"] for c in chars])

    for char in char_fk_multiple:
        assert char["char"]
