#!/usr/bin/env python
# -*- coding: utf8 - *-

from __future__ import print_function, unicode_literals

from cihai.bootstrap import bootstrap_unihan
from cihai.core import Cihai


def variant_list(unihan, field):
    for char in unihan.with_fields(field):
        print("Character: {}".format(char.char))
        for var in char.untagged_vars(field):
            print(var)


def script(unihan_options={}):
    """Wrapped so we can test in tests/test_examples.py"""
    print("This example prints variant character data.")

    c = Cihai()
    c.add_dataset('cihai.unihan.Unihan', namespace='unihan')
    if not c.sql.is_bootstrapped:  # download and install Unihan to db
        bootstrap_unihan(c.sql.metadata, options=unihan_options)
        c.sql.reflect_db()  # automap new table created during bootstrap

    print("## ZVariants")
    variant_list(c.unihan, "kZVariant")

    print("## kSemanticVariant")
    variant_list(c.unihan, "kSemanticVariant")

    print("## kSpecializedSemanticVariant")
    variant_list(c.unihan, "kSpecializedSemanticVariant")


if __name__ == '__main__':
    script()
