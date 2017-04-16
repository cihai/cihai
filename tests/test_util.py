# -*- coding: utf-8 -*-
"""Tests for unihan.

cihai.testsuite.util
~~~~~~~~~~~~~~~~~~~~

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import unittest
import logging

from cihai import util

from cihai._compat import StringIO

log = logging.getLogger(__name__)

import pprint
pp = pprint.PrettyPrinter(indent=2).pprint


class UtilTestCase(unittest.TestCase):

    def test_dl_progress(self):
        out = StringIO()

        util._dl_progress(20, 10, 1000, out=out)

        result = out.getvalue().strip()
        expected = '20% [==========>                                        ]'

        self.assertEqual(result, expected)

    def test_import_string(self):
        # Borrows from werkzeug.testsuite.
        import cgi
        import cihai

        self.assertEqual(util.import_string('cgi.escape'), cgi.escape)
        self.assertEqual(util.import_string(u'cgi.escape'), cgi.escape)
        self.assertEqual(util.import_string('cgi:escape'), cgi.escape)
        self.assertIsNone(util.import_string('XXXXXXXXXXXX', True))
        self.assertIsNone(util.import_string('cgi.XXXXXXXXXXXX', True))

        self.assertEqual(util.import_string('cihai.cihai.Cihai'), cihai.cihai.Cihai)
        self.assertEqual(util.import_string('cihai.cihai:Cihai'), cihai.cihai.Cihai)
        self.assertEqual(util.import_string('cihai'), cihai)
        self.assertIsNone(util.import_string('XXXXX', True))
        self.assertIsNone(util.import_string('cihia.XXXXX', True))

        self.assertRaises(ImportError, util.import_string, 'XXXXXXXXXXXXXXXX')
        self.assertRaises(ImportError, util.import_string, 'cgi.XXXXXXXXXX')

    def test_find_modules(self):
        self.assertEqual(
            list(util.find_modules('cihai.datasets', include_packages=True)),
            ['cihai.datasets.decomp', 'cihai.datasets.unihan']
        )


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UtilTestCase))
    return suite
