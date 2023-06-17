"""Tests for core functionality of cihai.

Test :class:`Cihai` object. Other tests will use an instance of ``Cihai``
using the ``test_config.yml``.
"""

import dataclasses
import pathlib
import typing as t

import sqlalchemy

import cihai
from cihai.constants import UnihanConfig
from cihai.core import Cihai
from cihai.data.unihan import bootstrap, constants as unihan_constants

if t.TYPE_CHECKING:
    from unihan_etl.options import Options as UnihanOptions


def test_cihai_version() -> None:
    """Test cihai.__version__ returns current version."""
    assert cihai.__version__


def test_config_defaults() -> None:
    """Test cihai object defaults (no params passed)."""
    app = Cihai()

    assert hasattr(app.config, "database")


def test_config_dict_args() -> None:
    """Test initialization from dictionary."""
    expected = "sqlite:///"

    app = Cihai({"database": {"url": expected}})

    result = app.config.database.url

    assert result == expected


def test_yaml_config_and_override(test_config_file: pathlib.Path) -> None:
    """Test initialization from config file path."""
    app = Cihai.from_file(test_config_file)

    assert hasattr(app.config, "database")


def test_unihan_options(
    unihan_options: "UnihanOptions",
    engine: sqlalchemy.Engine,
    test_config_file: pathlib.Path,
) -> None:
    """Test initialization of UNIHAN with options."""
    app = Cihai.from_file(test_config_file)
    bootstrap.bootstrap_unihan(
        engine=engine,
        metadata=app.sql.metadata,
        options=unihan_options,
    )
    assert "Unihan" in app.sql.metadata.tables
    assert app.sql.metadata.tables["Unihan"].columns
    assert set(app.sql.metadata.tables["Unihan"].columns.keys()) == {
        *unihan_constants.UNIHAN_FIELDS,
        "ucn",
        "char",
    }
    assert bootstrap.is_bootstrapped(app.sql.metadata)


def test_bootstraps_unihan_by_default() -> None:
    """Test bootstrapping UNIHAN by default."""
    app = Cihai()

    assert UnihanConfig().datasets.items() == app.config.datasets.items()
    assert app.unihan, "cihai bootstraps unihan by default"


def test_cihai_without_unihan() -> None:
    """Test bootstrapping without UNIHAN."""
    app = Cihai(unihan=False)
    assert (
        dataclasses.asdict(UnihanConfig()).items()
        != dataclasses.asdict(app.config).items()
    ), "app can be initialized without unihan"
    assert not hasattr(app, "unihan")
