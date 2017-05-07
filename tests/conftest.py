# -*- coding: utf-8 -*-
import os

import pytest

from cihai.core import Cihai


@pytest.fixture
def cihai_obj():
    config_file = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'test_config.yml'
    ))
    return Cihai.from_file(config_file)
