:orphan:

.. _lore/2017/spec:

==================
Internals Planning
==================

Created 2017-04-29

.. note::

    This is a draft intended for the planning of cihai.


1. :ref:`zero_config` - cihai should be able to work without configuration with a
   default data backend.
2. cihai should be incrementally configurable, such as by specifying where
   data should be outputted.
3. cihai will use SQLAlchemy as a database backend to story information
   for retrieval.
4. cihai will make data accessible to third party libraries if they exist
   in the script's site-packages.

   e.g. If pandas if found, it will be able to return a pandas table for a
   queried set of information.
5. cihai will use unihan as a core and source of truth for information, as
   it contains all the glyphs and is reliable, free and well-maintained,
   and provides are good source of starter information.
6. cihai will adopt a standard data format to store additional CJK data
   sets within.

.. _zero_config:

Zero config
-----------

cihai will be able to be used immediately without a user configuring their
system.

cihai will use the `XDG specification`_ for determining where to check out
data to. This includes:

- Where to store downloaded source files, e.g. *XDG_CACHE_HOME/cihai/downloads*
- Where store default backend data, e.g. *XDG_DATA_DIRS/cihai/data*, as
  well as the default file name used within, e.g. *data.sqlite*
- Where to check for configuration files, e.g. *XDG_CONFIG_HOME/cihai*, as
  well as the default file name used within, e.g. *cihai.yaml*

These default directories will be where cihai will, by default, store
information and search for configuration used in :ref:`incremental_configuration`.

.. _incremental_configuration:

Incremental configuration
-------------------------

The SQLAlchemy data backend used, which for SQLite, also includes the file
path used to store the sqlite file, is customizable.

.. _XDG Specification: https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html
