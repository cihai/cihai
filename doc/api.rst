.. _api:

===
API
===

.. automodule:: cihai.core
    :members:

Bootstrapping
-------------

.. automodule:: cihai.bootstrap
    :members:

Configuration
-------------

.. automodule:: cihai.conf
    :members:

.. _cihai.conversion:

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

Exceptions
----------

When using cihai via Python, you can catch Cihai-specific exceptions via
these. All Cihai-specific exceptions are catchable via
:exc:`~cihai.exc.CihaiException` since its the base exception.

.. automodule:: cihai.exc
    :members:
    :inherited-members:
    :show-inheritance:

Utilities
---------

.. automodule:: cihai.util
    :members:
    :inherited-members:
    :show-inheritance:
