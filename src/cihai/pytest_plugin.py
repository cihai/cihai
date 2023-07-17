import contextlib
import getpass
import logging
import os
import pathlib
import typing as t
import zipfile

import pytest
from appdirs import AppDirs as BaseAppDirs

from cihai.core import Cihai
from unihan_etl._internal.app_dirs import AppDirs

logger = logging.getLogger(__name__)
USING_ZSH = "zsh" in os.getenv("SHELL", "")

PROJECT_PATH = pathlib.Path(__file__).parent.parent.parent
TESTS_PATH = PROJECT_PATH / "tests"
SAMPLE_FIXTURE_PATH = TESTS_PATH / "fixtures"

app_dirs = AppDirs(_app_dirs=BaseAppDirs("pytest-cihai", "cihai team"))


if t.TYPE_CHECKING:
    from cihai.types import UntypedDict
    from unihan_etl.options import Options as UnihanOptions


@pytest.fixture(scope="session")
def cihai_user_cache_path() -> pathlib.Path:
    """Override this to destination of your choice."""
    return app_dirs.user_cache_dir


@pytest.fixture(scope="session")
def cihai_project_cache_path() -> pathlib.Path:
    """Override this to destination of your choice."""
    return PROJECT_PATH / ".cihai_cache"


@pytest.fixture(scope="session")
def unihan_project_cache_path() -> pathlib.Path:
    """Override this to destination of your choice."""
    return PROJECT_PATH / ".unihan_cache"


@pytest.fixture(scope="session")
def cihai_cache_path(cihai_project_cache_path: pathlib.Path) -> pathlib.Path:
    """Override this to destination of your choice."""
    return cihai_project_cache_path


@pytest.fixture(scope="session")
def cihai_fixture_root(cihai_cache_path: pathlib.Path) -> pathlib.Path:
    return cihai_cache_path / "f"


@pytest.fixture(scope="session")
def cihai_full_path(cihai_fixture_root: pathlib.Path) -> pathlib.Path:
    return cihai_fixture_root / "full"


@pytest.fixture(scope="session")
def cihai_full_db_path(cihai_full_path: pathlib.Path) -> pathlib.Path:
    return cihai_full_path / "cihai.db"


@pytest.fixture(scope="session")
def cihai_full_db_dsn(cihai_full_db_path: pathlib.Path) -> str:
    cihai_full_db_path.parent.mkdir(exist_ok=True, parents=True)
    return f"sqlite:///{cihai_full_db_path}"


@pytest.fixture(scope="session")
def cihai_full_options(
    unihan_full_options: "UnihanOptions",
    cihai_full_db_dsn: str,
) -> "UntypedDict":
    """Setup a large portion of cihai, includes a similarly UnihanOptions."""
    return {
        "database": {"url": cihai_full_db_dsn or "sqlite:///:memory:"},
        "unihan": unihan_full_options,
    }


@pytest.fixture(scope="session")
def cihai_full(
    cihai_full_options: "UntypedDict",
    cihai_full_path: pathlib.Path,
) -> "Cihai":
    """Setup a tiny portion of UNIHAN, return a UnihanOptions."""
    return Cihai(config=cihai_full_options)


