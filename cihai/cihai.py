# -*- coding: utf8 - *-
"""

Cihai
-----

:class:`Cihai` is a bound to :class:`sqlalchemy.schema.MetaData` - A collection
of :class:`sqlalchemy.schema.Table`'s.

An instance of ``Cihai`` may use one or more ``dataset``. The dataset
provides a primary datasource (from the internet, or a CSV) in a format
that is friendly to relationship databases.

It install and access multiple :class:`sqlalchemy.schema.Table`.

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

import os
import zipfile
import csv
import hashlib
import argparse
import logging

import kaptan

from sqlalchemy import create_engine, MetaData, Table, String, Column, \
    Integer, Index

from . import conversion
from .util import get_datafile, merge_dict, convert_to_attr_dict
from ._compat import PY2, text_type, configparser

log = logging.getLogger(__name__)

cihai_config = get_datafile('cihai.conf')
cihai_db = get_datafile('cihai.db')
#engine = create_engine('sqlite:///%s' % cihai_db, echo=False)
engine = create_engine('sqlite:///:memory:')
meta = MetaData()


class NoDatasets(Exception):
    """Attempted to request data from Cihai without picking a dataset."""


class CihaiDatabase(object):
    """SQLAlchemy session data for cihai. Metadata is global."""

    _metadata = meta

    def __init__(self, engine=None):
        """Initialize CihaiDatabase back-end.

        :param engine: engine to connect to database with.
        :param type:class:`sqlalchemy.engine.Engine`

        """

        self._engine = engine

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

    Cihai object is inspired by `pypa/warehouse`_ Warehouse applicaton object.

    .. _pypa/warehouse: https://github.com/pypa/warehouse

    """

    def __init__(self, config, engine=None):

        #: configuration dictionary. Available as attributes. ``.config.debug``
        self.config = convert_to_attr_dict(config)

        #: list of current Middleware in session
        self._middleware = []

        #: :class:`sqlalchemy.schema.MetaData` object.
        self.metadata = MetaData()

    @classmethod
    def from_file(cls, config_path=None, *args, **kwargs):
        """Create a Cihai instance from a JSON or YAML config."""

        config = dict()
        configReader = kaptan.Kaptan()

        default_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "config.yml",
        ))
        config = configReader.import_config(default_path).get()

        if config_path:
            if not os.path.exists(config_path):
                raise Exception('{0} does not exist.'.format(os.path.abspath(config_path)))
            if not any(config_path.endswith(ext) for ext in ('json', 'yml', 'yaml', 'ini')):
                raise Exception(
                    '{0} does not have a yaml,yml,json,ini extension.'
                    .format(os.path.abspath(config_path))
                )
            else:
                custom_config = configReader.import_config(config_path).get()
                config = merge_dict(config, custom_config)

        return cls(config)

    @classmethod
    def from_cli(cls, argv):
        parser = argparse.ArgumentParser(prog="cihai")
        parser.add_argument("-c", "--config", dest="_config")

        args = parser.parse_args(argv)
        config = args._config if args._config is not None else None

        return cls.from_file(config)

    def use(self, middleware):
        """Add a middleware library to cihai.

        This is based off connect's version of adding middleware.

        """

        if not middleware in self._middleware:
            self._middleware.append(middleware)

    def get(self, request, *args, **kwargs):
        """Return results middleware.

        :param request: request / input data
        :type request: string
        :rtype: list

        """

        if not self._middleware:
            raise NoDatasets

        response = {}

        for m in self._middleware:
            if hasattr(m, 'get'):
                response = m.get(request, response, *args, **kwargs)
            if not response:
                break

        return response

    def reverse(self, request, *args, **kwargs):
        """Return results if exists in middleware.

        :param request: request / input data
        :type request: string
        :rtype: list

        """

        if not self._middleware:
            raise NoDatasets

        response = {}

        for m in self._middleware:
            if hasattr(m, 'reverse'):
                response = m.reverse(request, response, *args, **kwargs)
            if not response:
                break

        return response
