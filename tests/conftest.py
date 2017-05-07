# -*- coding: utf-8 -*-
import os

import pytest

from cihai.core import Cihai


@pytest.fixture
def test_config_file():
    return os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        'fixtures',
        'test_config.yml'
    ))


@pytest.fixture
def cihai_obj(test_config_file):
    return Cihai.from_file(test_config_file)
