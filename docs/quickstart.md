(quickstart)=

# Quickstart

cihai is designed to work out-of-the-box without configuration.

## Installation

```console
$ pip install --user cihai
```

## First lookup

Most projects start with {class}`cihai.core.Cihai`, bootstrap the
{attr}`~cihai.core.Cihai.unihan` dataset once, then query it with
{meth}`~cihai.data.unihan.dataset.Unihan.lookup_char` or
{meth}`~cihai.data.unihan.dataset.Unihan.reverse_char`.

This script is also tested by `tests/test_examples.py`.

```{literalinclude} ../examples/basic_usage.py
:language: python

```

(developmental-releases)=

### Developmental releases

New versions of cihai are published to PyPI as alpha, beta, or release candidates.
Identifiers like `a1`, `b1`, and `rc1` mark alpha, beta, and release candidates, respectively.

- [pip]\:

  ```console
  $ pip install --user --upgrade --pre cihai
  ```

- [pipx]\:

  ```console
  $ pipx run --pip-args '\--pre' --spec 'cihai' python -c "import cihai; print(cihai.__version__)"
  ```

- [uv]\:

  ```console
  $ uv add cihai --prerelease allow
  ```

- [uvx]\:

  ```console
  $ uvx --from 'cihai' --prerelease allow python -c "import cihai; print(cihai.__version__)"
  ```

(configuration)=

## Configuration

By default, cihai requires no configuration. The defaults file locations are
{term}`XDG Base Directory` for the users' system, as well as SQLite to store, seek, and retrieve
data.

You can override cihai's default storage and file directories via a config file.

The default configuration is at {data}`cihai.constants.DEFAULT_CONFIG`.

Database configuration accepts any SQLAlchemy {external+sqlalchemy:ref}`database_urls`. If you're
using a DB other than SQLite, such as Postgres, be sure to install the requisite driver, such as
[psycopg][psycopg].

[xdg directories]: https://specifications.freedesktop.org/basedir-spec/basedir-spec-0.6.html

### Advanced Config

cihai is designed to allow you to incrementally override settings to your liking.

Internally, the config is parsed through {func}`cihai.config.expand_config`. This will replace
environment variables, XDG variables and tildes. You can also enter absolute paths.

Environmental variables require a dollar sign added to them, e.g. `${ENVVAR}`. XDG variables such as
_user_cache_dir_, _user_config_dir_, _user_data_dir_, _user_log_dir_, _site_config_dir_,
_site_data_dir_ are done via curly brackets only. E.g. `{site_config_dir}`. Tildes are just
replaced.

```{code-block} yaml

database:
  url: '${DATABASE_URL}'
dirs:
  data: '{user_data_dir}/mydata'
  cache: '~/cache/cihai'
  logs: '$ENVVAR/logs'

```

In the example above, Heroku's
[DATABASE_URL](https://devcenter.heroku.com/articles/heroku-postgresql#establish-primary-db) is
replaced as an environmental variable. The XDG variable for _user_data_dir_ is combined with
_mydata/_, which makes the data stored deeper. The environmental variable _$ENVVAR_ is also
replaced.

You may point to a custom config with {meth}`cihai.core.Cihai.from_file`.

You can also override bootstrapping settings. Pass a `unihan_options` dictionary to
{meth}`~cihai.data.unihan.dataset.Unihan.bootstrap`; the dictionary is passed to
{ref}`unihan-etl:index`'s {class}`unihan_etl.core.Packager` `option` param, which is
then merged on top of unihan-etl's default settings:

The `source` value can also point to a local path. You can use `fields` or `input_files` to narrow
the imported UNIHAN data.

```{code-block} yaml

unihan_options:
   source: 'https://custom-mirror.com/Unihan.zip'
   work_dir: '/path/to/unzip/files'
   zip_path: '/path/to/store/Unihan.zip'
   fields: ['kDefinition']
   input_files: ['Unihan_Readings.txt']

```

See {doc}`how-to/configuration` for a tested configuration-file example.

[psycopg]: http://initd.org/psycopg/
[pip]: https://pip.pypa.io/en/stable/
[pipx]: https://pypa.github.io/pipx/docs/
[uv]: https://docs.astral.sh/uv/
[uvx]: https://docs.astral.sh/uv/guides/tools/
