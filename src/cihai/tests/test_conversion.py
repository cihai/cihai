"""Tests for cihai.

test.conversion
~~~~~~~~~~~~~~~

"""
from cihai import conversion
from cihai._compat import string_types, text_type


def test_text_type():
    c1 = '(same as U+7A69 穩) firm; stable; secure'
    c2 = text_type()

    assert isinstance(c1, string_types)
    assert isinstance(c2, text_type)


"""Return UCN character from Python Unicode character.

Converts a one character Python unicode string (e.g. u'\\u4e00') to the
corresponding Unicode UCN ('U+4E00').

U+369D	kSemanticVariant	U+595E<kMatthews U+594E<kMatthews
U+3CE2	kTraditionalVariant	U+23FB7
U+3FF7	kSemanticVariant	U+7CD9<kMatthews,kMeyerWempe
U+345A	kDefinition	(non-classical form of 那) that, there
U+349A	kDefinition	(same as U+7A69 穩) firm; stable; secure,
        dependent upon others
U+34B5	kMandarin	mào
U+356D	kCantonese	au3 jaau1
"""


def test_ucn_from_unicode():
    text = '一'
    python_unicode = u'\u4e00'

    expected = "U+4E00"
    bytes_expected = b"U+4E00"

    assert conversion.python_to_ucn(python_unicode) == expected
    assert isinstance(conversion.python_to_ucn(python_unicode), text_type)
    assert isinstance(conversion.python_to_ucn(python_unicode, as_bytes=True), bytes)

    assert conversion.python_to_ucn(text, as_bytes=True) == bytes_expected


def test_ucn_from_unicode_16():
    text = '𦄀'
    python_unicode = u'\u26100'

    expected = "U+26100"
    bytes_expected = b"U+26100"

    assert conversion.python_to_ucn(python_unicode) == expected
    assert isinstance(conversion.python_to_ucn(python_unicode), text_type)
    assert isinstance(conversion.python_to_ucn(python_unicode, as_bytes=True), bytes)

    assert conversion.python_to_ucn(text, as_bytes=True) == bytes_expected


def test_ucn_to_unicode():
    before = 'U+4E00'
    expected = '\u4e00'

    result = conversion.ucn_to_unicode(before)

    assert result == expected

    assert isinstance(result, text_type)

    # wide character
    before = 'U+20001'
    expected = '\U00020001'

    result = conversion.ucn_to_unicode(before)

    assert result == expected
    assert isinstance(result, text_type)

    before = '(same as U+7A69 穩) firm; stable; secure'
    expected = '(same as 穩 穩) firm; stable; secure'

    result = conversion.ucnstring_to_unicode(before)

    assert result == expected
    assert isinstance(result, text_type)


"""Return EUC character from a Python Unicode character.

    Converts a one character Python unicode string (e.g. u'\\u4e00') to the
    corresponding EUC hex ('d2bb').

"""


def test_hexd():
    assert conversion.hexd(0xFFFF) == 'ffff'


def test_euc_from_unicode():
    expected = '一'  # u'\u4e00'
    euc_bytestring = b'd2bb'
    euc_unicode = 'd2bb'

    result = conversion.python_to_euc(expected, as_bytes=True)

    assert euc_bytestring == result
    assert isinstance(result, bytes)

    result = conversion.python_to_euc(expected)

    assert euc_unicode == result
    assert isinstance(result, text_type)


def test_euc_to_utf8():
    expected = '一'
    euc_bytestring = b'b0ec'

    result = conversion.euc_to_utf8(euc_bytestring)

    assert expected == result


def test_euc_to_unicode():
    expected = '一'
    expected_ustring = u'\u4e00'
    euc_bytestring = b'd2bb'

    result = conversion.euc_to_unicode(euc_bytestring)

    assert expected == expected_ustring
    assert isinstance(result, text_type)

    assert expected == result
    assert expected_ustring == result
