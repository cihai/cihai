# -*- coding: utf8 - *-
from __future__ import absolute_import, print_function, unicode_literals

from cihai import extension
from cihai.core import Cihai


class SimplestDataset(extension.Dataset):
    def lookup(self, search):
        return 'hi'

def test_add_extensions2():
    c = Cihai()
    c.add_dataset(SimplestDataset, namespace='simple')
    assert hasattr(c, 'simple')
    assert isinstance(c.simple, extension.Dataset)
    assert hasattr(c.simple, 'simple', 'lookup')
    assert callable(c.simple.lookup)
    assert c.simple.lookup() == 'hi'
