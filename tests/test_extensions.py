# -*- coding: utf8 - *-
from __future__ import absolute_import, print_function, unicode_literals

from cihai import extension
from cihai.core import Cihai


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
