"""Extension tests for cihai."""

import typing as t

from cihai import extend
from cihai.core import Cihai
from cihai.data.unihan.dataset import Unihan, UnihanVariants


class SimplestDataset(extend.Dataset):
    """Barebones dataset for cihai."""

    def a_method(self) -> str:
        """Return a string."""
        return "hi"


def test_add_dataset() -> None:
    """Test adding a dataset."""
    c = Cihai()
    c.add_dataset(SimplestDataset, namespace="simple")
    assert hasattr(c, "simple")
    assert isinstance(c.simple, extend.Dataset)

    simple = SimplestDataset(cihai=c)
    assert hasattr(simple, "a_method")
    assert callable(simple.a_method)
    assert simple.a_method() == "hi"


class SimplestSQLAlchemyDataset(extend.Dataset, extend.SQLAlchemyMixin):
    """Basic SQLAlchemy dataset for cihai."""

    def a_method(self) -> str:
        """Return a string."""
        return "hi"


def test_add_dataset_with_db() -> None:
    """Test adding dataset with SQLAlchemy to Cihai."""
    c = Cihai()
    c.add_dataset(SimplestSQLAlchemyDataset, namespace="simple")
    assert hasattr(c, "simple")
    assert isinstance(c.simple, extend.Dataset)

    s = SimplestSQLAlchemyDataset(cihai=c)
    assert hasattr(s, "a_method")
    assert callable(s.a_method)
    assert s.a_method() == "hi"

    assert hasattr(c, "sql")
    assert hasattr(c.simple, "sql")


def test_add_dataset_unihan(unihan_options: dict[str, object]) -> None:
    """Test adding UNIHAN dataset to Cihai."""
    c = Cihai()
    c.add_dataset(Unihan, namespace="unihan")
    assert hasattr(c, "unihan")
    assert isinstance(c.unihan, extend.Dataset)

    assert c.unihan.sql is not None

    c.unihan.bootstrap(options=unihan_options)
    U = c.sql.base.classes.Unihan

    first_glyph = (
        c.unihan.sql.session.query(U).filter(U.kDefinition.isnot(None)).first()
    )

    assert first_glyph is not None

    char = first_glyph.char
    kdef_query = c.unihan.lookup_char(char=char).first()
    assert kdef_query is not None
    assert kdef_query.kDefinition == first_glyph.kDefinition

    char_query = c.unihan.reverse_char(hints=[first_glyph.kDefinition]).first()
    assert char_query is not None

    assert char_query.char == char, "works with list of column value matches"

    reverse_query = c.unihan.reverse_char(hints=first_glyph.kDefinition).first()

    assert reverse_query is not None

    assert reverse_query.char == char, "works with strings"

    c.unihan.add_plugin(UnihanVariants, "variants")
    assert hasattr(c.unihan, "variants")

    def variant_list(
        field: str,
    ) -> t.Generator[tuple[Unihan, list[str]], str, None]:
        for char in c.unihan.with_fields([field]):
            yield (char, list(char.untagged_vars(field)))

    result = dict(variant_list("kZVariant"))

    assert len(result.values()) > 0
    assert len(result.keys()) > 0
