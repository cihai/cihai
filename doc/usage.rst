.. _usage:

=====
Usage
=====

cihai is designed to work out-of-the-box without configuration.

Installation
------------

.. code-block:: sh

   $ pip install --user cihai

Configuration
-------------

By default, cihai relies on the XDG directories on the users' system, as
well as SQLite to store, seek, and retrieve the data.

Set up config to point to a database you want to import datasets into (and
read from).

.. code-block:: yaml

   debug: True
   database:
     url: 'sqlite:///${data_dir}/cihai.db'  # sqlalchemy db url
   datasets:
     - 'cihai.datasets.unihan'

Then you may point to the config with the ``-c`` argument,
``$ cihai -c path/to/config.yaml``.

