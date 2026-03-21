---
name: update-unihan-etl
description: >
  Update the unihan-etl dependency in cihai to the latest version with atomic,
  well-documented commits. This skill should be used when the user asks to
  "update unihan-etl", "bump unihan-etl", "upgrade unihan-etl", "check for
  unihan-etl updates", "update unihan-etl dependency", or mentions updating
  the unihan-etl dependency in cihai. Covers discovery, package bump, code
  adaptation, test updates, and CHANGES entries as separate commits.
user-invocable: true
allowed-tools: ["Bash", "Read", "Grep", "Glob", "Edit", "Write", "WebSearch", "Agent", "AskUserQuestion"]
argument-hint: "[--dry-run] [--no-pr]"
---

# Update unihan-etl in cihai

Workflow for updating cihai's primary data dependency (unihan-etl) with separate, atomic commits following established project conventions.

Parse `$ARGUMENTS` for flags:

| Flag | Effect |
|------|--------|
| `--dry-run` | Analyze and report what would change without making modifications |
| `--no-pr` | Skip PR creation at the end |

## Phase 1: Discovery

**Goal**: Determine current and target versions, assess what changed.

### 1a. Check current state

Read `pyproject.toml` in cihai and extract the `unihan-etl` version constraint from `dependencies`.

```bash
grep 'unihan-etl' pyproject.toml
```

Also check the installed version:

```bash
uv pip show unihan-etl
```

### 1b. Ensure local unihan-etl clone is fresh

The local clone lives at `~/work/cihai/unihan-etl/`. Fetch and check tags:

```bash
cd ~/work/cihai/unihan-etl && git fetch --tags origin
git tag --sort=-v:refname | head -5
```

### 1c. Identify the target version

Compare the current pinned version (from pyproject.toml) with the latest tag from the local clone. If already at latest, report "cihai is already on the latest unihan-etl (vX.Y.Z)" and stop — unless `$ARGUMENTS` explicitly names a version.

### 1d. Study what changed

Read the unihan-etl CHANGES file between the current and target versions:

```bash
cd ~/work/cihai/unihan-etl && git log v<current>..v<target> --oneline
```

Read the CHANGES entries for the target version. Focus on changes to the APIs cihai imports:

| File | Import | What to check |
|------|--------|---------------|
| `src/cihai/core.py` | `from unihan_etl.util import merge_dict` | Function signature, return type |
| `src/cihai/data/unihan/bootstrap.py` | `from unihan_etl import core as unihan` | `Packager.__init__`, `download()`, `export()` |
| `src/cihai/data/unihan/bootstrap.py` | `from unihan_etl.constants import UNIHAN_MANIFEST` | Constant shape, field names |
| `src/cihai/data/unihan/bootstrap.py` | `from unihan_etl.util import merge_dict` | Same as above |
| `src/cihai/data/unihan/bootstrap.py` | `from unihan_etl.options import Options as UnihanOptions` | Dataclass fields (TYPE_CHECKING only) |
| `tests/test_utils.py` | `from unihan_etl.util import merge_dict` | Same as above |

Also grep for any new imports that may have been added since this table was written:

```bash
grep -r "unihan_etl\|unihan-etl" src/ tests/
```

### 1e. Assess impact

Classify the update into one of three tiers:

| Tier | Description | Commits needed |
|------|-------------|----------------|
| **Simple bump** | No API changes, maintenance/docs only | 2 (package + CHANGES) |
| **Adaptation** | API changes require code updates | 3-4 (package + code + tests + CHANGES) |
| **Feature integration** | New features to adopt in cihai | 3-5 (package + code + tests + CHANGES, possibly split) |

Present findings to user and confirm before proceeding.

If `--dry-run`, report findings and stop here.

---

## Phase 2: Package Bump Commit

**Goal**: Update the version constraint and lock file.

### 2a. Create or verify branch

Check if a branch already exists:

```bash
git branch --list "unihan-etl-v<target>"
```

If not, create one:

```bash
git checkout -b unihan-etl-v<target>
```

### 2b. Update pyproject.toml

Change the `unihan-etl` dependency version constraint. cihai uses compatible-release constraints (`~=`):

```
"unihan-etl~=0.XX.Y"
```

### 2c. Remove uv.sources override (if present)

Check `pyproject.toml` for a `[tool.uv.sources]` section pointing unihan-etl at a branch or local path. If found, remove it before locking.

### 2d. Update lock file

```bash
uv lock
```

### 2e. Verify installation

```bash
uv sync && uv run python -c "import unihan_etl; print(unihan_etl.__version__)"
```

### 2f. Commit

Stage only `pyproject.toml` and `uv.lock`. Commit message format:

```
py(deps) Bump unihan-etl v<old> -> v<new>

See also:
- https://github.com/cihai/unihan-etl/blob/v<new>/CHANGES#unihan-etl-<slug>
- https://unihan-etl.git-pull.com/history.html#unihan-etl-<slug>
```

