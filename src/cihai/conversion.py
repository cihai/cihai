# flake8: noqa: E501
"""Conversion functions for various CJK encodings and representations.

Notes
-----
Original methods and docs based upon `ltchinese`_, license `MIT`_ Steven
Kryskalla.

.. versionadded:: 0.1
    Python 2/3 compatibility.

    - PEP8, PEP257.
    - ``int()`` casting for comparisons
    - Python 3 support.
    - Python 3 fix for :meth:`~.ucn_to_python`.
    - Python 3 ``__future__`` statements.
    - All methods converting to ``_python`` will return ``Unicode``.
    - All methods converting Unicode to x will return bytestring.
    - Add :meth:`~.ucnstring_to_python`
    - Any other change upon @ `conversion.py @9227813`_.

The following terms are used to represent the encodings / representation used
in the conversion functions (the samples on the right are for the character
U+4E00 (yi1; "one")):

========================== ====================================================
GB2312 (Kuten/Quwei form)  "5027" [used in the "GB2312" field of Unihan.txt]
GB2312 (ISO-2022 form)     "523B" [the "internal representation" of GB code]
EUC-CN                     "D2BB" [this is the "external encoding" of GB2312-
                                    ISO2022's "internal representation"; also
                                    the form that Ocrat uses]
UTF-8                      "E4 B8 80" [used in the "UTF-8" field in Unihan.txt]
-------------------------- ----------------------------------------------------
Unihan UCN                 "U+4E00"   [used by Unicode Inc.]
-------------------------- ----------------------------------------------------
internal Python unicode    u"\u4e00"  [this is the most useful form!]
internal Python 'utf8'     "\\xe4\\xb8\\x80"
internal Python 'gb2312'   "\\xd2\\xbb"
internal Python 'euc-cn'   "\\xd2\\xbb"
internal Python 'gb18030'  "\\xd2\\xbb"
========================== ====================================================

See these resources for more information:
 * Wikipedia "Extended_Unix_Code" article

   * "EUC-CN is the usual way to use the GB2312 standard for simplified Chinese
     characters ... the ISO-2022 form of GB2312 is not normally used"

 * Wikipedia "HZ_(encoding)" article (the example conversion)

 * Wikipedia "Numeric_character_reference" article

 * Unihan (look for "Encoding forms", "Mappings to Major Standards")

   * e.g. http://www.unicode.org/cgi-bin/GetUnihanData.pl?codepoint=4E00

.. _ltchinese: https://bitbucket.org/lost_theory/ltchinese
.. _MIT: https://bitbucket.org/lost_theory/ltchinese/src/9227813/LICENSE.txt
.. _conversion.py @9227813: https://bitbucket.org/lost_theory/ltchinese/raw/9227813/ltchinese/conversion.py
"""
import logging
import re
import typing as t

if t.TYPE_CHECKING:
    from typing_extensions import TypeAlias

log = logging.getLogger(__name__)


def hexd(n: int) -> str:
    """Return hex digits (strip '0x' at the beginning)."""
    return hex(n)[2:]


def kuten_to_gb2312(kuten: str) -> bytes:
    """
    Convert GB kuten / quwei form (94 zones * 94 points) to GB2312-1980 /
    ISO-2022-CN hex (internal representation)
    """
    zone, point = int(kuten[:2]), int(kuten[2:])
    hi, lo = hexd(zone + 0x20), hexd(point + 0x20)

    gb2312 = f"{hi}{lo}"

    assert isinstance(gb2312, bytes)
    return gb2312


def gb2312_to_euc(gb2312hex: str) -> bytes:
    """
    Convert GB2312-1980 hex (internal representation) to EUC-CN hex (the
    "external encoding")
    """
    hi_int, lo_int = int(gb2312hex[:2], 16), int(gb2312hex[2:], 16)
    hi, lo = hexd(hi_int + 0x80), hexd(lo_int + 0x80)

    euc = f"{hi}{lo}"
    assert isinstance(euc, bytes)
    return euc


def euc_to_python(hexstr: bytes) -> str:
    """Convert a EUC-CN (GB2312) hex to a Python unicode string."""
    hi = hexstr[0:2]
    lo = hexstr[2:4]
    gb_enc = b"\\x" + hi + b"\\x" + lo
    return gb_enc.decode("gb2312")


def euc_to_utf8(euchex: bytes) -> str:
    """Convert EUC hex (e.g. "d2bb") to UTF8 hex (e.g. "e4 b8 80")."""
    utf8 = euc_to_python(euchex).encode("utf-8")
    uf8 = utf8.decode("unicode_escape")

    uf8_bytes = uf8.encode("latin1")

    uf8 = uf8_bytes.decode("euc-jp")
    return uf8


def ucn_to_unicode(ucn: str) -> str:
    """
    Convert a Unicode Universal Character Number (e.g. "U+4E00" or "4E00") to
    Python unicode (u'\\u4e00')
    """
    if isinstance(ucn, str):
        ucn = ucn.strip("U+")
        if len(ucn) > int(4):
            char_bytes = b"\\U" + format(int(ucn, 16), "08x").encode("latin1")
            char = char_bytes.decode("unicode_escape")
        else:
            char = chr(int(ucn, 16))
    else:
        char = chr(ucn)

    assert isinstance(char, str)

    return char