@pytest.fixture(scope="session")
def ensure_cihai_full(
    cihai_full_path: pathlib.Path,
    unihan_full_options: "UnihanOptions",
    cihai_full: "Cihai",
) -> None:
    """Downloads and extracts a full UNIHAN, return a UnihanOptions.

    >>> import pathlib

    >>> from cihai.core import Cihai
    >>> from unihan_etl.options import Options as UnihanOptions

    >>> def test_ensure_cihai_full(
    ...     cihai_full_path: pathlib.Path,
    ...     unihan_full_options: "UnihanOptions",
    ...     cihai_full: "Cihai",
    ... ) -> None:
    ...     cihai_full.bootstrap()
    ...
    ...     if not cihai_full.unihan.is_bootstrapped:
    ...         cihai_full.unihan.bootstrap(unihan_full_options)
    ...
    ...     conn = cihai_full.sql.engine.connect()
    ...     conn.close()
    ...
    ...     unihan_full_destination = unihan_full_options.destination
    ...     assert unihan_full_destination.exists()
    ...     assert unihan_full_destination.stat().st_size > 20_000_000
    ...
    ...     assert unihan_full_options.work_dir.exists()
    ...     unihan_readings = unihan_full_options.work_dir / 'Unihan_Readings.txt'
    ...     assert unihan_readings.stat().st_size > 6200000

    .. ::
        >>> locals().keys()
        dict_keys(...)

        >>> source = ''.join([e.source for e in request._pyfuncitem.dtest.examples][:4])
        >>> pytester = request.getfixturevalue('pytester')

        >>> pytester.makepyfile(**{'ensure_cihai_full_1.py': source})
        PosixPath(...)

        >>> result = pytester.runpytest('ensure_cihai_full_1.py', '--disable-warnings')
        ===...

        >>> result.assert_outcomes(passed=1)

    Extending fixtures:

    >>> import pathlib

    >>> import pytest

    >>> from cihai.core import Cihai
    >>> from unihan_etl.options import Options as UnihanOptions

    >>> @pytest.fixture
    ... def my_cihai(
    ...     cihai_full_path: pathlib.Path,
    ...     unihan_full_options: "UnihanOptions",
    ...     cihai_full: "Cihai",
    ... ) -> "Cihai":
    ...     return cihai_full

    >>> def test_my_extended_cihai_Fixture(my_cihai: "Cihai") -> None:
    ...     my_cihai.bootstrap()
    ...     if not my_cihai.unihan.is_bootstrapped:
    ...         my_cihai.unihan.bootstrap(unihan_full_options)
    ...
    ...     conn = my_cihai.sql.engine.connect()
    ...     conn.close()
    ...

    .. ::
        >>> locals().keys()
        dict_keys(...)

        >>> source = ''.join([
        ...     e.source for e in request._pyfuncitem.dtest.examples][10:16]
        ... )
        >>> pytester = request.getfixturevalue('pytester')

        >>> pytester.makepyfile(**{'example_2.py': source})
        PosixPath(...)

        >>> result = pytester.runpytest('example_2.py', '--disable-warnings')
        ===...

        >>> result.assert_outcomes(passed=1)
    """
    pkgr = Cihai(config={"unihan": unihan_full_options})
    pkgr.bootstrap()


@pytest.fixture(scope="session")
def cihai_quick_path(cihai_fixture_root: pathlib.Path) -> pathlib.Path:
    return cihai_fixture_root / "quick"


@pytest.fixture(scope="session")
def cihai_quick_zip_path(cihai_quick_path: pathlib.Path) -> pathlib.Path:
    return cihai_quick_path / "downloads" / "Unihan.zip"


@pytest.fixture(scope="session")
def cihai_quick_zip(
    cihai_quick_path: pathlib.Path,
    cihai_quick_zip_path: pathlib.Path,
    cihai_sample_fixture_files: list[pathlib.Path],
) -> zipfile.ZipFile:
    files = []
    for f in cihai_sample_fixture_files:
        files += [f]

    with contextlib.suppress(FileExistsError):
        cihai_quick_zip_path.parent.mkdir(parents=True)

    zf = zipfile.ZipFile(cihai_quick_zip_path, "a")
    for _f in cihai_sample_fixture_files:
        if _f.name not in zf.namelist():
            zf.write(_f, _f.name)
    zf.close()

    return zf


@pytest.fixture(scope="session")
def cihai_quick_db_path(cihai_quick_path: pathlib.Path) -> pathlib.Path:
    return cihai_quick_path / "cihai.db"


@pytest.fixture(scope="session")
def cihai_quick_db_dsn(cihai_quick_db_path: pathlib.Path) -> str:
    cihai_quick_db_path.parent.mkdir(exist_ok=True, parents=True)
    return f"sqlite:///{cihai_quick_db_path}"


@pytest.fixture(scope="session")
def cihai_quick_options(
    unihan_quick_options: "UnihanOptions",
    cihai_quick_db_dsn: str,
) -> "UntypedDict":
    """Setup a tiny portion of cihai, includes a similarly UnihanOptions."""
    return {
        "database": {"url": cihai_quick_db_dsn or "sqlite:///:memory:"},
        "unihan": unihan_quick_options,
    }


@pytest.fixture(scope="session")
def cihai_quick(
    cihai_quick_path: pathlib.Path,
    cihai_quick_options: "UntypedDict",
) -> "Cihai":
    """Setup a tiny portion of UNIHAN, return a UnihanOptions."""
    return Cihai(cihai_quick_options)


