# -*- coding: utf8 - *-

from __future__ import absolute_import, print_function, unicode_literals

import os

from appdirs import AppDirs

from cihai._compat import string_types

#: XDG App directory locations
dirs = AppDirs("cihai", "cihai team")  # appname  # app author


def expand_config(d):
    """
    Expand configuration XDG variables.

    Parameters
    ----------
    d : dict
        config information

    Notes
    -----

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
    """
    context = {
        'user_cache_dir': dirs.user_cache_dir,
        'user_config_dir': dirs.user_config_dir,
        'user_data_dir': dirs.user_data_dir,
        'user_log_dir': dirs.user_log_dir,
        'site_config_dir': dirs.site_config_dir,
        'site_data_dir': dirs.site_data_dir,
    }

    for k, v in d.items():
        if isinstance(v, dict):
            expand_config(v)
        if isinstance(v, string_types):
            d[k] = os.path.expanduser(os.path.expandvars(d[k]))
            d[k] = d[k].format(**context)


class Configurator(object):
    def __init__(self, namespace=''):
        """
        Manage configs. Used on Cihai and available for its extensions.

        Instance attributes
        -------------------

        data : dict
            property / getters for options
        _data : dict
            where the raw dictionary resides

        Parameters
        ----------
        namespace : str, optional
            Creates a configuration object that reads/writes on a namespace.

            Leaving this empty / reads and writes to the root level cihai config.

            Namespace is designed for plugins to manage settings.
        """
        #: XDG App directory locations
        self.dirs = AppDirs("cihai", "cihai team")  # appname  # app author

        self.namespace = namespace

    def get_names(self):
        """
        Return a list of possible places config can reside, and order of search.

        This is based on XDG. So it will look for
        """
        pass

    @property
    def file(self):
        """Find a config file where it exists, as the first place."""
        return

    def read(self):
        """Read to dictionary."""
        return

    def get_delta(self, **updates):
        """Returns the difference of whatever user customizations differ from
        cihai.conf.DEFAULT_CONFIG.
        """
        pass

    def write(self, **updates):
        """If no delta is created from DEFAULT, it not write.

        If file doesn't exist, it will create.
        """
        if updates:
            self._data.update(**updates)
        # save file
        pass
