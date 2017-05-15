# -*- coding: utf8 - *-
"""Cihai client object."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import argparse
import logging
import os

import kaptan
from sqlalchemy import create_engine

from cihai import db, exc, bootstrap
from cihai.util import merge_dict
from cihai.conf import default_config, expand_config, dirs

log = logging.getLogger(__name__)

about = {}
about_file = os.path.join(os.path.dirname(__file__), '__about__.py')
with open(about_file) as fp:
    exec(fp.read(), about)


def get_parser():
    """Return :py:class:`argparse.ArgumentParser` instance for CLI.

    :returns: argument parser for CLI use.
    :rtype: :py:class:`argparse.ArgumentParser`

    """
    parser = argparse.ArgumentParser(
        prog=about['__title__'],
        description=about['__description__']
    )
    parser.add_argument(
        "-c", "--config", dest="_config",
        help="Custom configuration file."
    )
    return parser


class Cihai(object):

    """Cihai query client.

    Inspired by the early `pypa/warehouse`_ applicaton object.

    .. _pypa/warehouse: https://github.com/pypa/warehouse

    """

    #: :class:`sqlalchemy.engine.Engine` instance.
    engine = None

    #: :class:`sqlalchemy.schema.MetaData` instance.
    metadata = None

    #: configuration dictionary.
    config = None

    #: :py:mod:`dict` of default config, can be monkey-patched during tests
    default_config = default_config()

    def __init__(self, config={}):

        # Merge custom configuration settings on top of defaults
        self.config = merge_dict(self.default_config, config)

        #: Expand template variables
        expand_config(self.config)

        self.engine = create_engine(self.config['database']['url'])

        self.metadata = db.metadata
        self.metadata.bind = self.engine

        if not os.path.exists(dirs.user_data_dir):
            os.makedirs(dirs.user_data_dir)

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

        :param argv: list of arguments, i.e. ``['-c', 'config.yml']``.
        :type argv: list
        :rtype: :class:`Cihai`

        """
        parser = get_parser()

        args = parser.parse_args(argv)

        config = args._config if args._config is not None else {}
        return cls.from_file(config)

    @property
    def is_bootstrapped(self):
        """Return True if UNIHAN and database is set up."""
        return bootstrap.is_bootstrapped(self.metadata)
