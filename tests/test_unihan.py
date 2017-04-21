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

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import logging
import os
import shutil
import tempfile
import zipfile

from cihai.test import CihaiHelper

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
