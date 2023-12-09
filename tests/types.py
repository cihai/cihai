"""Typings for cihai test module."""
import pathlib
import typing as t


class UnihanOptions(t.TypedDict):
    """Unihan Options dictionary."""

    source: pathlib.Path
    work_dir: pathlib.Path
    zip_path: pathlib.Path
