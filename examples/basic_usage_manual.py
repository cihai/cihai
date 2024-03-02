#!/usr/bin/env python
"""Demonstrate what basic_usage's unihan=True (default Cihai) does under the hood."""

import typing as t

from cihai.core import Cihai


def run(unihan_options: t.Optional[t.Dict[str, object]] = None) -> None:
    """Demonstrate cihai usage using explicit UNIHAN lookups."""
    if unihan_options is None:
        unihan_options = {}

    c = Cihai(unihan=False)
    c.add_dataset("cihai.data.unihan.dataset.Unihan", namespace="unihan")

    if not c.unihan.is_bootstrapped:  # download and install Unihan to db
        c.unihan.bootstrap(unihan_options)

    query = c.unihan.lookup_char("㐭")
    glyph = query.first()
    assert glyph is not None
    print("lookup for 㐭: %s" % glyph.kDefinition)

    query = c.unihan.reverse_char("granary")
    print('matches for "granary": %s ' % ", ".join([glph.char for glph in query]))


if __name__ == "__main__":
    run()
