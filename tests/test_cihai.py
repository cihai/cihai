# -*- coding: utf-8 -*-
"""Tests for cihai.

Test :class:`Cihai` object. Other tests will use an instance of ``Cihai``
using the ``test_config.yml``.

"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import os

import cihai
from cihai.core import Cihai, Storage, dirs, expand_config


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


def test_yaml_config_and_override(test_config_file):
    cihai = Cihai.from_cli(['-c', test_config_file])

    assert cihai.config['debug']


def test_data_path_default():

    expected = os.path.abspath(os.path.join(
        os.path.dirname(cihai.__file__),
        'data/'
    ))

    c = Cihai.from_file()
    result = c.config['data_path']

    assert expected == result


def test_expand_config_xdg_vars():
    initial_dict = {
        'dirs': {
            'cache': '{user_cache_dir}',
            'data': '{user_cache_dir}/data'
        }
    }

    expected_dict = {
        'dirs': {
            'cache': dirs.user_cache_dir,
            'data': os.path.join(dirs.user_cache_dir, 'data')
        }
    }

    expand_config(initial_dict)
    assert initial_dict == expected_dict


def test_expand_config_user_vars():
    initial_dict = {
        'dirs': {
            'cache': '~',
        }
    }

    expected_dict = {
        'dirs': {
            'cache': os.path.expanduser('~'),
        }
    }

    expand_config(initial_dict)
    assert initial_dict == expected_dict


def test_expand_config_env_vars(tmpdir, monkeypatch):
    monkeypatch.setenv('MYDIR', str(tmpdir))
    initial_dict = {
        'dirs': {
            'cache': '${MYDIR}',
        }
    }

    expected_dict = {
        'dirs': {
            'cache': os.environ.get('MYDIR'),
        }
    }

    expand_config(initial_dict)
    assert initial_dict == expected_dict
