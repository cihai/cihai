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
2. :ref:`incremental_config` cihai should be incrementally configurable, such as
   by specifying where data should be outputted.
3. :ref:`relational_backend` cihai will use SQLAlchemy as a database backend to story information
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
information and search for configuration used in :ref:`incremental_config`.

.. _incremental_config:

Incremental configuration
-------------------------

The SQLAlchemy data backend used, which for SQLite, also includes the file
path used to store the sqlite file, is customizable.

.. _XDG Specification: https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html

.. _relational_backend:

Relational backend
------------------

cihai will be bowered by a relational database backend.

Most python distributions include support for `sqlite`_, which in
conjunction with :ref:`zero configuration <zero_config>`, makes for data
store that will work across a wide array of systems.

The data that cihai organizes will be primarily indexable by the glyph,
and joined upon the glyph to pull in an ever expanding assortment of
information on that character.

.. _sqlite: https://www.sqlite.org/
