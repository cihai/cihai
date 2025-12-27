(contributing)=

(developing)=

(workflow)=

# Contributing

As an open source project, all cihai projects accept contributions through GitHub, GitLab and Codeberg. Below you will find
resources on the internals of the project.

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

[uv] is a required package to develop.

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
$ uv sync --all-extras --dev
```

Justfile commands prefixed with `watch-` will watch files and rerun.

## Tests

[pytest] is used for tests.

```console
$ uv run py.test
```

### Rerun on file change

via [pytest-watcher] (works out of the box):

```console
$ just start
```

via [`entr(1)`] (requires installation):

```console
$ just watch-test
```

[pytest-watcher]: https://github.com/olzhasar/pytest-watcher

### Manual (just the command, please)

```console
$ uv run py.test
```

or:

```console
$ just test
```

### pytest options

_For filename / test names within, examples will be for [cihai], if using a
different cihai project check the filename and test names accordingly_:

`PYTEST_ADDOPTS` can be set in the commands below. For more
information read [docs.pytest.com] for the latest documentation.

[docs.pytest.com]: https://docs.pytest.org/

Verbose:

```console
$ env PYTEST_ADDOPTS="-verbose" just start
```

Pick a file:

```console
$ env PYTEST_ADDOPTS="tests/test_cihai.py" just start
```

Drop into `test_cihai_version()` in `tests/test_cihai.py`:

```console
$ env PYTEST_ADDOPTS="-s -x -vv tests/test_cihai.py" just start
```

Drop into `test_cihai_version()` in `tests/test_cihai.py` and stop on first error:

```console
$ env PYTEST_ADDOPTS="-s -x -vv tests/test_cihai.py::test_cihai" just start
```

Drop into `pdb` on first error:

```console
$ env PYTEST_ADDOPTS="-x -s --pdb" just start
```

If you have [ipython] installed:

```console
$ env PYTEST_ADDOPTS="--pdbcls=IPython.terminal.debugger:TerminalPdb" just start
```

[ipython]: https://ipython.org/

```console
$ just test
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

From home directory: `just start-docs` From inside `docs/`: `just start`

[sphinx-autobuild]: https://github.com/executablebooks/sphinx-autobuild

### Manual documentation (the hard way)

`cd docs/` and `just html` to build. `just serve` to start http server.

Helpers: `just build-docs`, `just serve-docs`

Rebuild docs on file change: `just watch-docs` (requires [entr(1)])

Rebuild docs and run server via one terminal: `just dev-docs`

### View documentation locally

To find the URL of the preview server, read the terminal, the URL may very
depending on the project! An example of what to look for:

```console
[I 220816 14:43:41 server:335] Serving on http://127.0.0.1:8035
```

## Formatting / Linting

### black

[black] is used for formatting.

````{tab} Command

uv:

```console
$ uv run black .
```

If you setup manually:

```console
$ black .
```

````

In the future, `ruff` (below) may replace black as formatter.

### ruff

The project uses [ruff] to handle sorting imports and linting.

````{tab} Command

uv:

```console
$ uv run ruff
```

If you setup manually:

```console
$ ruff check .
```

````

````{tab} just

```console
$ just ruff
```

````

````{tab} Watch

```console
$ just watch-ruff
```

requires [`entr(1)`].

````

````{tab} Fix files

uv:

```console
$ uv run ruff check . --fix
```

If you setup manually:

```console
$ ruff check . --fix
```

````

### mypy

[mypy] is used for static type checking.

````{tab} Command

uv:

```console
$ uv run mypy .
```

If you setup manually:

```console
$ mypy .
```

````

````{tab} just

```console
$ just mypy
```

````

````{tab} Watch

```console
$ just watch-mypy
```

requires [`entr(1)`].
````

## Releasing

Since this software used in production projects, we don't release breaking changes
until there's a major feature release.

Choose what the next version is. Assuming it's version 0.9.0, it could be:

- 0.9.0post0: postrelease, if there was a packaging issue
- 0.9.1: bugfix / security / tweak
- 0.10.0: breaking changes, new features

Let's assume we pick 0.9.1

`CHANGES`: Assure any PRs merged since last release are mentioned. Give a thank you to the
contributor. Set the header with the new version and the date. Leave the "current" header and
_Insert changes/features/fixes for next release here_ at the top:

```markdown
## package-name 0.10.x (unreleased)

- _Insert changes/features/fixes for next release here_

## package-name 0.9.1 (2020-10-12)

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

[uv] handles virtualenv creation, package requirements, versioning,
building, and publishing. Therefore there is no setup.py or requirements files.

Update `__version__` in `__about__.py` and `pyproject.toml`::

    git commit -m 'build(cihai): Tag v0.1.1'
    git tag v0.1.1
    git push
    git push --tags

GitHub Actions will detect the new git tag, and in its own workflow run `uv
build` and push to PyPI.

[uv]: https://github.com/astral-sh/uv
[entr(1)]: http://eradman.com/entrproject/
[`entr(1)`]: http://eradman.com/entrproject/
[black]: https://github.com/psf/black
[ruff]: https://ruff.rs
[mypy]: http://mypy-lang.org/
