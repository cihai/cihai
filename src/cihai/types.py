"""Typings for cihai."""
import pathlib
import typing as t

from typing_extensions import NotRequired, TypedDict

if t.TYPE_CHECKING:
    from typing_extensions import TypeAlias

    from cihai.extend import Dataset


UntypedDict: "TypeAlias" = t.Dict[str, object]


class RawPluginConfigDict(TypedDict):
    """Barebones plugin config dictionary."""

    pass


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

    plugins: NotRequired[t.Dict[str, RawPluginConfigDict]]
    datasets: t.Dict[str, t.Union[str, "Dataset"]]
    database: RawDatabaseConfigDict
    dirs: RawDirsConfigDict
    debug: bool


class ConfigDict(TypedDict):
    """Cihai Configuration dictionary."""

    plugins: t.Dict[str, RawPluginConfigDict]
    datasets: t.Dict[str, t.Union[str, "Dataset"]]
    database: RawDatabaseConfigDict
    dirs: RawDirsConfigDict
    debug: bool
