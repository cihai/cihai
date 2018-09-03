# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from cihai import utils


def test_merge_dict():
    dict1 = {'hi world': 1, 'innerdict': {'hey': 1}}
    dict2 = {'innerdict': {'welcome': 2}}

    expected = {'hi world': 1, 'innerdict': {'hey': 1, 'welcome': 2}}

    assert utils.merge_dict(dict1, dict2) == expected
