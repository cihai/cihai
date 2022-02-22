import os

from appdirs import AppDirs

from cihai.config import Configurator, expand_config

#: XDG App directory locations
dirs = AppDirs("cihai", "cihai team")  # appname  # app author


def test_configurator(tmpdir):
    c = Configurator()
    isinstance(c.dirs, AppDirs)

    assert c


def test_expand_config_xdg_vars():
    initial_dict = {
        "dirs": {"cache": "{user_cache_dir}", "data": "{user_cache_dir}/data"}
    }

    expected_dict = {
        "dirs": {
            "cache": dirs.user_cache_dir,
            "data": os.path.join(dirs.user_cache_dir, "data"),
        }
    }

    expand_config(initial_dict, dirs)
    assert initial_dict == expected_dict


def test_expand_config_user_vars():
    initial_dict = {"dirs": {"cache": "~"}}

    expected_dict = {"dirs": {"cache": os.path.expanduser("~")}}

    expand_config(initial_dict, dirs)
    assert initial_dict == expected_dict


def test_expand_config_env_vars(tmpdir, monkeypatch):
    monkeypatch.setenv("MYDIR", str(tmpdir))
    initial_dict = {"dirs": {"cache": "${MYDIR}"}}

    expected_dict = {"dirs": {"cache": os.environ.get("MYDIR")}}

    expand_config(initial_dict, dirs)
    assert initial_dict == expected_dict
