#!/usr/bin/env python
from cihai.core import Cihai


def variant_list(unihan, field):
    for char in unihan.with_fields(field):
        print("Character: {}".format(char.char))
        for var in char.untagged_vars(field):
            print(var)


def run(unihan_options=None):
    """Wrapped so we can test in tests/test_examples.py"""
    print("This example prints variant character data.")

    c = Cihai()
    if not c.unihan.is_bootstrapped:  # download and install Unihan to db
        c.unihan.bootstrap(unihan_options)

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
