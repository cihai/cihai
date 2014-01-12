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
import zipfile
import shutil

import sqlalchemy

from sqlalchemy import Table, MetaData

import cihai

from .cihai import CihaiHelper
from .helpers import TestCase
from ..util import get_datafile
from ..datasets import unihan
from .._compat import StringIO
from .. import Cihai, CihaiDataset

log = logging.getLogger(__name__)


class UnihanTestCase(CihaiHelper):
    """Utilities to retrieve cihai information in a relational-friendly format.
    """

    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.mkdtemp()
        cls.zip_filename = 'zipfile.zip'
        cls.tempzip_filepath = os.path.join(cls.tempdir, cls.zip_filename)
        zf = zipfile.ZipFile(cls.tempzip_filepath, 'a')
        zf.writestr("d.txt", "DDDDDDDDDD")
        zf.close()

        cls.zf = zf

        super(UnihanTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):

        shutil.rmtree(cls.tempdir)

        super(UnihanTestCase, cls).tearDownClass()

    def test_in_columns(self):
        u = self.cihai.use(unihan.Unihan)

        columns = ['hey', 'kDefinition', 'kWhat']
        result = unihan.in_columns('kDefinition', columns)

        self.assertTrue(result)

    def test_dl_progress(self):
        out = StringIO()

        unihan._dl_progress(20, 10, 1000, out=out)

        result = out.getvalue().strip()
        expected = '20% [==========>                                        ]'

        self.assertEqual(result, expected)

    def test_save(self):

        u = self.cihai.use(unihan.Unihan)
        src_filepath = self.tempzip_filepath

        tempdir = tempfile.mkdtemp()

        dest_filepath = os.path.join(tempdir, self.zip_filename)
        unihan.save(src_filepath, dest_filepath, shutil.copy)

        result = os.path.exists(dest_filepath)

        shutil.rmtree(tempdir)

        self.assertTrue(result)

    def test_download(self):

        u = self.cihai.use(unihan.Unihan)

        src_filepath = self.tempzip_filepath

        tempdir = self.tempdir
        dest_filepath = os.path.join(tempdir, 'data', self.zip_filename)

        unihan.download(src_filepath, dest_filepath, shutil.copy)

        result = os.path.dirname(os.path.join(dest_filepath, 'data'))
        self.assertTrue(
            result,
            msg="Creates data directory if doesn't exist."
        )

    def test_extract(self):

        zf = unihan.extract(self.tempzip_filepath)

        self.assertEqual(len(zf.infolist()), 1)
        self.assertEqual(zf.infolist()[0].file_size, 10)
        self.assertEqual(zf.infolist()[0].filename, "d.txt")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UnihanTestCase))
    return suite
