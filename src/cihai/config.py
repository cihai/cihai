import os
import pathlib
import typing as t

from appdirs import AppDirs

from cihai.constants import app_dirs

if t.TYPE_CHECKING:
    from .types import UntypedDict


def expand_config(d: "UntypedDict", dirs: "AppDirs" = app_dirs) -> None:
    """
    Expand configuration XDG variables, environmental variables, and tildes.

    Parameters
    ----------
    d : dict
        config information
    dirs : appdirs.AppDirs
        XDG application mapping

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

    See Also
    --------
    os.path.expanduser, os.path.expandvars :
        Standard library functions for expanding variables. Same concept, used inside.
    """
    context = {
        "user_cache_dir": dirs.user_cache_dir,
        "user_config_dir": dirs.user_config_dir,
        "user_data_dir": dirs.user_data_dir,
        "user_log_dir": dirs.user_log_dir,
        "site_config_dir": dirs.site_config_dir,
        "site_data_dir": dirs.site_data_dir,
    }

    if "datasets" in d and "plugins" not in d:
        d["datasets"] = {}

    for k, v in d.items():
        if isinstance(v, dict):
            expand_config(v, dirs)
        if isinstance(v, str):
            d[k] = os.path.expanduser(  # NOQA: PTH111
                os.path.expandvars(v).format(**context),
            )

            path = pathlib.Path(t.cast(str, d[k]))
            if path.exists() or any(
                str(path).startswith(app_dir) for app_dir in context.values()
            ):
                d[k] = path
