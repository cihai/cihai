# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import logging

from cihai import util

log = logging.getLogger(__name__)


def test_merge_dict():
    dict1 = {
        'hi world': 1,
        'innerdict': {
            'hey': 1
        }
    }
    dict2 = {
        'innerdict': {
            'welcome': 2
        }
    }

    expected = {
        'hi world': 1,
        'innerdict': {
            'hey': 1,
            'welcome': 2
        }
    }

    assert util.merge_dict(dict1, dict2) == expected
