# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import logging

import pytest
from cihai import util
from cihai._compat import StringIO

log = logging.getLogger(__name__)


def test_dl_progress():
    out = StringIO()

    util._dl_progress(20, 10, 1000, out=out)

    result = out.getvalue().strip()
    expected = '20% [==========>                                        ]'

    assert result == expected


def test_import_string():
    # Borrows from werkzeug.testsuite.
    import cgi
    import cihai

    assert util.import_string('cgi.escape') == cgi.escape
    assert util.import_string(u'cgi.escape') == cgi.escape
    assert util.import_string('cgi:escape') == cgi.escape
    assert util.import_string('XXXXXXXXXXXX', True) is None
    assert util.import_string('cgi.XXXXXXXXXXXX', True) is None

    assert util.import_string('cihai.core.Cihai') == cihai.core.Cihai
    assert util.import_string('cihai.core:Cihai') == cihai.core.Cihai
    assert util.import_string('cihai') == cihai
    assert util.import_string('XXXXX', True) is None
    assert util.import_string('cihia.XXXXX', True) is None

    pytest.raises(ImportError, util.import_string, 'XXXXXXXXXXXXXXXX')
    pytest.raises(ImportError, util.import_string, 'cgi.XXXXXXXXXX')


def test_find_modules():
    assert list(
        util.find_modules('cihai.datasets', include_packages=True)
    ), ['cihai.datasets.decomp', 'cihai.datasets.unihan']
