# Contributing

Thanks for looking. Bug reports with a reproduction, and notes on where the
documentation misled you, are the most useful contributions right now.

How this project writes prose — README, `CHANGES`, commit messages,
docstrings, source comments, log messages, and documentation under `docs/`
— is set out separately in [WRITING.md](WRITING.md). Read that before
changing any of it. The constraints every change is held to, and the map of
what is where, are in [AGENTS.md](../AGENTS.md).

## Getting set up

```console
$ git clone https://github.com/cihai/cihai.git
```

```console
$ cd cihai
```

```console
$ uv sync --all-extras --dev
```

`justfile` commands prefixed `watch-` watch files and rerun on change,
requiring [`entr(1)`](https://eradman.com/entrproject/). `just start` and
`just start-docs` watch without it, via `pytest-watcher` and
`sphinx-autobuild` respectively.

## The gates

CI is the order of record — `.github/workflows/tests.yml` runs all four, and
every one has to pass before a change is done. A change is not complete
while any test fails, even one unrelated to what you touched.

Format:

```console
$ uv run ruff format .
```

Lint:

```console
$ uv run ruff check . --fix --show-fixes
```

`ruff`'s isort rule requires `from __future__ import annotations` at the
top of every module (`required-imports` in `pyproject.toml`) and enforces
import order; it does not enforce namespace-style imports for the standard
library, so keep that by hand: `import pathlib`, not
`from pathlib import Path`; `import typing as t`, then `t.NamedTuple` and
friends. Third-party packages may use `from x import y`.

Type-check:

```console
$ uv run mypy .
```

`[tool.mypy]` sets `strict = true`. It also scopes a bare `uv run mypy` to
`src/` and `tests/` only; CI's explicit `uv run mypy .` also reaches
`docs/conf.py` and `examples/`. Run the CI form.

Test:

```console
$ uv run pytest
```

`uv run py.test` and `just test` run the same suite.

Documentation is a gate, not a courtesy. Examples in docstrings and under
`docs/` are executed by `pytest`; the doctest flags live in
`pyproject.toml`, so there is no separate doctest step and a green `pytest`
is the proof. Which blocks qualify, and the one mistake that silently
removes a test, are in
[WRITING.md](WRITING.md#documented-examples-that-run).

Before claiming a test or a gate works, show it failing. A gate that has
never been red is an assumption.

## Tests

The root `conftest.py` provides fixtures that isolate `HOME`, the working
directory, and the doctest namespace:

- `set_home` redirects `HOME` to a temporary user directory. It runs
  automatically for every doctest and is available to any test.
- `tmp_path` is injected into `doctest_namespace`, so a doctest may use it
  without importing or constructing it.
- `cwd_default` chdirs into a temporary path for every test.

Prefer these fixtures over manual `HOME`/environment manipulation or
`tempfile`.

- Favor `tmp_path` and `monkeypatch` over `tempfile` and `unittest.mock`.
- **Functional tests only.** Write tests as standalone `test_*` functions,
  not `class TestFoo:` groupings. This applies to pytest tests, not
  doctests.
- `Cihai` bootstraps the UNIHAN dataset via `unihan-etl`; tests redirect XDG
  data directories to temporary locations — do not hardcode a path.
- Avoid network calls in tests; rely on fixtures and cached data.
- Summarize large data outputs in tests and docs rather than inlining them.
- Use `uv run ptw .` (or `just start`) for a continuous test loop during
  development.

Pick a single file or test with `PYTEST_ADDOPTS`:

```console
$ env PYTEST_ADDOPTS="tests/test_cihai.py::test_cihai_version" \
    just start
```

Drop into `pdb` on first failure:

```console
$ env PYTEST_ADDOPTS="-x -s --pdb" just start
```

With [IPython](https://ipython.org/) installed, use its debugger instead:

```console
$ env PYTEST_ADDOPTS="--pdbcls=IPython.terminal.debugger:TerminalPdb" \
    just start
```

When stuck: minimize to a failing MVP test, remove noisy debugging output,
and keep the test loop fast with `ptw`.

## Documentation

[sphinx-autobuild] builds the docs, watches for changes, and serves them.

From the project root:

```console
$ just start-docs
```

To build once without serving:

```console
$ just build-docs
```

To serve an already-built copy:

```console
$ just serve-docs
```

To watch and serve in one terminal:

```console
$ just dev-docs
```

[sphinx-autobuild]: https://github.com/executablebooks/sphinx-autobuild

Cross-references and MyST roles (`{class}`, `{meth}`, `{ref}`, `{doc}`, and
the rest) follow
[WRITING.md](WRITING.md#documentation-cross-references). `just build-docs`
catches a broken cross-reference before you commit; the doctests do not.

## Releasing

Never create tags. Never push tags. The owner handles tagging and tag
pushes, because a tag triggers the publish workflow. See
[Release commits](WRITING.md#release-commits).

Since cihai is used in production projects, breaking changes are deferred
until a major feature release. Given a current version of `0.38.0`:

- `0.38.0post0` — post-release, packaging fix only
- `0.38.1` — bugfix, security, or tweak
- `0.39.0` — new features or breaking changes

Release checklist:

1. Update `CHANGES` — every merged PR since the last tag is listed, the
   header is set to the new version and today's date, and the *unreleased*
   placeholder stays at the top.
2. Bump the version in `pyproject.toml` and `src/cihai/__about__.py`.
3. Commit, tag, and push:

```console
$ git commit -m 'Tag v0.38.1'
```

```console
$ git tag v0.38.1
```

```console
$ git push
```

```console
$ git push --tags
```

GitHub Actions detects the new tag and runs `uv build` followed by a
publish to PyPI. If CI is unavailable, `uv build` then `uv publish` do the
same from a local checkout.

The full checklist and version-numbering rationale live at
[docs/project/releasing.md](https://cihai.git-pull.com/project/releasing.html).

## Pull requests

One subject per pull request. Unrelated cleanup found along the way belongs
in its own commit, and usually in its own pull request.

Discuss a substantial change via an issue before making it.

Commit format is in [WRITING.md](WRITING.md#commits).

## Decorum

- Participants will be tolerant of opposing views.
- Participants must ensure that their language and actions are free of
  personal attacks and disparaging personal remarks.
- When interpreting the words and actions of others, participants should
  always assume good intentions.
- Behaviour which can be reasonably considered harassment will not be
  tolerated.

Based on
[Ruby's Community Conduct Guideline](https://www.ruby-lang.org/en/conduct/).

## Security

Please do not open a public issue for a vulnerability. This repository has
no `SECURITY.md`; report privately via the Security tab at
<https://github.com/cihai/cihai/security>, which offers a private advisory
report if the maintainers have enabled it.
