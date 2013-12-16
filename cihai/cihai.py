# -*- coding: utf8 - *-
"""Unihan file parsing, importing and codec handling.

cihai.unihan
~~~~~~~~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import zipfile
import csv
import logging
import hashlib

from sqlalchemy import create_engine, MetaData, Table, String, Column, \
    Integer, Index

from . import conversion
from ._compat import PY2, text_type, configparser

log = logging.getLogger(__name__)


class Cihai(object):

    """

    Holds instance of database engine and metadata.

    """

    def use(self, middleware):
        """Add a middleware library to cihai."""
        pass

    def get(self, char, *args, **kwargs):
        """Return results if exists in middleware."""

    def reverse(self, char, *args, **kwargs):
        """Return results if exists in middleware."""


class CihaiResults(object):
    pass
