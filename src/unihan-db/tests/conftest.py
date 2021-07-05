import os
import zipfile

import pytest

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from unihan_db.bootstrap import UNIHAN_FILES


@pytest.fixture
def fixture_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixtures'))


@pytest.fixture
def test_config_file(fixture_path):
    return os.path.join(fixture_path, 'test_config.yml')


@pytest.fixture
def zip_path(tmpdir):
    return tmpdir.join('Unihan.zip')


@pytest.fixture
def zip_file(zip_path, fixture_path):
    _files = []
    for f in UNIHAN_FILES:
        _files += [os.path.join(fixture_path, f)]
    zf = zipfile.ZipFile(str(zip_path), 'a')
    for f in _files:
        zf.write(f, os.path.basename(f))
    zf.close()
    return zf


@pytest.fixture
def unihan_options(zip_file, zip_path, tmpdir):
    return {
        'source': str(zip_path),
        'work_dir': str(tmpdir),
        'zip_path': str(tmpdir.join('downloads').join('Moo.zip')),
        'expand': True,
    }


@pytest.fixture(scope='function')
def tmpdb_file(tmpdir):
    return tmpdir.join('test.db')


@pytest.fixture
def engine():
    return create_engine('sqlite:///:memory:')


@pytest.fixture(scope='function')
def session(engine, request):
    connection = engine.connect()
    transaction = connection.begin()
    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def metadata(engine):
    metadata = MetaData()
    metadata.engine = engine
    return metadata
