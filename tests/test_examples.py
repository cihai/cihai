import pytest

import examples.basic_usage
import examples.basic_usage_manual
import examples.dataset
import examples.variant_ts_difficulties
import examples.variants


def test_dataset(unihan_options):
    examples.dataset.run()


def test_variants(unihan_options):
    examples.variants.run(unihan_options=unihan_options)


def test_ts_difficulties(unihan_options):
    examples.variant_ts_difficulties.run(unihan_options=unihan_options)


def test_basic_usage(unihan_options, capsys: pytest.CaptureFixture[str]):
    examples.basic_usage.run(unihan_options=unihan_options)

    captured = capsys.readouterr()

    assert "lookup for 好: good" in captured.out
    assert 'matches for "good": 好' in captured.out


def test_basic_usage_manual(unihan_options, capsys: pytest.CaptureFixture[str]):
    examples.basic_usage_manual.run(unihan_options=unihan_options)

    captured = capsys.readouterr()

    assert "lookup for 好: good" in captured.out
    assert 'matches for "good": 好' in captured.out
