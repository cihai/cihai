#!/usr/bin/env python
# -*- coding: utf8 - *-
"""Cihai client object."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import argparse
import logging
import os

import kaptan
from appdirs import AppDirs
from sqlalchemy import Table, create_engine

from cihai import db, exc
from cihai._compat import string_types
from cihai.util import merge_dict

log = logging.getLogger(__name__)

dirs = AppDirs(
    "cihai",      # appname
    "cihai team"  # app author
)


def default_config():
    config_reader = kaptan.Kaptan()
    default_config_file = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        "config.yml",
    ))
    return config_reader.import_config(default_config_file).get()


def expand_config(d):
    """Expand configuration XDG variables.

    *Environmentable variables* are expanded via :py:func:`os.path.expandvars`.
    So ``${PWD}`` would be replaced by the current PWD in the shell,
    ``${USER}`` would be the user running the app.

    *XDG variables* are expanded via :py:meth:`str.format`. These do not have a
    dollar sign. They are:

    - ``{user_cache_dir}``
    - ``{user_config_dir}``
    - ``{user_data_dir}``
    - ``{user_log_dir}``
    - ``{site_config_dir}``
    - ``{site_data_dir}``

    :param d: dictionary of config info
    :type d: dict
    """
    context = {
        'user_cache_dir': dirs.user_cache_dir,
        'user_config_dir': dirs.user_config_dir,
        'user_data_dir': dirs.user_data_dir,
        'user_log_dir': dirs.user_log_dir,
        'site_config_dir': dirs.site_config_dir,
        'site_data_dir': dirs.site_data_dir
    }

    for k, v in d.items():
        if isinstance(v, dict):
            expand_config(v)
        if isinstance(v, string_types):
            d[k] = os.path.expanduser(os.path.expandvars(d[k]))
            d[k] = d[k].format(**context)


class Storage(object):
    """Mixin generic sqlalchemy yum-yums for relational data."""

    def __init__(self, cihai, engine, metadata):
        """Initialize Storage back-end.

        :param engine: engine to connect to database with.
        :param type:class:`sqlalchemy.engine.Engine`

        """

        #: :class:`Cihai` application object.
        self.cihai = cihai

        #: :class:`sqlalchemy.engine.Engine` instance.
        self.engine = engine

        #: :class:`sqlalchemy.schema.MetaData` instance.
        self.metadata = metadata

    def get_table(self, table_name):
        """Return :class:`~sqlalchemy.schema.Table`.

        :param table_name: name of sql table
        :type table_name: str
        :rtype: :class:`sqlalchemy.schema.Table`

        """

        return Table(table_name, self.metadata, autoload=True)

    def table_exists(self, table_name):

        """Return True if table exists in db."""

        return True if table_name in self.metadata.tables else False

    def get_datapath(self, filename):
        """Return absolute filepath in relation to :attr:`self.data_path`.

        :param filename: file name relative to ``./data``.
        :type filename: str
        :returns: Absolute path to data file.
        :rtype: str

        """

        data_path = self.cihai.config['data_path']

        return os.path.join(data_path, filename)


class Cihai(object):

    """Cihai query client. May use :meth:`~.get()` to grab 中文.

    Cihai object is inspired by `pypa/warehouse`_ Warehouse applicaton object.

    .. _pypa/warehouse: https://github.com/pypa/warehouse

    """

    def __init__(self, config, engine=None):

        #: configuration dictionary. Available as attributes. ``.config.debug``
        self.config = merge_dict(default_config(), config)

        #: Expand template variables
        expand_config(self.config)

        #: absolute path to cihai data files.
        if 'data_path' not in self.config:
            self.config['data_path'] = os.path.abspath(os.path.join(
                os.path.dirname(__file__), 'data/'
            ))

        if engine is None and self.config['database']['url']:
            engine = create_engine(self.config['database']['url'])
        #: :class:`sqlalchemy.engine.Engine` instance.
        self.engine = engine

        #: :class:`sqlalchemy.schema.MetaData` instance.
        self.metadata = db.metadata
        self.metadata.bind = self.engine

    @classmethod
    def from_file(cls, config_path=None, *args, **kwargs):
        """Create a Cihai instance from a JSON or YAML config.

        :param config_path: path to custom config file
        :type confiig_path: str
        :rtype: :class:`Cihai`

        """

        config_reader = kaptan.Kaptan()

        config = {}

        if config_path:
            if not os.path.exists(config_path):
                raise exc.CihaiException(
                    '{0} does not exist.'.format(os.path.abspath(config_path)))
            if not any(
                config_path.endswith(ext) for ext in
                ('json', 'yml', 'yaml', 'ini')
            ):
                raise exc.CihaiException(
                    '{0} does not have a yaml,yml,json,ini extension.'
                    .format(os.path.abspath(config_path))
                )
            else:
                custom_config = config_reader.import_config(config_path).get()
                config = merge_dict(config, custom_config)

        return cls(config)

    @classmethod
    def from_cli(cls, argv):
        """Cihai from :py:class:`argparse` / CLI args.

        :param argv: list of arguments, i.e. ``['-c', 'dev/config.yml']``.
        :type argv: list
        :rtype: :class:`Cihai`

        """
        parser = argparse.ArgumentParser(prog="cihai")
        parser.add_argument("-c", "--config", dest="_config")

        args = parser.parse_args(argv)
        config = args._config if args._config is not None else None

        return cls.from_file(config)
