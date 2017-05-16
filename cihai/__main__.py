#!/usr/bin/env python
# -*- coding: utf8 - *-
"""For accessing cihai as a package."""

import sys
import os


def run():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, base)
    from .core import Cihai

    app = Cihai.from_cli(sys.argv[1:])
    if not app.is_bootstrapped:
        from .bootstrap import bootstrap_unihan
        bootstrap_unihan(app.metadata)


if __name__ == '__main__':
    sys.exit(run())
