"""Tests for cihai.

Test :class:`Cihai` object. Other tests will use an instance of ``Cihai``
using the ``test_config.yml``.

"""
import typing as t

import sqlalchemy

import cihai
from cihai.constants import UNIHAN_CONFIG
from cihai.core import Cihai
from cihai.data.unihan import bootstrap, constants as unihan_constants


def test_cihai_version() -> None:
    assert cihai.__version__


def test_config_defaults() -> None:
    """Test config defaults."""

    app = Cihai()

    assert "database" in app.config


def test_config_dict_args() -> None:
    """Accepts dict as config."""

    expected = "world"

    app = Cihai({"hello": expected})

    result = app.config["hello"]  # type: ignore

    assert result == expected


def test_yaml_config_and_override(test_config_file: str) -> None:
    app = Cihai.from_file(test_config_file)

    assert app.config["database"]


def test_unihan_options(
    unihan_options: t.Dict[str, object],
    engine: sqlalchemy.Engine,
    test_config_file: str,
) -> None:
    app = Cihai.from_file(test_config_file)
    bootstrap.bootstrap_unihan(
        engine=engine, metadata=app.sql.metadata, options=unihan_options
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
    app = Cihai()
    assert UNIHAN_CONFIG.items() == app.config.items()
    assert app.unihan, "cihai bootstraps unihan by default"


def test_cihai_without_unihan() -> None:
    app = Cihai(unihan=False)
    assert (
        UNIHAN_CONFIG.items() != app.config.items()
    ), "app can be initialized without unihan"
    assert not hasattr(app, "unihan")
