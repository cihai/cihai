"""Test configuration for cihai."""

import os
import pathlib
import typing as t

import pytest

from cihai.config import expand_config
from cihai.constants import app_dirs

if t.TYPE_CHECKING:
    from cihai.types import UntypedDict


def test_expand_config_xdg_vars() -> None:
    """Test resolution of XDG Variables."""
    initial_dict: UntypedDict = {
        "dirs": {"cache": "{user_cache_dir}", "data": "{user_cache_dir}/data"},
    }

    expected_dict: UntypedDict = {
        "dirs": {
            "cache": pathlib.Path(app_dirs.user_cache_dir),
            "data": pathlib.Path(app_dirs.user_cache_dir) / "data",
        },
    }

    expand_config(initial_dict, app_dirs)
    assert initial_dict == expected_dict


def test_expand_config_user_vars() -> None:
    """Test resolution of home directory ("~")."""
    initial_dict: UntypedDict = {"dirs": {"cache": "~"}}

    expected_dict: UntypedDict = {"dirs": {"cache": pathlib.Path.home()}}

    expand_config(initial_dict, app_dirs)
    assert initial_dict == expected_dict


def test_expand_config_env_vars(tmpdir: str, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test resolution of environment variables."""
    monkeypatch.setenv("MYDIR", str(tmpdir))
    initial_dict: UntypedDict = {"dirs": {"cache": "${MYDIR}"}}

    expected_dict: UntypedDict = {
        "dirs": {"cache": pathlib.Path(str(os.environ.get("MYDIR")))},
    }

    expand_config(initial_dict, app_dirs)
    assert initial_dict == expected_dict
