#!/usr/bin/env python
# -*- coding: utf8 - *-

from __future__ import print_function, unicode_literals

from cihai.bootstrap import bootstrap_unihan
from cihai.core import Cihai

c = Cihai()
if not c.is_bootstrapped:  # download and install Unihan to db
    bootstrap_unihan(c.metadata)
    c.reflect_db()         # automap new table created during bootstrap

query = c.lookup_char('好')
glyph = query.first()
print("lookup for 好: %s" % glyph.kDefinition)

query = c.reverse_char('good')
print('matches for "good": %s ' % ', '.join([glph.char for glph in query]))
