``cihai`` - China fit in to a python package.

Status
------

Being built against unit tests. See the `Travis Builds`_ and
`Revision History`_.

.. _Travis Builds: https://travis-ci.org/tony/cihai/builds
.. _Revision History: https://github.com/tony/cihai/commits/master

Features
--------

- Python wrapper for `Unihan`_.

.. image:: https://travis-ci.org/tony/cihai.png?branch=master
    :target: https://travis-ci.org/tony/cihai

.. image:: https://badge.fury.io/py/cihai.png
    :target: http://badge.fury.io/py/cihai

==============  ==========================================================
Python support  Python 2.6, 2.7, >= 3.3
Source          https://github.com/tony/cihai
Docs            http://cihai.rtfd.org
Changelog       http://cihai.readthedocs.org/en/latest/history.html
API             http://cihai.readthedocs.org/en/latest/api.html
Issues          https://github.com/tony/cihai/issues
Travis          http://travis-ci.org/tony/cihai
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
