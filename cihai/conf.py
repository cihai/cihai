# -*- coding: utf8 - *-

from __future__ import absolute_import, print_function, unicode_literals

import os

import kaptan
from appdirs import AppDirs

from cihai._compat import string_types

#: XDG App directory locations
dirs = AppDirs(
    "cihai",      # appname
    "cihai team"  # app author
)

#: Default configuration file location
DEFAULT_CONFIG_FILE = os.path.abspath(os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "conf", "default.yml",
))


def default_config(config_file=DEFAULT_CONFIG_FILE):
    """Return default configuration for cihai.

    :returns: Default configuration settings
    :rtype: dict
    """
    config_reader = kaptan.Kaptan()
    return config_reader.import_config(config_file).get()


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
