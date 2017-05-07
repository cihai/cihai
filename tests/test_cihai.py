# -*- coding: utf-8 -*-
"""Tests for cihai.

Test :class:`Cihai` object. Other tests will use an instance of ``Cihai``
using the ``test_config.yml``.

"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import os

import cihai
from cihai.core import Cihai, Storage


def test_config_defaults():
    """Test config defaults."""

    cihai = Cihai.from_file()

    assert 'debug' in cihai.config
    assert not cihai.config['debug']


def test_config_dict_args():
    """Accepts dict as config."""

    expected = 'world'

    cihai = Cihai({
        'hello': expected
    })

    result = cihai.config['hello']

    assert result == expected


def test_yaml_config_and_override():
    config = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        'fixtures',
        'test_config.yml'
    ))

    cihai = Cihai.from_cli(['-c', config])

    assert cihai.config['debug']


def test_data_path_default():

    expected = os.path.abspath(os.path.join(
        os.path.dirname(cihai.__file__),
        'data/'
    ))

    c = Cihai.from_file()
    result = c.config['data_path']

    assert expected == result
