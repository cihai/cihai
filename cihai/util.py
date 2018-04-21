# -*- coding: utf8 - *-
"""
Utility and helper methods for cihai.
"""
from __future__ import absolute_import, print_function, unicode_literals

import collections
import sys


def merge_dict(base, additional):
    """
    Combine two dictionary-like objects.

    Notes
    -----
    Code from https://github.com/pypa/warehouse
    Copyright 2013 Donald Stufft

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    """
    if base is None:
        return additional

    if additional is None:
        return base

    if not (isinstance(base, collections.Mapping)
            and isinstance(additional, collections.Mapping)):
        return additional

    merged = base
    for key, value in additional.items():
        if isinstance(value, collections.Mapping):
            merged[key] = merge_dict(merged.get(key), value)
        else:
            merged[key] = value

    return merged


def supports_wide():
    """Return affirmative if python interpreter supports wide characters.

    Returns
    -------
    bool :
        True if python supports wide character sets
    """
    return sys.maxunicode > 0xffff
