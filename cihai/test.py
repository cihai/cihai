# -*- coding: utf-8 -*-
"""Helpers for cihai testsuite.

cihai.test
~~~~~~~~~~

"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import logging
import os

logger = logging.getLogger(__name__)


def get_datafile(filename):
    """Wrapper around util.get_datafile for picking test fixtures."""

    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'fixtures/', filename)
