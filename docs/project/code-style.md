# Code Style

cihai follows consistent coding standards across all repositories in the
cihai organization.

## Formatting and linting

[ruff](https://ruff.rs) handles formatting, import sorting, and linting in a
single tool.

```console
$ uv run ruff check .
```

```console
$ uv run ruff format .
```

Auto-fix safe lint violations:

```console
$ uv run ruff check . --fix --show-fixes
```

## Type checking

[mypy](http://mypy-lang.org/) with `strict = true` is used for static type
checking.

```console
$ uv run mypy .
```

## Docstrings

Use [NumPy-style](https://numpydoc.readthedocs.io/en/latest/format.html)
docstrings with reStructuredText markup.

## Imports

- Use `from __future__ import annotations` at the top of every module.
- Use namespace imports for the standard library: `import pathlib` rather than
  `from pathlib import Path`.
- Use `import typing as t` and access members via `t.NamedTuple`, etc.
