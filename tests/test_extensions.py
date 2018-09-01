# -*- coding: utf8 - *-
from __future__ import absolute_import, print_function, unicode_literals

from cihai import extension
from cihai.bootstrap import bootstrap_unihan
from cihai.core import Cihai
from cihai.unihan import Unihan


class SimplestDataset(extension.Dataset):
    def a_method(self):
        return 'hi'


def test_add_dataset():
    c = Cihai()
    c.add_dataset(SimplestDataset, namespace='simple')
    assert hasattr(c, 'simple')
    assert isinstance(c.simple, extension.Dataset)
    assert hasattr(c.simple, 'a_method')
    assert callable(c.simple.a_method)
    assert c.simple.a_method() == 'hi'


class SimplestSQLAlchemyDataset(extension.Dataset, extension.DatasetSQLAlchemyMixin):
    def a_method(self):
        return 'hi'


def test_add_dataset_with_db():
    c = Cihai()
    c.add_dataset(SimplestSQLAlchemyDataset, namespace='simple')
    assert hasattr(c, 'simple')
    assert isinstance(c.simple, extension.Dataset)
    assert hasattr(c.simple, 'a_method')
    assert callable(c.simple.a_method)
    assert c.simple.a_method() == 'hi'

    assert hasattr(c, 'sql')
    assert hasattr(c.simple, 'sql')


def test_add_dataset_unihan(unihan_options):
    c = Cihai()
    c.add_dataset(Unihan, namespace='unihan')
    assert hasattr(c, 'unihan')
    assert isinstance(c.unihan, extension.Dataset)

    c.unihan.sql

    bootstrap_unihan(c.sql.metadata, unihan_options)
    c.unihan.bootstrap()
    U = c.sql.base.classes.Unihan

    first_glyph = c.unihan.sql.session.query(U).first()

    char = first_glyph.char
    assert (
        c.unihan.lookup_char(char=char).first().kDefinition == first_glyph.kDefinition
    )
