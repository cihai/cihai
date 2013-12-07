# -*- coding: utf-8 -*-
"""Helpers for libunihan testsuite.

libunihan.testsuite.helpers
~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

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

logger = logging.getLogger(__name__)
