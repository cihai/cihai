import pathlib
import typing as t

from appdirs import AppDirs

if t.TYPE_CHECKING:
    from cihai.types import ConfigDict

#: XDG App directory locations
app_dirs = AppDirs("cihai", "cihai team")

#: Default configuration
DEFAULT_CONFIG: "ConfigDict" = {
    "debug": False,
    "database": {"url": "sqlite:///{user_data_dir}/cihai.db"},
    "dirs": {
        "cache": pathlib.Path(app_dirs.user_cache_dir),
        "log": pathlib.Path(app_dirs.user_log_dir),
        "data": pathlib.Path(app_dirs.user_data_dir),
    },
    "datasets": {},
    "plugins": {},
}

#: User will be prompted to automatically configure their installation for UNIHAN
UNIHAN_CONFIG = {
    "datasets": {"unihan": "cihai.data.unihan.dataset.Unihan"},
    # Turn off by default for using as a plugin example in examples/
    # "plugins": {"unihan": {"variants": "cihai.data.unihan.dataset.UnihanVariants"}},
}
