# -*- coding: utf-8 -*-
"""Tests for cihai.

cihai.testsuite.conversion
~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import tempfile
import logging
import unittest

from .helpers import TestCase
from .._compat import PY2, text_type, string_types
from ..util import get_datafile
from .. import conversion

log = logging.getLogger(__name__)


class Util(TestCase):

    def test_text_type(self):
        c1 = '(same as U+7A69 穩) firm; stable; secure'
        c2 = text_type()

        self.assertIsInstance(c1, string_types)
        self.assertIsInstance(c2, text_type)


class UCN(TestCase):

    """Return UCN character from Python Unicode character.

    Converts a one character Python unicode string (e.g. u'\\u4e00') to the
    corresponding Unicode UCN ('U+4E00').

    """

    # U+369D	kSemanticVariant	U+595E<kMatthews U+594E<kMatthews
    # U+3CE2	kTraditionalVariant	U+23FB7
    # U+3FF7	kSemanticVariant	U+7CD9<kMatthews,kMeyerWempe
    # U+345A	kDefinition	(non-classical form of 那) that, there
    # U+349A	kDefinition	(same as U+7A69 穩) firm; stable; secure, dependent upon others
    # U+34B5	kMandarin	mào
    # U+356D	kCantonese	au3 jaau1

    def test_from_unicode(self):
        text = '一'
        python_unicode = u'\u4e00'

        expected = "U+4E00"
        bytes_expected = b"U+4E00"

        self.assertEqual(conversion.python_to_ucn(python_unicode), expected)
        self.assertIsInstance(
            conversion.python_to_ucn(python_unicode),
            text_type
        )
        self.assertIsInstance(
            conversion.python_to_ucn(python_unicode, as_bytes=True),
            bytes
        )

        self.assertEqual(conversion.python_to_ucn(text, as_bytes=True), bytes_expected)

    def test_from_unicode_16(self):
        text = '𦄀'
        python_unicode = u'\u26100'

        expected = "U+26100"
        bytes_expected = b"U+26100"

        self.assertEqual(conversion.python_to_ucn(python_unicode), expected)
        self.assertIsInstance(
            conversion.python_to_ucn(python_unicode),
            text_type
        )
        self.assertIsInstance(
            conversion.python_to_ucn(python_unicode, as_bytes=True),
            bytes
        )

        self.assertEqual(conversion.python_to_ucn(text, as_bytes=True), bytes_expected)

    def test_to_unicode(self):
        before = 'U+4E00'
        expected = '\u4e00'

        result = conversion.ucn_to_unicode(before)

        self.assertEqual(result, expected)

        self.assertIsInstance(result, text_type)

        # wide character
        before = 'U+20001'
        expected = '\U00020001'

        result = conversion.ucn_to_unicode(before)

        self.assertEqual(result, expected)
        self.assertIsInstance(result, text_type)

        before = '(same as U+7A69 穩) firm; stable; secure'
        expected = '(same as 穩 穩) firm; stable; secure'

        result = conversion.ucnstring_to_unicode(before)

        self.assertEqual(result, expected)
        self.assertIsInstance(result, text_type)


class EUC(TestCase):

    """Return EUC character from a Python Unicode character.

    Converts a one character Python unicode string (e.g. u'\\u4e00') to the
    corresponding EUC hex ('d2bb').

    """

    def test_from_unicode(self):
        expected = '一'  # u'\u4e00'
        euc_bytestring = b'd2bb'
        euc_unicode = 'd2bb'

        result = conversion.python_to_euc(expected, as_bytes=True)

        self.assertEqual(euc_bytestring, result)
        self.assertIsInstance(result, bytes)

        result = conversion.python_to_euc(expected)

        self.assertEqual(euc_unicode, result)
        self.assertIsInstance(result, text_type)

    def test_to_unicode(self):
        # = '一'
        expected = '一'
        expected_ustring = u'\u4e00'
        euc_bytestring = b'd2bb'

        result = conversion.euc_to_unicode(euc_bytestring)

        self.assertEqual(expected, expected_ustring)
        self.assertIsInstance(result, text_type)

        self.assertEqual(expected, result)
        self.assertEqual(expected_ustring, result)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(EUC))
    suite.addTest(unittest.makeSuite(UCN))
    suite.addTest(unittest.makeSuite(Util))
    return suite
