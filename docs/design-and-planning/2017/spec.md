---
orphan: true
---

(design-and-planning-2017-spec)=

# Internals Planning

Created 2017-04-29

1. {ref}`zero_config` - cihai should be able to work without configuration with a default data
   backend.
2. {ref}`incremental_config` cihai should be incrementally configurable, such as by specifying where
   data should be outputted.
3. {ref}`relational_backend` cihai will use [SQLAlchemy][sqlalchemy] as a database backend to story
   information for retrieval.
4. {ref}`automatic_extensions` cihai will make data accessible to third party libraries if they
   exist in the script's site-packages.

   e.g. If [pandas][pandas] is found, it will be able to return a {class}`pandas.DataFrame` for a
   queried set of information.

5. {ref}`unihan_core` cihai will use [UNIHAN][unihan] as a core and source of truth for information,
   as it contains all the glyphs and is reliable, free and well-maintained, and provides are good
   source of starter information.
6. {ref}`data_normalization` cihai will adopt a standard data format to store additional CJK data
   sets within.
7. {ref}`data_liberation` cihai libraries will be available under permissive licenses.

(zero-config)=

## Zero config

cihai will be able to be used immediately without a user configuring their system.

cihai will conform with the [XDG specification][xdg specification] for determining where to check
out data to. This includes:

- Where to store downloaded source files, e.g. _XDG_CACHE_HOME/cihai/downloads_
- Where store default backend data, e.g. _XDG_DATA_DIRS/cihai/data_, as well as the default file
  name used within, e.g. _data.sqlite_
- Where to check for configuration files, e.g. _XDG_CONFIG_HOME/cihai_, as well as the default file
  name used within, e.g. _cihai.yaml_

These default directories will be where cihai will, by default, store information and search for
configuration used in {ref}`incremental_config`.

(incremental-config)=

## Incremental configuration

The [SQLAlchemy][sqlalchemy] data backend used, which for SQLite, also includes the file path used
to store the SQLite file, is customizable.

[xdg specification]: https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html

(relational-backend)=

## Relational backend

cihai will be powered by a relational database backend.

Most python distributions include support for [SQLite][sqlite], which in conjunction with
{ref}`zero configuration <zero_config>`, makes for data store that will work across a wide array of
systems.

The data that cihai organizes will be primarily indexable by the glyph, and joined upon the glyph to
pull in an ever expanding assortment of information on that character.

(automatic-extensions)=

## Automatic extension detection

Don't reinvent the wheel, interoperate.

cihai will check for libraries such as pandas and other tabular libraries to easily produce native
objects for the user based on their cihai data lookup.

This comes at no performance penalty since the ability to export in a third party object, such as a
{class}`pandas.DataFrame`.

(unihan-core)=

## UNIHAN core

cihai's library of CJK information will be backed on the reliable [UNIHAN][unihan] database, which
is a approved by the Unicode Consortium.

### Operation

It is to be determined if UNIHAN will be vendorized in the packaging or retrieved remotely.

(data-normalization)=

## Data normalization

CJK datasets made available by cihai and contributors should follow, a yet to be determined,
standard for keeping data conserved, readily available and sustainable.

### Standards

The initial consideration, since 2013, was datasets would follow [Data Packages][data packages].

In place of Data Packages, a simpler, and more lax guideline and alone with python interfaces may be
considered. This determination is pending further review of datasets.

In place of frictionlessdata's data package libraries, cihai may option for a simpler, yet more
powerful system for making tabular data.

(data-liberation)=

## Data liberation

CC-0, MIT, ISC, BSD. Data sets should be available under licenses free from unintended side effects
of derivative creation.

[sqlite]: https://sqlite.org/
[pandas]: http://pandas.pydata.org/
[sqlalchemy]: https://www.sqlalchemy.org
[unihan]: http://www.unicode.org/reports/tr38/
[data packages]: http://frictionlessdata.io/data-packages/
