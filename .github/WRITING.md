# Writing

How this project writes prose, for humans and agents alike. It governs
`README.md`, `CHANGES`, commit messages, docstrings, source comments, log
messages, and documentation under `docs/` — every surface a reader reaches.

For environment setup, the gates, and pull request workflow, see
[CONTRIBUTING.md](CONTRIBUTING.md).

## Voice

Three surfaces, one voice. A docstring says what a caller may rely on; a
`CHANGES` entry says what changed; prose says what happens. All three are
present tense, lead with the thing being described, and stop. Why it was built
that way belongs in the commit message, which is timestamped and attached to
the diff.

The most useful editing operation is deleting the introductory sentence.

Lead with verbs and name concrete things. Put identifiers in backticks. Prefer
short declarative sentences, one operational fact each. Do not explain Python
to Python developers; do explain this project's semantics — what a `Cihai`
object does, what `bootstrap()` builds, what a dataset or plugin is.

Type annotations describe shape. Documentation describes meaning. A sentence
that restates a signature has said nothing.

Use MUST, SHOULD, and MAY only where the normative sense is meant. Say what
actually happens rather than that something is "supported".

| Instead of                       | Prefer                             |
| --------------------------------- | ----------------------------------- |
| "We added…"                      | "`Unihan.reverse_char` now accepts…" |
| "New and improved"               | "`Cihai.from_file` now…"           |
| "powerful", "seamless"           | state the capability               |
| "easily", "simply", "just"       | omit                               |
| "simple", "obvious", "intuitive" | omit                                |
| "robust"                         | name the failure that is handled    |
| "comprehensive"                  | name what is covered                |
| "production-ready"               | state the guarantee                 |
| "optimized", "blazingly fast"    | give the magnitude                  |
| "various fixes"                  | name the components                 |
| "under the hood"                 | omit unless observable              |
| "please note that", "note that"  | state the fact                      |
| "leverage", "utilize"            | "use"                               |
| "delve into"                     | "read", or omit                     |
| "best practices"                 | name the practice                   |
| "in order to"                    | "to"                                |

## Who you are writing for

The default reader writes Python and looks up CJK character data through
cihai's object API — a `Cihai` instance and its `unihan` dataset,
`lookup_char`, `reverse_char`. They know which characters they care about and
are comfortable in Python, but you cannot assume they know UNIHAN's field
vocabulary (`kDefinition`, `kMandarin`), cihai's internals — config expansion,
the `extend` machinery, the SQLAlchemy layer under `c.sql` — or that a
one-time `bootstrap()` builds the local database.

A second, smaller reader extends cihai or works on it: a custom `Dataset` or
`DatasetPlugin`, `unihan_options` tuning, a Postgres backend, contributing.
Serve them too, but mark their material opt-in ("for the rarer cases",
"advanced") so the default reader knows they can stop. Never make the common
case pay a comprehension tax for the advanced one.

Rules that follow:

- **Second person, present tense, active.** "You look up a character", not "A
  character is looked up". Address the reader who is doing the thing.
- **Concept before API surface.** Open by saying what the object or method
  *is* and what it does for the reader. The signature — the parameters, the
  config keys — is the last detail they need, not the first. A page that
  opens with a method signature has buried the idea under its mechanics.
- **Say when they can stop.** Lead with the default and the reassurance: cihai
  works out of the box, SQLite and XDG paths need no configuration. Let a
  skimmer leave after one paragraph.
- **Grant permission, do not demand attention.** "Reach for this when…", "for
  the rarer cases" — tell readers they are in the right place without
  implying they must read on.
- **Progressive disclosure.** Order by how many readers need it: the common
  lookup, then the one config key a few will tune, then a custom dataset or
  plugin, then raw SQLAlchemy through `c.sql`. Each step is for a smaller
  audience than the last.
- **Lean on the flow.** The reader thinks construct → bootstrap → query: make
  a `Cihai`, `bootstrap()` once, then `lookup_char` / `reverse_char`.
  Reinforce that chain — a `Dataset` plugs into `Cihai`, a `DatasetPlugin`
  plugs into a dataset. It is the mental model the whole library hangs on.
- **Name the trade-off.** If a call costs something — `bootstrap()` downloads
  UNIHAN and builds the database once, narrowing `unihan_options` fields
  trades coverage for speed, dropping to `c.sql` trades the dataset
  conveniences for raw queries — say so, and say what it buys. State it; do
  not sell it.
