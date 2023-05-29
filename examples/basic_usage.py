#!/usr/bin/env python
import typing as t

from cihai.core import Cihai


def run(unihan_options: t.Optional[t.Dict[str, object]] = None) -> None:
    if unihan_options is None:
        unihan_options = {}
    c = Cihai()

    if not c.unihan.is_bootstrapped:  # download and install Unihan to db
        c.unihan.bootstrap(unihan_options)

    query = c.unihan.lookup_char("好")
    glyph = query.first()

    assert glyph is not None
    print("lookup for 好: %s" % glyph.kDefinition)

    query = c.unihan.reverse_char("good")
    print('matches for "good": %s ' % ", ".join([glph.char for glph in query]))


if __name__ == "__main__":
    run()
