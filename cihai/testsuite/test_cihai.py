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
import re
import tempfile
import random
import logging

import sqlalchemy

from .. import conversion

from .helpers import unittest, CihaiTestCase
from .._compat import PY2, text_type
from ..cihai import Cihai, NoDatasets

log = logging.getLogger(__name__)


class CihaiInstance(CihaiTestCase):

    def test_no_datasets(self):
        c = Cihai()
        self.assertIsInstance(c, Cihai)

        with self.assertRaises(NoDatasets) as e:
            c = c.get('好')

        with self.assertRaises(NoDatasets) as e:
            c = c.reverse('好')

        # there is no _metadata until :attr:`~.metadata` is accessed.
        self.assertFalse(c._metadata, sqlalchemy.MetaData)
        self.assertIsInstance(c.metadata, sqlalchemy.MetaData)
        self.assertIsInstance(c._metadata, sqlalchemy.MetaData)
