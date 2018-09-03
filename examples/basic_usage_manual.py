#!/usr/bin/env python
# -*- coding: utf8 - *-
"""
Demonstrate what basic_usage's unihan=True (default Cihai) does under
the hood.
"""
from __future__ import print_function, unicode_literals

from cihai.core import Cihai
from cihai.data.unihan.bootstrap import bootstrap_unihan


def run(unihan_options={}):
    c = Cihai(unihan=False)
    c.add_dataset('cihai.data.unihan.dataset.Unihan', namespace='unihan')

    if not c.sql.is_bootstrapped:  # download and install Unihan to db
        bootstrap_unihan(c.sql.metadata, options=unihan_options)
        c.sql.reflect_db()  # automap new table created during bootstrap

    query = c.unihan.lookup_char('好')
    glyph = query.first()
    print("lookup for 好: %s" % glyph.kDefinition)

    query = c.unihan.reverse_char('good')
    print('matches for "good": %s ' % ', '.join([glph.char for glph in query]))


if __name__ == '__main__':
    run()
