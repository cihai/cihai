*cihai* - United front to provide open, accessible, and standardized
access to CJK data

|pypi| |docs| |build-status| |coverage| |license|

Current Datasets
----------------

- `cihaidata-unihan`_ - `Unihan`_ data package

Tool
----

*In development*

- Single tool for interfacing with CJK data, compare to `cjklib`_.
- API, in python, for programatically interfacing with data.
- Compatible with python 2.7, 3.3+, and pypy/pypy3.
- Designed against a robust test suite. See `Travis Builds`_ and
  `Revision History`_.
- Supports `Unihan`_, upcoming support for character decomposition, dictionaries
  (CEDict).
- Extensible. For new data sets, read more about how you can `extend`_ cihai to
  support new `datapackages`_ compatible datasets.
- For more, see `internals`_ for design philosophy.

Workgroup and Standardization
-----------------------------

- Find undigitized data sets relating to CJK
- Clarifying and negotiate license details of data sets, see `permissively licensing your dataset`_.
- Create standardized, consistent packages for all data sets
- Maintain aforementioned datasets
- Continue to improve current infrastructure and packages while seeking out rare and undigitized CJK data for preservation and access

Troubleshooting
---------------

Python 2.7 and UCS
""""""""""""""""""

Note, to get this working on python 2.7, you must have python built with
*UCS4* via ``--enable-unicode=ucs4``. You can test for UCS4 with:

.. code-block:: python

   >>> import sys
   >>> sys.maxunicode > 0xffff
   True

Most packaged and included python distributions will already be build with
UCS4 (such as Ubuntu's system python). On python 3.3 and greater, this
distinction no longer exists, no action is needed.

.. _Travis Builds: https://travis-ci.org/cihai/cihai/builds
.. _Revision History: https://github.com/cihai/cihai/commits/master
.. _cjklib: http://cjklib.org/
.. _extend: https://cihai.git-pull.com/en/latest/extending.html
.. _permissively licensing your dataset: https://cihai.git-pull.com/en/latest/lore/information_liberation.html
.. _internals: https://cihai.git-pull.com/en/latest/lore/internals.html

==============  ==========================================================
Python support  Python 2.7, >= 3.3, pypy
Source          https://github.com/cihai/cihai
Docs            https://cihai.git-pull.com
Changelog       https://cihai.git-pull.com/en/latest/history.html
API             https://cihai.git-pull.com/en/latest/api.html
Issues          https://github.com/cihai/cihai/issues
Travis          https://travis-ci.org/cihai/cihai
Test coverage   https://coveralls.io/r/cihai/cihai
pypi            https://pypi.python.org/pypi/cihai
OpenHub         https://www.openhub.net/p/cihai
License         `BSD`_.
git repo        .. code-block:: bash

                    $ git clone https://github.com/cihai/cihai.git
install stable  .. code-block:: bash

                    $ pip install cihai
install dev     .. code-block:: bash

                    $ git clone https://github.com/cihai/cihai.git cihai
                    $ cd ./cihai
                    $ virtualenv .env
                    $ source .env/bin/activate
                    $ pip install -e .
tests           .. code-block:: bash

                    $ python setup.py test
==============  ==========================================================

.. _BSD: http://opensource.org/licenses/BSD-3-Clause
.. _Documentation: https://cihai.git-pull.com/en/latest/
.. _API: https://cihai.git-pull.com/en/latest/api.html
.. _Unihan: http://www.unicode.org/charts/unihan.html
.. _datapackages: http://dataprotocols.org/data-packages/
.. _datapackage.json format: https://github.com/datasets/gdp/blob/master/datapackage.json
.. _simple data format: http://data.okfn.org/standards/simple-data-format
.. _PEP 301\: python package format: http://www.python.org/dev/peps/pep-0301/
.. _cihaidata-unihan: https://cihaidata-unihan.git-pull.com

.. |pypi| image:: https://img.shields.io/pypi/v/cihai.svg
    :alt: Python Package
    :target: http://badge.fury.io/py/cihai

.. |build-status| image:: https://img.shields.io/travis/cihai/cihai.svg
   :alt: Build Status
   :target: https://travis-ci.org/cihai/cihai

.. |coverage| image:: https://codecov.io/gh/cihai/cihai/branch/master/graph/badge.svg
    :alt: Code Coverage
    :target: https://codecov.io/gh/cihai/cihai

.. |license| image:: https://img.shields.io/github/license/cihai/cihai.svg
    :alt: License 

.. |docs| image:: https://readthedocs.org/projects/cihai/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://readthedocs.org/projects/cihai/
