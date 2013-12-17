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


class NoDatasets(Exception):
    """Attempted to request data from Cihai without picking a dataset."""


class Cihai(object):

    """

    Holds instance of database engine and metadata.

    Can add dictionaries and datasets via :meth:`.use()`.

    """

    _metadata = None
    _middleware = []

    def use(self, middleware):
        """Add a middleware library to cihai.

        This is based off connect's version of adding middleware.

        """
        pass

    def get(self, char, *args, **kwargs):
        """Return results if exists in middleware.

        :param char: chinese character
        :type char: string
        :rtype: list

        """

        results = []

        if not self._middleware:
            raise NoDatasets

        for middleware in self._middleware:
            results.append(middleware.get(char))

        return results

    def reverse(self, char, *args, **kwargs):
        """Return results if exists in middleware.

        :param char: chinese character
        :type char: string
        :rtype: list

        """

        results = []

        if not self._middleware:
            raise NoDatasets

        for middleware in self._middleware:
            results.append(middleware.reverse(char))

        return results

    @property
    def metadata(self):
        """Return the instance metadata."""
        if not self._metadata:
            self._metadata = MetaData(bind=engine)
            self._metadata.reflect()

        return self._metadata


class CihaiMiddleware(object):
    pass
