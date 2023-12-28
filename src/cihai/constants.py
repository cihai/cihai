"""Constants for cihai."""

import dataclasses
import pathlib
import typing as t

from appdirs import AppDirs as BaseAppDirs

from cihai.__about__ import (
    __author__,
    __package_name__,
)
from unihan_etl._internal.app_dirs import AppDirs

if t.TYPE_CHECKING:
    from typing_extensions import TypeAlias

    from cihai.types import PluginMap


#: XDG App directory locations
_app_dirs = BaseAppDirs(__package_name__, __author__)
app_dirs = AppDirs(_app_dirs=_app_dirs)


#: Default configuration
# DEFAULT_CONFIG: "UntypedDict" = {}


@dataclasses.dataclass
class Database:
    """Database configuration for Cihai."""

    url: str = "sqlite:///{user_data_dir}/cihai.db"


DatasetName: "TypeAlias" = str
Dataset: "TypeAlias" = str
Datasets = dict[DatasetName, Dataset]


@dataclasses.dataclass
class Config:
    """Cihai configuration."""

    debug: bool = False
    database: Database = dataclasses.field(default_factory=Database)
    dirs: AppDirs = dataclasses.field(default_factory=lambda: app_dirs)
    datasets: Datasets = dataclasses.field(default_factory=dict)
    plugins: "PluginMap" = dataclasses.field(default_factory=dict)

    def __post_init__(self) -> None:
        """Resolve variables and paths for Cihai configuration."""
        if isinstance(self.dirs, BaseAppDirs):
            self.dirs = AppDirs(_app_dirs=self.dirs)
        if isinstance(self.dirs, dict):
            self.dirs = AppDirs(_app_dirs=_app_dirs, **self.dirs)
            # for k, v in directories.items():
            #     setattr(
            #         self.dirs,
            #         k,

        if isinstance(self.database, dict):
            database_url = self.database.get("url")
            if isinstance(database_url, pathlib.Path):
                database_url = str(database_url)
            if isinstance(database_url, str):
                self.database["url"] = database_url.format(
                    **dataclasses.asdict(self.dirs),
                )

            self.database = Database(**self.database)


DEFAULT_CONFIG = Config()


class UnihanConfigDict(t.TypedDict):
    """Unihan configuration dictionary."""

    datasets: Datasets


#: User will be prompted to automatically configure their installation for UNIHAN
UNIHAN_CONFIG: "UnihanConfigDict" = UnihanConfigDict(
    {
        "datasets": {"unihan": "cihai.data.unihan.dataset.Unihan"},
        # Turn off by default for using as a plugin example in examples/
    },
)


@dataclasses.dataclass
class UnihanConfig:
    """Unihan configuration."""

    datasets: Datasets = dataclasses.field(
        default_factory=lambda: UNIHAN_CONFIG["datasets"],
    )
