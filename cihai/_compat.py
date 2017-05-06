# -*- coding: utf8 -*-
# flake8: NOQA
import sys

PY2 = sys.version_info[0] == 2

if PY2:
    unichr = unichr
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)
    from urllib import urlretrieve

    from cStringIO import StringIO as BytesIO
    from StringIO import StringIO
    import cPickle as pickle

    import urlparse

    def console_to_str(s):
        return s.decode('utf_8')

    exec('def reraise(tp, value, tb=None):\n raise tp, value, tb')

else:
    unichr = chr
    text_type = str
    string_types = (str,)
    integer_types = (int, )

    from io import StringIO, BytesIO

    import urllib.parse as urllib
    import urllib.parse as urlparse
    from urllib.request import urlretrieve

    console_encoding = sys.__stdout__.encoding

    def console_to_str(s):
        """ From pypa/pip project, pip.backwardwardcompat. License MIT. """
        try:
            return s.decode(console_encoding)
        except UnicodeDecodeError:
            return s.decode('utf_8')

    def reraise(tp, value, tb=None):
        if value.__traceback__ is not tb:
            raise(value.with_traceback(tb))
        raise value
