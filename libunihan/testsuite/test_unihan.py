# -*- coding: utf-8 -*-
"""Tests for libunihan.

libunihan.testsuite.test_unihan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

import os
import tempfile
import logging

from .helpers import TestCase
from ..unihan import get_datafile, UnihanReader

log = logging.getLogger(__name__)


class UnihanData(TestCase):

    def test_zip(self):
        self.assertEqual(2, 2)

    def test_files(self):
        """Test unihan text file data."""
        pass


class UnihanDataCSV(TestCase):

    def test_print_top(self):
        with open(get_datafile('Unihan_Readings.txt'), 'r') as csvfile:
            csvfile = filter(lambda row: row[0] != '#', csvfile)
            r = UnihanReader(
                csvfile,
                fieldnames=['char', 'field', 'value'],
                delimiter='\t'
            )

            r = list(r)[:5]
            print('\n')

            for row in r:
                rowlines = []
                for key in row.keys():
                    rowlines.append(row[key])
                try:
                    rowline = '\t'.join(rowlines)
                except UnicodeDecodeError as e:
                    print(
                        'row: %s (%s) gives:\n%s' % (
                            row, row['char'], e
                        )
                    )

                print('%s' % rowline)
