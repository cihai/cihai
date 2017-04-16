*cihai* - united front to provide open, accessible, and standardized
access to CJK data

|pypi| |docs| |build-status| |coverage| |license|

Attempt at building successor of the Han Character library `cjklib`_.

- compatible with python 2.7+ and 3.3+.
- built against unit tests. See `Travis Builds`_ and `Revision History`_.
- supports `Unihan`_, see `current datasets`_.  - upcoming supports for
  character decomposition, dictionaries (CEDict).
- extensible to new datasets, see more about `Extending`_ cihai to
  support new `datapackages`_ compatible datasets.

See `Internals`_ for design philosophy.

.. _Travis Builds: https://travis-ci.org/cihai/cihai/builds
.. _Revision History: https://github.com/cihai/cihai/commits/master
.. _cjklib: http://cjklib.org/
.. _current datasets: https://cihai.git-pull.com/en/latest/api.html#datasets
.. _Extending: https://cihai.git-pull.com/en/latest/extending.html
.. _permissively licensing your dataset: https://cihai.git-pull.com/en/latest/information_liberation.html
.. _Internals: https://cihai.git-pull.com/en/latest/internals.html

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
