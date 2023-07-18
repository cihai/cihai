#!/usr/bin/env python
import typing as t

from cihai.core import Cihai
from cihai.data.unihan.dataset import Unihan


def variant_list(unihan: Unihan, field: str) -> None:
    for char in unihan.with_fields([field]):
        print(f"Character: {char.char}")
        for var in char.untagged_vars(field):
            print(var)


def run(unihan_options: t.Optional[t.Dict[str, object]] = None) -> None:
    if unihan_options is None:
        unihan_options = {}

    """Wrapped so we can test in tests/test_examples.py"""
    print("This example prints variant character data.")

    c = Cihai(config={"unihan_options": unihan_options})
    if not c.unihan.is_bootstrapped:  # download and install Unihan to db
        c.unihan.bootstrap()

    c.unihan.add_plugin(
        "cihai.data.unihan.dataset.UnihanVariants", namespace="variants"
    )

    print("## ZVariants")
    variant_list(c.unihan, "kZVariant")

    print("## kSemanticVariant")
    variant_list(c.unihan, "kSemanticVariant")

    print("## kSpecializedSemanticVariant")
    variant_list(c.unihan, "kSpecializedSemanticVariant")


if __name__ == "__main__":
    run()
