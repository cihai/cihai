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
#engine = create_engine('sqlite:///%s' % cihai_db, echo=False)
engine = create_engine('sqlite:///:memory:')
meta = MetaData()


class NoDatasets(Exception):
    """Attempted to request data from Cihai without picking a dataset."""


class CihaiDatabase(object):
    """SQLAlchemy session data for cihai. Metadata is global.

    The principal goal of Cihai is to have the diverse array of CJK
    datasets through a simple convention::

        c = Cihai()  # Make a python object.

    Because of this, Cihai has tight integration with SQLAlchemy. Plugins are
    attached to MetaData objects.


    1. Congruence between a widely known Python object + Data backend +
       Contextual to database instance.

    2. An instance of Cihai and its plugins will run from the same database,
       the connect metadata is the same for all plugins searched through with
       ``.get()`` and ``.reverse()``.

    3. It's possible to pass in data to pass :class:`sqlalchemy.schema.MetaData`
       into a plugin directly. This means a plugin like ``Unihan`` can be used
       and instantiated without Cihai as a dependency.

    Cihai wants all CJK data to be retrievable in a common way. To do this, a
    best practice is adopted.

    If you have a dataset you want usable in CJK, all it takes at a minimum
    is a python object with ``.get`` and ``.reverse``.

    The goal is to keep extensions decoupled.

    Plugins always will have MetaData for the database sent to them. It's
    best practice to, next, grab the data.

    All that happened above was creating an instance of Cihai(). When
    ``Cihai()`` is instantiated, ``__init__`` will accept
    an :class:`sqlalchemy.engine.Engine`.



    In the future, CLI version may automatically invoke ``Cihai`` as sqlite, or
    read a configuration for a different back-end.


    The user may then attach datasets::

        from cihai_sample import SampleDataset
        c.use(SampleDataset)

    Since a dataset has been added, it's now possible to ``.get()``.

    .. note:
        ``.use`` follows the naming convention of Node's connect. In a python
        applicatoin you may be familiar with seeing methods like
        ``.register_backend`` or ``.register``.

    If an exception is raised from the datasets, an exception will be caught.
    In CLI / interactive mode, the user will be prompted to install the data,
    which will run the dataset's ``.install()`` method.


    """

    _metadata = meta

    def __init__(self, engine):
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