The version slug uses dashes and includes the release date: `0-41-0-2026-03-21`. Extract the date from the CHANGES heading (e.g., `## unihan-etl 0.41.0 (2026-03-21)`). For the GitHub anchor, strip dots only: `0410` (no dashes, no date).

**Exemplar** (from real history):
```
py(deps) Bump unihan-etl v0.38.0 -> v0.39.1

See also:
- https://github.com/cihai/unihan-etl/blob/v0.39.1/CHANGES#unihan-etl-0391-2026-01-24
- https://unihan-etl.git-pull.com/history.html#unihan-etl-0-39-1-2026-01-24
```

---

## Phase 3: Code Adaptation Commit (if needed)

**Goal**: Update cihai source code for API changes.

Skip this phase entirely if the unihan-etl update has no breaking or API changes affecting cihai.

### 3a. Identify affected code

Search cihai source for usage of changed unihan-etl APIs:

```bash
grep -r "from unihan_etl" src/
grep -r "import unihan_etl" src/
```

Cross-reference with the breaking changes identified in Phase 1d.

### 3b. Make code changes

Adapt imports, type annotations, function calls, and error handling to match the new unihan-etl API.

### 3c. Run type checking and tests

```bash
uv run mypy
uv run pytest
```

Fix any failures that stem from API changes (not test-specific issues — those go in Phase 4).

### 3d. Commit

Stage only `src/` files. Commit message format uses the affected module as scope:

```
<module>(fix|feat[detail]): description of adaptation

why: unihan-etl <new> changed <what>
what:
- Specific change 1
- Specific change 2
```

---

## Phase 4: Test Adaptation Commit (if needed)

**Goal**: Update test code for API or behavior changes.

Skip if no test changes are required.

### 4a. Run full test suite

```bash
uv run pytest
```

### 4b. Fix test failures

Address failures caused by changed unihan-etl behavior, fixtures, or output formats.

### 4c. Commit

Stage only `tests/` and `conftest.py` files. Commit message format:

```
tests(fix|feat[detail]): description

why: Explanation tied to the unihan-etl update
what:
- Specific test changes
```

---

## Phase 5: CHANGES Entry Commit

**Goal**: Document the update in the changelog.

### 5a. Determine section

For unihan-etl bumps, the entry goes under `### Breaking changes` in the unreleased section. This is the established convention — even minor bumps use this section because they change the minimum dependency version.

### 5b. Write the entry

Format depends on the tier:

**Simple bump** — single bullet:
```markdown
### Breaking changes

- Bump unihan-etl v<old> -> v<new> (#???)
```

**Adaptation / Feature integration** — bullet with description:
```markdown
### Breaking changes

- Bump unihan-etl v<old> -> v<new> (#???)

  Brief description of what the new version brings or requires.
```

### 5c. Insert into CHANGES

Find the insertion point after the placeholder comments in the unreleased section:
```
<!-- END PLACEHOLDER - ADD NEW CHANGELOG ENTRIES BELOW THIS LINE -->
```
and
```
<!-- Maintainers, insert changes / features for the next release here -->
```

Insert the entry after both comments. If these placeholders are not found, insert after the first `## ` heading in the unreleased section.

### 5d. Commit

Stage only `CHANGES`. Commit message:

```
docs(CHANGES) Bump unihan-etl v<old> -> v<new>
```

---

## Phase 6: Verification

**Goal**: Ensure everything works before pushing.

### 6a. Full quality check

```bash
uv run ruff format .
uv run ruff check . --fix --show-fixes
uv run mypy
uv run pytest
```

All four must pass. If any fail, fix and create a new commit for the appropriate phase.

### 6b. Review commits

```bash
git log --oneline origin/master..HEAD
```

Verify the commit sequence matches the expected pattern:
1. `py(deps) Bump unihan-etl X -> Y`
2. (optional) code adaptation commit(s)
3. (optional) test adaptation commit(s)
4. `docs(CHANGES) Bump unihan-etl vX -> vY`

---

## Phase 7: PR (unless --no-pr)

**Goal**: Push and open a pull request.

### 7a. Push

```bash
git push -u origin unihan-etl-v<target>
```

### 7b. Create PR

```bash
gh pr create --title "py(deps) Bump unihan-etl v<old> -> v<new>" --body "$(cat <<'EOF'
## Summary

- Bump unihan-etl from v<old> to v<new>
- [List any code/test adaptations]

See unihan-etl CHANGES: https://unihan-etl.git-pull.com/history.html#unihan-etl-<version-slug>

## Test plan

- [ ] `uv run pytest` passes
- [ ] `uv run mypy` passes
- [ ] `uv run ruff check .` passes
EOF
)"
```

### 7c. Update CHANGES PR number

After PR creation, update the `(#???)` placeholder in CHANGES with the actual PR number. Amend the CHANGES commit or create a follow-up commit:

```
docs(CHANGES) Add PR number for unihan-etl bump
```

Report the PR URL.

---

## Additional Resources

### Reference Files

- **`references/commit-patterns.md`** — Real commit messages from cihai history for all unihan-etl bump tiers, including URL slug formats and CHANGES conventions.
