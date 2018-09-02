#!/usr/bin/env python
# -*- coding: utf8 - *-

from __future__ import print_function, unicode_literals

from cihai.bootstrap import bootstrap_unihan
from cihai.core import Cihai

c = Cihai()
if not c.is_bootstrapped:  # download and install Unihan to db
    bootstrap_unihan(c.metadata)
    c.reflect_db()  # automap new table created during bootstrap


print(
    "This example prints some tricky cases of character-by-character "
    "Traditional-Simplified mapping."
)
print("https://www.unicode.org/reports/tr38/#N10211")
print("3.7.1 bullet 4")


for char in c.with_fields("kTraditionalVariant", "kSimplifiedVariant"):
    print("Character: {}".format(char.char))
    trad = set(char.untagged_vars("kTraditionalVariant"))
    simp = set(char.untagged_vars("kSimplifiedVariant"))
    if c.char in trad and c.char in simp:
        print("Case 1")
    else:
        print("Case 2 (non-idempotent)")
    for trad_var in trad:
        print("s2t: {}".format(trad_var))
    for simp_var in simp:
        print("t2s: {}".format(simp_var))
