"""Typings for cihai test module."""

from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    import pathlib


class UnihanOptions(t.TypedDict):
    """Unihan Options dictionary."""

    source: pathlib.Path
    work_dir: pathlib.Path
    zip_path: pathlib.Path
