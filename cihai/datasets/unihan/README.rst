Standards
---------

Follows `datapackages`_ format.

- `datapackage.json format`_ - has metadata for source file
- `json table schema`_ - ``datapackage.json`` schema information.
- `simple data format`_ - ``scripts/process.py`` produces ``data/unihan.csv``
- *(optional)* `PEP 301: python package format`_ - python package installation.
- *(optional)* `cihai dataset API`_  - python client API ``setup.py``.

Structure
---------

.. code-block:: bash

    # dataset metadata, schema information.
    datapackage.json

    # (future) when this package is stable, unihan.csv will be provided
    data/unihan.csv

    # script to download dataset and convert to clean CSV.
    scripts/process.py

    # cihai's python related modules, public-facing python API.
    __init__.py

    # unihan module code
    unihan.py


Cihai is *not* required for:

- ``data/unihan.csv`` - `simple data format`_ compatible csv file.
- ``scripts/process.py`` - create a ``data/unihan.csv``.

When this module is stable, ``data/unihan.csv`` will have prepared
releases, without requires using ``scripts/process.py``. ``process.py``
will not require external libraries.

Intended usage
--------------

(Not ready)

.. code-block:: bash

    $ ./scripts/process.py

Creates ``data/unihan.csv``.

Examples
--------

- https://github.com/datasets/gdp
- https://github.com/datasets/country-codes

Related links:

- CSV *Simple Data Format* (SDF): http://data.okfn.org/standards/simple-data-format
- Tools: http://data.okfn.org/tools

.. _datapackages: http://dataprotocols.org/data-packages/
.. _datapackage.json format: https://github.com/datasets/gdp/blob/master/datapackage.json
.. _json table schema: http://dataprotocols.org/json-table-schema/
.. _simple data format: http://data.okfn.org/standards/simple-data-format
.. _cihai dataset API: http://cihai.readthedocs.org/en/latest/extending.html
.. _PEP 301\: python package format: http://www.python.org/dev/peps/pep-0301/
