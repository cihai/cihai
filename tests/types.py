import pathlib
from typing_extensions import TypedDict


class UnihanOptions(TypedDict):
    source: pathlib.Path
    work_dir: pathlib.Path
    zip_path: pathlib.Path
