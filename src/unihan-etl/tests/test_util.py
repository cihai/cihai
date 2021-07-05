from unihan_etl._compat import text_type
from unihan_etl.util import ucn_to_unicode, ucnstring_to_unicode


def test_conversion_ucn_to_unicode():
    before = 'U+4E00'
    expected = '\u4e00'

    result = ucn_to_unicode(before)

    assert result == expected

    assert isinstance(result, text_type)

    # wide character
    before = 'U+20001'
    expected = '\U00020001'

    result = ucn_to_unicode(before)

    assert result == expected
    assert isinstance(result, text_type)

    before = '(same as U+7A69 穩) firm; stable; secure'
    expected = '(same as 穩 穩) firm; stable; secure'

    result = ucnstring_to_unicode(before)

    assert result == expected
    assert isinstance(result, text_type)
