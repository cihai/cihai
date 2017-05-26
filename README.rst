*cihai* - Python library for `CJK`_ (chinese, japanese, korean) data

|pypi| |docs| |build-status| |coverage| |license|

This project is under active development. Follow our progress and check
back for updates!

Usage
-----

Python library only
"""""""""""""""""""

.. code-block:: sh

   $ pip install --user cihai

.. code-block:: python

   from cihai.core import Cihai
   from cihai.bootstrap import bootstrap_unihan

   c = Cihai()
   if not c.is_bootstrapped:  # download and install Unihan to db
       bootstrap_unihan(c.metadata)
       c.reflect_db()         # automap new table created during bootstrap

   query = c.lookup_char('好')
   glyph = query.first()
   print("lookup for 好: %s" % glyph.kDefinition)
   # lookup for 好: good, excellent, fine; well

   query = c.reverse_char('good')
   print('matches for "good": %s ' % ', '.join([glph.char for glph in query]))
   # matches for "good": 㑘, 㑤, 㓛, 㘬, 㙉, 㚃, 㚒, 㚥, 㛦, 㜴, 㜺, 㝖, 㤛, 㦝, ...

See `API`_ documentation and `/examples
<https://github.com/cihai/cihai/tree/master/examples>`_.

CLI front-end (`cihai-cli`_)
""""""""""""""""""""""""""""

.. code-block:: sh

   $ pip install --user cihai-cli

.. code-block:: sh

   # character lookup
   $ cihai info 好
   char: 好
   kCantonese: hou2 hou3
   kDefinition: good, excellent, fine; well
   kHangul: 호
   kJapaneseOn: KOU
   kKorean: HO
   kMandarin: hǎo
   kTang: '*xɑ̀u *xɑ̌u'
   kTotalStrokes: '6'
   kVietnamese: háo
   ucn: U+597D

   # reverse lookup
   $ cihai reverse library
   char: 圕
   kCangjie: WLGA
   kCantonese: syu1
   kCihaiT: '308.302'
   kDefinition: library
   kMandarin: tú
   kTotalStrokes: '13'
   ucn: U+5715
   --------

No library, just data
"""""""""""""""""""""

All datasets that cihai uses have stand-alone tools to export their data.
No library required.

- `unihan-etl <https://unihan-etl.git-pull.com>`_ - `UNIHAN`_ data
  exports for csv, yaml and json.

Quick links
-----------

- `Usage`_
- `Datasets`_ a full list of current and future data sets
- Python `API`_
- `2017 roadmap <https://cihai.git-pull.com/en/latest/design-and-planning/2017/spec.html>`_

.. _API: https://cihai.git-pull.com/en/latest/api.html
.. _Datasets: https://cihai.git-pull.com/en/latest/datasets.html
.. _Usage: https://cihai.git-pull.com/en/latest/usage.html

==============  ==========================================================
Python support  Python 2.7, >= 3.5, pypy
Source          https://github.com/cihai/cihai
Docs            https://cihai.git-pull.com
Changelog       https://cihai.git-pull.com/en/latest/history.html
API             https://cihai.git-pull.com/en/latest/api.html
Issues          https://github.com/cihai/cihai/issues
Travis          https://travis-ci.org/cihai/cihai
Test coverage   https://codecov.io/gh/cihai/cihai
pypi            https://pypi.python.org/pypi/cihai
OpenHub         https://www.openhub.net/p/cihai
License         MIT
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
    :target: https://readthedocs.org/projects/cihai/

.. _CJK: https://cihai.git-pull.com/en/latest/glossary.html#term-cjk
.. _UNIHAN: http://unicode.org/charts/unihan.html
.. _variants: http://www.unicode.org/reports/tr38/tr38-21.html#N10211
.. _cihai.conversion: http://cihai.git-pull.com/en/latest/api.html#conversion
.. _cihai-cli: https://cihai-cli.git-pull.com
