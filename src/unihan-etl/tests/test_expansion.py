"""Test expansion of multi-value fields in UNIHAN."""
import pytest

from unihan_etl import constants, expansion


def test_expands_spaces(expanded_data):
    for item in expanded_data:
        for field in item.keys():
            if field in constants.SPACE_DELIMITED_LIST_FIELDS and item[field]:
                assert isinstance(item[field], list)


def test_expand_kCantonese(expanded_data):
    # test kCantonese
    item = [i for i in expanded_data if i['ucn'] == 'U+342B'][0]
    if item['ucn'] == 'U+342B':
        assert set(item['kCantonese']) == set(['gun3', 'hung1', 'zung1'])
    else:
        assert False, "Missing field U+342B kCantonese"


@pytest.mark.parametrize(
    "ucn,field,expected",
    [
        ("U+37AE", "kJapaneseKun", ['DERU', 'DASU']),
        ("U+37AE", "kJapaneseOn", ['SHUTSU', 'SUI']),
        (
            "U+37AE",
            "kDefinition",
            ['variant of 出 U+51FA, to go out, send out', 'to stand', 'to produce'],
        ),
    ],
)
def test_expand(expanded_data, ucn, field, expected):
    # test kDefinition (split on ;), kJapanese, kJapaneseKun
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert set(item[field]) == set(expected)


@pytest.mark.parametrize(
    "ucn,expected",
    [
        ("U+346E", {"zh-Hans": "hún", "zh-Hant": "hún"}),  # U+346E	kMandarin	hún
        ("U+4FFE", {"zh-Hans": "bǐ", "zh-Hant": "bì"}),  # U+4FFE	kMandarin	bǐ bì
    ],
)
def test_expand_kMandarin(expanded_data, ucn, expected):
    """
    The most customary pinyin reading for this character. When there are two
    values, then the first is preferred for zh-Hans (CN) and the second is
    preferred for zh-Hant (TW). When there is only one value, it is appropriate
    for both.
    """
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kMandarin'] == expected


@pytest.mark.parametrize(
    "ucn,expected",
    [
        ("U+8303", {"zh-Hans": 8, "zh-Hant": 9}),  # U+8303	kTotalStrokes	8 9
        ("U+34D6", {"zh-Hans": 13, "zh-Hant": 13}),  # U+34D6	kTotalStrokes	13
    ],
)
def test_expand_kTotalStrokes(expanded_data, ucn, expected):
    """
    The total number of strokes in the character (including the radical). When
    there are two values, then the first is preferred for zh-Hans (CN) and the
    second is preferred for zh-Hant (TW). When there is only one value, it is
    appropriate for both.
    """
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kTotalStrokes'] == expected


@pytest.mark.parametrize(
    "ucn,expected",
    [
        # U+34AD      kIRGHanyuDaZidian       10273.120
        ("U+34AD", [{"volume": 1, "page": 273, "character": 12, "virtual": 0}]),
        # U+34AF      kIRGHanyuDaZidian       10275.091
        ("U+34AF", [{"volume": 1, "page": 275, "character": 9, "virtual": 1}]),
    ],
)
def test_expand_kIRGHanyuDaZidian(ucn, expected, expanded_data):
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kIRGHanyuDaZidian'] == expected


