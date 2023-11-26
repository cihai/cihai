"""Conftest.py (root-level).

We keep this in root pytest fixtures in pytest's doctest plugin to be available, as well
as avoiding conftest.py from being included in the wheel, in addition to pytest_plugin
for pytester only being available via the root directory.

See "pytest_plugins in non-top-level conftest files" in
https://docs.pytest.org/en/stable/deprecations.html
"""
import getpass
import pathlib
import typing as t

import pytest

pytest_plugins = ["pytester"]


@pytest.fixture(scope="session")
def home_path(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    return tmp_path_factory.mktemp("home")


@pytest.fixture(scope="session")
def home_user_name() -> str:
    """Default username to set for :func:`user_path` fixture."""
    return getpass.getuser()


@pytest.fixture(scope="session")
def user_path(home_path: pathlib.Path, home_user_name: str) -> pathlib.Path:
    p = home_path / home_user_name
    p.mkdir()
    return p


@pytest.fixture(scope="function")
def set_home(
    monkeypatch: pytest.MonkeyPatch,
    user_path: pathlib.Path,
) -> None:
    monkeypatch.setenv("HOME", str(user_path))


@pytest.fixture(scope="function")
def project_root(
    monkeypatch: pytest.MonkeyPatch,
    user_path: pathlib.Path,
) -> pathlib.Path:
    return pathlib.Path(__file__).parent


@pytest.fixture(autouse=True)
def add_doctest_fixtures(
    request: pytest.FixtureRequest,
    doctest_namespace: t.Dict[str, t.Any],
    tmp_path: pathlib.Path,
    set_home: pathlib.Path,
) -> None:
    from _pytest.doctest import DoctestItem

    if isinstance(request._pyfuncitem, DoctestItem):
        request.getfixturevalue("set_home")
    doctest_namespace["tmp_path"] = tmp_path


@pytest.fixture(autouse=True)
def setup(
    request: pytest.FixtureRequest,
    set_home: pathlib.Path,
) -> None:
    pass


@pytest.fixture(autouse=True)
def cwd_default(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
    monkeypatch.chdir(tmp_path)
