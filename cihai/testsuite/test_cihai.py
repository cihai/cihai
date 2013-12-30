# -*- coding: utf-8 -*-
"""Tests for cihai.

cihai.testsuite.test_cihai
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import tempfile
import logging

from .helpers import TestCase, get_datafile
from .._compat import PY2, text_type, string_types
from ..util import get_datafile
from .. import conversion

log = logging.getLogger(__name__)

"""Cihai

1. Create a table for unicode characters.
2. Create query to provide ID value for unicode character. Establish
    fk.
3. Test expression from 2 can be used in a new query.

Note:
    Don't get test full integration.
"""


class Cihai(object):

    """the Cihai object."""

    def __init__(self):
        pass


class FixturesTest(TestCase):

    def test_unihan_csv_exist(self):
        pass


def create_unicode_characters():
    pass


class InitialUnicode(TestCase):

    def test_generate_unicode(self):
        from .. import conversion

        ranges = {
            'CJK Unified Ideographs': range(0x4E00,0x9FFF + 1)
        }

        unicode_range = [chars for block_name, chars in ranges.items()]
        for c in unicode_range[0]:
            char = unichr(int(c))
            ucn = conversion.python_to_ucn(char)
            print(c, char, ucn)
        print(len(unicode_range[0]))
