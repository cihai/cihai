# -*- coding: utf8 - *-
"""
Cihai Extension System

Status: Experimental, API can change

As a pilot, the UNIHAN library, and an extension for it, in #131 [1]_

See Also
--------
.. [1] Add variant methods. Github issues for cihai.
   https://github.com/cihai/cihai/pull/131. Accessed September 1st, 2018.
"""
from __future__ import absolute_import, print_function, unicode_literals


from ._compat import with_metaclass


class ExtensionMeta(type):
    """Core metaclass for an extension"""


class ExtensionBase(object):
    pass


class Extension(with_metaclass(ExtensionMeta, ExtensionBase)):
    namespace = '__'

    def bootstrap(self):
        raise NotImplemented

    def check(self):
        """Can check to see if bootstrapped, can be updated."""
        raise NotImplemented

    def get_config(self):
        raise NotImplemented

    @property
    def config(self):
        """Easy access to config."""
        return self.get_config()


class ComputedField(object):
    def __init__(self, lookup_fn, reverse_fn):
        pass


class DirectField(object):
    pass


class Unihan(Extension):
    character = DirectField()
    variant = ComputedField(lookup_fn=None, reverse_fn=None)