@pytest.mark.parametrize(
    "ucn,expected",
    [
        (
            "U+5EFE",
            [
                {  # U+5EFE	kHanyuPinyin	10513.110,10514.010,10514.020:gǒng
                    "locations": [
                        {"volume": 1, "page": 513, "character": 11, "virtual": 0},
                        {"volume": 1, "page": 514, "character": 1, "virtual": 0},
                        {"volume": 1, "page": 514, "character": 2, "virtual": 0},
                    ],
                    "readings": ["gǒng"],
                }
            ],
        ),
        (
            "U+5364",
            [
                {  # U+5364	kHanyuPinyin	10093.130:xī,lǔ 74609.020:lǔ,xī
                    "locations": [
                        {"volume": 1, "page": 93, "character": 13, "virtual": 0}
                    ],
                    "readings": ["xī", "lǔ"],
                },
                {
                    "locations": [
                        {"volume": 7, "page": 4609, "character": 2, "virtual": 0}
                    ],
                    "readings": ["lǔ", "xī"],
                },
            ],
        ),
        (
            "U+34D8",
            [
                {  # U+34D8	kHanyuPinyin	10278.080,10278.090:sù
                    "locations": [
                        {"volume": 1, "page": 278, "character": 8, "virtual": 0},
                        {"volume": 1, "page": 278, "character": 9, "virtual": 0},
                    ],
                    "readings": ["sù"],
                }
            ],
        ),
        (
            "U+34CE",
            [
                {  # U+34CE	kHanyuPinyin	10297.260:qīn,qìn,qǐn
                    "locations": [
                        {"volume": 1, "page": 297, "character": 26, "virtual": 0}
                    ],
                    "readings": ["qīn", "qìn", "qǐn"],
                }
            ],
        ),
    ],
)
def test_expand_kHanyuPinyin(expanded_data, ucn, expected):
    """
    Each location has the form “ABCDE.XYZ” (as in “kHanYu”); multiple
    locations for a given pīnyīn reading are separated by “,” (comma). The
    list of locations is followed by “:” (colon), followed by a
    comma-separated list of one or more pīnyīn readings. Where multiple
    pīnyīn readings are associated with a given mapping, these are ordered as
    in HDZ (for the most part reflecting relative commonality). The following
    are representative records.

    | U+34CE | 㓎 | 10297.260: qīn,qìn,qǐn |
    | U+34D8 | 㓘 | 10278.080,10278.090: sù |
    | U+5364 | 卤 | 10093.130: xī,lǔ 74609.020: lǔ,xī |
    | U+5EFE | 廾 | 10513.110,10514.010,10514.020: gǒng |

    For example, the “kHanyuPinyin” value for 卤 U+5364 is
    10093.130: xī,lǔ 74609.020: lǔ,xī”. This means that 卤 U+5364 is found in
    kHanYu” at entries 10093.130 and 74609.020. The former entry has the two
    pīnyīn readings xī and lǔ (in that order), whereas the latter entry has
    the readings lǔ and xī (reversing the order).
    """
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kHanyuPinyin'] == expected


@pytest.mark.parametrize(
    "ucn,expected",
    [
        (
            "U+9BF5",
            [
                {  # U+9BF5 kHanYu  74699.122
                    "volume": 7,
                    "page": 4699,
                    "character": 12,
                    "virtual": 2,
                }
            ],
        ),
        (
            "U+34B9",
            [
                {  # U+34B9	kHanYu	10254.060 10254.100
                    "volume": 1,
                    "page": 254,
                    "character": 6,
                    "virtual": 0,
                },
                {"volume": 1, "page": 254, "character": 10, "virtual": 0},
            ],
        ),
        (
            'U+34AD',
            [
                {  # U+34AD	kHanYu	10273.120
                    "volume": 1,
                    "page": 273,
                    "character": 12,
                    "virtual": 0,
                }
            ],
        ),
    ],
)
def test_expand_HanYu(expanded_data, ucn, expected):
    """
    The character references are given in the form “ABCDE.XYZ”, in which: “A”
    is the volume number [1..8]; “BCDE” is the zero-padded page number
    [0001..4809]; “XY” is the zero-padded number of the character on the page
    [01..32]; “Z” is “0” for a character actually in the dictionary, and
    greater than 0 for a character assigned a “virtual” position in the
    dictionary. For example, 53024.060 indicates an actual HDZ character, the
    6th character on Page 3,024 of Volume 5 (i.e. 籉 [U+7C49]). Note that the
    Volume 8 “BCDE” references are in the range [0008..0044] inclusive,
    referring to the pagination of the “Appendix of Addendum” at the end of
    that volume (beginning after p. 5746).

    The first character assigned a given virtual position has an index ending
    in 1; the second assigned the same virtual position has an index ending in
    2; and so on.
    """
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kHanYu'] == expected


