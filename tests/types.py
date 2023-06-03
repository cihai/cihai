import pathlib
import typing as t


class UnihanOptions(t.TypedDict):
    source: pathlib.Path
    work_dir: pathlib.Path
    zip_path: pathlib.Path
