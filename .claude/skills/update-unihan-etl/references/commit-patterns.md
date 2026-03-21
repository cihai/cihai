# unihan-etl Bump Commit Patterns

Real commit sequences from cihai's git history, organized by update tier.

## Tier 1: Simple Bump (2 commits)

When unihan-etl has no API changes affecting cihai — maintenance, CLI changes, docs, or internal refactors.

### Example: v0.38.0 -> v0.39.1 (cihai v0.36.1)

**Commit 1** — Package bump (`cedbcba`):
```
py(deps) Bump unihan-etl v0.38.0 -> v0.39.1

See also:
- https://github.com/cihai/unihan-etl/blob/v0.39.1/CHANGES#unihan-etl-0391-2026-01-24
- https://unihan-etl.git-pull.com/history.html#unihan-etl-0-39-1-2026-01-24
```
Files: `pyproject.toml`, `uv.lock`

**Commit 2** — CHANGES (`1ee463d`):
```
docs(CHANGES) Bump unihan-etl v0.38.0 -> v0.39.1

See also:
- https://github.com/cihai/unihan-etl/blob/v0.39.1/CHANGES#unihan-etl-0391-2026-01-24
- https://unihan-etl.git-pull.com/history.html#unihan-etl-0-39-1-2026-01-24
```
Files: `CHANGES`

CHANGES entry:
```markdown
### Breaking changes

- Bump unihan-etl v0.38.0 -> v0.39.1 (#389)
```

### Example: v0.37.0 -> v0.38.0 (cihai v0.36.0)

**Commit 1** — Package bump (`f3833e3`):
```
py(deps) unihan-etl 0.37.0 -> 0.38.0
```
Files: `pyproject.toml`, `uv.lock`

**Commit 2** — CHANGES (`842e866`):
```
docs(CHANGES) Note unihan-etl bump
```
Files: `CHANGES`

CHANGES entry:
```markdown
- Bump unihan-etl v0.37.0 -> v0.38.0
```

Note: The v0.38.0 -> v0.39.1 bump is the more polished template — prefer that format with "See also" links and version numbers in the CHANGES commit subject.

---

## Tier 2: Adaptation (3-4 commits)

When unihan-etl has API changes that require updates to cihai source or tests. No historical example exists — cihai's API surface from unihan-etl is very stable (`Packager`, `UNIHAN_MANIFEST`, `merge_dict`, `Options`).

Expected pattern if adaptation is needed:

**Commit 1** — Package bump:
```
py(deps) Bump unihan-etl v<old> -> v<new>

See also:
- https://github.com/cihai/unihan-etl/blob/v<new>/CHANGES#unihan-etl-<slug>
- https://unihan-etl.git-pull.com/history.html#unihan-etl-<slug>
```
Files: `pyproject.toml`, `uv.lock`

**Commit 2** — Code adaptation:
```
<module>(fix[detail]): description of adaptation

why: unihan-etl <new> changed <what>
what:
- Specific change 1
- Specific change 2
```
Files: `src/` only

**Commit 3** — Test adaptation (if needed):
```
tests(fix[detail]): description

why: Explanation tied to the unihan-etl update
what:
- Specific test changes
```
Files: `tests/` only

**Commit 4** — CHANGES:
```
docs(CHANGES) Bump unihan-etl v<old> -> v<new>
```
Files: `CHANGES`

---

## Tier 3: Feature Integration (3-5 commits)

When cihai adopts new unihan-etl features — e.g., new field types, new data constants, new export formats.

No historical example in cihai. Expected CHANGES entry would go under `### What's new` or `### Development` rather than `### Breaking changes`, depending on whether a minimum version bump is involved.

---

## Commit Message Conventions

### Package bump commit

Pattern: `py(deps) Bump unihan-etl v<old> -> v<new>`

- No PR number in the commit message (that's for CHANGES)
- Body includes "See also" links to both GitHub CHANGES and docs site
- Files: only `pyproject.toml` and `uv.lock`

### Code adaptation commit

Pattern: `<module>(fix|feat[detail]): description`

- Scope reflects the affected cihai module (e.g., `data/unihan/bootstrap`)
- Detail in brackets names the specific function or component
- Body has `why:` and `what:` sections per project conventions
- Files: only `src/` directory

### Test adaptation commit

Pattern: `tests(fix|feat[detail]): description`

- Scope is always `tests`
- Detail names the test module (e.g., `test_core`, `test_utils`)
- Files: only `tests/` and optionally `conftest.py`

### CHANGES commit

Pattern: `docs(CHANGES) Bump unihan-etl v<old> -> v<new>`

- No PR number, no version suffix
- Subject describes what the CHANGES covers, not that a CHANGES entry was added
- Files: only `CHANGES`

---

## URL Patterns

### "See also" links

Two URLs per commit body:
- **GitHub**: `https://github.com/cihai/unihan-etl/blob/v<ver>/CHANGES#unihan-etl-<github-slug>`
- **Docs**: `https://unihan-etl.git-pull.com/history.html#unihan-etl-<docs-slug>`

### Version slug formats

The slug format differs between GitHub and docs:

| Target | Format | Example for v0.39.1 (2026-01-24) |
|--------|--------|----------------------------------|
| GitHub anchor | Dots stripped, no date | `0391` |
| Docs anchor | Dashes, with date | `0-39-1-2026-01-24` |

Full URL examples:
- `https://github.com/cihai/unihan-etl/blob/v0.39.1/CHANGES#unihan-etl-0391-2026-01-24`
- `https://unihan-etl.git-pull.com/history.html#unihan-etl-0-39-1-2026-01-24`

To extract the date, read the CHANGES heading: `## unihan-etl 0.39.1 (2026-01-24)`.

---

## CHANGES Entry Conventions

### Section selection

| Update type | CHANGES section |
|-------------|----------------|
| Minimum version bump | `### Breaking changes` |
| New features adopted | `### What's new` |
| Bug fixes from unihan-etl | `### Bug fixes` |
| Test changes | `### Tests` |
| Maintenance-only bump | `### Development` |

### Insertion point

Insert after the placeholder comments in the unreleased section:
```
<!-- END PLACEHOLDER - ADD NEW CHANGELOG ENTRIES BELOW THIS LINE -->

<!-- Maintainers, insert changes / features for the next release here -->
```

### PR number handling

- Use `(#???)` as placeholder if no PR exists yet
- Replace with actual number after PR creation
- CHANGES entries reference PRs; commit messages do not
