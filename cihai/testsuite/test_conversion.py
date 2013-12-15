# -*- coding: utf-8 -*-
"""Tests for cihai.

cihai.testsuite.test_conversion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import tempfile
import logging

from .helpers import TestCase
from .._compat import PY2, text_type, string_types
from ..unihan import get_datafile, UnihanReader
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

        expected = b"U+4E00"

        self.assertEqual(expected, conversion.python_to_ucn(python_unicode))
        self.assertEqual(expected, conversion.python_to_ucn(text))

    def test_to_unicode(self):
        before = 'U+4E00'
        expected = '\u4e00'

        after = conversion.ucn_to_unicode(before)

        self.assertEqual(expected, after)

        self.assertIsInstance(after, text_type)

        # wide character
        before = 'U+20001'
        expected = '\U00020001'

        after = conversion.ucnstring_to_unicode(before)

        self.assertEqual(
            expected,
            after
        )

        self.assertIsInstance(after, text_type)

        before = '(same as U+7A69 穩) firm; stable; secure'
        expected = '(same as 穩 穩) firm; stable; secure'

        after = conversion.ucnstring_to_unicode(before)

        self.assertEqual(
            expected,
            after
        )
        self.assertIsInstance(after, text_type)


class EUC(TestCase):

    """Return EUC character from a Python Unicode character.

    Converts a one character Python unicode string (e.g. u'\\u4e00') to the
    corresponding EUC hex ('d2bb').

    """

    def test_from_unicode(self):
        text = '一'
        python_unicode = u'\u4e00'

        pass

    def test_to_unicode(self):
        text = '一'
        python_unicode = u'\u4e00'
        euc_bytestring = b'd2bb'

        self.assertEqual(text, python_unicode)
        self.assertIsInstance(
            conversion.euc_to_unicode(euc_bytestring),
            text_type
        )

        self.assertEqual(
            conversion.euc_to_unicode(euc_bytestring),
            text
        )

        self.assertEqual(
            conversion.euc_to_unicode(euc_bytestring),
            python_unicode
        )


class NCR(TestCase):

    """Return Unicode NCR string from a Python unicode string.

    Converts a one character Python unicode string (e.g. u'\\u4e00') to the
    corresponding Unicode NCR ('&x4E00;').

    Change the output format by passing the following parameters:

    :param decimal: (default False) output the decimal value instead of hex.
    :param hex: (default False) (same as decimal=True)
    :param xml: (default False) just display the decimal or hex value, i.e.
        strip off the '&#', '&x', and ';'

    No parameters - default behavior: hex=True, xml=True.

    """

    def test_from_unicode(self):
        text = '一'
        python_unicode = u'\u4e00'

        pass

    def test_to_unicode(self):
        pass