@pytest.mark.parametrize(
    "ucn,expected",
    [
        # U+4E9D      kRSAdobe_Japan1_6       C+17245+7.2.6 C+17245+28.2.6
        (
            "U+4E9D",
            [
                {
                    "type": "C",
                    "cid": 17245,
                    "radical": 7,
                    "strokes": 2,
                    "strokes-residue": 6,
                },
                {
                    "type": "C",
                    "cid": 17245,
                    "radical": 28,
                    "strokes": 2,
                    "strokes-residue": 6,
                },
            ],
        ),
        # U+4E9E      kRSAdobe_Japan1_6       C+4108+7.2.6
        (
            "U+4E9E",
            [
                {
                    "type": "C",
                    "cid": 4108,
                    "radical": 7,
                    "strokes": 2,
                    "strokes-residue": 6,
                }
            ],
        ),
        # U+4E30      kRSAdobe_Japan1_6       C+14301+2.1.3 V+15386+2.1.3
        (
            "U+4E30",
            [
                {
                    "type": "C",
                    "cid": 14301,
                    "radical": 2,
                    "strokes": 1,
                    "strokes-residue": 3,
                },
                {
                    "type": "V",
                    "cid": 15386,
                    "radical": 2,
                    "strokes": 1,
                    "strokes-residue": 3,
                },
            ],
        ),
    ],
)
def test_expand_kRSAdobe_Japan1_6(expanded_data, ucn, expected):
    """
    The value consists of a number of space-separated entries. Each entry
    consists of three pieces of information separated by a plus sign:

    1) C or V. “C” indicates that the Unicode code point maps directly to the
    Adobe-Japan1-6 CID that appears after it, and “V” indicates that it is
    considered a variant form, and thus not directly encoded.

    2) The Adobe-Japan1-6 CID.

    3) Radical-stroke data for the indicated Adobe-Japan1-6 CID. The
    radical-stroke data consists of three pieces separated by periods: the
    KangXi radical (1-214), the number of strokes in the form the radical
    takes in the glyph, and the number of strokes in the residue. The standard
    Unicode radical-stroke form can be obtained by omitting the second value,
    and the total strokes in the glyph from adding the second and third
    values.
    """
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kRSAdobe_Japan1_6'] == expected


@pytest.mark.parametrize(
    "field,ucn,expected",
    [
        # U+4E55      kRSJapanese     4.6
        ('kRSJapanese', 'U+4E55', [{"radical": 4, "strokes": 6, "simplified": False}]),
        # U+4E99      kRSKangXi       7.4
        ('kRSKangXi', 'U+4E99', [{"radical": 7, "strokes": 4, "simplified": False}]),
        # U+4E9A      kRSKangXi       1.5
        ('kRSKangXi', 'U+4E9A', [{"radical": 1, "strokes": 5, "simplified": False}]),
        # U+4E54      kRSKanWa        37.3
        ('kRSKanWa', 'U+4E54', [{"radical": 37, "strokes": 3, "simplified": False}]),
        # U+4E55      kRSKanWa        4.6
        ('kRSKanWa', 'U+4E55', [{"radical": 4, "strokes": 6, "simplified": False}]),
        # U+5378      kRSKorean       26.7
        ('kRSKorean', 'U+5378', [{"radical": 26, "strokes": 7, "simplified": False}]),
    ],
)
def test_expand_radical_stroke_counts(expanded_data, field, ucn, expected):
    """kRSJapanese"""
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item[field] == expected


@pytest.mark.parametrize(
    "ucn,expected",
    [
        # U+3491      kRSUnicode      9.13
        ('U+3491', [{"radical": 9, "strokes": 13, "simplified": False}]),
        # U+4336       kRSUnicode      120'.3
        ('U+4336', [{"radical": 120, "strokes": 3, "simplified": True}]),
    ],
)
def test_expand_kRSUnihan(expanded_data, ucn, expected):
    """
    The standard radical/stroke count for this character in the form
    “radical.additional strokes”. The radical is indicated by a number in the
    range (1..214) inclusive. An apostrophe (') after the radical indicates a
    simplified version of the given radical. The “additional strokes” value is
    the residual stroke-count, the count of all strokes remaining after
    eliminating all strokes associated with the radical.
    """
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kRSUnicode'] == expected


