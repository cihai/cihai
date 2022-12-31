import pathlib
import typing as t

if t.TYPE_CHECKING:
    from cihai.extend import Dataset


class RawPluginConfigDict(t.TypedDict):
    pass


class RawDirsConfigDict(t.TypedDict):
    cache: t.Union[str, pathlib.Path]
    log: t.Union[str, pathlib.Path]
    data: t.Union[str, pathlib.Path]


class DirsConfigDict(t.TypedDict):
    cache: pathlib.Path
    log: pathlib.Path
    data: pathlib.Path


class RawDatabaseConfigDict(t.TypedDict):
    url: str


class RawConfigDict(t.TypedDict):
    plugins: t.Dict[str, RawPluginConfigDict]
    datasets: t.Dict[str, t.Union[str, "Dataset"]]
    database: RawDatabaseConfigDict
    dirs: RawDirsConfigDict
    debug: bool


class ConfigDict(t.TypedDict):
    plugins: t.Dict[str, RawPluginConfigDict]
    datasets: t.Dict[str, t.Union[str, "Dataset"]]
    database: RawDatabaseConfigDict
    dirs: RawDirsConfigDict
    debug: bool
