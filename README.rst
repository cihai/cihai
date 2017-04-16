.. image:: https://travis-ci.org/cihai/cihai.png?branch=master
    :target: https://travis-ci.org/cihai/cihai

.. image:: https://badge.fury.io/py/cihai.png
    :target: http://badge.fury.io/py/cihai

.. image:: https://coveralls.io/repos/cihai/cihai/badge.png?branch=master
    :target: https://coveralls.io/r/cihai/cihai?branch=master

``cihai`` - China fit into a python package. Part of the `cihai`_
project.

.. _cihai: https://github.com/cihai/
.. _cihai-handbook: https://github.com/cihai/cihai-handbook
.. _cihai team: https://github.com/cihai?tab=members
.. _cihai: https://github.com/cihai/cihai
.. _cihaidata-unihan on github: https://github.com/cihai/cihaidata-unihan

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
.. _current datasets: http://cihai.readthedocs.org/en/latest/api.html#datasets
.. _Extending: http://cihai.readthedocs.org/en/latest/extending.html
.. _permissively licensing your dataset: http://cihai.readthedocs.org/en/latest/information_liberation.html
.. _Internals: http://cihai.readthedocs.org/en/latest/internals.html

==============  ==========================================================
Python support  Python 2.7, >= 3.3
Source          https://github.com/cihai/cihai
Docs            http://cihai.rtfd.org
Changelog       http://cihai.readthedocs.org/en/latest/history.html
API             http://cihai.readthedocs.org/en/latest/api.html
Issues          https://github.com/cihai/cihai/issues
Travis          http://travis-ci.org/cihai/cihai
Test coverage   https://coveralls.io/r/cihai/cihai
pypi            https://pypi.python.org/pypi/cihai
Ohloh           https://www.ohloh.net/p/cihai
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
.. _Documentation: http://cihai.readthedocs.org/en/latest/
.. _API: http://cihai.readthedocs.org/en/latest/api.html
.. _Unihan: http://www.unicode.org/charts/unihan.html
.. _datapackages: http://dataprotocols.org/data-packages/
.. _datapackage.json format: https://github.com/datasets/gdp/blob/master/datapackage.json
.. _simple data format: http://data.okfn.org/standards/simple-data-format
.. _PEP 301\: python package format: http://www.python.org/dev/peps/pep-0301/
