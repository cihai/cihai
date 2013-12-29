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


"""
