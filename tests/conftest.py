import pathlib
import typing as t
import zipfile

import pytest
import sqlalchemy

from cihai.data.unihan.constants import UNIHAN_FILES

if t.TYPE_CHECKING:
    from .types import UnihanOptions


@pytest.fixture
def tests_path() -> pathlib.Path:
    return pathlib.Path(__file__).parent


@pytest.fixture
def fixture_path(tests_path: pathlib.Path) -> pathlib.Path:
    return tests_path / "fixtures"


@pytest.fixture
def test_config_file(fixture_path: pathlib.Path) -> pathlib.Path:
    return fixture_path / "test_config.yml"


@pytest.fixture
def zip_path(tmp_path: pathlib.Path) -> pathlib.Path:
    return tmp_path / "Unihan.zip"


@pytest.fixture
def zip_file(zip_path: pathlib.Path, fixture_path: pathlib.Path) -> zipfile.ZipFile:
    _files = []
    for f in UNIHAN_FILES:
        _files += [fixture_path / f]
    zf = zipfile.ZipFile(zip_path, "a")
    for _f in _files:
        zf.write(_f, _f.name)
    zf.close()
    return zf


@pytest.fixture
def unihan_options(
    zip_file: zipfile.ZipFile, zip_path: pathlib.Path, tmp_path: pathlib.Path
) -> "UnihanOptions":
    return {
        "source": zip_path,
        "work_dir": tmp_path,
        "zip_path": tmp_path / "downloads" / "Moo.zip",
    }


@pytest.fixture(scope="function")
def tmpdb_file(tmpdir: pathlib.Path) -> pathlib.Path:
    return tmpdir / "test.db"


@pytest.fixture(scope="session")
def engine() -> sqlalchemy.Engine:
    return sqlalchemy.create_engine("sqlite:///")


@pytest.fixture(scope="session")
def metadata() -> sqlalchemy.MetaData:
    return sqlalchemy.MetaData()
