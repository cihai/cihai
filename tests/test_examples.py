"""Test examples/ found in cihai source directory."""
import importlib
import importlib.util
import pathlib
import re
import sys
import types
import typing as t

import pytest

from unihan_etl.options import Options as UnihanOptions


class LoadScriptFn(t.Protocol):
    """Protocol typings for load_script()."""

    def __callable__(
        self, example: str, project_root: pathlib.Path
    ) -> types.ModuleType:
        """Return script as a module."""
        ...


def load_script(example: str, project_root: pathlib.Path) -> types.ModuleType:
    """Load script as module via name and project root."""
    file_path = f"{project_root}/examples/{example}.py"
    module_name = "run"

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    assert spec.loader is not None
    spec.loader.exec_module(module)

    return module


def test_dataset(
    unihan_options: "UnihanOptions",
    project_root: pathlib.Path,
) -> None:
    """Test example dataset."""
    example = load_script("dataset", project_root=project_root)
    example.run()


def test_variants(
    unihan_quick_options: "UnihanOptions",
    unihan_ensure_quick: None,
    project_root: pathlib.Path,
) -> None:
    """Test variants."""
    example = load_script("variants", project_root=project_root)
    # print(f"unihan_quick_options: {unihan_quick_options}")
    # unihan_quick_options.fields = ["kDefinition"] + [
    #     field for field in unihan_quick_options.fields if field.endswith("Variant")
    # ]
    # print(f"unihan_quick_options filtered: {unihan_quick_options}")

    example.run(unihan_options=unihan_quick_options)


def test_ts_difficulties(
    unihan_options: "UnihanOptions", project_root: pathlib.Path
) -> None:
    """Test variant_ts_difficulties."""
    example = load_script("variant_ts_difficulties", project_root=project_root)
    example.run(unihan_options=unihan_options)


def test_basic_usage(
    capsys: pytest.CaptureFixture[str],
    unihan_options: "UnihanOptions",
    project_root: pathlib.Path,
) -> None:
    """Test basic_usage."""
    example = load_script("basic_usage", project_root=project_root)
    example.run(unihan_options=unihan_options)

    captured = capsys.readouterr()

    assert "lookup for 好: good" in captured.out
    assert re.search(r'matches for "good": .*好', captured.out, re.MULTILINE)


def test_basic_usage_manual(
    capsys: pytest.CaptureFixture[str],
    unihan_options: "UnihanOptions",
    project_root: pathlib.Path,
) -> None:
    """Test basic_usage_manual."""
    example = load_script("basic_usage_manual", project_root=project_root)
    example.run(unihan_options=unihan_options)

    captured = capsys.readouterr()

    assert "lookup for 好: good" in captured.out
    assert re.search(r'matches for "good": .*好', captured.out, re.MULTILINE)
