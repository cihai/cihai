Follows `datapackages`_ format.

- `datapackage.json format`_
- `json table schema`_ 

Structure
---------

.. code-block::

    # dataset metadata, schema information.
    datapackage.json

    # (future) when this package is stable, unihan.csv will be provided
    data/unihan.csv

    # script to download dataset and convert to clean CSV.
    scripts/process.py

    # cihai's python related modules
    __init__.py

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
