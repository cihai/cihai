#!/usr/bin/env python
import typing as t

from cihai.core import Cihai


def run(unihan_options: t.Optional[t.Dict[str, object]] = None) -> None:
    if unihan_options is None:
        unihan_options = {}

    c = Cihai()
    if not c.unihan.is_bootstrapped:  # download and install Unihan to db
        c.unihan.bootstrap(unihan_options)

    c.unihan.add_plugin(
        "cihai.data.unihan.dataset.UnihanVariants", namespace="variants"
    )

    print(
        "This example prints some tricky cases of character-by-character "
        "Traditional-Simplified mapping."
    )
    print("https://www.unicode.org/reports/tr38/#N10211")
    print("3.7.1 bullet 4")

    for char in c.unihan.with_fields(["kTraditionalVariant", "kSimplifiedVariant"]):
        print(f"Character: {char.char}")
        trad = set(char.untagged_vars("kTraditionalVariant"))
        simp = set(char.untagged_vars("kSimplifiedVariant"))
        Unihan = c.sql.base.classes.Unihan
        if Unihan.char in trad and Unihan.char in simp:
            print("Case 1")
        else:
            print("Case 2 (non-idempotent)")
        for trad_var in trad:
            print(f"s2t: {trad_var}")
        for simp_var in simp:
            print(f"t2s: {simp_var}")


if __name__ == "__main__":
    run()
