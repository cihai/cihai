"""Test examples/ found in cihai source directory."""

from __future__ import annotations

import importlib.util
import logging
import re
import sys
import typing as t

import pytest

if t.TYPE_CHECKING:
    import pathlib
    import types

    from .types import UnihanOptions


class LoadScriptFn(t.Protocol):
    """Protocol typings for load_script()."""

    def __callable__(
        self,
        example: str,
        project_root: pathlib.Path,
    ) -> types.ModuleType:
        """Return script as a module."""
        ...


class LiteralincludeExampleCase(t.NamedTuple):
    """Example script included from documentation."""

    example: str
    test_name: str
    test_id: str


LITERALINCLUDE_EXAMPLE_CASES = [
    LiteralincludeExampleCase(
        example="basic_usage",
        test_name="test_basic_usage",
        test_id="basic-usage",
    ),
    LiteralincludeExampleCase(
        example="variants",
        test_name="test_variants",
        test_id="variants",
    ),
    LiteralincludeExampleCase(
        example="variant_ts_difficulties",
        test_name="test_ts_difficulties",
        test_id="variant-ts-difficulties",
    ),
    LiteralincludeExampleCase(
        example="dataset",
        test_name="test_dataset",
        test_id="dataset",
    ),
]


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


def literalinclude_examples(project_root: pathlib.Path) -> set[str]:
    """Return example script names included from docs."""
    docs_path = project_root / "docs"
    pattern = re.compile(
        r"```\{literalinclude\}\s+(?:\.\./)+examples/([A-Za-z0-9_]+)\.py",
    )
    included: set[str] = set()
    for path in docs_path.rglob("*.md"):
        if "_build" in path.parts:
            continue
        for match in pattern.finditer(path.read_text(encoding="utf-8")):
            included.add(match.group(1))
    return included


@pytest.mark.parametrize(
    ("case",),
    [(case,) for case in LITERALINCLUDE_EXAMPLE_CASES],
    ids=[case.test_id for case in LITERALINCLUDE_EXAMPLE_CASES],
)
def test_literalincluded_examples_have_pytest_cases(
    case: LiteralincludeExampleCase,
    project_root: pathlib.Path,
) -> None:
    """Every documented example script should have a pytest case."""
    assert case.example in literalinclude_examples(project_root)
    assert case.test_name in globals()


def test_all_literalincluded_examples_are_registered(
    project_root: pathlib.Path,
) -> None:
    """New literalincludes should be added to example coverage."""
    expected = {case.example for case in LITERALINCLUDE_EXAMPLE_CASES}

    assert literalinclude_examples(project_root) <= expected


def test_variants_passes_unihan_options_to_bootstrap(
    monkeypatch: pytest.MonkeyPatch,
    project_root: pathlib.Path,
) -> None:
    """Variants example should use fixture-backed bootstrap options."""

    class FakeUnihan:
        is_bootstrapped = False

        def __init__(self) -> None:
            self.bootstrap_options: dict[str, object] | None = None

        def bootstrap(self, options: dict[str, object] | None = None) -> None:
            self.bootstrap_options = options

        def add_plugin(self, class_string: str, namespace: str) -> None:
            assert class_string == "cihai.data.unihan.dataset.UnihanVariants"
            assert namespace == "variants"

        def with_fields(self, fields: list[str]) -> list[object]:
            assert fields
            return []

    class FakeCihai:
        instances: t.ClassVar[list[FakeCihai]] = []

        def __init__(self, config: dict[str, object] | None = None) -> None:
            self.config = config
            self.unihan = FakeUnihan()
            self.instances.append(self)

    unihan_options: dict[str, object] = {"fields": ["kDefinition"]}
    example = load_script("variants", project_root=project_root)
    monkeypatch.setattr(example, "Cihai", FakeCihai)

    example.run(unihan_options=unihan_options)

    instance = FakeCihai.instances[-1]
    assert instance.config == {"unihan_options": unihan_options}
    assert instance.unihan.bootstrap_options is unihan_options


def test_dataset(
    unihan_options: UnihanOptions,
    project_root: pathlib.Path,
) -> None:
    """Test example dataset."""
    example = load_script("dataset", project_root=project_root)
    example.run()


def test_variants(
    unihan_options: UnihanOptions,
    project_root: pathlib.Path,
) -> None:
    """Test variants."""
    example = load_script("variants", project_root=project_root)
    example.run(unihan_options=unihan_options)


def test_ts_difficulties(
    unihan_options: UnihanOptions,
    project_root: pathlib.Path,
) -> None:
    """Test variant_ts_difficulties."""
    example = load_script("variant_ts_difficulties", project_root=project_root)
    example.run(unihan_options=unihan_options)


def test_basic_usage(
    caplog: pytest.LogCaptureFixture,
    unihan_options: UnihanOptions,
    project_root: pathlib.Path,
) -> None:
    """Test basic_usage."""
    caplog.set_level(logging.INFO)

    example = load_script("basic_usage", project_root=project_root)
    example.run(unihan_options=unihan_options)

    output = "".join(list(caplog.messages))

    assert "lookup for 㐭: (same as 廩) a granary, to supply (foodstuff)" in output
    assert re.search(
        r'matches for "granary": .*㐭',
        output,
        re.MULTILINE,
    )


def test_basic_usage_manual(
    caplog: pytest.LogCaptureFixture,
    unihan_options: UnihanOptions,
    project_root: pathlib.Path,
) -> None:
    """Test basic_usage_manual."""
    caplog.set_level(logging.INFO)

    example = load_script("basic_usage_manual", project_root=project_root)
    example.run(unihan_options=unihan_options)

    output = "".join(list(caplog.messages))

    assert "lookup for 㐭: (same as 廩) a granary, to supply (foodstuff)" in output
    assert re.search(
        r'matches for "granary": .*㐭',
        output,
        re.MULTILINE,
    )
