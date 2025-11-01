"""Typings for cihai.

This is meant to be imported from inside :const:`typing.TYPE_CHECKING` so it does not
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
    from typing import TypeAlias

    from cihai.extend import Dataset


UntypedDict: TypeAlias = dict[str, object]


class RawPluginConfigDict(TypedDict):
    """Barebones plugin config dictionary."""


class RawDirsConfigDict(TypedDict):
    """Raw directory config dictionary."""

    cache: str | pathlib.Path
    log: str | pathlib.Path
    data: str | pathlib.Path


class DirsConfigDict(TypedDict):
    """Directory config dictionary."""

    cache: pathlib.Path
    log: pathlib.Path
    data: pathlib.Path


class RawDatabaseConfigDict(TypedDict):
    """Raw database config dictionary."""

    url: str


class RawConfigDict(TypedDict):
    """Raw, unresolved configuration dictionary."""

    plugins: NotRequired[dict[str, RawPluginConfigDict]]
    datasets: dict[str, str | Dataset]
    database: RawDatabaseConfigDict
    dirs: RawDirsConfigDict
    debug: bool


class ConfigDict(TypedDict):
    """Cihai Configuration dictionary."""

    plugins: dict[str, RawPluginConfigDict]
    datasets: dict[str, str | Dataset]
    database: RawDatabaseConfigDict
    dirs: RawDirsConfigDict
    debug: bool
