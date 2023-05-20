import pytest

from cihai import exc


def test_base_exception() -> None:
    with pytest.raises(exc.CihaiException):
        raise exc.CihaiException()  # Make sure its base of CihaiException

    with pytest.raises(Exception, match=""):
        raise exc.CihaiException()  # Extends python base exception
