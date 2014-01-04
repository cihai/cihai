# -*- coding: utf8 - *-
"""Exceptions for Cihai.

cihai.exc
~~~~~~~~~

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals


class NoDatasets(Exception):
    """Attempted to request data from Cihai without picking a dataset."""
