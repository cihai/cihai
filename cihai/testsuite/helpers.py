# -*- coding: utf-8 -*-
"""Helpers for cihai testsuite.

cihai.testsuite.helpers
~~~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

try:
    import unittest2 as unittest
except ImportError:  # Python 2.7
    import unittest
import os
import copy
import logging
import tempfile
import shutil
import uuid

from ..cihai import Cihai

logger = logging.getLogger(__name__)


class TestCase(unittest.TestCase):
    pass


class CihaiTestCase(TestCase):
    c = None  # :class:`Cihai` instance.

    def setUp(self):
        if not self.c:
            self.c = Cihai()
