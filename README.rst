.. image:: https://travis-ci.org/tony/cihai.png?branch=master
    :target: https://travis-ci.org/tony/cihai

.. image:: https://badge.fury.io/py/cihai.png
    :target: http://badge.fury.io/py/cihai

.. image:: https://coveralls.io/repos/tony/cihai/badge.png?branch=master
    :target: https://coveralls.io/r/tony/cihai?branch=master

``cihai`` - China fit into a python package.

Note: this is being rewritten from scratch at the moment.

Attempt at building successor of the Han Character library `cjklib`_.

- compatible with python 2.7+ and 3.3+.
- built using TDD and python best practices.
- supports `Unihan`_, see `current datasets`_.
- upcoming supports for character decomposition, dictionaries (CEDict).
- extensible to new datasets, see more about `Extending`_ cihai's 
  knowledge.

Being built against unit tests. See the `Travis Builds`_ and
`Revision History`_.

.. _Travis Builds: https://travis-ci.org/tony/cihai/builds
.. _Revision History: https://github.com/tony/cihai/commits/master
.. _cjklib: http://cjklib.org/0.3/
.. _current datasets: http://cihai.readthedocs.org/en/latest/api.html#datasets
.. _Extending: http://cihai.readthedocs.org/en/latest/extending.html

==============  ==========================================================
Python support  Python 2.7, >= 3.3
Source          https://github.com/tony/cihai
Docs            http://cihai.rtfd.org
Changelog       http://cihai.readthedocs.org/en/latest/history.html
API             http://cihai.readthedocs.org/en/latest/api.html
Issues          https://github.com/tony/cihai/issues
Travis          http://travis-ci.org/tony/cihai
Test coverage   https://coveralls.io/r/tony/cihai
pypi            https://pypi.python.org/pypi/cihai
Ohloh           https://www.ohloh.net/p/cihai
License         `BSD`_.
git repo        .. code-block:: bash

                    $ git clone https://github.com/tony/cihai.git
install dev     .. code-block:: bash

                    $ git clone https://github.com/tony/cihai.git cihai
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
