# -*- coding: utf8 -*-
# flake8: noqa

import collections
import sys

PY2 = sys.version_info[0] == 2

if PY2:
    unichr = unichr
    text_type = unicode
    string_types = (str, unicode)

    from itertools import izip
    from urllib import urlretrieve

    from cStringIO import StringIO as BytesIO
    from StringIO import StringIO

    Mapping = collections.Mapping

    exec('def reraise(tp, value, tb=None):\n raise tp, value, tb')
else:
    unichr = chr
    text_type = str
    string_types = (str,)

    from io import BytesIO, StringIO
    from urllib.request import urlretrieve

    izip = zip

    Mapping = collections.abc.Mapping

    def reraise(tp, value, tb=None):
        if value.__traceback__ is not tb:
            raise (value.with_traceback(tb))
        raise value
