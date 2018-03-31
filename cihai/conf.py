# -*- coding: utf8 - *-

from __future__ import absolute_import, print_function, unicode_literals

import os

from appdirs import AppDirs

from cihai._compat import string_types

#: XDG App directory locations
dirs = AppDirs(
    "cihai",      # appname
    "cihai team"  # app author
)


#: Default configuration
DEFAULT_CONFIG = {
    "debug": False,
    "database": {
        "url": 'sqlite:///{user_data_dir}/cihai.db'
    },
    "dirs": {
        "cache": '{user_cache_dir}',
        "log": '{user_log_dir}',
        "data": '{user_data_dir}'
    }
}


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
        'site_data_dir': dirs.site_data_dir
    }

    for k, v in d.items():
        if isinstance(v, dict):
            expand_config(v)
        if isinstance(v, string_types):
            d[k] = os.path.expanduser(os.path.expandvars(d[k]))
            d[k] = d[k].format(**context)
