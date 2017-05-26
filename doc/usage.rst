.. _usage:

=====
Usage
=====

cihai is designed to work out-of-the-box without configuration.

Installation
------------

.. code-block:: sh

   $ pip install --user cihai

.. _configuration:

Configuration
-------------

By default, cihai requires no configuration. The defaults file locations
are :term:`XDG Base Directory` for the users' system, as well as SQLite to store,
seek, and retrieve data.

You can override cihai's default storage and file directories via a config
file.

The default configuration is at :attr:`cihai.conf.DEFAULT_CONFIG`.

Database configuration accepts any SQLAlchemy :sqlalchemy:ref:`database_urls`.
If you're using a DB other than SQLite, such as Postgres, be sure to
install the requisite driver, such as `psycopg`_.

.. _XDG directories: https://specifications.freedesktop.org/basedir-spec/basedir-spec-0.6.html

Advanced Config
"""""""""""""""

cihai is designed to allow you to incrementally override settings to your
liking.

Internally, the config is parsed through :func:`cihai.conf.expand_config`.
This will replace environment variables, XDG variables and tildes. You can
also enter absolute paths.

Environmental variables require a dollar sign added to them, e.g.
``${ENVVAR}``. XDG variables such as *user_cache_dir*, *user_config_dir*, 
*user_data_dir*, *user_log_dir*, *site_config_dir*, *site_data_dir* are
done via curly brackets only. E.g. ``{site_config_dir}``. Tildes are just
replaced.

.. code-block:: yaml
   
   database:
     url: '${DATABASE_URL}'
   dirs:
     data: '{user_cache_dir}/mydata'
     cache: '~/cache/cihai'
     logs: '$ENVVAR/logs'

In the example above, Heroku's `DATABASE_URL <https://devcenter.heroku.com/articles/heroku-postgresql#establish-primary-db>`_
is replaced as an environmental variable. The XDG variable for *user_cache_dir*
is combined with *mydata/*, which makes the data stored deeper. The
environmental variable *$ENVVAR* is also replaced.

You may point to a custom config with the ``-c`` argument,
``$ cihai -c path/to/config.yaml``.

You can also override bootstrapping settings. The "unihan_options"
dictionary in Cihai's configuration will be passed right to
:ref:`unihan-etl:index`'s :class:`unihan_etl.process.Packager`
``option`` param, which is then merged on top of unihan-etl's default
settings:

.. code-block:: yaml
   
   unihan_options:
      source: 'https://custom-mirror.com/Unihan.zip'  # local paths work too
      work_dir: '/path/to/unzip/files'
      zip_path: '/path/to/store/Unihan.zip'
      fields: ['kDefinition']  # and / or:
      input_files: ['Unihan_Readings.txt']

.. _psycopg: http://initd.org/psycopg/
