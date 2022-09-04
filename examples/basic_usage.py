#!/usr/bin/env python
from cihai.core import Cihai


def run(unihan_options=None):
    c = Cihai()

    if not c.unihan.is_bootstrapped:  # download and install Unihan to db
        c.unihan.bootstrap(unihan_options)

    query = c.unihan.lookup_char("好")
    glyph = query.first()
    print("lookup for 好: %s" % glyph.kDefinition)

    query = c.unihan.reverse_char("good")
    print('matches for "good": %s ' % ", ".join([glph.char for glph in query]))


if __name__ == "__main__":
    run()