@pytest.mark.parametrize(
    "ucn,expected",
    [
        # U+34BC      kCheungBauer    055/08;TLBO;mang4
        (
            'U+34BC',
            [{"radical": 55, "strokes": 8, "cangjie": "TLBO", "readings": ["mang4"]}],
        ),
        # U+356C  kCheungBauer    030/04;;gung1
        (
            'U+356C',
            [{"radical": 30, "strokes": 4, "cangjie": None, "readings": ["gung1"]}],
        ),
        # U+3598  kCheungBauer    030/07;RMMV;san2,seon2
        (
            'U+3598',
            [
                {
                    "radical": 30,
                    "strokes": 7,
                    "cangjie": "RMMV",
                    "readings": ["san2", "seon2"],
                }
            ],
        ),
    ],
)
def test_expand_kCheungBauer(expanded_data, ucn, expected):
    """
    Each data value consists of three pieces, separated by semicolons:

    (1) the character’s radical-stroke index as a three-digit radical, slash,
    two-digit stroke count;
    (2) the character’s cangjie input code (if any); and
    (3) a comma-separated list of Cantonese readings using the jyutping
    romanization in alphabetical order.
    """
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kCheungBauer'] == expected


@pytest.mark.parametrize(
    "ucn,expected",
    [
        # U+34D6      kCihaiT 170.105
        ("U+34D6", [{"page": 170, "row": 1, "character": 5}])
    ],
)
def test_expand_kCihaiT(expanded_data, ucn, expected):
    """
    The position is indicated by a decimal number. The digits to the left of
    the decimal are the page number. The first digit after the decimal is the
    row on the page, and the remaining two digits after the decimal are the
    position on the row.
    """
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kCihaiT'] == expected


@pytest.mark.parametrize(
    "ucn,expected",
    [
        # U+9F7C  kDaeJaweon      2075.100
        ("U+9F7C", {"page": 2075, "character": 10, "virtual": 0}),
        # U+4E37  kDaeJaweon      0162.211
        ("U+4E37", {"page": 162, "character": 21, "virtual": 1}),
    ],
)
def test_expand_kDaeJaweon(expanded_data, ucn, expected):
    """
    The position is in the form “page.position” with the final digit in the
    position being “0” for characters actually in the dictionary and “1” for
    characters not found in the dictionary and assigned a “virtual” position in
    the dictionary.
    """
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kDaeJaweon'] == expected


@pytest.mark.parametrize(
    "ucn,expected",
    [
        # U+48D3  kIICore CG
        ("U+48D3", [{'priority': 'C', 'sources': ['G']}]),
        # U+4E09  kIICore AGTJHKMP
        ("U+4E09", [{'priority': 'A', 'sources': ['G', 'T', 'J', 'H', 'K', 'M', 'P']}]),
        # U+4E0E  kIICore AGJ
        ("U+4E0E", [{'priority': 'A', 'sources': ['G', 'J']}]),
    ],
)
def test_expand_kIICore(expanded_data, ucn, expected):
    """
    Each value consists of a letter (A, B, or C), indicating priority value,
    and one or more letters (G, H, J, K, M, P, or T), indicating source. The
    source letters are the same as used for IRG sources, except that "P" is
    used instead of "KP".
    """
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kIICore'] == expected


@pytest.mark.parametrize(
    "ucn,expected",
    [
        # U+4E07  kIRGDaeJaweon   0137.070
        ("U+4E07", [{"page": 137, "character": 7, "virtual": 0}]),
        # U+4E37  kIRGDaeJaweon   0162.211
        ("U+4E37", [{"page": 162, "character": 21, "virtual": 1}]),
    ],
)
def test_expand_kIRGDaeJaweon(expanded_data, ucn, expected):
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kIRGDaeJaweon'] == expected


@pytest.mark.parametrize(
    "ucn,expected",
    [
        # U+342C      kFenn   871P
        ("U+342C", [{"phonetic": '871', "frequency": "P"}]),
        # U+3431      kFenn   281K
        ("U+3431", [{"phonetic": '281', "frequency": "K"}]),
        # U+9918      kFenn   31A
        ("U+9918", [{"phonetic": '31', "frequency": "A"}]),
        # U+807D      kFenn   381aA
        ("U+807D", [{"phonetic": '381a', "frequency": "A"}]),
    ],
)
def test_expand_kFenn(expanded_data, ucn, expected):
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kFenn'] == expected


