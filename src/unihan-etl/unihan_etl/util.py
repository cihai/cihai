"""Utility and helper methods for script.

util
~~~~

"""
import re
import sys

from ._compat import Mapping, string_types, text_type, unichr


def ucn_to_unicode(ucn):
    """Return a python unicode value from a UCN.

    Converts a Unicode Universal Character Number (e.g. "U+4E00" or "4E00") to
    Python unicode (u'\\u4e00')"""
    if isinstance(ucn, string_types):
        ucn = ucn.strip("U+")
        if len(ucn) > int(4):
            char = b'\U' + format(int(ucn, 16), '08x').encode('latin1')
            char = char.decode('unicode_escape')
        else:
            char = unichr(int(ucn, 16))
    else:
        char = unichr(ucn)

    assert isinstance(char, text_type)

    return char


def ucnstring_to_python(ucn_string):
    """Return string with Unicode UCN (e.g. "U+4E00") to native Python Unicode
    (u'\\u4e00').
    """
    res = re.findall(r"U\+[0-9a-fA-F]*", ucn_string)
    for r in res:
        ucn_string = ucn_string.replace(text_type(r), text_type(ucn_to_unicode(r)))

    ucn_string = ucn_string.encode('utf-8')

    assert isinstance(ucn_string, bytes)
    return ucn_string


def ucnstring_to_unicode(ucn_string):
    """Return ucnstring as Unicode."""
    ucn_string = ucnstring_to_python(ucn_string).decode('utf-8')

    assert isinstance(ucn_string, text_type)
    return ucn_string


def _dl_progress(count, block_size, total_size, out=sys.stdout):
    """
    MIT License: https://github.com/okfn/dpm-old/blob/master/dpm/util.py

    Modification for testing: http://stackoverflow.com/a/4220278

    """

    def format_size(bytes):
        if bytes > 1000 * 1000:
            return '%.1fMb' % (bytes / 1000.0 / 1000)
        elif bytes > 10 * 1000:
            return '%iKb' % (bytes / 1000)
        elif bytes > 1000:
            return '%.1fKb' % (bytes / 1000.0)
        else:
            return '%ib' % bytes

    if not count:
        print('Total size: %s' % format_size(total_size))
    last_percent = int((count - 1) * block_size * 100 / total_size)
    # may have downloaded less if count*block_size > total_size
    maxdownloaded = count * block_size
    percent = min(int(maxdownloaded * 100 / total_size), 100)
    out.flush()
    if percent > last_percent:
        # TODO: is this acceptable? Do we want to do something nicer?
        out.write(
            '%3d%% [%s>%s]\r'
            % (
                percent,
                int(round(percent / 2)) * '=',
                int(round(50 - percent / 2)) * ' ',
            )
        )
        out.flush()
    if maxdownloaded >= total_size:
        print('\n')


def merge_dict(base, additional):
    if base is None:
        return additional

    if additional is None:
        return base

    if not (isinstance(base, Mapping) and isinstance(additional, Mapping)):
        return additional

    merged = base
    for key, value in additional.items():
        if isinstance(value, Mapping):
            merged[key] = merge_dict(merged.get(key), value)
        else:
            merged[key] = value

    return merged
