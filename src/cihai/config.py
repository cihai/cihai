"""Configuration options for Cihai app."""

import dataclasses
import os
import pathlib
import typing as t

from cihai.constants import DEFAULT_CONFIG, app_dirs

if t.TYPE_CHECKING:
    from cihai.constants import Config
    from cihai.types import UntypedDict
    from unihan_etl._internal.app_dirs import AppDirs

    C = t.TypeVar("C", Config, UntypedDict)


def is_default_option(field_name: str, val: t.Any) -> bool:
    """Return True if field default option in configuration."""
    return bool(val == getattr(DEFAULT_CONFIG, field_name, ""))


def expand_config(
    d: "C",
    dirs: "AppDirs" = app_dirs,
) -> "C":
    """
    Expand configuration XDG variables, environmental variables, and tildes.

    Parameters
    ----------
    d : dict or Options
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

    if dataclasses.is_dataclass(d):
        for field in dataclasses.fields(d):
            if field.name == "dirs":
                continue

            v = getattr(d, field.name)
            if dataclasses.is_dataclass(v):
                setattr(d, field.name, expand_config(getattr(d, field.name)))
                v = getattr(d, field.name)

            if isinstance(v, dict):
                setattr(d, field.name, expand_config(v, dirs))
                v = getattr(d, field.name)

            if isinstance(v, pathlib.Path):
                setattr(d, field.name, str(v))
                v = getattr(d, field.name)

            if isinstance(v, str):
                setattr(
                    d,
                    field.name,
                    os.path.expanduser(  # noqa: PTH111
                        os.path.expandvars(v).format(**context),
                    ),
                )

                path = pathlib.Path(t.cast("str", getattr(d, field.name)))
                if path.exists() or any(
                    str(path).startswith(str(app_dir)) for app_dir in context.values()
                ):
                    setattr(d, field.name, path)
    elif isinstance(d, dict):
        if "datasets" in d and "plugins" not in d:
            d["datasets"] = {}

        for k, v in d.items():
            if isinstance(v, dict):
                v = d[k] = expand_config(v, dirs)
            if isinstance(v, pathlib.Path):
                v = d[k] = str(v)
            if isinstance(v, str):
                d[k] = os.path.expanduser(  # noqa: PTH111
                    os.path.expandvars(v).format(**context),
                )

                path = pathlib.Path(t.cast("str", d[k]))
                if path.exists() or any(
                    str(path).startswith(str(app_dir)) for app_dir in context.values()
                ):
                    d[k] = path

    return d
