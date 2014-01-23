# -*- coding: utf-8 -*-
"""Tests for unihan.

cihaidata_unihan.testsuite.unihan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
import zipfile
import shutil

import sqlalchemy

from sqlalchemy import Table, MetaData

import cihai

from cihai.testsuite.cihai import CihaiHelper
from cihai.testsuite.helpers import TestCase
from cihai.util import get_datafile
from cihai.datasets import unihan
from cihai._compat import StringIO, text_type
from cihai import Cihai, CihaiDataset

log = logging.getLogger(__name__)


class UnihanHelper(CihaiHelper):

    config = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        'test_config.yml'
    ))

    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.mkdtemp()
        cls.zip_filename = 'zipfile.zip'
        cls.tempzip_filepath = os.path.join(cls.tempdir, cls.zip_filename)
        zf = zipfile.ZipFile(cls.tempzip_filepath, 'a')
        zf.writestr("d.txt", "DDDDDDDDDD")
        zf.close()

        cls.zf = zf

        super(UnihanHelper, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):

        shutil.rmtree(cls.tempdir)

        super(UnihanHelper, cls).tearDownClass()


# def suite():
    # suite = unittest.TestSuite()
    # return suite