@pytest.mark.parametrize(
    "ucn,expected",
    [
        # U+4E0B      kHanyuPinlu     xià(6430) xia(249)
        (
            "U+4E0B",
            [
                {"phonetic": "xià", "frequency": 6430},
                {"phonetic": "xia", "frequency": 249},
            ],
        ),
        # U+4E09      kHanyuPinlu     sān(3030)
        ("U+4E09", [{"phonetic": "sān", "frequency": 3030}]),
        # U+55EF	kHanyuPinlu	ń(48) ň(48) ǹ(48) ńg(48) ňg(48) ǹg(48)
        (
            "U+55EF",
            [
                {"phonetic": "ń", "frequency": 48},
                {"phonetic": "ň", "frequency": 48},
                {"phonetic": "ǹ", "frequency": 48},
                {"phonetic": "ńg", "frequency": 48},
                {"phonetic": "ňg", "frequency": 48},
                {"phonetic": "ǹg", "frequency": 48},
            ],
        ),
    ],
)
def test_expand_kHanyuPinlu(expanded_data, ucn, expected):
    """
    Immediately following the pronunciation, a numeric string appears in
    parentheses: e.g. in “ā(392)” the numeric string “392” indicates the sum
    total of the frequencies of the pronunciations of the character as given in
    HYPLCD.
    """
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kHanyuPinlu'] == expected


@pytest.mark.parametrize(
    "ucn,expected",
    [
        # U+4E00  kHDZRadBreak    ⼀[U+2F00]:10001.010
        (
            'U+4E00',
            {
                "radical": "⼀",
                "ucn": "U+2F00",
                "location": {"volume": 1, "page": 1, "character": 1, "virtual": False},
            },
        ),
        # U+4E59  kHDZRadBreak    ⼄[U+2F04]:10047.040
        (
            'U+4E59',
            {
                "radical": "⼄",
                "ucn": "U+2F04",
                "location": {"volume": 1, "page": 47, "character": 4, "virtual": False},
            },
        ),
    ],
)
def test_expand_kHDZRadBreak(expanded_data, ucn, expected):
    """
    Hanyu Da Zidian has a radical break beginning at this character’s position.
    The field consists of the radical (with its Unicode code point), a colon,
    and then the Hanyu Da Zidian position as in the kHanyu field.
    """
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kHDZRadBreak'] == expected


@pytest.mark.parametrize(
    "ucn,expected",
    [
        # U+349D      kSBGY   479.12 495.09
        ("U+349D", [{"page": 479, "character": 12}, {"page": 495, "character": 9}]),
        # U+349F      kSBGY   296.38
        ("U+349F", [{"page": 296, "character": 38}]),
    ],
)
def test_expand_kSBGY(expanded_data, ucn, expected):
    """
    The 25334 character references are given in the form “ABC.XY”, in which:
    "ABC” is the zero-padded page number [004..546]; “XY” is the zero-padded
    number of the character on the page [01..73]. For example, 364.38
    indicates the 38th character on Page 364 (i.e. 澍). Where a given Unicode
    Scalar Value (USV) has more than one reference, these are space-delimited.
    """
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kSBGY'] == expected


@pytest.mark.parametrize(
    "ucn,fieldval,expected",
    [
        # U+91B1  kXHC1983        0295.011:fā 0884.081:pō
        (
            "U+91B1",
            "0295.011:fā 0884.081:pō",
            [
                {
                    "locations": [
                        {"page": 295, "character": 1, "entry": 1, "substituted": False}
                    ],
                    "reading": "fā",
                },
                {
                    "locations": [
                        {"page": 884, "character": 8, "entry": 1, "substituted": False}
                    ],
                    "reading": "pō",
                },
            ],
        ),
        # U+379E  kXHC1983        1092.070*,1092.071:sóng
        (
            "U+379E",
            "1092.070*,1092.071:sóng",
            [
                {
                    "locations": [
                        {"page": 1092, "character": 7, "entry": 0, "substituted": True},
                        {
                            "page": 1092,
                            "character": 7,
                            "entry": 1,
                            "substituted": False,
                        },
                    ],
                    "reading": "sóng",
                }
            ],
        ),
        # U+5750  kXHC1983        1551.040,1552.011:zuò
        (
            "U+5750",
            "1551.040,1552.011:zuò",
            [
                {
                    "locations": [
                        {
                            "page": 1551,
                            "character": 4,
                            "entry": 0,
                            "substituted": False,
                        },
                        {
                            "page": 1552,
                            "character": 1,
                            "entry": 1,
                            "substituted": False,
                        },
                    ],
                    "reading": "zuò",
                }
            ],
        ),
    ],
)
def test_expand_kXHC1983(expanded_data, ucn, fieldval, expected):
    r"""
    Each pīnyīn reading is preceded by the character’s location(s) in the
    dictionary, separated from the reading by “:” (colon); multiple locations
    for a given reading are separated by “,” (comma); multiple “location:
    reading” values are separated by “ ” (space). Each location reference is of
    the form /[0-9]{4}\.[0-9]{3}\*?/ . The number preceding the period is the
    page number, zero-padded to four digits. The first two digits of the number
    following the period are the entry’s position on the page, zero-padded. The
    third digit is 0 for a main entry and greater than 0 for a parenthesized
    variant of the main entry. A trailing “*” (asterisk) on the location
    indicates an encoded variant substituted for an unencoded character (see
    below).

    As of the present writing (Unicode 5.1), the XHC source data contains 204
    unencoded characters (198 of which were represented by PUA or CJK
    Compatibility [or in one case, by non-CJK, see below] characters), for the
    most part simplified variants. Each of these 198 characters in the source
    is replaced by one or more encoded variants (references in all 204 cases
    are marked with a trailing “*”; see above). Many of these unencoded forms
    are already in the pipeline for future encoding, and future revisions of
    this data will eliminate trailing asterisks from mappings.
    """
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kXHC1983'] == expected

    assert expansion.expand_field('kXHC1983', fieldval) == expected


