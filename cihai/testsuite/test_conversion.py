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


class Conversion(TestCase):

    # U+369D	kSemanticVariant	U+595E<kMatthews U+594E<kMatthews
    # U+3CE2	kTraditionalVariant	U+23FB7
    # U+3FF7	kSemanticVariant	U+7CD9<kMatthews,kMeyerWempe
    # U+345A	kDefinition	(non-classical form of 那) that, there
    # U+349A	kDefinition	(same as U+7A69 穩) firm; stable; secure, dependent upon others
    # U+34B5	kMandarin	mào
    # U+356D	kCantonese	au3 jaau1

    def test_ucnstring_to_python(self):
        # U+349A	kDefinition	(same as U+7A69 穩) firm; stable; secure, dependent upon others
        c1 = '(same as U+7A69 穩) firm; stable; secure'

        c2 = conversion.ucnstring_to_python(c1)
        self.assertIsInstance(c2, text_type)

    def test_ucnstring_to_unicode(self):
        pass

    def test_euc_to_python(self):
        text = '一'
        python = u'\u4e00'
        euc = b'd2bb'

        self.assertEqual(text, python)
        self.assertIsInstance(
            conversion.euc_to_python(euc),
            text_type
        )

        self.assertEqual(
            conversion.euc_to_python(euc),
            text
        )

        self.assertEqual(
            conversion.euc_to_python(euc),
            python
        )

    def test_ncrstring_to_python(self):
        pass

    def test_string_to_ncr(self):
        pass
