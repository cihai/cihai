import os
import pathlib
import typing as t

import pytest
from appdirs import AppDirs

from cihai.config import expand_config

if t.TYPE_CHECKING:
    from cihai.types import UntypedDict


#: XDG App directory locations
dirs = AppDirs("cihai", "cihai team")  # appname  # app author


def test_expand_config_xdg_vars() -> None:
    initial_dict: UntypedDict = {
        "dirs": {"cache": "{user_cache_dir}", "data": "{user_cache_dir}/data"}
    }

    expected_dict: UntypedDict = {
        "dirs": {
            "cache": pathlib.Path(dirs.user_cache_dir),
            "data": pathlib.Path(dirs.user_cache_dir) / "data",
        }
    }

    expand_config(initial_dict, dirs)
    assert initial_dict == expected_dict


def test_expand_config_user_vars() -> None:
    initial_dict: UntypedDict = {"dirs": {"cache": "~"}}

    expected_dict: UntypedDict = {"dirs": {"cache": pathlib.Path.home()}}

    expand_config(initial_dict, dirs)
    assert initial_dict == expected_dict


def test_expand_config_env_vars(tmpdir: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MYDIR", str(tmpdir))
    initial_dict: UntypedDict = {"dirs": {"cache": "${MYDIR}"}}

    expected_dict: UntypedDict = {
        "dirs": {"cache": pathlib.Path(str(os.environ.get("MYDIR")))}
    }

    expand_config(initial_dict, dirs)
    assert initial_dict == expected_dict
