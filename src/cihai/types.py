import pathlib
import typing as t

from typing_extensions import NotRequired, TypedDict

from cihai._internal.types import StrPath


class RawConfigDict(t.TypedDict):
    name: str
    dir: StrPath
    url: str


RawConfigDir = dict[str, RawConfigDict]
RawConfig = dict[str, RawConfigDir]


class ConfigDict(TypedDict):
    name: str
    dir: pathlib.Path
    url: str
    shell_command_after: NotRequired[t.Optional[t.List[str]]]


ConfigDir = dict[str, ConfigDict]
Config = dict[str, ConfigDir]
