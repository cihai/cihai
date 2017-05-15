# -*- coding: utf-8 -*-
"""Tests for cihai.

Test :class:`Cihai` object. Other tests will use an instance of ``Cihai``
using the ``test_config.yml``.

"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

from cihai import bootstrap
from cihai.core import Cihai


def test_config_defaults():
    """Test config defaults."""

    app = Cihai()

    assert 'debug' in app.config
    assert not app.config['debug']


def test_config_dict_args():
    """Accepts dict as config."""

    expected = 'world'

    app = Cihai({
        'hello': expected
    })

    result = app.config['hello']

    assert result == expected


def test_yaml_config_and_override(test_config_file):
    app = Cihai.from_cli(['-c', test_config_file])

    assert app.config['debug']


def test_unihan_options(unihan_options, test_config_file):
    app = Cihai.from_cli(['-c', test_config_file])
    bootstrap.bootstrap_unihan(app.metadata, unihan_options)
    assert 'Unihan' in app.metadata.tables
    assert app.metadata.tables['Unihan'].columns
    assert set(app.metadata.tables['Unihan'].columns.keys()) == \
        set(bootstrap.UNIHAN_FIELDS + ['ucn', 'char'])
    assert bootstrap.is_bootstrapped(app.metadata)
