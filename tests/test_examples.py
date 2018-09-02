# -*- coding: utf8 - *-
from __future__ import absolute_import, print_function, unicode_literals

import examples.basic_usage
import examples.variant_ts_difficulties
import examples.variants


def test_variants(unihan_options):
    examples.variants.run(unihan_options=unihan_options)


def test_ts_difficulties(unihan_options):
    examples.variant_ts_difficulties.run(unihan_options=unihan_options)


def test_basic_usage(unihan_options):
    examples.basic_usage.run(unihan_options=unihan_options)
