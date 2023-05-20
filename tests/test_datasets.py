"""Tests for cihai datasets

tests.datasets
~~~~~~~~~~~~~~

These tests will be tested against a fixture of :class:`Cihai` which uses the
settings found in ``test_config.yml``.

"""
import random
import typing as t

import pytest

import sqlalchemy
from sqlalchemy import MetaData

from cihai import conversion

if t.TYPE_CHECKING:
    from sqlalchemy.engine import ResultProxy
    from sqlalchemy.sql import ClauseElement


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


class Char(t.TypedDict):
    id: int
    char: str
    ucn: str


def get_char_fk(char: str) -> int:
    q = (
        unicode_table.select(unicode_table.c.id)
        .where(unicode_table.c.char == char)
        .limit(1)
        .execute()
    )
    assert q is not None
    row = q.fetchone()

    assert row is not None
    assert isinstance(row.id, int)
    return row.id


def get_char_fk_multiple(*args: t.Sequence[str]) -> "ResultProxy":
    """Retrieve the Rows"""

    or_ops: t.List[t.Union[str, bool, "ClauseElement"]] = []

    for arg in args:
        or_ops.append(unicode_table.c.char == arg)

    or_op = sqlalchemy.or_(*or_ops)

    results = unicode_table.select().where(or_op).execute()

    assert results is not None

    return results


@pytest.fixture(scope="session")
def chars() -> t.List[Char]:
    chars: t.List[Char] = []

    while len(chars) < 3:
        c: int = 0x4E00 + random.randint(1, 333)
        char = Char(
            {
                # In SQLAlchemy, sqlite supports this
                # https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#insert-on-conflict-upsert
                "id": c,
                "char": chr(int(c)),
                "ucn": conversion.python_to_ucn(chr(int(c)), as_bytes=False),
            }
        )

        q = unicode_table.select().where(unicode_table.c.id == char["id"])

        assert q is not None

        ex = q.execute()

        assert ex is not None

        exists = ex.first() is not None
        if char not in chars and not exists:
            chars.append(char)
        else:
            continue

    assert metadata.bind is not None

    metadata.bind.execute(unicode_table.insert(), chars)
    return chars


def test_insert_row(chars: t.List[Char]) -> None:
    cjkchar = chars[0]

    query = (
        unicode_table.select()
        .where(unicode_table.c.char == cjkchar["char"])
        .limit(1)
        .execute()
    )

    assert query is not None
    row = query.fetchone()

    assert row is not None
    assert row.char == cjkchar["char"]


def test_insert_bad_fk() -> None:
    example_bad_key = sample_table.insert().values(value="", char_id="wat").execute()

    assert example_bad_key


def test_insert_on_foreign_key(chars: t.List[Char]) -> None:
    cjkchar = chars[0]
    char = cjkchar["char"]

    sample_table.insert().values(char_id=get_char_fk(char), value="hey").execute()

    select_char = unicode_table.select().where(unicode_table.c.char == char).limit(1)
    query = select_char.execute()
    assert query is not None
    row = query.fetchone()

    assert row is not None


def test_get_char_foreign_key_multiple(chars: t.List[Char]) -> None:
    char_fk_multiple = get_char_fk_multiple(*[c["char"] for c in chars])

    for char in char_fk_multiple:
        assert char["char"]
