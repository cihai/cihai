#!/usr/bin/env python
"""CJK Variant lookup example for Cihai."""

import typing as t

from cihai.core import Cihai
from cihai.data.unihan.dataset import Unihan


def variant_list(unihan: Unihan, field: str) -> None:
    """Return a list of variants for a CJK character."""
    for char in unihan.with_fields([field]):
        for _var in char.untagged_vars(field):
            pass


def run(unihan_options: t.Optional[t.Dict[str, object]] = None) -> None:
    """Lookup variants for a CJK character. Accepts UNIHAN options dictionary."""
    if unihan_options is None:
        unihan_options = {}

    """Wrapped so we can test in tests/test_examples.py"""

    c = Cihai(config={"unihan_options": unihan_options})
    if not c.unihan.is_bootstrapped:  # download and install Unihan to db
        c.unihan.bootstrap()

    c.unihan.add_plugin(
        "cihai.data.unihan.dataset.UnihanVariants",
        namespace="variants",
    )

    variant_list(c.unihan, "kZVariant")

    variant_list(c.unihan, "kSemanticVariant")

    variant_list(c.unihan, "kSpecializedSemanticVariant")


if __name__ == "__main__":
    run()
