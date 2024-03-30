#!/usr/bin/env python
"""Cihai example for difficult cases of traditional and simplified CJK variants."""

import logging
import typing as t

from cihai.core import Cihai

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def run(unihan_options: t.Optional[t.Dict[str, object]] = None) -> None:
    """log.info difficult traditional / simplified CJK variants."""
    if unihan_options is None:
        unihan_options = {}

    c = Cihai()
    if not c.unihan.is_bootstrapped:  # download and install Unihan to db
        c.unihan.bootstrap(unihan_options)

    c.unihan.add_plugin(
        "cihai.data.unihan.dataset.UnihanVariants",
        namespace="variants",
    )

    log.info(
        "This example log.infos some tricky cases of character-by-character "
        "Traditional-Simplified mapping.",
    )
    log.info("https://www.unicode.org/reports/tr38/#N10211")
    log.info("3.7.1 bullet 4")

    for char in c.unihan.with_fields(["kTraditionalVariant", "kSimplifiedVariant"]):
        log.info(f"Character: {char.char}")
        trad = set(char.untagged_vars("kTraditionalVariant"))
        simp = set(char.untagged_vars("kSimplifiedVariant"))
        Unihan = c.sql.base.classes.Unihan
        if Unihan.char in trad and Unihan.char in simp:
            log.info("Case 1")
        else:
            log.info("Case 2 (non-idempotent)")
        for trad_var in trad:
            log.info(f"s2t: {trad_var}")
        for simp_var in simp:
            log.info(f"t2s: {simp_var}")


if __name__ == "__main__":
    run()
