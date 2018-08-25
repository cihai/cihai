# -*- coding: utf-8 -*-

import pytest

from cihai import exc


def test_base_exception():
    with pytest.raises(
        exc.CihaiException,
        message="Make sure no one removes or renames base CihaiException",
    ):
        raise exc.CihaiException()

    with pytest.raises(Exception, message="Extends python base exception"):
        raise exc.CihaiException()
