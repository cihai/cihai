# -*- coding: utf8 - *-
"""Exceptions for Cihai.

cihai.exc
~~~~~~~~~

"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)


class NoDatasets(Exception):
    """Attempted to request data from Cihai without picking a dataset."""
