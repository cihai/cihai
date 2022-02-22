"""Tests for cihai.

Test :class:`Cihai` object. Other tests will use an instance of ``Cihai``
using the ``test_config.yml``.

"""
import cihai
from cihai.constants import UNIHAN_CONFIG
from cihai.core import Cihai
from cihai.data.unihan import bootstrap


def test_cihai_version():
    assert cihai.__version__


def test_config_defaults():
    """Test config defaults."""

    app = Cihai()

    assert "database" in app.config


def test_config_dict_args():
    """Accepts dict as config."""

    expected = "world"

    app = Cihai({"hello": expected})

    result = app.config["hello"]

    assert result == expected


def test_yaml_config_and_override(test_config_file):
    app = Cihai.from_file(test_config_file)

    assert app.config["database"]


def test_unihan_options(unihan_options, test_config_file):
    app = Cihai.from_file(test_config_file)
    bootstrap.bootstrap_unihan(app.sql.metadata, unihan_options)
    assert "Unihan" in app.sql.metadata.tables
    assert app.sql.metadata.tables["Unihan"].columns
    assert set(app.sql.metadata.tables["Unihan"].columns.keys()) == set(
        bootstrap.UNIHAN_FIELDS + ["ucn", "char"]
    )
    assert bootstrap.is_bootstrapped(app.sql.metadata)


def test_bootstraps_unihan_by_default():
    app = Cihai()
    assert UNIHAN_CONFIG.items() == app.config.items()
    assert app.unihan, "cihai bootstraps unihan by default"


def test_cihai_without_unihan():
    app = Cihai(unihan=False)
    assert (
        UNIHAN_CONFIG.items() != app.config.items()
    ), "app can be initialized without unihan"
    assert not hasattr(app, "unihan")
