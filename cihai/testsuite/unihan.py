# -*- coding: utf-8 -*-
"""Tests for unihan.

cihai.testsuite.unihan
~~~~~~~~~~~~~~~~~~~~~~

Unihan

id char ucn colName colNmae colName

load csv's mapped by colNmae and individual names into a dict.

'中' {
'ucn': '',
'kDefinition': ''
}

1. insert dict/struct of { 'unihanFileName': ['colName', 'colName'] }
    return cols, records

    Idea: Create a special iter class for it.
    Idea 2: Function, return cols, struct above

What a data set should provide.

1. Download the code.
2. Extract it (if necessary).
3. Extract the code

Get Cihai test object working with the local package directory files.

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import tempfile
import logging
import unittest

import sqlalchemy

from sqlalchemy import Table, MetaData

import cihai

from .cihai import CihaiHelper
from .helpers import TestCase
from ..util import get_datafile
from ..datasets import unihan
from .. import Cihai, CihaiDataset

log = logging.getLogger(__name__)


class UnihanTestCase(CihaiHelper):
    """Utilities to retrieve cihai information in a relational-friendly format.
    """
    def test_this(self):
        self.assertIsInstance(self.cihai, Cihai)

        u = self.cihai.use(unihan.Unihan)

        with open(u.get_datapath('Unihan_IRGSources.txt')) as hi:
            print(hi.read())

    def test_in_columns(self):
        u = self.cihai.use(unihan.Unihan)

        # columns = ['hey', 'kDefinition', 'kWhat']
        # result = u.install.in_columns('kDefinition')

        # self.assertTrue(result)

    def test_not_junk(self):
        pass

    def test_csv_to_dictlists(self):
        pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UnihanTestCase))
    return suite
