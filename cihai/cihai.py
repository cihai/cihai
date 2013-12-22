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
meta = MetaData()


class NoDatasets(Exception):
    """Attempted to request data from Cihai without picking a dataset."""


class CihaiDatabase(object):
    """SQLAlchemy session data for cihai. Metadata is global."""

    _metadata = meta
    _engine = engine

    @property
    def metadata(self):
        """Return global metadata object, reflect tables.

        :rtype: :class:`sqlalchemy.schema.MetaData`

        """

        if not self._metadata.bind:
            # No engine binded yet, bind and reflect tables.
            self._metadata.bind = self._engine
            self._metadata.reflect()

        return self._metadata

    def get_table(self, table_name):
        """Return :class:`~sqlalchemy.schema.Table`.

        :param table_name: name of sql table
        :type table_name: string
        :rtype: :class:`sqlalchemy.schema.Table`

        """

        return Table(table_name, self.metadata, autoload=True)

    def table_exists(self, table_name):
        """Return True if table exists in db."""

        return True if table_name in self.metadata.tables else False


class Cihai(object):

    """Cihai query client. May use :meth:`~.get()` to grab 中文.

    Add dictionaries and datasets via :meth:`.use()`.

    """

    def __init__(self, *args, **kwargs):
        super(Cihai, self).__init__(*args, **kwargs)

        self._middleware = []

    def use(self, middleware):
        """Add a middleware library to cihai.

        This is based off connect's version of adding middleware.

        """

        for m in self._middleware:
            if isinstance(m, middleware):
                raise Exception('Dataset already added.')

        if isinstance(middleware, type):
            # middleware is still a raw class, instantiate.
            middleware = middleware()

        self._middleware.append(middleware)

    def get(self, request, *args, **kwargs):
        """Return results middleware.

        :param request: request / input data
        :type request: string
        :rtype: list

        """

        response = {}

        if not self._middleware:
            raise NoDatasets

        for middleware in self._middleware:
            response = middleware.get(request, response, *args, **kwargs)

        return response

    def reverse(self, request, *args, **kwargs):
        """Return results if exists in middleware.

        :param request: request / input data
        :type request: string
        :rtype: list

        """

        response = {}

        if not self._middleware:
            raise NoDatasets

        for middleware in self._middleware:
            response = middleware.reverse(request, response, *args, **kwargs)

        return response
