#!/usr/bin/env python
"""CJK Variant lookup example for Cihai."""

import logging
import typing as t

from cihai.core import Cihai
from cihai.data.unihan.dataset import Unihan

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def variant_list(unihan: Unihan, field: str) -> None:
    """Return a list of variants for a CJK character."""
    for char in unihan.with_fields([field]):
        log.info(f"Character: {char.char}")
        for var in char.untagged_vars(field):
            log.info(var)


def run(unihan_options: t.Optional[dict[str, object]] = None) -> None:
    """Lookup variants for a CJK character. Accepts UNIHAN options dictionary."""
    if unihan_options is None:
        unihan_options = {}

    """Wrapped so we can test in tests/test_examples.py"""
    log.info("This example log.infos variant character data.")

    c = Cihai(config={"plugins": {"variants": unihan_options}})
    if not c.unihan.is_bootstrapped:  # download and install Unihan to db
        c.unihan.bootstrap()

    c.unihan.add_plugin(
        "cihai.data.unihan.dataset.UnihanVariants",
        namespace="variants",
    )

    log.info("## ZVariants")
    variant_list(c.unihan, "kZVariant")

    log.info("## kSemanticVariant")
    variant_list(c.unihan, "kSemanticVariant")

    log.info("## kSpecializedSemanticVariant")
    variant_list(c.unihan, "kSpecializedSemanticVariant")


if __name__ == "__main__":
    run()
