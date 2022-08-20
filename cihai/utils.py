"""
Utility and helper methods for cihai.
"""
import sys

from . import exc
from ._compat import collections_abc


def merge_dict(base, additional):
    """
    Combine two dictionary-like objects.

    Notes
    -----
    Code from https://github.com/pypa/warehouse
    Copyright 2013 Donald Stufft

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    """
    if base is None:
        return additional

    if additional is None:
        return base

    if not (
        isinstance(base, collections_abc.Mapping)
        and isinstance(additional, collections_abc.Mapping)
    ):
        return additional

    merged = base
    for key, value in additional.items():
        if isinstance(value, collections_abc.Mapping):
            merged[key] = merge_dict(merged.get(key), value)
        else:
            merged[key] = value

    return merged


def supports_wide():
    """Return affirmative if python interpreter supports wide characters.

    Returns
    -------
    bool :
        True if python supports wide character sets
    """
    return sys.maxunicode > 0xFFFF


def import_string(import_name: str, silent: bool = False):
    """Imports an object based on a string.

    This is useful if you want to use import paths as endpoints or
    something similar.  An import path can  be specified either in dotted
    notation (``xml.sax.saxutils.escape``) or with a colon as object
    delimiter (``xml.sax.saxutils:escape``).

    If `silent` is True the return value will be `None` if the import fails.

    Parameters
    ----------
    import_name : string
        the dotted name for the object to import.
    silent : bool
        if set to `True` import errors are ignored and `None` is returned instead.

    Returns
    -------
    imported object

    Raises
    ------
    cihai.exc.ImportStringError (ImportError, cihai.exc.CihaiException)

    Notes
    -----
    This is from werkzeug.utils d36aaf1 on May 23, 2022, LICENSE BSD.
    https://github.com/pallets/werkzeug

    Changes:
    - Exception raised is cihai.exc.ImportStringError
    - Format with black
    """
    import_name = import_name.replace(":", ".")
    try:
        try:
            __import__(import_name)
        except ImportError:
            if "." not in import_name:
                raise
        else:
            return sys.modules[import_name]

        module_name, obj_name = import_name.rsplit(".", 1)
        module = __import__(module_name, globals(), locals(), [obj_name])
        try:
            return getattr(module, obj_name)
        except AttributeError as e:
            raise ImportError(e) from None
    except ImportError as e:
        if not silent:
            raise exc.ImportStringError(import_name, e).with_traceback(
                sys.exc_info()[2]
            ) from None
    return None
