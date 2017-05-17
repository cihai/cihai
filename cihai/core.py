# -*- coding: utf8 - *-
"""Cihai core functionality."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import logging
import os

import kaptan
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from cihai import db, exc, bootstrap
from cihai.util import merge_dict
from cihai.conf import default_config, expand_config, dirs

log = logging.getLogger(__name__)


class Cihai(object):

    """Cihai application object.

    Inspired by the early `pypa/warehouse`_ applicaton object.

    **Invocation from python:**

    Note: For Cihai to be used properly, it must be first bootstrapped with
    the UNIHAN database. :attr:`~cihai.core.Cihai.is_bootstrapped`
    to return if the database is installed for the app's configuration
    settings.

    To bootstrap the cihai environment programatically, create the Cihai
    object and pass its :attr:`~cihai.core.Cihai.metadata`:

    .. code-block:: python

        from cihai.core import Cihai
        from cihai.bootstrap import bootstrap_unihan

        c = Cihai()
        if not c.is_bootstrapped:
            bootstrap_unihan(c.metadata)

    **Configuration templates:**

    The ``config`` :py:class:`dict` parameter supports a basic template system
    for replacing :term:`XDG Base Directory` directory variables, tildes
    and environmentas variables. This is done by passing the option dict
    through :func:`cihai.conf.expand_config` during initialization.

    .. _pypa/warehouse: https://github.com/pypa/warehouse

    """

    #: :class:`sqlalchemy.engine.Engine` instance.
    engine = None

    #: :class:`sqlalchemy.schema.MetaData` instance.
    metadata = None

    #: :class:`sqlalchemy.orm.session.Session` instance.
    session = None

    #: :class:`sqlalchemy.ext.automap.AutomapBase` instance.
    base = None

    #: configuration dictionary.
    config = None

    #: :py:class:`dict` of default config, can be monkey-patched during tests
    default_config = default_config()

    def __init__(self, config={}):

        # Merge custom configuration settings on top of defaults
        self.config = merge_dict(self.default_config, config)

        #: Expand template variables
        expand_config(self.config)

        if not os.path.exists(dirs.user_data_dir):
            os.makedirs(dirs.user_data_dir)

        self.engine = create_engine(self.config['database']['url'])

        self.metadata = db.metadata
        self.metadata.bind = self.engine
        self.metadata.reflect(views=True, extend_existing=True)
        self.base = automap_base(metadata=self.metadata)
        self.base.prepare()
        self.session = Session(self.engine)

    @classmethod
    def from_file(cls, config_path=None, *args, **kwargs):
        """Create a Cihai instance from a JSON or YAML config.

        :param config_path: path to custom config file
        :type config_path: str
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

    @property
    def is_bootstrapped(self):
        """Return True if UNIHAN and database is set up."""
        return bootstrap.is_bootstrapped(self.metadata)
