import pathlib
import textwrap
import typing as t

import pytest

if t.TYPE_CHECKING:
    from cihai.core import Cihai
    from unihan_etl.options import Options as UnihanOptions

FixtureFileDict = dict[str, str]


def test_thing(
    cihai_full_path: pathlib.Path,
    unihan_full_options: "UnihanOptions",
    cihai_full: "Cihai",
) -> None:
    cihai_full.bootstrap()

    if not cihai_full.unihan.is_bootstrapped:  # download and install Unihan to db
        cihai_full.unihan.bootstrap(unihan_full_options)

    conn = cihai_full.sql.engine.connect()
    conn.close()

    unihan_full_destination = unihan_full_options.destination
    assert unihan_full_destination.exists()
    assert unihan_full_destination.stat().st_size > 20_000_000

    assert unihan_full_options.work_dir.exists()
    unihan_readings = unihan_full_options.work_dir / "Unihan_Readings.txt"
    assert unihan_readings.stat().st_size > 6200000


class PytestPluginFixture(t.NamedTuple):
    # pytest
    test_id: str

    # Content
    files: FixtureFileDict
    tests_passed: int


FIXTURES = [
    PytestPluginFixture(
        test_id="ensure_cihai_full",
        files={
            "ensure_cihai_full.py": textwrap.dedent(
                """
import pathlib

from cihai.core import Cihai
from unihan_etl.options import Options as UnihanOptions

def test_ensure_cihai_full(
    cihai_full_path: pathlib.Path,
    unihan_full_options: "UnihanOptions",
    cihai_full: "Cihai",
) -> None:
    assert cihai_full_path is not None
    assert unihan_full_options is not None
    assert cihai_full is not None

    assert isinstance(cihai_full_path, pathlib.Path)
    assert isinstance(unihan_full_options, UnihanOptions)
    assert isinstance(cihai_full, Cihai)

    if not cihai_full.unihan.is_bootstrapped:  # download and install Unihan to db
        cihai_full.unihan.bootstrap(unihan_full_options)

    conn = cihai_full.sql.engine.connect()
    conn.close()

    unihan_full_destination = unihan_full_options.destination
    assert unihan_full_destination.exists()
    assert unihan_full_destination.stat().st_size > 20_000_000

    assert unihan_full_options.work_dir.exists()
    unihan_readings = unihan_full_options.work_dir / 'Unihan_Readings.txt'
    assert unihan_readings.stat().st_size > 6200000
        """,
            ),
        },
        tests_passed=1,
    ),
    PytestPluginFixture(
        test_id="ensure_cihai_quick",
        files={
            "ensure_cihai_quick.py": textwrap.dedent(
                """
def test_ensure_cihai_quick() -> None:
    assert True
        """,
            ),
        },
        tests_passed=1,
    ),
]


@pytest.mark.parametrize(
    PytestPluginFixture._fields,
    FIXTURES,
    ids=[f.test_id for f in FIXTURES],
)
def test_plugin(
    pytester: pytest.Pytester,
    monkeypatch: pytest.MonkeyPatch,
    test_id: str,
    files: FixtureFileDict,
    tests_passed: int,
) -> None:
    # Initialize variables
    pytester.plugins = ["pytest_plugin"]
    pytester.makefile(
        ".ini",
        pytest=textwrap.dedent(
            """
[pytest]
addopts=-vv
        """.strip(),
        ),
    )
    pytester.makeconftest(
        textwrap.dedent(
            r"""
import pathlib
import pytest

@pytest.fixture(autouse=True)
def setup(
    request: pytest.FixtureRequest,
) -> None:
    pass
    """,
        ),
    )
    tests_path = pytester.path / "tests"
    first_test_key = next(iter(files.keys()))
    first_test_filename = str(tests_path / first_test_key)

    # Setup Files
    tests_path.mkdir()
    for file_name, text in files.items():
        file = tests_path / file_name
        file.write_text(
            text,
            encoding="utf-8",
        )
    first_test_key = next(iter(files.keys()))
    first_test_filename = str(tests_path / first_test_key)

    # Test
    result = pytester.runpytest(str(first_test_filename))
    result.assert_outcomes(passed=1)
