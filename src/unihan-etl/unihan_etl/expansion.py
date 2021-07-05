"""
Functions to uncompact details inside field values.

Notes
-----

:func:`re.compile` operations are inside of expand functions:

1. readability
2. module-level function bytecode is cached in python
3. the last used compiled regexes are cached
"""
import re

import zhon.hanzi
import zhon.pinyin

from unihan_etl.constants import SPACE_DELIMITED_FIELDS

#: diacritics from kHanyuPinlu
N_DIACRITICS = 'ńňǹ'


def expand_kDefinition(value):
    return [c.strip() for c in value.split(';')]


def expand_kMandarin(value):
    cn = value[0]
    if len(value) == 1:
        tw = value[0]
    else:
        tw = value[1]
    return {"zh-Hans": cn, "zh-Hant": tw}


def expand_kTotalStrokes(value):
    cn = value[0]
    if len(value) == 1:
        tw = value[0]
    else:
        tw = value[1]
    return {"zh-Hans": int(cn), "zh-Hant": int(tw)}


def expand_kHanYu(value):
    pattern = re.compile(
        r"""
        (?P<volume>[1-8])
        (?P<page>[0-9]{4})\.
        (?P<character>[0-3][0-9])
        (?P<virtual>[0-3])
    """,
        re.X,
    )

    for i, v in enumerate(value):
        m = pattern.match(v).groupdict()
        value[i] = {
            "volume": int(m['volume']),
            "page": int(m['page']),
            "character": int(m['character']),
            "virtual": int(m['virtual']),
        }
    return value


def expand_kIRGHanyuDaZidian(value):
    pattern = re.compile(
        r"""
        (?P<volume>[1-8])
        (?P<page>[0-9]{4})\.
        (?P<character>[0-3][0-9])
        (?P<virtual>[01])
    """,
        re.X,
    )

    for i, v in enumerate(value):
        m = pattern.match(v).groupdict()
        value[i] = {
            "volume": int(m['volume']),
            "page": int(m['page']),
            "character": int(m['character']),
            "virtual": int(m['virtual']),
        }
    return value


def expand_kHanyuPinyin(value):
    location_pattern = re.compile(
        r"""
        (?P<volume>[1-8])
        (?P<page>[0-9]{4})\.
        (?P<character>[0-3][0-9])
        (?P<virtual>[0-3])
    """,
        re.X,
    )

    for i, v in enumerate(value):
        v = [s.split(',') for s in v.split(':')]
        value[i] = {"locations": v[0], "readings": v[1]}

        for n, loc in enumerate(value[i]['locations']):
            m = location_pattern.match(loc).groupdict()
            value[i]['locations'][n] = {
                "volume": int(m['volume']),
                "page": int(m['page']),
                "character": int(m['character']),
                "virtual": int(m['virtual']),
            }
    return value


def expand_kXHC1983(value):
    pattern = re.compile(
        r"""
        (?P<page>[0-9]{4})\.
        (?P<character>[0-9]{2})
        (?P<entry>[0-9]{1})
        (?P<substituted>\*?)
    """,
        re.X,
    )

    for i, v in enumerate(value):
        vals = v.split(':')
        value[i] = {"locations": vals[0].split(','), "reading": vals[1]}

        for n, loc in enumerate(value[i]['locations']):
            m = pattern.match(loc).groupdict()
            value[i]['locations'][n] = {
                "page": int(m['page']),
                "character": int(m['character']),
                "entry": int(m['entry']),
                "substituted": m['substituted'] == "*",
            }
    return value


def expand_kCheungBauer(value):
    pattern = re.compile(
        r"""
        (?P<radical>[0-9]{3})\/(?P<strokes>[0-9]{2});
        (?P<cangjie>[A-Z]*);
        (?P<readings>[a-z1-6\[\]\/,]+)
    """,
        re.X,
    )
    for i, v in enumerate(value):
        m = pattern.match(v).groupdict()
        value[i] = {
            "radical": int(m['radical']),
            "strokes": int(m['strokes']),
            "cangjie": m['cangjie'] or None,
            "readings": m['readings'].split(','),
        }
    return value


def expand_kRSAdobe_Japan1_6(value):
    pattern = re.compile(
        r"""
        (?P<type>[CV])\+
        (?P<cid>[0-9]{1,5})\+
        (?P<radical>[1-9][0-9]{0,2})\.
        (?P<strokes>[1-9][0-9]?)\.
        (?P<strokes_residue>[0-9]{1,2})
    """,
        re.X,
    )

    for i, v in enumerate(value):
        m = pattern.match(v).groupdict()

        value[i] = {
            "type": m['type'],
            "cid": int(m['cid']),
            "radical": int(m['radical']),
            "strokes": int(m['strokes']),
            "strokes-residue": int(m['strokes_residue']),
        }
    return value


def expand_kCihaiT(value):
    pattern = re.compile(
        r"""
        (?P<page>[1-9][0-9]{0,3})\.
        (?P<row>[0-9]{1})
        (?P<character>[0-9]{2})
    """,
        re.X,
    )
    for i, v in enumerate(value):
        m = pattern.match(v).groupdict()
        value[i] = {
            "page": int(m['page']),
            "row": int(m['row']),
            "character": int(m['character']),
        }
    return value


def expand_kIICore(value):
    for i, v in enumerate(value):
        value[i] = {"priority": v[0], "sources": list(v[1:])}
    return value