@pytest.mark.parametrize(
    "ucn,fieldval,expected",
    [
        # U+348C      kIRG_GSource    GKX-0118.03
        ("U+348C", "GKX-0118.03", {"source": "GKX", "location": "0118.03"}),
        # U+2A660  kIRG_GSource    G4K
        ("U+2A660", "G4K", {"source": "G4K", "location": None}),
        # U+348D      kIRG_GSource    G5-3272
        ("U+348D", "G5-3272", {"source": "G5", "location": "3272"}),
    ],
)
def test_expand_kIRG_GSource(expanded_data, ucn, fieldval, expected):
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kIRG_GSource'] == expected

    assert expansion.expand_field('kIRG_GSource', fieldval) == expected


@pytest.mark.parametrize(
    "ucn,fieldval,expected",
    [
        # U+347E      kIRG_HSource    H-8F59
        ("U+347E", "H-8F59", {"source": "H", "location": "8F59"}),
        # U+4E00      kIRG_HSource    HB1-A440
        ("U+4E00", "HB1-A440", {"source": "HB1", "location": "A440"}),
        # U+4E07      kIRG_HSource    HB2-C945
        ("U+4E07", "HB2-C945", {"source": "HB2", "location": "C945"}),
    ],
)
def test_expand_kIRG_HSource(expanded_data, ucn, fieldval, expected):
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kIRG_HSource'] == expected

    assert expansion.expand_field('kIRG_HSource', fieldval) == expected


@pytest.mark.parametrize(
    "ucn,fieldval,expected",
    [
        # U+3400	kIRG_JSource	JA-2121
        ("U+3400", "JA-2121", {"source": "JA", "location": "2121"}),
        # U+3402	kIRG_JSource	JA3-2E23
        ("U+3402", "JA3-2E23", {"source": "JA3", "location": "2E23"}),
    ],
)
def test_expand_kIRG_JSource(expanded_data, ucn, fieldval, expected):
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kIRG_JSource'] == expected

    assert expansion.expand_field('kIRG_JSource', fieldval) == expected


