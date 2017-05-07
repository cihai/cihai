# -*- coding: utf-8 -*-
"""Tests for cihai.

test.cihai
~~~~~~~~~~

Test :class:`Cihai` object. Other tests will use an instance of ``Cihai``
using the ``test_config.yml``.

"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import os

import cihai
import pytest
from cihai.core import Cihai, Storage


@pytest.fixture
def cihai_obj():
    config_file = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'test_config.yml'
    ))
    return Cihai.from_file(config_file)


class MyDataset(Storage):
    pass


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


def test_config_loads_module():
    from cihai.datasets import unihan  # NOQA

    cihai = Cihai({
        'datasets': ['cihai.datasets.unihan']
    })

    assert unihan in cihai.models


def test_yaml_config_and_override():
    config = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
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


def test_data_path_by_config_custom():
    """Test default data_path from config."""
    expected = '/home/r00t'

    cihai = Cihai({
        'data_path': expected
    })

    mydataset = cihai.add_dataset(MyDataset)

    result = mydataset.get_datapath('data_path')
    assert expected in result


def test_cihai_database_uses_same_metadata(cihai_obj):
    """Storage subclasses uses the same MetaData instance."""

    c = cihai_obj
    mydataset = c.add_dataset(MyDataset)
    assert mydataset.metadata == cihai_obj.metadata


def test_has_application_custom_config():

    expected = '/home/r00t'

    cihai = Cihai({
        'data_path': expected
    })

    mydataset = cihai.add_dataset(MyDataset)

    result = mydataset.cihai.config['data_path']
    assert expected == result
