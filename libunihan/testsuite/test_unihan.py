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

log = logging.getLogger(__name__)


class TestUnihan(TestCase):

    def test_latest(self):
        self.assertEqual(2, 2)
