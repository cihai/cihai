#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""China fit in to a python package.

cihai
~~~~~

:copyright: Copyright 2013-2014 Tony Narlock.
:license: BSD, see LICENSE for details

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

__title__ = 'cihai'
__version__ = '0.0.1'
__author__ = 'Tony Narlock'
__license__ = 'BSD 3-clause'
__copyright__ = 'Copyright 2013-2014 Tony Narlock'

from . import log, util, conversion

from .cihai import Cihai, CihaiDatabase
