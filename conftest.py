"""Conftest.py (root-level).

We keep this in root pytest fixtures in pytest's doctest plugin to be available, as well
as avoiding conftest.py from being included in the wheel, in addition to pytest_plugin
for pytester only being available via the root directory.

See "pytest_plugins in non-top-level conftest files" in
https://docs.pytest.org/en/stable/deprecations.html
"""

from __future__ import annotations

import getpass
import pathlib
import typing as t

import pytest

pytest_plugins = ["pytester"]


@pytest.fixture(scope="session")
def home_path(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    """Ensure a random, temporary home directory, return as ``Path``."""
    return tmp_path_factory.mktemp("home")


@pytest.fixture(scope="session")
def home_user_name() -> str:
    """Return default username to set for :func:`user_path` fixture."""
    return getpass.getuser()


@pytest.fixture(scope="session")
def user_path(home_path: pathlib.Path, home_user_name: str) -> pathlib.Path:
    """Return path to user's home directory."""
    p = home_path / home_user_name
    p.mkdir()
    return p


@pytest.fixture
def set_home(
    monkeypatch: pytest.MonkeyPatch,
    user_path: pathlib.Path,
) -> None:
    """Set user's ``HOME`` environmental variable to ``user_path`` fixture."""
    monkeypatch.setenv("HOME", str(user_path))


@pytest.fixture
def project_root(
    monkeypatch: pytest.MonkeyPatch,
    user_path: pathlib.Path,
) -> pathlib.Path:
    """Return project root."""
    return pathlib.Path(__file__).parent


@pytest.fixture(autouse=True)
def add_doctest_fixtures(
    request: pytest.FixtureRequest,
    doctest_namespace: dict[str, t.Any],
    tmp_path: pathlib.Path,
    set_home: pathlib.Path,
) -> None:
    """Harness pytest fixtures to doctests namespace."""
    from _pytest.doctest import DoctestItem

    if isinstance(request._pyfuncitem, DoctestItem):
        request.getfixturevalue("set_home")
    doctest_namespace["tmp_path"] = tmp_path


@pytest.fixture(autouse=True)
def setup(
    request: pytest.FixtureRequest,
    set_home: pathlib.Path,
) -> None:
    """Bootstrap pytest fixtures."""


@pytest.fixture(autouse=True)
def cwd_default(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
    """Set current working directory to random path."""
    monkeypatch.chdir(tmp_path)
