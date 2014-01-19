#!/usr/bin/env python
# -*- coding: utf8 - *-
"""Cihai dataset for `Unihan`_, Han Unification from Unicode, Inc.

cihai.datasets.unihan
~~~~~~~~~~~~~~~~~~~~~

todo: install manifest for installing files remotely via pip-type of URL.
        git+, hg+, svn+, http://
todo: extract files if from zip/tar.gz

:function:`~.download()` - Download data file from source.
:function:`~.convert()` - Source files into tabular, relational friendly csv.
:function:`~.install()` - Install
:function:`~.check_install()` -

"""

from __future__ import absolute_import, division, print_function, \
    with_statement, unicode_literals

from .unihan import Unihan, check_install, create_table, flatten_datasets
from .scripts import save, download, extract, convert
