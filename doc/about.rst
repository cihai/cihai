.. _cihai:
   
About cihai
===========

cihai is a loose set of tools aimed at helping developers access CJKV
information.

I'm creating this tool to help me with CJKV-related projects. In the
process, I want to see that my generic efforts can be helpful to the
public. This is me open sourcing these components. I hope that they
can be of assistance and those who find it useful can contribute back.


- Python

  - General respect as a scripting language
  - Unicode support (via ``unicode_literals`` Python 2.x, by default in
    Python 3.x)
  - Nice documentation tools
    Sphinx
  - Cross-platform
    This avoids shell-scripts which may work on one system, but fail on a
    BSD system that lacks Bash.
  - Nice standard library
  - Nice support libraries: SQLAlchemy makes it easy to drop-in into
    SQLite as a backend

- UNIHAN as a core of data

  Unihan is bootstrapped by default on cihai.

  - Code points and variants
  - Already includes various reputable data sources

- Minimal buy-in

  cihai is not meant to be a land-locked set of tools. For instance,
  unihan-etl is available as a standalone export tool for the UNIHAN
  database, as well as a used as a library script within cihai itself.

  The idea is to create really high quality tooling, with a high bar
  for documentation.

  Goals:

  - Zero-configuration
    cihai works out of the box. It downloads UNIHAN and installs it for
    you.
  - Configurable
    Defaults can be overridden.
  - Provide tested, working examples
  - Provide high quality, documented internals
  - Make extras optional
  - Where it makes sense, adopt and conform to standards

    For instance, use of UNIHAN as a core provides a reputable spine of
    data to work with CJKV information.

    In addition, adoption of respected libraries that have documentation,
    and help available online. For instance, the python standard library,
    and if SQL is used, SQLAlchemy has documentation too.

    Many systems include python by default. Of those installations, most
    include `SQLite built-in <https://docs.python.org/3/library/sqlite3.html>`__.
