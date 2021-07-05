import os
import zipfile

import pytest

from unihan_etl import constants, process
from unihan_etl.process import DEFAULT_OPTIONS, Packager
from unihan_etl.util import merge_dict


@pytest.fixture
def test_options():
    return merge_dict(DEFAULT_OPTIONS.copy(), {'input_files': ['Unihan_Readings.txt']})


@pytest.fixture(scope="session")
def mock_zip_filename():
    return 'Unihan.zip'


@pytest.fixture(scope="session")
def fixture_dir():
    return str(os.path.join(os.path.dirname(__file__), 'fixtures'))


@pytest.fixture(scope="session")
def fixture_files(fixture_dir):
    files = [
        'Unihan_DictionaryIndices.txt',
        'Unihan_DictionaryLikeData.txt',
        'Unihan_IRGSources.txt',
        'Unihan_NumericValues.txt',
        'Unihan_OtherMappings.txt',
        'Unihan_RadicalStrokeCounts.txt',
        'Unihan_Readings.txt',
        'Unihan_Variants.txt',
    ]
    return [os.path.join(fixture_dir, f) for f in files]


@pytest.fixture(scope="session")
def sample_data2(fixture_files):
    return process.load_data(files=fixture_files)


@pytest.fixture(scope="session")
def mock_test_dir(tmpdir_factory):
    fn = tmpdir_factory.mktemp('unihan_etl')
    return fn


@pytest.fixture(scope="session")
def mock_zip_file(mock_test_dir, mock_zip_filename):
    return mock_test_dir.join(mock_zip_filename)


@pytest.fixture(scope="session")
def mock_zip(mock_zip_file, sample_data):
    zf = zipfile.ZipFile(str(mock_zip_file), 'a')
    zf.writestr("Unihan_Readings.txt", sample_data.encode('utf-8'))
    zf.close()
    return zf


@pytest.fixture(scope="session")
def TestPackager(mock_test_dir, mock_zip_file):
    # monkey-patching builder
    options = {
        'work_dir': str(mock_test_dir),
        'zip_path': str(mock_zip_file),
        'destination': str(mock_test_dir.join('unihan.csv')),
    }
    return Packager(options)


@pytest.fixture(scope="session")
def columns():
    return (
        constants.CUSTOM_DELIMITED_FIELDS
        + constants.INDEX_FIELDS
        + constants.SPACE_DELIMITED_FIELDS
    )


@pytest.fixture(scope="session")
def normalized_data(columns, fixture_files):
    data = process.load_data(files=fixture_files)

    return process.normalize(data, columns)


@pytest.fixture(scope="session")
def expanded_data(normalized_data):
    return process.expand_delimiters(normalized_data)


@pytest.fixture(scope="session")
def sample_data():
    return """\
U+3400	kCantonese	jau1
U+3400	kDefinition	(same as U+4E18 丘) hillock or mound
U+3400	kMandarin	qiū
U+3401	kCantonese	tim2
U+3401	kDefinition	to lick; to taste, a mat, bamboo bark
U+3401	kHanyuPinyin	10019.020:tiàn
"""
