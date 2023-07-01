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

from cihai import conversion

if t.TYPE_CHECKING:
    pass


cjk_ranges: t.Dict[
    str, t.Sequence[int]
] = {  # http://www.unicode.org/reports/tr38/#BlockListing
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


class Char(t.TypedDict):
    id: int
    char: str
    ucn: str


@pytest.fixture(scope="session")
def unihan_table(
    engine: sqlalchemy.Engine, metadata: sqlalchemy.MetaData
) -> sqlalchemy.Table:
    return sqlalchemy.Table(
        "cjk",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer(), primary_key=True),
        sqlalchemy.Column("char", sqlalchemy.String()),
        sqlalchemy.Column("ucn", sqlalchemy.String()),
    )


@pytest.fixture(scope="session")
def sample_table(
    engine: sqlalchemy.Engine, metadata: sqlalchemy.MetaData
) -> sqlalchemy.Table:
    return sqlalchemy.Table(
        "sample_table",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer(), primary_key=True),
        sqlalchemy.Column("char_id", sqlalchemy.ForeignKey("cjk.id")),
        sqlalchemy.Column("value", sqlalchemy.String()),
    )


@pytest.fixture(autouse=True, scope="session")
def create_all(
    engine: sqlalchemy.Engine,
    metadata: sqlalchemy.MetaData,
    unihan_table: sqlalchemy.Table,
    sample_table: sqlalchemy.Table,
) -> None:
    metadata.create_all(engine)


def get_char_fk(
    char: str, engine: sqlalchemy.Engine, unihan_table: sqlalchemy.Table
) -> int:
    with engine.connect() as connection:
        results = connection.execute(
            sqlalchemy.select(unihan_table.c.id)
            .select_from(unihan_table)
            .where(unihan_table.c.char == char)
            .limit(1)
        )
        row = results.fetchone()
        assert row is not None
        foreign_key = row.id
        assert isinstance(foreign_key, int)
        return foreign_key


def get_char_fk_multiple(
    engine: sqlalchemy.Engine, unihan_table: sqlalchemy.Table, *args: t.List[str]
) -> sqlalchemy.Result[t.Any]:
    """Retrieve the Rows"""
    with engine.connect() as connection:
        return connection.execute(
            sqlalchemy.select(unihan_table).where(
                unihan_table.c.char.in_([str(arg) for arg in args])
            )
        )


@pytest.fixture(scope="session")
def chars(
    metadata: sqlalchemy.MetaData,
    engine: sqlalchemy.Engine,
    unihan_table: sqlalchemy.Table,
) -> t.List[Char]:
    chars: t.List[Char] = []

    while len(chars) < 3:
        c = 0x4E00 + random.randint(1, 333)
        char = Char(
            id=c,
            char=chr(int(c)),
            ucn=conversion.python_to_ucn(chr(int(c)), as_bytes=False),
        )

        if char not in chars:
            chars.append(char)

    with engine.connect() as connection:
        connection.execute(sqlalchemy.insert(unihan_table), chars)

        count = connection.scalar(
            sqlalchemy.select(sqlalchemy.func.count()).select_from(unihan_table)
        )
        assert isinstance(count, int)
        assert count > 0, "Setup should have more than 1 row of data added"

        connection.commit()
    return chars


def test_insert_row(
    chars: t.List[Char], unihan_table: sqlalchemy.Table, engine: sqlalchemy.Engine
) -> None:
    cjkchar = chars[0]

    with engine.connect() as connection:
        row = connection.execute(
            sqlalchemy.select(unihan_table)
            .where(unihan_table.c.char == cjkchar["char"])
            .limit(1)
            .select_from(unihan_table)
        ).fetchone()

        assert row is not None
        assert row.char == cjkchar["char"]


def test_insert_bad_key(
    sample_table: sqlalchemy.Table, engine: sqlalchemy.Engine
) -> None:
    with engine.connect() as connection:
        bad_key = connection.execute(
            sqlalchemy.insert(sample_table),
            [{"value": "", "char_id": "non_existant_char"}],
        )

        assert bad_key


def test_insert_on_foreign_key(
    chars: t.List[Char],
    sample_table: sqlalchemy.Table,
    unihan_table: sqlalchemy.Table,
    engine: sqlalchemy.Engine,
) -> None:
    cjkchar = chars[0]
    char = cjkchar["char"]

    with engine.connect() as connection:
        connection.execute(
            sqlalchemy.insert(sample_table),
            [
                {
                    "char_id": get_char_fk(
                        char, engine=engine, unihan_table=unihan_table
                    ),
                    "value": "hey",
                }
            ],
        )

        select_char = unihan_table.select().where(unihan_table.c.char == char).limit(1)
        row = connection.execute(select_char).fetchone()

        assert row is not None


def test_get_char_foreign_key_multiple(
    chars: t.List[Char], engine: sqlalchemy.Engine, unihan_table: sqlalchemy.Table
) -> None:
    char_fk_multiple = get_char_fk_multiple(
        engine, unihan_table, [c["char"] for c in chars]
    )

    for char in char_fk_multiple:
        assert char is not None
        assert isinstance(char, dict)
        assert char["char"]
