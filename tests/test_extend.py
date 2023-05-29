import typing as t

from cihai import extend
from cihai.core import Cihai
from cihai.data.unihan.dataset import Unihan, UnihanVariants


class SimplestDataset(extend.Dataset):
    def a_method(self) -> str:
        return "hi"


def test_add_dataset() -> None:
    c = Cihai()
    c.add_dataset(SimplestDataset, namespace="simple")
    assert hasattr(c, "simple")
    assert isinstance(c.simple, extend.Dataset)

    simple = SimplestDataset()
    assert hasattr(simple, "a_method")
    assert callable(simple.a_method)
    assert simple.a_method() == "hi"


class SimplestSQLAlchemyDataset(extend.Dataset, extend.SQLAlchemyMixin):
    def a_method(self) -> str:
        return "hi"


def test_add_dataset_with_db() -> None:
    c = Cihai()
    c.add_dataset(SimplestSQLAlchemyDataset, namespace="simple")
    assert hasattr(c, "simple")
    assert isinstance(c.simple, extend.Dataset)

    s = SimplestSQLAlchemyDataset()
    assert hasattr(s, "a_method")
    assert callable(s.a_method)
    assert s.a_method() == "hi"

    assert hasattr(c, "sql")
    assert hasattr(c.simple, "sql")


def test_add_dataset_unihan(unihan_options: t.Dict[str, object]) -> None:
    c = Cihai()
    c.add_dataset(Unihan, namespace="unihan")
    assert hasattr(c, "unihan")
    assert isinstance(c.unihan, extend.Dataset)

    c.unihan.sql

    c.unihan.bootstrap(options=unihan_options)
    U = c.sql.base.classes.Unihan

    first_glyph = (
        c.unihan.sql.session.query(U).filter(U.kDefinition.isnot(None)).first()
    )

    assert first_glyph is not None

    char = first_glyph.char
    kDefQuery = c.unihan.lookup_char(char=char).first()
    assert kDefQuery is not None
    assert kDefQuery.kDefinition == first_glyph.kDefinition

    charQuery = c.unihan.reverse_char(hints=[first_glyph.kDefinition]).first()
    assert charQuery is not None

    assert charQuery.char == char, "works with list of column value matches"

    reverse_query = c.unihan.reverse_char(hints=first_glyph.kDefinition).first()

    assert reverse_query is not None

    assert reverse_query.char == char, "works with strings"

    c.unihan.add_plugin(UnihanVariants, "variants")
    assert hasattr(c.unihan, "variants")

    def variant_list(
        field: str,
    ) -> t.Generator[t.Tuple[Unihan, t.List[str]], str, None]:
        for char in c.unihan.with_fields([field]):
            variants: t.List[str] = []
            for var in char.untagged_vars(field):
                variants.append(var)
            yield (char, variants)

    result = dict(variant_list("kZVariant"))

    assert len(result.values()) > 0
    assert len(result.keys()) > 0
