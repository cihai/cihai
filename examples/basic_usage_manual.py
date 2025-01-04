#!/usr/bin/env python
"""Demonstrate what basic_usage's unihan=True (default Cihai) does under the hood."""

from __future__ import annotations

import logging

from cihai.core import Cihai

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def run(unihan_options: dict[str, object] | None = None) -> None:
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
    log.info(f"lookup for 㐭: {glyph.kDefinition}")

    query = c.unihan.reverse_char("granary")
    log.info(
        'matches for "granary": {} '.format(", ".join([glph.char for glph in query])),
    )


if __name__ == "__main__":
    run()
