# -*- coding: utf-8 -*-
"""Tests for cihai.

cihai.testsuite
~~~~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from ..log import DebugLogFormatter
import logging
log = logging.getLogger()


if not log.handlers:
    channel = logging.StreamHandler()
    channel.setFormatter(DebugLogFormatter())
    log.addHandler(channel)
    log.setLevel('INFO')

    # enable DEBUG message if channel is at testsuite + testsuite.* packages.
    testsuite_logger = logging.getLogger(__name__)

    testsuite_logger.setLevel('INFO')


def suite():
    """Return TestSuite."""
    try:
        import unittest2 as unittest
    except ImportError:  # Python 2.7
        import unittest

    return unittest.TestLoader().discover('.', pattern="test_*.py")
