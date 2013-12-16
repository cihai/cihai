# -*- coding: utf8 - *-
"""Cihai object.

cihai.cihai
~~~~~~~~~~~

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
from .util import get_datafile
from ._compat import PY2, text_type, configparser

log = logging.getLogger(__name__)

cihai_config = get_datafile('cihai.conf')
cihai_db = get_datafile('cihai.db')
engine = create_engine('sqlite:///%s' % cihai_db, echo=False)


class Cihai(object):

    """

    Holds instance of database engine and metadata.

    """

    _metadata = None

    def use(self, middleware):
        """Add a middleware library to cihai."""
        pass

    def get(self, char, *args, **kwargs):
        """Return results if exists in middleware."""

    def reverse(self, char, *args, **kwargs):
        """Return results if exists in middleware."""

    @property
    def metadata(self):
        """Return the metadata."""
        if not self._metadata:
            self._metadata = MetaData(bind=engine)
            self._metadata.reflect()

        return self._metadata


class CihaiMiddleware(object):
    pass
