#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""China fit in to a python package.

cihai
~~~~~

:copyright: Copyright 2013 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

__version__ = '0.0.1'

from . import log, util, conversion

from .cihai import Cihai, CihaiDatabase
