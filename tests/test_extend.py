from cihai import extend
from cihai.core import Cihai
from cihai.data.unihan.dataset import Unihan, UnihanVariants


class SimplestDataset(extend.Dataset):
    def a_method(self):
        return "hi"


def test_add_dataset():
    c = Cihai()
    c.add_dataset(SimplestDataset, namespace="simple")
    assert hasattr(c, "simple")
    assert isinstance(c.simple, extend.Dataset)
    assert hasattr(c.simple, "a_method")
    assert callable(c.simple.a_method)
    assert c.simple.a_method() == "hi"


class SimplestSQLAlchemyDataset(extend.Dataset, extend.SQLAlchemyMixin):
    def a_method(self):
        return "hi"


def test_add_dataset_with_db():
    c = Cihai()
    c.add_dataset(SimplestSQLAlchemyDataset, namespace="simple")
    assert hasattr(c, "simple")
    assert isinstance(c.simple, extend.Dataset)
    assert hasattr(c.simple, "a_method")
    assert callable(c.simple.a_method)
    assert c.simple.a_method() == "hi"

    assert hasattr(c, "sql")
    assert hasattr(c.simple, "sql")


def test_add_dataset_unihan(unihan_options):
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

    char = first_glyph.char
    assert (
        c.unihan.lookup_char(char=char).first().kDefinition == first_glyph.kDefinition
    )

    assert (
        c.unihan.reverse_char(hints=[first_glyph.kDefinition]).first().char == char
    ), "works with list of column value matches"

    assert (
        c.unihan.reverse_char(hints=first_glyph.kDefinition).first().char == char
    ), "works with strings"

    c.unihan.add_plugin(UnihanVariants, "variants")
    assert hasattr(c.unihan, "variants")

    def variant_list(field):
        for char in c.unihan.with_fields(field):
            variants = []
            for var in char.untagged_vars(field):
                variants.append(var)
            yield (char, variants)

    result = {char: variants for (char, variants) in variant_list("kZVariant")}

    assert len(result.values()) > 0
    assert len(result.keys()) > 0
