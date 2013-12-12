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
import tempfile
import logging

import sqlalchemy

from .helpers import TestCase, unittest
from .._compat import PY2, text_type
from ..unihan import get_datafile, get_table, UnihanReader, metadata, \
    UNIHAN_FILES

log = logging.getLogger(__name__)


class UnihanData(TestCase):

    def test_zip(self):
        self.assertEqual(2, 2)

    def test_files(self):
        """Test unihan text file data."""
        pass


class UnihanTable(TestCase):

    def test_returns_instance_table(self):
        table = get_table('Unihan_NumericValues')

        self.assertIsInstance(table, sqlalchemy.Table)

    def test_returns_metadata_has_csv_tables(self):
        for filename in UNIHAN_FILES:
            tablename = filename.split('.')[0]
            self.assertIn(tablename, [table for table in metadata.tables])


class UnihanDataCSV(TestCase):

    @unittest.skip('Wait until helper TestCase is implemented.')
    def test_print_top(self):
        with open(get_datafile('Unihan_Readings.txt'), 'r') as csvfile:
            # py3.3 regression http://bugs.python.org/issue18829
            delim = b'\t' if PY2 else '\t'
            csvfile = filter(lambda row: row[0] != '#', csvfile)
            r = UnihanReader(
                csvfile,
                fieldnames=['char', 'field', 'value'],
                delimiter=delim
            )

            r = list(r)[:5]
            print('\n')

            for row in r:
                rowlines = []
                for key in row.keys():
                    if key == 'field' and not isinstance(row[key], text_type):
                        # import cchardet as chardet
                        # log.error(chardet.detect(row[key]))
                        # codec = chardet.detect(row[key])['encoding']
                        #row[key] = row[key].decode(codec)
                        self.assertIsInstance(row[key], text_type)
                    elif key == 'value':
                        # import chardet
                        # log.error(chardet.detect(row[key]))
                        # codec = chardet.detect(row[key])['encoding']
                        # #row[key] = row[key].decode(codec)
                        # self.assertIsInstance(row[key], text_type)
                        pass

                    rowlines.append(row[key])
                try:
                    rowline = '\t'.join(rowlines)
                except UnicodeDecodeError as e:
                    log.info('row: %s (%s) gives:\n%s' % (row, row['char'], e))

                print('%s' % rowline)


