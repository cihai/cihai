import importlib
import importlib.util
import sys
import types

import pytest


def load_script(example: str) -> types.ModuleType:
    file_path = f"examples/{example}.py"
    module_name = "run"

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    assert spec.loader is not None
    spec.loader.exec_module(module)

    return module


def test_dataset(unihan_options):
    example = load_script("dataset")
    example.run()


def test_variants(unihan_options):
    example = load_script("variants")
    example.run()


def test_ts_difficulties(unihan_options):
    example = load_script("variant_ts_difficulties")
    example.run(unihan_options=unihan_options)


def test_basic_usage(unihan_options, capsys: pytest.CaptureFixture[str]):
    example = load_script("basic_usage")
    example.run(unihan_options=unihan_options)

    captured = capsys.readouterr()

    assert "lookup for 好: good" in captured.out
    assert 'matches for "good": 好' in captured.out


def test_basic_usage_manual(unihan_options, capsys: pytest.CaptureFixture[str]):
    example = load_script("basic_usage_manual")
    example.run(unihan_options=unihan_options)

    captured = capsys.readouterr()

    assert "lookup for 好: good" in captured.out
    assert 'matches for "good": 好' in captured.out
