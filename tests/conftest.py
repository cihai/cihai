"""Pytest configuration for cihai tests."""

import dataclasses
import pathlib
import zipfile

import pytest
import sqlalchemy

from cihai.data.unihan.constants import (
    UNIHAN_ETL_DEFAULT_OPTIONS,
    UNIHAN_ETL_DEFAULT_OPTIONS_DICT,
    UNIHAN_FILES,
)
from unihan_etl.options import Options as UnihanOptions


@pytest.fixture
def tests_path() -> pathlib.Path:
    """Return cihai tests/ directory."""
    return pathlib.Path(__file__).parent


@pytest.fixture
def fixture_path(tests_path: pathlib.Path) -> pathlib.Path:
    """Return cihai tests/fixtures/ directory."""
    return tests_path / "fixtures"


@pytest.fixture
def test_config_file(fixture_path: pathlib.Path) -> pathlib.Path:
    """Return cihai test configuration file."""
    return fixture_path / "test_config.yml"


@pytest.fixture
def zip_path(tmp_path: pathlib.Path) -> pathlib.Path:
    """Return path to test Unihan.zip file."""
    return tmp_path / "Unihan.zip"


@pytest.fixture
def zip_file(zip_path: pathlib.Path, fixture_path: pathlib.Path) -> zipfile.ZipFile:
    """Create and return ZipFile of UNIHAN."""
    files = []
    for f in UNIHAN_FILES:
        files += [fixture_path / f]
    zf = zipfile.ZipFile(zip_path, "a")
    for _f in files:
        zf.write(_f, _f.name)
    zf.close()
    return zf


@pytest.fixture
def unihan_options(
    zip_file: zipfile.ZipFile,
    zip_path: pathlib.Path,
    tmp_path: pathlib.Path,
) -> UnihanOptions:
    """Return test UnihanOptions."""
    return UnihanOptions(
        source=str(zip_path),
        work_dir=tmp_path,
        zip_path=tmp_path / "downloads" / "Moo.zip",
        destination=tmp_path / "unihan.csv",
        **UNIHAN_ETL_DEFAULT_OPTIONS_DICT,
    )
    return UnihanOptions(
        **(
            dataclasses.asdict(UNIHAN_ETL_DEFAULT_OPTIONS)
            | dataclasses.asdict(
                UnihanOptions(
                    source=str(zip_path),
                    work_dir=tmp_path,
                    zip_path=tmp_path / "downloads" / "Moo.zip",
                    input_files=UNIHAN_FILES,
                    destination=tmp_path / "unihan.csv",
                ),
            )
        ),
    )


@pytest.fixture
def tmpdb_file(tmpdir: pathlib.Path) -> pathlib.Path:
    """Return test.db file."""
    return tmpdir / "test.db"


@pytest.fixture(scope="session")
def engine() -> sqlalchemy.Engine:
    """Return in-memory SQLite SQLAlchemy engine for cihai tests."""
    return sqlalchemy.create_engine("sqlite:///")


@pytest.fixture(scope="session")
def metadata() -> sqlalchemy.MetaData:
    """Return SQLAlchemy Metadata for cihai tests."""
    return sqlalchemy.MetaData()
