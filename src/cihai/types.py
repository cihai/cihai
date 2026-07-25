"""Typings for cihai.

This is meant to be imported from inside ``typing.TYPE_CHECKING`` so it does not
require ``typing_extensions`` at runtime:

>>> from typing import TYPE_CHECKING
>>> if TYPE_CHECKING:
...     from .types import DirsConfigDict
>>> def my_fn(dir_config: "DirsConfigDict") -> None:
...     pass
"""

from __future__ import annotations

import sys
import typing as t
from typing import TypedDict

if sys.version_info >= (3, 11):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired

if t.TYPE_CHECKING:
    import pathlib

    from cihai.extend import Dataset


UntypedDict: t.TypeAlias = dict[str, object]


class RawPluginConfigDict(TypedDict):
    """Barebones plugin config dictionary."""


class RawDirsConfigDict(TypedDict):
    """Raw directory config dictionary.

    Values may be :py:class:`str` templates holding XDG placeholders such as
    ``{user_cache_dir}``, environment variables, or a tilde;
    :func:`cihai.config.expand_config` resolves them to
    :py:class:`pathlib.Path`.

    Attributes
    ----------
    cache : str | pathlib.Path
        Cache directory, defaulting to the XDG user cache directory.
    log : str | pathlib.Path
        Log directory, defaulting to the XDG user log directory.
    data : str | pathlib.Path
        Persistent data directory, home to the SQLite database in the default
        config, defaulting to the XDG user data directory.
    """

    cache: str | pathlib.Path
    log: str | pathlib.Path
    data: str | pathlib.Path


class DirsConfigDict(TypedDict):
    """Directory config dictionary.

    Resolved counterpart of :class:`RawDirsConfigDict`: templates, environment
    variables, and tildes are already expanded.

    Attributes
    ----------
    cache : pathlib.Path
        Cache directory, defaulting to the XDG user cache directory.
    log : pathlib.Path
        Log directory, defaulting to the XDG user log directory.
    data : pathlib.Path
        Persistent data directory, home to the SQLite database in the default
        config, defaulting to the XDG user data directory.
    """

    cache: pathlib.Path
    log: pathlib.Path
    data: pathlib.Path


class RawDatabaseConfigDict(TypedDict):
    """Raw database config dictionary.

    Attributes
    ----------
    url : str
        SQLAlchemy database URL, handed to
        :func:`sqlalchemy.create_engine` by :class:`cihai.db.Database`. Before
        :func:`cihai.config.expand_config` runs it may carry XDG placeholders,
        as the default ``sqlite:///{user_data_dir}/cihai.db`` does.
    """

    url: str


class RawConfigDict(TypedDict):
    """Raw, unresolved configuration dictionary.

    Shape a caller passes to :class:`cihai.core.Cihai`, before it is merged
    over :data:`cihai.constants.DEFAULT_CONFIG` and its templates expanded.

    Attributes
    ----------
    plugins : NotRequired[dict[str, RawPluginConfigDict]]
        Dataset plugins, keyed by the namespace of the dataset they extend.
        Omitted when no dataset carries plugins.
    datasets : dict[str, str | Dataset]
        Datasets to bootstrap, keyed by the attribute namespace they are bound
        to on the :class:`cihai.core.Cihai` object. A value is either a dotted
        import path resolved through :func:`cihai.utils.import_string` or a
        :class:`cihai.extend.Dataset` subclass.
    database : RawDatabaseConfigDict
        Database connection settings.
    dirs : RawDirsConfigDict
        Cache, log, and data directories.
    debug : bool
        Debug flag, ``False`` in the default config.
    """

    plugins: NotRequired[dict[str, RawPluginConfigDict]]
    datasets: dict[str, str | Dataset]
    database: RawDatabaseConfigDict
    dirs: RawDirsConfigDict
    debug: bool


class ConfigDict(TypedDict):
    """Cihai Configuration dictionary.

    Shape of :attr:`cihai.core.Cihai.config`: user input merged over
    :data:`cihai.constants.DEFAULT_CONFIG` with templates expanded, so every
    key is present.

    Attributes
    ----------
    plugins : dict[str, RawPluginConfigDict]
        Dataset plugins, keyed by the namespace of the dataset they extend. An
        empty mapping when no dataset carries plugins.
    datasets : dict[str, str | Dataset]
        Datasets to bootstrap, keyed by the attribute namespace they are bound
        to on the :class:`cihai.core.Cihai` object. A value is either a dotted
        import path resolved through :func:`cihai.utils.import_string` or a
        :class:`cihai.extend.Dataset` subclass.
    database : RawDatabaseConfigDict
        Database connection settings.
    dirs : RawDirsConfigDict
        Cache, log, and data directories.
    debug : bool
        Debug flag, ``False`` in the default config.
    """

    plugins: dict[str, RawPluginConfigDict]
    datasets: dict[str, str | Dataset]
    database: RawDatabaseConfigDict
    dirs: RawDirsConfigDict
    debug: bool
