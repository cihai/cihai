# Documentation voice

This file covers the *voice* of prose under `docs/` — how to frame a
page so a reader meets the idea before its API surface. It complements
the repository-root `AGENTS.md`, which already governs code blocks,
doctest style, changelog conventions, and MyST roles. When the two
overlap, the root file wins; this one only answers the question it
leaves open: how should the prose sound?

## Who you are writing for

The default reader writes Python and looks up CJK character data
through cihai's object API — a `Cihai` instance and its `unihan`
dataset, `lookup_char`, `reverse_char`. They know which characters
they care about and are comfortable in Python, but you cannot assume
they know UNIHAN's field vocabulary (`kDefinition`, `kMandarin`),
cihai's internals — config expansion, the `extend` machinery, the
SQLAlchemy layer under `c.sql` — or that a one-time `bootstrap()`
builds the local database.

A second, smaller reader extends cihai or works on it: a custom
`Dataset` or `DatasetPlugin`, `unihan_options` tuning, a Postgres
backend, contributing. Serve them too, but mark their material opt-in
("for the rarer cases", "advanced") so the default reader knows they
can stop. Never make the common case pay a comprehension tax for the
advanced one.

## Voice

- **Second person, present tense, active.** "You look up a character",
  not "A character is looked up". Address the reader who is doing the
  thing.
- **Concept before API surface.** Open by saying what the object or
  method *is* and what it does for the reader. The signature — the
  parameters, the config keys — is the last detail they need, not the
  first. A page that opens with a method signature has buried the idea
  under its mechanics.
- **Say when they can stop.** Lead with the default and the
  reassurance: cihai works out of the box, SQLite and XDG paths need
  no configuration. Let a skimmer leave after one paragraph.
- **Grant permission, don't demand attention.** "Reach for this
  when…", "for the rarer cases" — tell readers they're in the right
  place without implying they must read on.
- **Progressive disclosure.** Order by how many readers need it: the
  common lookup → the one config key a few will tune → a custom
  dataset or plugin → raw SQLAlchemy through `c.sql`. Each step is for
  a smaller audience than the last.
- **Lean on the flow.** The reader thinks construct → bootstrap →
  query: make a `Cihai`, `bootstrap()` once, then `lookup_char` /
  `reverse_char`. Reinforce that chain — a `Dataset` plugs into
  `Cihai`, a `DatasetPlugin` plugs into a dataset. It is the mental
  model the whole library hangs on.
- **Name the trade-off.** If a call costs something — `bootstrap()`
  downloads UNIHAN and builds the database once, narrowing
  `unihan_options` fields trades coverage for speed, dropping to
  `c.sql` trades the dataset conveniences for raw queries — say so,
  and say what it buys. State it; don't sell it.
- **Frame by concept, not by mechanism.** Don't headline a feature by
  its UNIHAN field key or YAML config key in prose; that names the
  implementation surface, which is the reader's last concern. Name the
  concept — "readings", "variants", "where the data lives". The
  mechanics vocabulary — a field table, a `database.url` key — belongs
  in a reference table or the API docs, and only there.

## Examples that run

Prose examples under `docs/` are doctests — `testpaths` includes
`docs/`, so pytest executes every `>>>` block on a page. Doctests run
with `HOME` redirected to a temporary directory (`set_home`), with
`tmp_path` in the `doctest_namespace` — never a real user database.

- Bootstrapping UNIHAN downloads data, so keep doctests to what runs
  without a bootstrapped database. Heavier flows belong in `examples/`
  scripts pulled into a page with `{literalinclude}` (the way
  `docs/topics/examples.md` does) — `tests/test_examples.py` executes
  those — or in `tests/`.
- Ellipsis output (`...`) already works when output varies:
  `doctest_optionflags` enables `ELLIPSIS` globally. Use a
  ```` ```console ```` block for shell commands at a `$` prompt.

## What stays precise

Warm the framing, never the facts. UNIHAN field names, config-key
tables, resolution-order lists, exact error strings, and class or
method cross-references carry meaning in their exact form — leave them
alone. The friendly voice belongs in the sentences *around* a precise
block, introducing it, not inside it paraphrasing it into vagueness.

## Cross-references

Point the advanced reader at the deep-dive rather than inlining it,
and put the link where their interest peaks — on the phrase that made
them curious ("write your own dataset") — not as a standalone
footnote the eye skips. Use the MyST roles listed in the root
`AGENTS.md` (`{class}`, `{meth}`, `{func}`, `{attr}`, `{exc}`,
`{ref}`, `{doc}`, `{term}`). A `{ref}` must match its target's anchor
exactly — anchors mix hyphen, underscore, and dotted forms across
pages (`developmental-releases`, `internal_api`, `cihai.conversion`).
`just build-docs` catches a broken cross-reference; the doctests do
not — so build the docs before you commit.

Link the first prose mention of any symbol that has a useful
destination on that page. This includes Python objects, cihai APIs,
CJK terms with glossary entries, dataset and topic pages, and
external tools or projects (unihan-etl, SQLAlchemy). Use the most
specific target available: `{class}`, `{meth}`, `{func}`, `{mod}`,
`{exc}`, or `{attr}` for API objects; `{ref}`, `{doc}`, or `{term}`
for documentation pages, section anchors, and glossary entries; and a
Markdown link or reference link for external projects. After the
first linked mention on a page, later mentions can stay plain unless
the distance or context makes another link useful.

Do not rely on a later reference section to satisfy the first-mention
rule. If the first occurrence would be a heading, grid-card teaser, or
introductory sentence, link that occurrence or retitle the heading so
the first prose mention can carry the link. Leave command examples,
code blocks, and literal configuration values as code; link the
surrounding prose instead.

## A page that does this

`docs/quickstart.md` is the worked example: it opens with the
reassurance that cihai works out of the box, its configuration
section leads with the default (SQLite, XDG paths, no config file
needed) before showing overrides, "Advanced Config" is explicitly a
later, smaller-audience section, and the precise parts — the YAML
config blocks, the `unihan_options` passthrough to
`unihan_etl.core.Packager` — stay exact. Read it before reshaping
another page.

## Before you commit

- Does the page open with what the feature *is*, or with how to call
  it?
- Can a reader who needs only the common case stop after the first
  paragraph?
- Is anything framed by its UNIHAN field key or config key that should
  be named by concept instead?
- Are the advanced and extension parts clearly marked opt-in?
- Do the doctests run (`just test` covers `docs/`), and did you leave
  every code block, table, error string, and cross-reference exact?
- Did `just build-docs` stay clean — no new warning, no broken
  cross-reference?
