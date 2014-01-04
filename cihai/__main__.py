# -*- coding: utf8 - *-
"""For accessing cihai as a package.

"""

import sys
import os


def run():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, base)
    from cihai import Cihai

    return Cihai.from_cli(sys.argv[1:])

if __name__ == '__main__':
    exit = run()
    if exit:
        sys.exit(exit)
