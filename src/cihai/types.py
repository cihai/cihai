"""Typings for cihai.

This is meant to be imported from inside :const:`typing.TYPE_CHECKING` so it does not
require ``typing_extensions`` at runtime:

>>> from typing import TYPE_CHECKING
>>> if TYPE_CHECKING:
...     from .types import DirsConfigDict
>>> def my_fn(dir_config: "DirsConfigDict") -> None:
...     pass
"""

import pathlib
import typing as t

from typing_extensions import NotRequired, TypedDict

if t.TYPE_CHECKING:
    from typing_extensions import TypeAlias

    from cihai.extend import Dataset


UntypedDict: "TypeAlias" = dict[str, object]


class RawPluginConfigDict(TypedDict):
    """Barebones plugin config dictionary."""


class RawDirsConfigDict(TypedDict):
    """Raw directory config dictionary."""

    cache: t.Union[str, pathlib.Path]
    log: t.Union[str, pathlib.Path]
    data: t.Union[str, pathlib.Path]


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
    datasets: dict[str, t.Union[str, "Dataset"]]
    database: RawDatabaseConfigDict
    dirs: RawDirsConfigDict
    debug: bool


class ConfigDict(TypedDict):
    """Cihai Configuration dictionary."""

    plugins: dict[str, RawPluginConfigDict]
    datasets: dict[str, t.Union[str, "Dataset"]]
    database: RawDatabaseConfigDict
    dirs: RawDirsConfigDict
    debug: bool
