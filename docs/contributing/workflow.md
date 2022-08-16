(developing)=

(workflow)=

# Development workflow

:::{note}

This guide applies to all cihai projects, not just the cihai repo.

:::

Cihai projects use standard conventions and patterns based on best practices in python.

To be efficient at debugging, developing, testing, documenting, etc. it helps to familiarize yourself with the tool within, independently if needed.

`<cihai-project>` can be assumed to be an existing or future cihai project, including 
[cihai](https://github.com/cihai/cihai),
[cihai-cli](https://github.com/cihai/cihai-cli),
[unihan-etl](https://github.com/cihai/unihan-etl),
[unihan-db](https://github.com/cihai/unihan-db). 
See [GitHub](https://github.com/cihai), [GitLab](https:/gitlab.com/cihai) and
[Codeberg](https://codeberg.org/cihai).

## Development environment

[poetry] is a required package to develop.

```console
$ git clone https://github.com/cihai/<cihai-project>.git
```

```console
$ cd <cihai-project>
```

So if `<cihai-project>` is [cihai]:

```console
$ git clone https://github.com/cihai/cihai.git
```

```console
$ cd cihai
```

## Install dependencies

```console
$ poetry install -E "docs test coverage lint format"
```

Makefile commands prefixed with `watch_` will watch files and rerun.

## Tests

[pytest] is used for tests.

```console
$ poetry run py.test
```

### Rerun on file change

via [pytest-watcher] (works out of the box):

```console
$ make start
```

via [`entr(1)`] (requires installation):

```console
$ make watch_test
```

[pytest-watcher]: https://github.com/olzhasar/pytest-watcher

### Manual (just the command, please)

```console
$ poetry run py.test
```

or:

```console
$ make test
```

### pytest options

_For filename / test names within, examples will be for [cihai], if using a
different cihai project check the filename and test names accordingly_:

`PYTEST_ADDOPTS` can be set in the commands below. For more
information read [docs.pytest.com] for the latest documentation.

[docs.pytest.com]: https://docs.pytest.org/

Verbose:

```console
$ env PYTEST_ADDOPTS="-verbose" make start
```

Pick a file:

```console
$ env PYTEST_ADDOPTS="tests/test_cihai.py" poetry run make start
```

Drop into `test_cihai_version()` in `tests/test_cihai.py`:

```console
$ env PYTEST_ADDOPTS="-s -x -vv tests/test_cihai.py" poetry run make start
```

Drop into `test_cihai_version()` in `tests/test_cihai.py` and stop on first error:

```console
$ env PYTEST_ADDOPTS="-s -x -vv tests/test_cihai.py::test_cihai" poetry run make start
```

Drop into `pdb` on first error:

```console
$ env PYTEST_ADDOPTS="-x -s --pdb" make start
```

If you have [ipython] installed:

```console
$ env PYTEST_ADDOPTS="--pdbcls=IPython.terminal.debugger:TerminalPdb" make start
```

[ipython]: https://ipython.org/

```console
$ make test
```

You probably didn't see anything but tests scroll by.

If you found a problem or are trying to write a test, you can file an
on the tracker for the relevant cihai project.

(test-specific-tests)=

### Manual invocation

Test only a file:

```console
$ py.test tests/test_cihai.py
```

will test the `tests/test_cihai.py` tests.

```console
$ py.test tests/test_cihai.py::test_cihai_version
```

tests `test_cihai_version()` inside of `tests/test_cihai.py`.

Multiple can be separated by spaces:

```console
$ py.test tests/test_{conversion,exc}.py tests/test_config.py::test_configurator
```

## Documentation

[sphinx-autobuild] will automatically build the docs, watch for file changes and launch a server.

From home directory: `make start_docs` From inside `docs/`: `make start`

[sphinx-autobuild]: https://github.com/executablebooks/sphinx-autobuild

### Manual documentation (the hard way)

`cd docs/` and `make html` to build. `make serve` to start http server.

Helpers: `make build_docs`, `make serve_docs`

Rebuild docs on file change: `make watch_docs` (requires [entr(1)])

Rebuild docs and run server via one terminal: `make dev_docs` (requires above, and a `make(1)` with
`-J` support, e.g. GNU Make)

### View documentation locally

To find the URL of the preview server, read the terminal, the URL may very
depending on the project! An example of what to look for:

```console
[I 220816 14:43:41 server:335] Serving on http://127.0.0.1:8035
```

## Formatting

The project uses [black] and [isort] (one after the other). Configurations are in `pyproject.toml`
and `setup.cfg`:

- `make black isort`: Run `black` first, then `isort` to handle import nuances

## Linting

[flake8] and [mypy] run via CI in our GitHub Actions. See the configuration in `pyproject.toml` and
`setup.cfg`.

### flake8

[flake8] provides fast, reliable, barebones styling and linting.

````{tab} Command

poetry:

```console
$ poetry run flake8
```

If you setup manually:

```console
$ flake8
```

````

````{tab} make

```console
$ make flake8
```

````

````{tab} Watch

```console
$ make watch_flake8
```

requires [`entr(1)`].

````

````{tab} Configuration

See `[flake8]` in setup.cfg.

```{literalinclude} ../../setup.cfg
:language: ini
:start-at: "[flake8]"
:end-before: "[isort]"

```

````

### mypy

[mypy] is used for static type checking.

````{tab} Command

poetry:

```console
$ poetry run mypy .
```

If you setup manually:

```console
$ mypy .
```

````

````{tab} make

```console
$ make mypy
```

````

````{tab} Watch

```console
$ make watch_mypy
```

requires [`entr(1)`].
````

## Releasing

Since this software used in production projects, we don't want to release breaking changes.

Choose what the next version is. Assuming it's version 0.9.0, it could be:

- 0.9.0post0: postrelease, if there was a packaging issue
- 0.9.1: bugfix / security / tweak
- 0.10.0: breaking changes, new features

Let's assume we pick 0.9.1

`CHANGES`: Assure any PRs merged since last release are mentioned. Give a thank you to the
contributor. Set the header with the new version and the date. Leave the "current" header and
_Insert changes/features/fixes for next release here_ at the top:

```markdown
package-name 0.10.x (unreleased)
--------------------------------
- *Insert changes/features/fixes for next release here*

package-name 0.9.1 (2020-10-12)
-------------------------------
- :issue:`1`: Fix bug
```

`package_name/__init__.py` and `__about__.py` - Set version

```console
$ git commit -m 'Tag v0.9.1'
```

```console
$ git push
```

Important: Create and push the tag. Make sure the version is correct and the
`pyproject.toml` and `__about__.py` match the version being deployed.

```console
$ git tag v0.9.1
```

```console
$ git push --tags
```

### Automated deployment

CI will automatically push to the PyPI index when a tag is pushed.

### Manual deployment

:::{note}

This requires PyPI access.

:::

In addition to virtualenv creation and installing dependencies, [poetry] handles
building the package and publishing. Therefore there is no setup.py or requirements files.

```console
$ poetry build
```

```console
$ poetry deploy
```

[poetry]: https://python-poetry.org/
[entr(1)]: http://eradman.com/entrproject/
[`entr(1)`]: http://eradman.com/entrproject/
[black]: https://github.com/psf/black
[isort]: https://pypi.org/project/isort/
[flake8]: https://flake8.pycqa.org/
[mypy]: http://mypy-lang.org/
