#!/usr/bin/env python
"""Cihai example for difficult cases of traditional and simplified CJK variants."""

import typing as t

from cihai.core import Cihai


def run(unihan_options: t.Optional[t.Dict[str, object]] = None) -> None:
    """Print difficult traditional / simplified CJK variants."""
    if unihan_options is None:
        unihan_options = {}

    c = Cihai()
    if not c.unihan.is_bootstrapped:  # download and install Unihan to db
        c.unihan.bootstrap(unihan_options)

    c.unihan.add_plugin(
        "cihai.data.unihan.dataset.UnihanVariants",
        namespace="variants",
    )

    for char in c.unihan.with_fields(["kTraditionalVariant", "kSimplifiedVariant"]):
        trad = set(char.untagged_vars("kTraditionalVariant"))
        simp = set(char.untagged_vars("kSimplifiedVariant"))
        Unihan = c.sql.base.classes.Unihan
        if Unihan.char in trad and Unihan.char in simp:
            pass
        else:
            pass
        for _trad_var in trad:
            pass
        for _simp_var in simp:
            pass


if __name__ == "__main__":
    run()