@pytest.mark.parametrize(
    "field,ucn,fieldval,expected",
    [
        # U+3ED0  kIRG_KPSource   KP0-EAB2
        ("kIRG_KPSource", "U+3ED0", "KP0-EAB2", {"source": "KP0", "location": "EAB2"}),
        # U+340C  kIRG_KPSource   KP1-3451
        ("kIRG_KPSource", "U+340C", "KP1-3451", {"source": "KP1", "location": "3451"}),
        # U+4E06  kIRG_KSource    K2-2121
        ("kIRG_KSource", "U+4E06", "K2-2121", {"source": "K2", "location": "2121"}),
        # U+3401  kIRG_KSource    K3-2121
        ("kIRG_KSource", "U+3401", "K3-2121", {"source": "K3", "location": "2121"}),
        # U+21290	kIRG_MSource	MAC-00077
        (
            "kIRG_MSource",
            "U+21290",
            "MAC-00077",
            {"source": "MAC", "location": "00077"},
        ),
        # U+3400  kIRG_TSource    T6-222C
        ("kIRG_TSource", "U+3400", "T6-222C", {"source": "T6", "location": "222C"}),
        # U+3401  kIRG_TSource    T4-2224
        ("kIRG_TSource", "U+3401", "T4-2224", {"source": "T4", "location": "2224"}),
        # U+22016 kIRG_USource    UTC-00069
        (
            "kIRG_USource",
            "U+22016",
            "UTC-00069",
            {"source": "UTC", "location": "00069"},
        ),
        # U+221EC kIRG_USource    UCI-00937
        (
            "kIRG_USource",
            "U+221EC",
            "UCI-00937",
            {"source": "UCI", "location": "00937"},
        ),
        # U+346B  kIRG_VSource    V0-3034
        ("kIRG_VSource", "U+346B", "V0-3034", {"source": "V0", "location": "3034"}),
        # U+340C  kIRG_VSource    V2-8874
        ("kIRG_VSource", "U+340C", "V2-8874", {"source": "V2", "location": "8874"}),
    ],
)
def test_expand_kIRG_KPSource(expanded_data, field, ucn, fieldval, expected):
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item[field] == expected

    assert expansion.expand_field(field, fieldval) == expected


@pytest.mark.parametrize(
    "ucn,fieldval,expected",
    [
        # U+340C  kGSR    0004f
        ("U+340C", "0004f", [{"set": 4, "letter": "f", "apostrophe": False}]),
        # U+371D	kGSR	0651k'
        ("U+371D", "0651k'", [{"set": 651, "letter": "k", "apostrophe": True}]),
        # U+9AE2  kGSR    0004e' 0850s
        (
            "U+9AE2",
            "0004e' 0850s",
            [
                {"set": 4, "letter": "e", "apostrophe": True},
                {"set": 850, "letter": "s", "apostrophe": False},
            ],
        ),
    ],
)
def test_expand_kGSR(expanded_data, ucn, fieldval, expected):
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kGSR'] == expected

    assert expansion.expand_field('kGSR', fieldval) == expected


@pytest.mark.parametrize(
    "ucn,fieldval,expected",
    [
        # U+34BC  kCheungBauerIndex       402.06
        ("U+34BC", "402.06", [{"page": 402, "character": 6}]),
        # U+3578  kCheungBauerIndex       351.02 351.03
        (
            "U+3578",
            "351.02 351.03",
            [{"page": 351, "character": 2}, {"page": 351, "character": 3}],
        ),
    ],
)
def test_expand_kCheungBauerIndex(expanded_data, ucn, fieldval, expected):
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kCheungBauerIndex'] == expected

    assert expansion.expand_field('kCheungBauerIndex', fieldval) == expected


@pytest.mark.parametrize(
    "ucn,fieldval,expected",
    [
        # U+348B      kFennIndex      480.05
        ("U+348B", "480.05", [{"page": 480, "character": 5}]),
        # U+349A      kFennIndex      602.04
        ("U+349A", "602.04", [{"page": 602, "character": 4}]),
    ],
)
def test_expand_kFennIndex(expanded_data, ucn, fieldval, expected):
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kFennIndex'] == expected

    assert expansion.expand_field('kFennIndex', fieldval) == expected


@pytest.mark.parametrize(
    "ucn,fieldval,expected",
    [
        # U+34AD      kIRGKangXi      0125.190
        ("U+34AD", "0125.190", [{"page": 125, "character": 19, "virtual": 0}]),
        # U+34AE      kIRGKangXi      0125.201
        ("U+34AE", "0125.201", [{"page": 125, "character": 20, "virtual": 1}]),
    ],
)
def test_expand_kIRGKangXi(expanded_data, ucn, fieldval, expected):
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kIRGKangXi'] == expected

    assert expansion.expand_field('kIRGKangXi', fieldval) == expected


@pytest.mark.parametrize(
    "ucn,fieldval,expected",
    [
        # U+4E00	kCCCII	213021
        ("U+4E00", "213021", ["213021"]),
        # U+4E0D	kCCCII	21302A
        ("U+4E0D", "21302A", ["21302A"]),
    ],
)
def test_expand_kCCCII(expanded_data, ucn, fieldval, expected):
    item = [i for i in expanded_data if i['ucn'] == ucn][0]
    assert item['kCCCII'] == expected

    assert expansion.expand_field('kCCCII', fieldval) == expected