def expand_kDaeJaweon(value):
    pattern = re.compile(
        r"""
        (?P<page>[0-9]{4})\.
        (?P<character>[0-9]{2})
        (?P<virtual>[01])
    """,
        re.X,
    )
    m = pattern.match(value).groupdict()

    value = {
        "page": int(m['page']),
        "character": int(m['character']),
        "virtual": int(m['virtual']),
    }
    return value


def expand_kIRGKangXi(value):
    for i, v in enumerate(value):
        value[i] = expand_kDaeJaweon(v)
    return value


def expand_kIRGDaeJaweon(value):
    for i, v in enumerate(value):
        value[i] = expand_kDaeJaweon(v)
    return value


def expand_kFenn(value):
    pattern = re.compile(
        """
        (?P<phonetic>[0-9]+a?)
        (?P<frequency>[A-KP*])
    """,
        re.X,
    )

    for i, v in enumerate(value):
        m = pattern.match(v).groupdict(v)
        value[i] = {"phonetic": m['phonetic'], "frequency": m['frequency']}
    return value


def expand_kHanyuPinlu(value):
    pattern = re.compile(
        r"""
        (?P<phonetic>[a-z({}{}]+)
        \((?P<frequency>[0-9]+)\)
    """.format(
            zhon.pinyin.lowercase, N_DIACRITICS
        ),
        re.X,
    )

    for i, v in enumerate(value):
        m = pattern.match(v).groupdict()
        value[i] = {"phonetic": m['phonetic'], "frequency": int(m['frequency'])}
    return value


def expand_kHDZRadBreak(value):
    rad, loc = value.split(':')

    location_pattern = re.compile(
        r"""
        (?P<volume>[1-8])
        (?P<page>[0-9]{4})\.
        (?P<character>[0-3][0-9])
        (?P<virtual>[01])
    """,
        re.X,
    )

    lmatches = location_pattern.match(loc).groupdict()
    location = {
        "volume": int(lmatches['volume']),
        "page": int(lmatches['page']),
        "character": int(lmatches['character']),
        "virtual": int(lmatches['virtual']),
    }

    pattern = re.compile(
        r"""
        (?P<radical>[{}]+)
        \[(?P<ucn>U\+2F[0-9A-D][0-9A-F])\]
    """.format(
            zhon.hanzi.radicals
        ),
        re.X,
    )
    m = pattern.match(rad).groupdict()

    return {"radical": m['radical'], "ucn": m['ucn'], "location": location}


def expand_kSBGY(value):
    for i, v in enumerate(value):
        vals = v.split('.')
        value[i] = {"page": int(vals[0]), "character": int(vals[1])}
    return value


def _expand_kRSGeneric(value):
    pattern = re.compile(
        r"""
        (?P<radical>[1-9][0-9]{0,2})
        (?P<simplified>\'?)\.
        (?P<strokes>-?[0-9]{1,2})
    """,
        re.X,
    )

    for i, v in enumerate(value):
        m = pattern.match(v).groupdict()
        value[i] = {
            "radical": int(m['radical']),
            "strokes": int(m['strokes']),
            "simplified": m['simplified'] == "'",
        }
    return value


expand_kRSUnicode = _expand_kRSGeneric
expand_kRSJapanese = _expand_kRSGeneric
expand_kRSKangXi = _expand_kRSGeneric
expand_kRSKanWa = _expand_kRSGeneric
expand_kRSKorean = _expand_kRSGeneric


def _expand_kIRG_GenericSource(value):
    v = value.split('-')

    return {"source": v[0], "location": v[1] if len(v) > 1 else None}


expand_kIRG_GSource = _expand_kIRG_GenericSource
expand_kIRG_HSource = _expand_kIRG_GenericSource
expand_kIRG_JSource = _expand_kIRG_GenericSource
expand_kIRG_KPSource = _expand_kIRG_GenericSource
expand_kIRG_KSource = _expand_kIRG_GenericSource
expand_kIRG_MSource = _expand_kIRG_GenericSource
expand_kIRG_TSource = _expand_kIRG_GenericSource
expand_kIRG_USource = _expand_kIRG_GenericSource
expand_kIRG_VSource = _expand_kIRG_GenericSource


def expand_kGSR(value):
    pattern = re.compile(
        r"""
        (?P<set>[0-9]{4})
        (?P<letter>[a-vx-z])
        (?P<apostrophe>\')?
    """,
        re.X,
    )

    for i, v in enumerate(value):
        m = pattern.match(v).groupdict()
        value[i] = {
            "set": int(m['set']),
            "letter": m['letter'],
            "apostrophe": m['apostrophe'] == "'",
        }
    return value


def expand_kCheungBauerIndex(value):
    for i, v in enumerate(value):
        m = v.split('.')
        value[i] = {"page": int(m[0]), "character": int(m[1])}
    return value


expand_kFennIndex = expand_kCheungBauerIndex


def expand_field(field, fvalue):
    """
    Return structured value of information in UNIHAN field.

    Parameters
    ----------
    field : str
        field name
    fvalue : str
        value of field

    Returns
    -------
    list or dict :
        expanded field information per UNIHAN's documentation
    """
    if field in SPACE_DELIMITED_FIELDS and fvalue:
        fvalue = fvalue.split(' ')

    try:
        expansion_func = eval('expand_%s' % field)
        return expansion_func(fvalue)
    except NameError:
        pass

    return fvalue
