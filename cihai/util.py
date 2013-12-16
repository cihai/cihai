# -*- coding: utf8 - *-
"""Utility and helper methods for cihai.

cihai.util
~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os


def get_datafile(filename):
    """Return absolute path to cihai data file.

    :param filename: file name relative to ``./data``.
    :type filename: string
    :returns: Absolute path to data file.
    :rtype: string

    """

    abspath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/', filename)
    return abspath