- **Frame by concept, not by mechanism.** Do not headline a feature by its
  UNIHAN field key or YAML config key in prose; that names the implementation
  surface, which is the reader's last concern. Name the concept —
  "readings", "variants", "where the data lives". The mechanics vocabulary —
  a field table, a `database.url` key — belongs in a reference table or the
  API docs, and only there.

**What stays precise.** Warm the framing, never the facts. UNIHAN field
names, config-key tables, resolution-order lists, exact error strings, and
class or method cross-references carry meaning in their exact form — leave
them alone. The friendly voice belongs in the sentences *around* a precise
block, introducing it, not inside it paraphrasing it into vagueness.

`docs/quickstart.md` is the worked example: it opens with the reassurance
that cihai works out of the box, its configuration section leads with the
default (SQLite, XDG paths, no config file needed) before showing overrides,
"Advanced Config" is explicitly a later, smaller-audience section, and the
precise parts — the YAML config blocks, the `unihan_options` passthrough to
`unihan_etl.core.Packager` — stay exact.

## README

A README is the shortest path from "what is this?" to competent use, not the
project's autobiography.

The first sentence is a contract. It says what abstraction the reader has
been handed, concretely enough to tell this package apart from the
neighbouring one.

Get to a runnable command or snippet before anything the reader can skip. A
logo, a mission statement, a comparison matrix and three paragraphs of
history in front of the install line all cost the same thing.

State the minimum Python version and meaningful platform constraints in
prose, not only in badges. `requires-python` in `pyproject.toml` is the
authority; the README must agree with it.

Name the distribution, the import, and the executable separately wherever
they differ — `cihai` the library and `cihai-cli` the command-line tool are
two distributions, published separately, imported and installed under
different names.

