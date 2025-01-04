"""Test bootstrapping of database."""

from __future__ import annotations

import typing as t

from cihai.core import Cihai
from cihai.data.unihan import bootstrap

if t.TYPE_CHECKING:
    import pathlib


def test_reflect_db(
    tmpdb_file: pathlib.Path,
    unihan_options: dict[str, object],
) -> None:
    """Verify database reflection."""
    c = Cihai(config={"database": {"url": f"sqlite:///{tmpdb_file}"}})
    assert not c.unihan.is_bootstrapped
    bootstrap.bootstrap_unihan(c.sql.engine, c.sql.metadata, unihan_options)
    assert not hasattr(c.sql.base.classes, "Unihan")
    c.unihan.sql.reflect_db()
    assert hasattr(c.sql.base.classes, "Unihan")