@pytest.fixture(scope="session")
def ensure_cihai_quick(
    cihai_quick_path: pathlib.Path,
    unihan_quick_options: "UnihanOptions",
    cihai_quick: "Cihai",
) -> None:
    """Setup a tiny portion of UNIHAN, return a UnihanOptions.

    >>> import pathlib

    >>> from cihai.core import Cihai
    >>> from unihan_etl.options import Options as UnihanOptions

    >>> def test_ensure_cihai_quick(
    ...     cihai_quick_path: pathlib.Path,
    ...     unihan_quick_options: "UnihanOptions",
    ...     cihai_quick: "Cihai",
    ... ) -> None:
    ...     cihai_quick.bootstrap()
    ...
    ...     if not cihai_quick.unihan.is_bootstrapped:
    ...         cihai_quick.unihan.bootstrap(unihan_quick_options)
    ...
    ...     conn = cihai_quick.sql.engine.connect()
    ...     conn.close()
    ...
    ...     unihan_quick_destination = unihan_quick_options.destination
    ...     assert unihan_quick_destination.exists()
    ...     assert unihan_quick_destination.stat().st_size == 171_968

    .. ::
        >>> locals().keys()
        dict_keys(...)

        >>> source = ''.join([e.source for e in request._pyfuncitem.dtest.examples][:4])
        >>> pytester = request.getfixturevalue('pytester')

        >>> pytester.makepyfile(**{'whatever.py': source})
        PosixPath(...)

        >>> result = pytester.runpytest('whatever.py', '--disable-warnings')
        ===...

        >>> result.assert_outcomes(passed=1)

    Extending fixtures:

    >>> import pathlib

    >>> import pytest

    >>> from cihai.core import Cihai
    >>> from unihan_etl.options import Options as UnihanOptions

    >>> @pytest.fixture
    ... def my_cihai(
    ...     cihai_quick_path: pathlib.Path,
    ...     unihan_quick_options: "UnihanOptions",
    ...     cihai_quick: "Cihai",
    ... ) -> "Cihai":
    ...     return cihai_quick

    >>> def test_my_extended_cihai_Fixture(my_cihai: "Cihai") -> None:
    ...     my_cihai.bootstrap()
    ...     if not my_cihai.unihan.is_bootstrapped:
    ...         my_cihai.unihan.bootstrap(unihan_quick_options)
    ...
    ...     conn = my_cihai.sql.engine.connect()
    ...     conn.close()

    .. ::
        >>> locals().keys()
        dict_keys(...)

        >>> source = ''.join(
        ...     [e.source for e in request._pyfuncitem.dtest.examples][10:16]
        ... )
        >>> pytester = request.getfixturevalue('pytester')

        >>> pytester.makepyfile(**{'example_2.py': source})
        PosixPath(...)

        >>> result = pytester.runpytest('example_2.py', '--disable-warnings')
        ===...

        >>> result.assert_outcomes(passed=1)
    """
    pkgr = Cihai({"unihan": unihan_quick_options})
    pkgr.bootstrap()


@pytest.fixture(scope="session")
def cihai_bootstrap_all(ensure_cihai_full: None, ensure_cihai_quick: None) -> None:
    """This should be used like so in your project's conftest.py:

    >>> import pytest
    >>> @pytest.fixture(scope="session", autouse=True)
    ... def bootstrap(cihai_bootstrap_all) -> None:
    ...     return None
    """
    return


@pytest.fixture(scope="session")
def cihai_home_path(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    """Temporary `/home/` path."""
    return tmp_path_factory.mktemp("home")


@pytest.fixture(scope="session")
def cihai_home_user_name() -> str:
    """Default username to set for :func:`cihai_user_path` fixture."""
    return getpass.getuser()


@pytest.fixture(scope="session")
def cihai_user_path(
    cihai_home_path: pathlib.Path,
    cihai_home_user_name: str,
) -> pathlib.Path:
    """Default temporary user directory.

    Used by: :func:`zshrc`

    Note: You will need to set the home directory, see :ref:`set_home`.
    """
    p = cihai_home_path / cihai_home_user_name
    p.mkdir()
    return p


@pytest.mark.skipif(not USING_ZSH, reason="Using ZSH")
@pytest.fixture(scope="session")
def cihai_zshrc(cihai_user_path: pathlib.Path) -> pathlib.Path:
    """This quiets ZSH default message.

    Needs a startup file .zshenv, .zprofile, .zshrc, .zlogin.
    """
    p = cihai_user_path / ".zshrc"
    p.touch()
    return p