def euc_to_unicode(hexstr: bytes) -> str:
    r"""
    Return EUC-CN (GB2312) hex to a Python unicode.

    Parameters
    ----------
    hexstr : bytes

    Returns
    -------
    unicode :
        Python unicode  e.g. ``u'\\u4e00'`` / '一'.

    Examples
    --------

    >>> u'\u4e00'.encode('gb2312').decode('utf-8')
    '\u04bb'

    >>> (b'\\x' + b'd2' + b'\\x' + b'bb').replace('\\x', '') \  # doctest: +SKIP
    ... .decode('hex').decode('utf-8')
    u'\u04bb'

    Note: bytes don't have a ``.replace``:

    >>> gb_enc = gb_enc.replace('\\x', '').decode('hex')  # doctest: +SKIP
    >>> gb_enc.decode('string_escape')  # Won't work with Python 3.x.  # doctest: +SKIP
    """
    hi = hexstr[0:2]
    lo = hexstr[2:4]
    # hi and lo are only 2 characters long, no risk with eval-ing them

    gb_enc = b"\\x" + hi + b"\\x" + lo
    assert isinstance(gb_enc, bytes)

    # Requires coercing back to str in 2.7
    gb_enc_uni_escape = gb_enc.decode("unicode_escape")

    gb_enc_bytes = gb_enc_uni_escape.encode("latin1")

    gb_enc_str = gb_enc_bytes.decode("gb2312")

    assert isinstance(gb_enc_str, str)
    return gb_enc_str


""" Convert from internal Python unicode / string objects """


@t.overload
def python_to_ucn(uni_char: str, as_bytes: t.Literal[True]) -> bytes:
    ...


@t.overload
def python_to_ucn(uni_char: str, as_bytes: t.Literal[False]) -> str:
    ...


@t.overload
def python_to_ucn(uni_char: str, as_bytes: t.Literal[False] = False) -> str:
    ...


def python_to_ucn(uni_char: str, as_bytes: bool = False) -> t.Union[bytes, str]:
    """
    Return UCN character from Python Unicode character.

    Converts a one character Python unicode string (e.g. u'\\u4e00') to the
    corresponding Unicode UCN ('U+4E00').
    """
    ucn = uni_char.encode("unicode_escape").decode("latin1")
    ucn = str(ucn).replace("\\", "").upper().lstrip("U")
    if len(ucn) > int(4):
        # get rid of the zeroes that Python uses to pad 32 byte UCNs
        ucn = ucn.lstrip("0")
    ucn = "U+" + ucn.upper()

    if as_bytes:
        return ucn.encode("latin1")

    return ucn


def python_to_euc(uni_char: str, as_bytes: bool = False) -> t.Union[bytes, str]:
    """
    Return EUC character from a Python Unicode character.

    Converts a one character Python unicode string (e.g. u'\\u4e00') to the
    corresponding EUC hex ('d2bb').
    """
    euc = repr(uni_char.encode("gb2312"))[1:-1].replace("\\x", "").strip("'")

    if as_bytes:
        return euc.encode("utf-8")

    return euc


def ucnstring_to_unicode(ucn_string: str) -> str:
    """Return ucnstring as Unicode."""
    ucn_string = ucnstring_to_python(ucn_string).decode("utf-8")

    assert isinstance(ucn_string, str)
    return ucn_string


def ucnstring_to_python(ucn_string: str) -> bytes:
    """
    Return string with Unicode UCN (e.g. "U+4E00") to native Python Unicode
    (u'\\u4e00').
    """
    res = re.findall(r"U\+[0-9a-fA-F]*", ucn_string)
    for r in res:
        ucn_string = ucn_string.replace(str(r), str(ucn_to_unicode(r)))

    ucn_bytestr = ucn_string.encode("utf-8")

    assert isinstance(ucn_bytestr, bytes)
    return ucn_bytestr


ParsedVar: "TypeAlias" = t.Tuple[str, t.Optional[str]]


def parse_var(var: str) -> ParsedVar:
    """
    Returns a tuple consisting of a string and a tag, or None, if none is
    specified.
    """
    bits = var.split("<", 1)
    tag = None if len(bits) < 2 else bits[1]
    return ucn_to_unicode(bits[0]), tag


ParsedVars: "TypeAlias" = t.Iterator[ParsedVar]


def parse_vars(_vars: str) -> t.Generator[ParsedVar, str, None]:
    """
    Return an iterator of (char, tag) tuples.
    """
    for var in _vars.split(" "):
        yield parse_var(var)


UntaggedVars: "TypeAlias" = t.Iterator[t.Any]


def parse_untagged(_vars: str) -> UntaggedVars:
    """
    Return an iterator of chars.
    """
    return (char for char, _tag in parse_vars(_vars))
