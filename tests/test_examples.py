# -*- coding: utf8 - *-
from __future__ import absolute_import, print_function, unicode_literals

import examples.variants


def test_examples(unihan_options):
    examples.variants.script(unihan_options=unihan_options)
