.. _api:

.. module:: cihai

===
API
===

.. automodule:: cihai.core

    .. autoclass:: Cihai
        :members:
        :show-inheritance:
        :inherited-members:

    .. autoclass:: Storage
        :members:
        :inherited-members:
        :show-inheritance:

Conversion
----------

.. autofunction:: cihai.conversion.euc_to_unicode
.. autofunction:: cihai.conversion.euc_to_utf8
.. autofunction:: cihai.conversion.gb2312_to_euc
.. autofunction:: cihai.conversion.kuten_to_gb2312
.. autofunction:: cihai.conversion.python_to_euc
.. autofunction:: cihai.conversion.python_to_ucn
.. autofunction:: cihai.conversion.ucn_to_unicode
.. autofunction:: cihai.conversion.ucnstring_to_python
.. autofunction:: cihai.conversion.ucnstring_to_unicode

Testing
-------

cihai provides helper functions and classes for testing cihai-compatible
libraries. Pull in cihai as a dependency and import them right into
your testsuite.

.. automodule:: cihai.test
    :members:
    :inherited-members:
    :show-inheritance:

Utilities
---------

.. automodule:: cihai.util
    :members:
    :inherited-members:
    :show-inheritance:
