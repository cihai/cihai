# AGENTS.md

cihai is a Python library for CJK (Chinese, Japanese, Korean) character
data: it bootstraps the UNIHAN dataset into a local SQL database and exposes
a dataset/plugin API for lookups and extensions.

Follow the conventions already in the tree, and keep a change scoped to what
was asked for.

## What is here

| Path                          | What it is                                        |
| ------------------------------ | -------------------------------------------------- |
| `src/cihai/core.py`            | `Cihai` app object: bootstraps datasets/plugins, exposes `sql` |
| `src/cihai/data/unihan/`       | UNIHAN dataset: `bootstrap`, `lookup_char`, `reverse_char` |
| `src/cihai/extend.py`          | `Dataset` / `DatasetPlugin` base classes            |
| `src/cihai/db.py`              | SQLAlchemy engine and session setup                |
| `src/cihai/config.py`, `_internal/config_reader.py` | Config loading and expansion |
| `src/cihai/constants.py`       | Default config, XDG paths                          |
| `src/cihai/conversion.py`, `utils.py`, `log.py`, `types.py` | Conversion, import helpers, logging, shared types |
| `src/cihai/exc.py`             | Exception hierarchy                                |
| `examples/`                    | Runnable scripts; `tests/test_examples.py` executes them |
| `tests/`                       | pytest suite; `conftest.py` holds the shared fixtures |
| `docs/`                        | Sphinx documentation source                        |
| `CHANGES`                      | Changelog, rendered at `docs/history.md`           |

## Which policy applies

- Documentation, user-facing text, `CHANGES`, commit messages, docstrings,
  source comments, and log messages:
  [.github/WRITING.md](.github/WRITING.md)
- Environment, the gates, tests, documentation builds, releases, and pull
  requests: [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)

Each of those is the single home for its subject. Where a rule seems to be
stated twice, the file listed above is the one that governs.

## Change discipline

- Make the smallest coherent change that solves the verified problem; keep
  unrelated cleanup out of it.
- Reuse an existing file, helper, API, or test before adding a new one.
- Add a file only for a durable boundary — a distinct responsibility,
  independent reuse, or splitting an oversized module — not for a
  single-use helper or a one-line re-export.
- Add a test for every user-visible behaviour change, and a `CHANGES` entry
  for every change to the public API, CLI, configuration, or output.
- A passing gate is evidence only once it has been shown capable of
  failing. Pair a new test with a deliberate break that proves it bites.

cihai bootstraps UNIHAN into one local SQL database per `Cihai` instance;
tests and doctests redirect `HOME` and XDG paths to a temporary location so
they never touch a real one — see
[Tests](.github/CONTRIBUTING.md#tests). `unihan-etl` owns the UNIHAN data
pipeline itself; `cihai` only consumes it.

## References

- Documentation: <https://cihai.git-pull.com>
- API reference: <https://cihai.git-pull.com/api/>
- Changelog: `CHANGES`
- Issue tracker: <https://github.com/cihai/cihai/issues>
- Upstream data pipeline: <https://github.com/cihai/unihan-etl>
