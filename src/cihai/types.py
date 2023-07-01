import pathlib
import typing as t

from typing_extensions import NotRequired, TypedDict

if t.TYPE_CHECKING:
    from typing_extensions import TypeAlias

    from cihai.extend import Dataset


UntypedDict: "TypeAlias" = t.Dict[str, object]


class RawPluginConfigDict(TypedDict):
    pass


class RawDirsConfigDict(TypedDict):
    cache: t.Union[str, pathlib.Path]
    log: t.Union[str, pathlib.Path]
    data: t.Union[str, pathlib.Path]


class DirsConfigDict(TypedDict):
    cache: pathlib.Path
    log: pathlib.Path
    data: pathlib.Path


class RawDatabaseConfigDict(TypedDict):
    url: str


class RawConfigDict(TypedDict):
    plugins: NotRequired[t.Dict[str, RawPluginConfigDict]]
    datasets: t.Dict[str, t.Union[str, "Dataset"]]
    database: RawDatabaseConfigDict
    dirs: RawDirsConfigDict
    debug: bool


class ConfigDict(TypedDict):
    plugins: t.Dict[str, RawPluginConfigDict]
    datasets: t.Dict[str, t.Union[str, "Dataset"]]
    database: RawDatabaseConfigDict
    dirs: RawDirsConfigDict
    debug: bool
