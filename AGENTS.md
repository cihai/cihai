# AGENTS.md

This file provides guidance to AI agents (including Claude Code and other LLM-powered tools) when working with code in this repository.

## CRITICAL REQUIREMENTS

### Test Success
- ALL tests MUST pass for code to be considered complete and working
- Never describe code as "working as expected" if there are ANY failing tests
- Even if specific feature tests pass, failing tests elsewhere indicate broken functionality
- Changes that break existing tests must be fixed before considering implementation complete
- A successful implementation must pass linting, type checking, AND all existing tests

## Project Overview

gp-libs (this repository) packages the **cihai** Python library, which offers programmatic access to CJK (Chinese, Japanese, Korean) data built on top of `unihan-etl` and SQLAlchemy.

Key features:
- `Cihai` application object bootstraps and manages the UNIHAN dataset
- Dataset and plugin system (`extend.py`) for adding data sources or processors
- Config templating that respects XDG base directories
- SQLAlchemy-backed storage with convenience helpers in `db.py`
- Utility helpers for conversions, constants, and logging

## Development Environment

This project uses:
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) for dependency management
- [ruff](https://github.com/astral-sh/ruff) for linting and formatting
- [mypy](https://github.com/python/mypy) for type checking
- [pytest](https://docs.pytest.org/) with doctests enabled
- [Sphinx](https://www.sphinx-doc.org/) + [Furo](https://github.com/pradyunsg/furo) for docs
- [gp-libs](https://gp-libs.git-pull.com) for shared docs/testing helpers

## Common Commands

### Setting Up Environment

```bash
# Install dependencies
uv pip install --editable .
uv pip sync

# Install with development dependencies (docs, tests, lint)
uv pip install --editable . -G dev
```

### Running Tests

```bash
# Run all tests (doctests included via pytest config)
just test
# or directly
uv run py.test

# Run a single test file
uv run py.test tests/test_core.py

# Run a specific test
uv run py.test tests/test_core.py::test_bootstrap

# Run tests with test watcher
just start
# or
uv run ptw .

# Run tests with doctests emphasized
uv run ptw . --now --doctest-modules
```

### Linting and Type Checking

```bash
# Run ruff for linting
just ruff
# or directly
uv run ruff check .

# Format code with ruff
just ruff-format
# or directly
uv run ruff format .

# Run mypy for type checking
just mypy
# or directly
uv run mypy src tests docs

# Watch mode for linting (using entr)
just watch-ruff
just watch-mypy
```

### Documentation

```bash
# Build documentation
just build-docs

# Start documentation server with auto-reload
just start-docs

# Live dev loop for docs
just dev-docs

# Update documentation CSS/JS
just design-docs
```

### Development Workflow

Follow this workflow for code changes:

1. **Format First**: `uv run ruff format .`
2. **Run Tests**: `uv run py.test`
3. **Run Linting**: `uv run ruff check . --fix --show-fixes`
4. **Check Types**: `uv run mypy`
5. **Verify Tests Again**: `uv run py.test`

## Code Architecture

cihai follows a dataset-centric design that bootstraps the UNIHAN corpus into a local SQL database and exposes a high-level API for lookups and extensions:

1. **Core** (`src/cihai/core.py`)
   - `Cihai` application object; merges config, bootstraps datasets/plugins, exposes `sql` handle.
   - Config templating via `expand_config` and XDG-aware directories.

2. **Database** (`src/cihai/db.py`)
   - SQLAlchemy engine/session setup and helpers for dataset storage.

3. **Extend** (`src/cihai/extend.py`)
   - Base classes for datasets/plugins, including SQLAlchemy mixins for shared DB access.

4. **Config & Internals** (`src/cihai/config.py`, `src/cihai/_internal/config_reader.py`)
   - Config loading/expansion from dict or YAML/JSON files; validation helpers.

5. **Data & Constants** (`src/cihai/constants.py`, `src/cihai/data/`)
   - Default configs, XDG paths, and dataset declarations for UNIHAN.

6. **Utilities** (`src/cihai/utils.py`, `src/cihai/conversion.py`, `src/cihai/log.py`, `src/cihai/types.py`)
   - Import helpers, conversion helpers, logging setup, and shared typing aliases.

7. **Exceptions** (`src/cihai/exc.py`)
   - Project-specific exception hierarchy.

## Testing Strategy

cihai uses pytest with doctests enabled via `pyproject.toml`. Key points:

- Root `conftest.py` provides fixtures that isolate `HOME`, working directory, and doctest namespace. Prefer these fixtures (`set_home`, `tmp_path`, etc.) over manual env manipulation.
- Doctests run automatically; keep examples minimal or move heavier scenarios into `tests/` or `examples/` with pytest fixtures.
- Use `pytest-watcher` (`uv run ptw .`) for continuous feedback during development.
- Favor `tmp_path` and `monkeypatch` fixtures instead of `tempfile`/`unittest.mock`.
- **Use functional tests only**: Write tests as standalone functions (`test_*`), not classes. Avoid `class TestFoo:` groupings. This applies to pytest tests, not doctests.

## Coding Standards

- Imports: prefer namespace imports for standard library (`import pathlib`) and `import typing as t`; third-party packages may use `from X import Y`; include `from __future__ import annotations` at the top of Python files.
- Docstrings: use NumPy style with reStructuredText formatting.
- Doctests: narrative style, blank lines between sections; move complex flows into dedicated tests.
- Lint/type: keep code ruff- and mypy-clean before requesting review.

## Logging Standards

These rules guide future logging changes; existing code may not yet conform.

### Logger setup

- Use `logging.getLogger(__name__)` in every module
- Add `NullHandler` in library `__init__.py` files
- Never configure handlers, levels, or formatters in library code — that's the application's job

### Structured context via `extra`

Pass structured data on every log call where useful for filtering, searching, or test assertions.

**Core keys** (stable, scalar, safe at any log level):

| Key | Type | Context |
|-----|------|---------|
| `unihan_field` | `str` | UNIHAN field name |
| `unihan_source_file` | `str` | source data file path |
| `unihan_record_count` | `int` | records processed |
| `cihai_dataset` | `str` | dataset name |
| `cihai_query` | `str` | lookup query |

**Heavy/optional keys** (DEBUG only, potentially large):

| Key | Type | Context |
|-----|------|---------|
| `unihan_stdout` | `list[str]` | subprocess stdout lines (truncate or cap; `%(unihan_stdout)s` produces repr) |
| `unihan_stderr` | `list[str]` | subprocess stderr lines (same caveats) |

Treat established keys as compatibility-sensitive — downstream users may build dashboards and alerts on them. Change deliberately.

### Key naming rules

- `snake_case`, not dotted; `unihan_` prefix
- Prefer stable scalars; avoid ad-hoc objects
- Heavy keys (`unihan_stdout`, `unihan_stderr`) are DEBUG-only; consider companion `unihan_stdout_len` fields or hard truncation (e.g. `stdout[:100]`)

### Lazy formatting

`logger.debug("msg %s", val)` not f-strings. Two rationales:
- Deferred string interpolation: skipped entirely when level is filtered
- Aggregator message template grouping: `"Running %s"` is one signature grouped ×10,000; f-strings make each line unique

When computing `val` itself is expensive, guard with `if logger.isEnabledFor(logging.DEBUG)`.

### stacklevel for wrappers

Increment for each wrapper layer so `%(filename)s:%(lineno)d` and OTel `code.filepath` point to the real caller. Verify whenever call depth changes.

### LoggerAdapter for persistent context

For objects with stable identity (Dataset, Reader, Exporter), use `LoggerAdapter` to avoid repeating the same `extra` on every call. Lead with the portable pattern (override `process()` to merge); `merge_extra=True` simplifies this on Python 3.13+.

### Log levels

| Level | Use for | Examples |
|-------|---------|----------|
| `DEBUG` | Internal mechanics, data I/O | Field parsing, record transformation steps |
| `INFO` | Data lifecycle, user-visible operations | Download completed, export finished, database bootstrapped |
| `WARNING` | Recoverable issues, deprecation, user-actionable config | Missing optional field, deprecated data format |
| `ERROR` | Failures that stop an operation | Download failed, parse error, database write failed |

Config discovery noise belongs in `DEBUG`; only surprising/user-actionable config issues → `WARNING`.

### Message style

- Lowercase, past tense for events: `"download completed"`, `"parse error"`
- No trailing punctuation
- Keep messages short; put details in `extra`, not the message string

### Exception logging

- Use `logger.exception()` only inside `except` blocks when you are **not** re-raising
- Use `logger.error(..., exc_info=True)` when you need the traceback outside an `except` block
- Avoid `logger.exception()` followed by `raise` — this duplicates the traceback. Either add context via `extra` that would otherwise be lost, or let the exception propagate

### Testing logs

Assert on `caplog.records` attributes, not string matching on `caplog.text`:
- Scope capture: `caplog.at_level(logging.DEBUG, logger="cihai.core")`
- Filter records rather than index by position: `[r for r in caplog.records if hasattr(r, "unihan_field")]`
- Assert on schema: `record.unihan_record_count == 100` not `"100 records" in caplog.text`
- `caplog.record_tuples` cannot access extra fields — always use `caplog.records`

### Avoid

- f-strings/`.format()` in log calls
- Unguarded logging in hot loops (guard with `isEnabledFor()`)
- Catch-log-reraise without adding new context
- `print()` for diagnostics
- Logging secret env var values (log key names only)
- Non-scalar ad-hoc objects in `extra`
- Requiring custom `extra` fields in format strings without safe defaults (missing keys raise `KeyError`)

## Git Commit Standards

Commit subjects: `Scope(type[detail]): concise description`

Body template:
```
why: Reason or impact.
what:
- Key technical changes
- Single topic only
```

Guidelines:
- Subject ≤50 chars; body lines ≤72 chars; imperative mood.
- One topic per commit; separate subject and body with a blank line.

Common commit types:
- **feat**: New features or enhancements
- **fix**: Bug fixes
- **refactor**: Code restructuring without functional change
- **docs**: Documentation updates
- **chore**: Maintenance (dependencies, tooling, config)
- **test**: Test-related updates
- **style**: Code style and formatting
- **py(deps)**: Dependencies
- **py(deps[dev])**: Dev dependencies
- **ai(rules[AGENTS])**: AI rule updates
- **ai(claude[rules])**: Claude Code rules (CLAUDE.md)
- **ai(claude[command])**: Claude Code command changes

#### Release commits

Never create tags. Never push tags. The user handles tagging and tag
pushes (tags trigger the CI publish workflow).

Release commit subjects are plain and short: `Tag v<version>`. Put
the detailed why/what in the commit body. Don't use the
`Scope(type[detail]):` format for releases — don't bury the lede.

## Data Considerations

- `Cihai` bootstraps the UNIHAN dataset via `unihan-etl`; tests redirect XDG data dirs to temporary locations—avoid hardcoding paths.
- Avoid network calls in tests; rely on fixtures and cached data wherever possible.
- Large data outputs should be summarized, not inlined, in tests and docs.

## Documentation Standards

### Code Blocks in Documentation

When writing documentation (README, CHANGES, docs/), follow these rules for code blocks:

**One command per code block.** This makes commands individually copyable.

**Put explanations outside the code block**, not as comments inside.

Good:

Run the tests:

```console
$ uv run pytest
```

Run with coverage:

```console
$ uv run pytest --cov
```

Bad:

```console
# Run the tests
$ uv run pytest

# Run with coverage
$ uv run pytest --cov
```

### Changelog Conventions

These rules apply when authoring entries in `CHANGES`, which is rendered as the Sphinx changelog page. Modeled on Django's release-notes shape — deliverables get titles and prose, not bullets. cihai's CHANGES already uses `#### Title (#NN)` in `### Development` and flat-bullet sections elsewhere; new entries should adopt the Django shape across all sections.

**Release entry boilerplate.** Every release header is `## cihai X.Y.Z (YYYY-MM-DD)`. The file opens with a `## cihai X.Y.Z (unreleased)` placeholder block fenced by `<!-- KEEP THIS PLACEHOLDER ... -->` and `<!-- END PLACEHOLDER ... -->` HTML comments — new release entries land immediately below the END marker, never above it.

**Open with a multi-sentence lead paragraph.** Plain prose, no italic. Open with the version as sentence subject (*"cihai X.Y.Z ships …"*) so the lead is self-contained when excerpted. Two to four sentences telling the reader what shipped and who cares — user-visible takeaways, not internal mechanism. Cross-reference detail docs with `{ref}` to keep the lead compact.

**Each deliverable is a section, not a bullet.** Inside `### What's new`, every distinct deliverable gets a `#### Deliverable title (#NN)` heading naming it in user vocabulary, followed by 1-3 prose paragraphs explaining what shipped. Don't wrap a paragraph in `- ` — bullets are for enumerable lists, not paragraph containers. Cross-link detail docs (`See {ref}\`foo\` for details.`) so prose stays focused.

**The deliverable test.** Before writing an entry, ask: "What's the deliverable, in user vocabulary?" If you can't answer in one sentence, the entry isn't ready. Mechanism (helper internals, byte counters, schema-validation locations) belongs in PR descriptions and code comments, not the changelog.

**Fixed subheadings**, in this order when present: `### Breaking changes`, `### Dependencies`, `### What's new`, `### Fixes`, `### Documentation`, `### Development`. Dev tooling (helper scripts, internal automation) lives under `### Development`. For breaking changes, show the migration path with concrete inline code (e.g. a `# Before` / `# After` fenced code block). Dependency floor bumps use the form ``Minimum `pkg>=X.Y.Z` (was `>=X.Y.W`)``.

**PR refs `(#NN)`** sit in each deliverable's `####` heading.

**When bullets are appropriate.** Catch-all sections (`### Fixes`, occasionally `### Documentation`) with 3+ genuinely small items use bullets — one line each, never paragraphs. If a bullet swells past two lines, promote it to a `#### Title (#NN)` heading with prose body.

**Anti-patterns.**

- Fragile metrics: token ceilings, third-party version pins, percent benchmarks, exact byte counts. Describe the *capability*, not the math.
- Internal jargon: private symbols (leading-underscore identifiers), algorithm names exposed for the first time, backend scaffolding.
- Walls of text dressed up as bullets.
- Buried breaking changes — they get their own subheading at the top of the entry.

**Always link autodoc'd APIs.** Any class, method, function, exception, or attribute that has its own rendered page must be cited via the appropriate role (`{class}`, `{meth}`, `{func}`, `{exc}`, `{attr}`) — never with plain backticks. Doc pages without explicit ref labels use `{doc}`. Plain backticks are correct for code syntax, env vars, parameter names, and file paths that aren't doc pages — anything without an autodoc destination.

**MyST roles.** Class references use `{class}`, methods use `{meth}`, functions use `{func}`, exceptions use `{exc}`, attributes use `{attr}`, internal anchors use `{ref}`, doc-path links use `{doc}`.

**Summarization style.** When a user asks "what changed in the latest version?" or similar, lead with the entry's lead paragraph (paraphrased if needed), followed by each `####` deliverable heading under `### What's new` with a one-sentence summary. Cite `(#NN)` only if the user asks for source links. Don't invent versions, dates, or numbers not present in `CHANGES`. Don't quote line numbers or file offsets — those shift as the file evolves.

## Debugging Tips

When stuck:
- Minimize to a failing MVP test; remove noisy debugging.
- Document findings briefly before iterating.
- Prefer small, reversible changes and keep the test loop fast (`ptw`).

## References

- Documentation: https://cihai.git-pull.com/
- API Reference: https://cihai.git-pull.com/api/
- Release notes: CHANGES
- Issue tracker/Q&A: https://github.com/cihai/cihai

## Shipped vs. Branch-Internal Narrative

Long-running branches accumulate tactical decisions — renames,
refactors, attempts-then-reverts, intermediate states. Commit messages
and the diff hold *what changed* and *why*. Do not restate either in
artifacts the downstream reader holds: code, docstrings, README,
CHANGES, PR descriptions, release notes, migration guides.

When deciding what counts as branch-internal, use trunk or the parent
branch as the baseline — not intermediate states inside the current
branch.

**The Published-Release Test**

Before adding rename history, "previously" / "formerly" / "no longer
X" phrasing, "removed" / "moved" / "refactored" / "fixed" diff
paraphrases, or `### Fixes` entries to a user-facing surface, ask:

> Did users of the most recently published release ever experience
> this old name, old behavior, or bug?

If the answer is no, it is branch-internal narrative. Move it to the
commit message and describe only the current state in the artifact.

**Keep in shipped artifacts**

- Deprecations and migration guides for symbols that actually shipped.
- `### Fixes` entries for bugs that affected users of a published
  release.
- Comments explaining *why the current code looks this way* —
  invariants, platform quirks, upstream bug workarounds — that make
  sense to a reader who never saw the previous version.

**Default**: when in doubt, keep the artifact clean and put the story
in the commit.

### Cleanup in Hindsight

When applying this rule retroactively from inside a feature branch,
first establish scope by diffing against the parent branch (or trunk)
to identify which commits this branch actually introduced. Then:

- **Commits introduced in this branch** — prompt the user with two
  options: `fixup!` commits with `git rebase --autosquash` to address
  each causal commit at its source, or a single cleanup commit at
  branch tip. User chooses.
- **Commits already in trunk or a parent branch** — default to
  leaving them alone. Do not raise them as cleanup candidates; act
  only on explicit user instruction. If the user opts in, fold the
  cleanup into a single commit at branch tip and do not rewrite trunk
  or parent-branch history.
- **Scope guard** — if cleaning in-branch bleed would touch a
  colleague's in-flight work or expand the branch beyond its stated
  goal, default to staying in lane: protect the project's current
  goal, leave prior bleed alone, and don't introduce new bleed in the
  current change.