Examples are executable, not illustrative fiction. Never
`your-command <some-options>`. See
[Documented examples that run](#documented-examples-that-run) for which
blocks are executed and how to write one that qualifies.

Document the semantic model, not the flag list. What matters is precedence,
what a lookup returns, and what a non-zero exit means — not an exhaustive
enumeration of every method or field.

State defaults explicitly — defaults are API. State negative guarantees
where they exist: no configuration required, no network access outside
`bootstrap()`. They establish boundaries faster than any amount of
description.

Headings stay conventional and stable, because people deep-link them. Badges
are few and load-bearing.

## Documented examples that run

Examples in this repository are tests. This section is the contract for
writing one the test suite can actually see.

**A fence tag is cosmetic. Only a `>>> ` prompt executes.** A block written
as

    ```{code-block} python

    c = Cihai()

    ```

is prose that looks like a test. Nothing collects it, nothing runs it, and
it can be wrong for years. The same block written with prompts is a test:

    ```{code-block} python

    >>> c = Cihai()

    ```

This is the single most expensive mistake available when editing
documentation, because removing the prompts leaves a green test suite and a
silently deleted test. When editing a file that contains examples, count the
prompts before and after.

**In this repository, an executed block under `docs/` is a MyST
`{code-block}` directive, not a bare fence.** Every one of the 18 prompted
blocks currently in the tree — in `docs/how-to/configuration.md`,
`docs/topics/troubleshooting.md`, and the design-and-planning pages — is
written `` ```{code-block} python `` with the prompts inside. Match that form
for a new executed example under `docs/`. The collector matches on the
`>>> ` text itself, not on the directive, so a bare ```` ```python ```` fence
with prompts would run too — but a bare `python` fence is this repository's
existing convention for an *illustrative, non-executed* snippet instead (the
second block in `docs/how-to/configuration.md`, and the example in
`README.md`, are both this: no prompts, not collected).

**Where examples run, in this repository.** `[tool.pytest.ini_options]` in
`pyproject.toml` sets `addopts = "--doctest-modules …"` and
`testpaths = ["src/cihai", "tests", "docs"]`. That collects docstring
examples anywhere under `src/cihai`, and every prompted block under `docs/`,
regardless of fence or directive. **`README.md` is not in `testpaths`.** A
`>>> ` block placed in `README.md` today would not run — it is not reachable
from any collected path. Keep `README.md`'s example as a plain, unprompted
`python` fence for that reason; adding prompts there would look like a test
without being one.

**`doctest_namespace`.** The root `conftest.py` provides an autouse fixture
that, for every doctest item, applies `set_home` — redirecting `HOME` to a
temporary directory, so no doctest ever touches a real user's config or
database — and injects `tmp_path` into `doctest_namespace`. `tmp_path` is the
only name a doctest may use without first defining it; anything else must be
constructed in the block itself.

**Bootstrapping downloads data.** `Unihan.bootstrap()` fetches and imports
the UNIHAN dataset. Keep doctests to what runs without a bootstrapped
database. A heavier flow belongs in an `examples/` script pulled into a page
with `{literalinclude}` (as `docs/quickstart.md` does with
`examples/basic_usage.py`) — `tests/test_examples.py` executes those — or in
`tests/` directly.

**`# doctest: +SKIP` is not permitted.** It is a workaround that tests
nothing. Use the fixtures.

**Do not downgrade a doctest to a non-executed block to make it pass.**
Stripping the `>>> ` prompts — from a `{code-block}` directive or a bare
fence alike — is what stops a block from running. If an example cannot
pass, fix the example or fix the code.

**Option flags.** `ELLIPSIS` and `NORMALIZE_WHITESPACE` are enabled globally
(`doctest_optionflags` in `pyproject.toml`), so `...` elides variable output
and whitespace differences do not fail a comparison. Reach for an inline
`# doctest: +FLAG` only for the block that needs it.

**Docstring examples** use the NumPy `Examples` section:

    Examples
    --------
    >>> from cihai.core import Cihai
    >>> c = Cihai()

**Shell commands** use a ```` ```console ```` block at a `$` prompt — see
[Code blocks](#code-blocks). Those are never collected as tests; they
document what to type, not what to assert.

## Docstrings

The prime directive: never restate the type. The annotation is the source of
truth; the docstring carries what the annotation cannot.

This is documentation debt wearing a docstring:

    def lookup_char(char: str) -> Query[Unihan]:
        """Look up a character.

        Parameters
        ----------
        char : str
            The character.

        Returns
        -------
        Query[Unihan]
            The query.
        """

Document instead the dimensions the type system cannot encode:

- **Mutation.** What it changes in place.
- **Ownership.** What the caller must close, release, or keep alive.
- **Ordering.** Whether results come back in a guaranteed order.
- **Timing.** What has finished by the time the call returns.
- **Failure.** Which exceptions are raised and what triggers each.
- **Idempotence.** Whether calling twice does anything the second time —
  `bootstrap()` is the case in point: calling it again should not
  re-download or re-import.
- **Concurrency.** Whether calls are coalesced, queued, or independent, and
  whether the object is thread-safe.
- **Units and ranges.** What a number means and what values are accepted.
- **Boundary behaviour.** What zero, empty, and the maximum do.
- **Platform.** Behaviour that differs by operating system or dependency
  version.
- **Security boundary.** What is executed, and what is only read.

The first sentence stands alone; tooling truncates there. PEP 257 applies:
triple double quotes, an imperative one-line summary ending in a period, a
blank line before any extended description. Do not repeat an introspectable
signature.

**One docstring dialect, enforced by the linter.** `ruff`'s `D` rule set
(`pydocstyle`, `convention = "numpy"`) is the enforcement; every docstring is
NumPy style with reStructuredText markup in the body. Narrative doctest
style — prose, then a blank line, then the `>>> ` block — over a wall of
assertions.

**Classes with fields** — `NamedTuple`, dataclasses — document every field in
an `Attributes` section:

    class UnihanAnnotationCase(t.NamedTuple):
        """Expected public UNIHAN annotation.

        Attributes
        ----------
        field_name : str
            UNIHAN field the annotation is expected to expose.
        test_id : str
            Parametrize id identifying the case.
        """

Autodoc renders every field whether or not you describe it, so an
undocumented `NamedTuple` field ships to the API docs as "Alias for field
number 0" and a dataclass field ships bare. Document all of them — a class
with three fields and two documented still ships a stub for the third.

## Source comments

A comment ships only if it passes all three gates. Fail any: delete or
rewrite. Borderline: delete — borderline means the information is
reconstructible, which is what makes deletion cheap.

**Loss.** Three years from now, would losing this cost a maintainer real time
rediscovering intent, an invariant, a constraint, or a failure mode the code
and tests do not already make obvious?

**Elite.** Would SQLite, Redis, the Go standard library, or CPython write
this comment, at this length? Those projects state the constraint and stop.
They do not argue with an imagined objector.

**Upkeep.** Will it stay true without maintenance? A comment that hand-syncs
a value the code owns — a count, an offset, a line reference, a duplicated
constant — is false the first time that value moves.

### Ceiling

One or two lines. A comment reaching four is either carrying several facts,
in which case split it, or arguing, in which case cut it to the fact.

Rationale, alternatives weighed, and the story of how the code got here
belong in the commit message: timestamped, attached to the exact diff, and
free to maintain.

A comment often holds both a constraint and the deliberation that found it.
Keep the constraint, cut the deliberation. "Runs at most once per second"
survives; "this is the right trade for now" does not.

### Keep

- Why over how: upstream quirks, protocol and compatibility constraints,
  performance tradeoffs still part of the contract.
- Invariants, preconditions, ordering, lifetime, and concurrency requirements
  that types and tests cannot express.
- Code that looks wrong but is not, so a later cleanup does not reintroduce
  the bug.
- A high-level sketch of an algorithm whose local operations do not reveal
  the whole.

### Delete

- Narration of the next lines; code translated into English.
- Restated names, types, defaults, or control flow.
- Values duplicated from the code and hand-synced.
- Justification, hedging, or apology for a choice.
- Speculation about future requirements.
- History version control already holds, including commented-out code.
- Ticket and issue numbers. They say nothing to a reader without tracker
  access, and they rot when the tracker moves. Unfinished work goes in the
  tracker, not the source.
- Transient observations — "currently", "for now", "the latest release" —
  that go stale with no nearby edit.

### The upkeep gate in practice

It reaches values that track our own code. It does not reach frozen external
facts.

Bad (Delete):

```python
# There are 321 tests to complete for servers.
```

Good (Keep):

```python
# CPython < 3.11 has no ExceptionGroup, so this branch stays.
```

### Documentation exception

Doctests, minimal usage examples, and `Parameters`, `Returns`, `Raises`, and
`Attributes` entries on public API are exempt from the loss gate — they
serve the caller, not the maintainer, and a doctest that runs is also a
test. They are exempt from nothing else. Ceiling: a good man page entry.

## Terminology and capitalization

Pick the domain noun and keep it. If the code calls something a dataset, do
not call it a data source in one paragraph and a plugin in the next. If the
method is `lookup_char`, write "look up" everywhere rather than alternating
with "find", "search", and "query".

Stable vocabulary is what makes search, deep links, and an agent's retrieval
work at all.

Python and PyPI keep their own capitalisation. Distribution names are
written as they are published — `cihai`, `cihai-cli`, `unihan-etl`.

Do not write counts into prose — how many symbols exist, how many tests
there are. They go stale silently and no reader needs them. Counts that pin
a fixture or guard an invariant are different, and belong in code.

### CJK and UNIHAN vocabulary

This is a Unicode/CJK data project; the following distinctions are load-
bearing and get blurred easily.

- **Character.** The Unicode/CJK entity being looked up — 好, 圕. This
  matches the `char` field, `lookup_char`, `reverse_char`. Use "character",
  not "glyph" or "symbol", when naming the thing a user looks up.
- **Codepoint / UCN.** The character's numeric identity in Unicode, written
  `U+597D` — uppercase `U`, a literal `+`, uppercase hex digits, in
  backticks. This is the `ucn` field in `cihai-cli`'s output. "Codepoint" and
  "UCN" (Unicode Character Notation) are interchangeable in prose; the field
  name `ucn` is what code and CLI output use.
- **Glyph.** In this codebase's own examples (`examples/basic_usage.py`,
  `README.md`, `docs/index.md`), `glyph` names the local variable holding one
  matched UNIHAN record — a row of field data for a character — not a
  rendered visual form. Follow that existing convention in example code; do
  not introduce "glyph" elsewhere to mean a font's rendering of a character,
  since cihai does not deal in font rendering at all.
- **UNIHAN field names** (`kDefinition`, `kMandarin`, `kTotalStrokes`, and
  the rest) are written literally, in backticks, in their exact `k`-prefixed
  camel case. Never re-case, pluralize, or paraphrase one — "the Mandarin
  reading field" is fine prose, but a field named in code is named exactly.
- **UNIHAN** the dataset is written all-caps in prose, matching the Unicode
  Consortium's own usage and `docs/glossary.md`. The Python identifiers that
  represent it keep their own case: the `Unihan` class, the
  `cihai.data.unihan` module, the `unihan` attribute on a `Cihai` instance,
  the `unihan-etl` and `unihan_etl` distribution and import names.
- **Writing CJK text in prose and examples.** Write the character itself,
  not a romanization, as the primary form — pair it with a gloss in
  parentheses on first use in explanatory prose ("好 (good)"). Keep a
  codepoint in backticks whenever it is cited (`U+597D`), and do not
  transliterate a codepoint into a character or vice versa without saying
  which you did.

## Logging

Applies to every `logger.*` call — log messages are a text surface a reader
(an operator reading output, or a test asserting on `caplog`) reaches, same
as an error message.

### Logger setup

- Use `logging.getLogger(__name__)` in every module.
- Add `NullHandler` in library `__init__.py` files.
- Never configure handlers, levels, or formatters in library code — that is
  the application's job.

### Structured context via `extra`

Pass structured data on every log call where useful for filtering,
searching, or test assertions.

**Core keys** (stable, scalar, safe at any log level):

| Key                  | Type  | Context                    |
| -------------------- | ----- | --------------------------- |
| `unihan_field`       | `str` | UNIHAN field name           |
| `unihan_source_file` | `str` | source data file path       |
| `unihan_record_count`| `int` | records processed           |
| `cihai_dataset`      | `str` | dataset name                |
| `cihai_query`        | `str` | lookup query                |

**Heavy/optional keys** (`DEBUG` only, potentially large):

| Key              | Type        | Context                                                          |
| ---------------- | ----------- | ------------------------------------------------------------------ |
| `unihan_stdout`  | `list[str]` | subprocess stdout lines (truncate or cap; `%(unihan_stdout)s` produces repr) |
| `unihan_stderr`  | `list[str]` | subprocess stderr lines (same caveats)                            |

Treat established keys as compatibility-sensitive — downstream users may
build dashboards and alerts on them. Change deliberately.

**Key naming.** `snake_case`, not dotted; `unihan_` prefix. Prefer stable
scalars; avoid ad-hoc objects. Heavy keys are `DEBUG`-only; consider a
companion `_len` field or hard truncation (`stdout[:100]`) instead of the
full payload.

### Lazy formatting

`logger.debug("msg %s", val)`, not an f-string. Two reasons: the
interpolation is skipped entirely when the level is filtered, and a log
aggregator groups `"Running %s"` as one signature across every call, where an
f-string makes each line unique. When computing `val` itself is expensive,
guard with `if logger.isEnabledFor(logging.DEBUG)`.

### `stacklevel` for wrappers

Increment for each wrapper layer so `%(filename)s:%(lineno)d` and the
OpenTelemetry `code.filepath` attribute point to the real caller. Verify
whenever call depth changes.

### `LoggerAdapter` for persistent context

For objects with stable identity (a `Dataset`, a reader, an exporter), use
`LoggerAdapter` to avoid repeating the same `extra` on every call. Prefer
overriding `process()` for the portable pattern; `merge_extra=True`
simplifies this on Python 3.13+.

### Log levels

| Level     | Use for                                       | Examples                                          |
| --------- | ---------------------------------------------- | -------------------------------------------------- |
| `DEBUG`   | Internal mechanics, data I/O                   | Field parsing, record transformation steps         |
| `INFO`    | Data lifecycle, user-visible operations        | Download completed, export finished, database bootstrapped |
| `WARNING` | Recoverable issues, deprecation, user-actionable config | Missing optional field, deprecated data format |
| `ERROR`   | Failures that stop an operation                | Download failed, parse error, database write failed |

Config discovery noise belongs in `DEBUG`; only surprising or
user-actionable config issues rise to `WARNING`.

### Message style

- Lowercase, past tense for events: `"download completed"`, `"parse error"`.
- No trailing punctuation.
- Keep messages short; put details in `extra`, not the message string.

### Exception logging

- Use `logger.exception()` only inside an `except` block when you are
  **not** re-raising.
- Use `logger.error(..., exc_info=True)` when the traceback is needed
  outside an `except` block.
- Avoid `logger.exception()` followed by `raise` — this duplicates the
  traceback. Either add context via `extra` that would otherwise be lost, or
  let the exception propagate.

### Testing logs

Assert on `caplog.records` attributes, not string matching on `caplog.text`:

- Scope capture: `caplog.at_level(logging.DEBUG, logger="cihai.core")`.
- Filter records rather than index by position:
  `[r for r in caplog.records if hasattr(r, "unihan_field")]`.
- Assert on schema: `record.unihan_record_count == 100`, not
  `"100 records" in caplog.text`.
- `caplog.record_tuples` cannot access extra fields — always use
  `caplog.records`.

### Avoid

- Catch-log-reraise without adding new context.
- `print()` for diagnostics.
- Logging secret environment variable values (log key names only).
- Requiring custom `extra` fields in format strings without safe defaults —
  a missing key raises `KeyError`.

## Documentation cross-references

Any class, method, function, exception, data object, or attribute that has
its own rendered API page must be cited via the matching MyST role — never
plain backticks: `{class}`, `{meth}`, `{func}`, `{exc}`, `{data}`, `{attr}`,
`{mod}`. A documentation page without an explicit ref label uses `{doc}`; an
anchor inside a page uses `{ref}`; a glossary term uses `{term}`. Plain
backticks are correct for code syntax, environment variables, parameter
names, and file paths that have no autodoc destination.

`{ref}` must match its target's anchor exactly — anchors mix hyphen,
underscore, and dotted forms across pages (`developmental-releases`,
`internal_api`, `cihai.conversion`). Get it wrong and the build emits a
warning, not a silent failure — see below.

**Link the first prose mention** of any symbol that has a useful destination
on the page: Python objects, cihai APIs, CJK terms with glossary entries,
dataset and topic pages, and external tools or projects (unihan-etl,
SQLAlchemy — use a Markdown link for those, not a role). After the first
linked mention on a page, later mentions can stay plain unless distance or
context makes another link useful.

Do not rely on a later reference section to satisfy the first-mention rule.
If the first occurrence would be a heading, grid-card teaser, or
introductory sentence, link that occurrence or retitle the heading so the
first prose mention can carry the link. Leave command examples, code blocks,
and literal configuration values as code; link the surrounding prose
instead.

**Build the docs before you commit.** `just build-docs` catches a broken
cross-reference; the doctests do not.

## Markdown

Prose wraps at 80 columns. Table rows, badge lines, and long links are
exempt, because breaking them harms rendering. A pull request or issue body
does not wrap at all: GitHub renders a single newline as a space in a file
and as a line break in a comment, so a wrapped comment body arrives as
ragged stubs.

GitHub alert blocks — `> [!NOTE]`, `> [!WARNING]` — render as literal text
outside GitHub, so reserve them for at most one load-bearing warning per
document. Write the sentence so it carries the fact on its own, and a
renderer that drops the marker loses nothing.

Do not use a local absolute path or an email address in anything published.

## Code blocks

Code blocks are paste-and-run units: pasting one block runs exactly one
intended action. Executed examples are exempt — the test suite runs them,
nobody pastes them.

- **One command per block.** Multiple steps may share a block only when
  explicitly chained with `&&`, `;`, or `\` continuations — the chain is
  then one logical command.
- **Explanations go in prose above the block**, never as `#` comments inside
  it.
- **Command menus are per-command blocks with prose lead-ins**, not tables.
- **Shell commands use the `console` tag with a `$ ` prefix.** This
  separates interactive commands from scripts and enables prompt-aware copy.
- **Split long commands with `\`** — one flag or flag+value pair per
  indented continuation line, positional arguments last.

Good — show the last ten commits as a graph:

```console
$ git log \
    --max-count=10 \
    --graph \
    --oneline
```

Bad:

```console
# Show the last ten commits as a graph
$ git log --max-count=10 --graph --oneline
```

## Commits

```
Scope(type[detail]): concise description

why: Explanation of necessity or impact.

what:
- Specific technical changes made
- Focused on a single topic
```

Keep the subject to 50 characters or fewer, excluding any trailing `(#NN)`
pull request reference, and wrap body lines at 72. Separate the `why:` and
`what:` blocks with a blank line.

Routine maintenance commits drop the colon and take a capitalised
description, which is what distinguishes them at a glance in
`git log --oneline`:

```
py(deps[dev]) Bump dev packages
.tool-versions(uv) uv 0.12.3 -> 0.12.5
ai(rules[AGENTS]) Judge comments by three gates
```

Everything that changes behaviour keeps the colon.

Common types:

- **feat**: New features or enhancements
- **fix**: Bug fixes
- **refactor**: Code restructuring without functional change
- **docs**: Documentation updates
- **chore**: Maintenance (dependencies, tooling, config)
- **test**: Test-related updates
- **style**: Code style and formatting
- **ci**: Workflow and pipeline changes
- **py(deps)**: Dependencies
- **py(deps[dev])**: Dev dependencies
- **ai(rules[AGENTS])**: AI rule updates

Example:

```
Unihan(feat[reverse_char]): Accept a list of hints

why: Match against several strings in one query instead of one call
  per hint.

what:
- Accept str | list[str] in reverse_char
- Normalize a single str to a one-element list
```

For a multi-line message, use a heredoc so the formatting survives:

```console
$ git commit -m "$(cat <<'EOF'
Scope(feat[detail]): Concise description

why: Explanation of the change.

what:
- First change
- Second change
EOF
)"
```

### Release commits

Never create tags. Never push tags. The owner handles tagging and tag
pushes, because a tag triggers the publish workflow.

A release commit subject is plain and short: `Tag v<version>`. The detailed
why and what go in the body. Do not use the `Scope(type[detail]):` format
for a release — it buries the lede.

## The changelog

`CHANGES` is the changelog, rendered as the project's changelog page at
{doc}`history` via `{include}`. Modeled on Django's release-notes shape:
deliverables get titles and prose, not bullets.

**Release entry boilerplate.** Every release header is
`## cihai X.Y.Z (YYYY-MM-DD)`. The file opens with a
`## cihai X.Y.Z (unreleased)` placeholder block fenced by
`<!-- KEEP THIS PLACEHOLDER ... -->` and
`<!-- END PLACEHOLDER ... -->` HTML comments — new entries land immediately
below the END marker, never above it.

**Open with a multi-sentence lead paragraph.** Plain prose, no italic. Open
with the version as the sentence subject ("cihai X.Y.Z ships …") so the lead
is self-contained when excerpted. Two to four sentences telling the reader
what shipped and who cares — user-visible takeaways, not internal mechanism.
Cross-reference detail docs with `{ref}` to keep the lead compact.

**Lead paragraphs are release-time material — off-limits to branches and PRs.**
The unreleased entry carries no lead paragraph and no version summary:
sections only (`### Breaking changes`, `### What's new` deliverables,
`### Fixes`, …). Speaking for the release — what the version "is", "ships",
or "focuses on" — is presumptuous before its scope is final; only the person
cutting the release writes that, and only when explicitly asked to release.
Never write or edit a lead paragraph from a feature branch, and never ask or
imply that a release should happen.

**Each deliverable is a section, not a bullet.** Inside `### What's new`,
every distinct deliverable gets a `#### Deliverable title (#NN)` heading
naming it in user vocabulary, followed by one to three prose paragraphs
explaining what shipped. Do not wrap a paragraph in `- ` — bullets are for
enumerable lists, not paragraph containers. Cross-link detail docs
(``See {ref}`foo` for details.``) so prose stays focused.

**The deliverable test.** Before writing an entry, ask: "What's the
deliverable, in user vocabulary?" If you cannot answer in one sentence, the
entry is not ready. Mechanism — helper internals, byte counters,
schema-validation locations — belongs in PR descriptions and code comments,
not the changelog.

**Fixed subheadings**, in this order when present: `### Breaking changes`,
`### Dependencies`, `### What's new`, `### Fixes`, `### Documentation`,
`### Development`. Dev tooling (helper scripts, internal automation) lives
under `### Development`. For breaking changes, show the migration path with
concrete inline code (a `# Before` / `# After` fenced block). Dependency
floor bumps use the form ``Minimum `pkg>=X.Y.Z` (was `>=X.Y.W`)``.

**PR refs `(#NN)`** sit in each deliverable's `####` heading.

**When bullets are appropriate.** Catch-all sections (`### Fixes`,
occasionally `### Documentation`) with three or more genuinely small items
use bullets — one line each, never paragraphs. If a bullet swells past two
lines, promote it to a `#### Title (#NN)` heading with a prose body.

**Anti-patterns.**

- Fragile metrics: token ceilings, third-party version pins, percent
  benchmarks, exact byte counts. Describe the capability, not the math.
- Internal jargon: private symbols (leading-underscore identifiers),
  algorithm names exposed for the first time, backend scaffolding.
- Walls of text dressed up as bullets.
- Buried breaking changes — give them their own subheading at the top of the
  entry.

**Always link autodoc'd APIs**, per
[Documentation cross-references](#documentation-cross-references) — never
plain backticks for a class, method, function, exception, data object, or
attribute that has its own rendered page.

**Versions are PEP 440 identifiers.** Semantic-versioning meaning applies to
the documented public API — which includes command names, options, exit
statuses, configuration keys, environment variables, and serialized formats,
not only imported Python symbols.

**Summarization style.** When asked "what changed in the latest version?" or
similar, lead with the entry's lead paragraph (paraphrased if needed),
followed by each `####` deliverable heading under `### What's new` with a
one-sentence summary. Cite `(#NN)` only if asked for source links. Do not
invent versions, dates, or numbers not present in `CHANGES`. Do not quote
line numbers or file offsets — those shift as the file evolves.

## Slop prevention

Treat AI slop as review-hostile noise, not as proof that text or code is
wrong. The goal is to maximise information density.

- **AI signatures.** No "Generated by", no conversational filler, no
  unexplained emoji, no tool metadata.
- **Brittle references.** No hard-coded line numbers, fragile file counts,
  dated "as of" claims, bare SHAs, or local absolute paths — unless they are
  strict evidentiary artefacts such as a benchmark log.
- **Diff narration.** Do not restate what moved, was renamed, or was removed
  in anything the reader holds alongside the diff: code, docstrings, README,
  CHANGES, or a pull request description. The diff and the commit message
  already carry it.
- **Branch-internal narrative.** Do not mention intermediate states,
  abandoned approaches, or "no longer" behaviour unless users of a published
  release actually experienced the old state — see
  [The published-release test](#the-published-release-test).
- **Low-value scaffolding.** No ownerless TODOs, unused future-proofing,
  debug artefacts, or defensive wrappers around failure modes nothing can
  reach.
- **Prose inflation.** The diction table under [Voice](#voice) governs;
  replace an inflated word with a concrete description of behaviour,
  constraints, or trade-offs.
- **Coded labels.** Write rules and findings as plain imperatives. No `[R1]`,
  `Option B`, or any index a reader has to decode.

Preserve the "why". Never delete a comment documenting an invariant, a
protocol constraint, a platform quirk, or an upstream workaround — those are
the facts [Source comments](#source-comments) keeps, and every other comment
is judged by it. Exact counts, dates, and SHAs are immune from the "brittle
references" rule when they serve as evidence — a benchmark result, a release
note, a stack trace, a lockfile.

### Durable source links

Link to a pinned revision, never to trunk. A pinned permalink is not a
brittle reference; an unlinked SHA dropped into prose is. `blob/master/…`
links rot silently — the file moves, lines shift, and the anchor lands on
unrelated code while still resolving.

- Prefer a release tag (`blob/v0.38.0/…`). Most durable, and it tells the
  reader which released version the claim held for.
- Otherwise use a 7-char commit ref (`blob/9a29b1a/…`) reachable from trunk.
  Use when there is no tag or the claim is about unreleased code. Never a
  PR-head SHA — it can be rebased or garbage-collected.
- Reserve `blob/master/…` for living documents meant to always show the
  latest state, such as a contributing guide.
- Line anchors (`#L120-L145`) are only safe on a pinned ref.

### The published-release test

Long-running branches accumulate tactical decisions — renames, refactors,
attempts-then-reverts. When deciding what counts as branch-internal, use
trunk or the parent branch as the baseline, not intermediate states inside
the current branch. Ask:

> Did users of the most recently published release ever experience this old
> name, old behavior, or bug?

If the answer is no, it is branch-internal narrative. Move it to the commit
message and describe only the final state in the artifact.

Keep in shipped artifacts: deprecations and migration guides for symbols
that actually shipped; `### Fixes` entries for bugs that affected users of a
published release; comments explaining why the current code looks this way
that make sense to a reader who never saw the previous version.

### Cleanup in hindsight

When applying these rules retroactively from inside a feature branch, first
establish scope by diffing against the parent branch (or trunk) to identify
which commits the branch actually introduced.

- **In-branch commits.** Offer two options: `fixup!` commits with
  `git rebase --autosquash` to address each causal commit at its source, or
  a single cleanup commit at branch tip.
- **Trunk or parent commits.** Default to leaving them alone. Act only on
  explicit instruction, folding into a single commit at branch tip rather
  than rewriting shared history.
- **Scope guard.** If cleaning prior slop would touch someone else's work or
  expand the branch beyond its stated goal, leave prior slop alone and
  protect the current goal.
