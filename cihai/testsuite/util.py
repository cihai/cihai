# -*- coding: utf-8 -*-
"""Tests for unihan.

cihai.testsuite.util
~~~~~~~~~~~~~~~~~~~~

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import unittest
import logging
from ..util import _dl_progress
from .._compat import StringIO

log = logging.getLogger(__name__)

import pprint
pp = pprint.PrettyPrinter(indent=2).pprint


class UtilTestCase(unittest.TestCase):

    def test_dl_progress(self):
        out = StringIO()

        _dl_progress(20, 10, 1000, out=out)

        result = out.getvalue().strip()
        expected = '20% [==========>                                        ]'

        self.assertEqual(result, expected)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UtilTestCase))
    return suite
