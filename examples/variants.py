#!/usr/bin/env python
# -*- coding: utf8 - *-

from __future__ import print_function, unicode_literals

from cihai.bootstrap import bootstrap_unihan
from cihai.core import Cihai

c = Cihai()
if not c.is_bootstrapped:  # download and install Unihan to db
    bootstrap_unihan(c.metadata)
    c.reflect_db()  # automap new table created during bootstrap


print("This example prints variant character data.")


def variant_list(field):
    for char in c.with_fields(field):
        print("Character: {}".format(char.char))
        for var in char.untagged_vars(field):
            print(var)


print("## ZVariants")
variant_list("kZVariant")

print("## kSemanticVariant")
variant_list("kSemanticVariant")

print("## kSpecializedSemanticVariant")
variant_list("kSpecializedSemanticVariant")
