# -*- coding: utf-8 -*-
"""Tests for cihai.

cihai.testsuite.test_unihan
~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import re
import tempfile
import random
import logging
import cProfile
from pstats import Stats

import sqlalchemy

from profilehooks import profile, coverage

from .. import conversion

from .helpers import unittest, TestCase
from .._compat import PY2, text_type, configparser
from ..util import get_datafile, UnicodeReader
from ..datasets.unihan import UNIHAN_DATASETS, Unihan
from ..conversion import ucn_to_unicode
from ..cihai import cihai_db, cihai_config, Cihai

log = logging.getLogger(__name__)


Unihan._engine = sqlalchemy.create_engine('sqlite:///:memory:')


class UnihanTestCase(TestCase):

    def setUp(self):
        pass


class UnihanInstall(TestCase):

    """Dump the Raw Unihan CSV's into SQLite database.

    1. default install dict
    2. open file, strip #'s
    3. count total entries
    4. concatenate csv files
    5. import to csv2dict
    6. count entries
    7. insert all into db
    8. verify counts of fields with db

    """

    def setUp(self):
        super(UnihanInstall, self).setUp()

    def test_datasets_schema(self):
        """UNIHAN_DATASETS schema is { 'FILENAME': ['fields'] }."""
        self.assertTrue(UNIHAN_DATASETS)
        self.assertIsInstance(UNIHAN_DATASETS, dict)

        for _file, fields in UNIHAN_DATASETS.items():
            self.assertIsInstance(_file, text_type)
            self.assertIsInstance(fields, list)
            for field in fields:
                self.assertIsInstance(field, text_type)

    #@profile
    def test_get_csv_rows(self):
        unihan = Unihan()
        table = unihan.install()


class UnihanMethods(UnihanTestCase):

    def setUp(self):
        super(UnihanMethods, self).setUp()

    def test__create_table(self):
        table_name = 'testTable_%s' % random.randint(1, 1337)
        unihan = Unihan()

        table = unihan._create_table(table_name)

        self.assertIsInstance(table, sqlalchemy.Table)
        self.assertTrue(table.exists())

        unihan.metadata.drop_all(tables=[table])

        self.assertFalse(table.exists())


class UnihanMiddleware(UnihanTestCase):

    def test_get(self):
        c = Cihai()
        c.use(Unihan)
        results = c.get('你', fields=['kDefinition'])

        self.assertIsInstance(results, dict)

    def test_reverse(self):

        c = Cihai()
        c.use(Unihan)
        results = c.reverse(r'%first%', fields=['kDefinition'])
