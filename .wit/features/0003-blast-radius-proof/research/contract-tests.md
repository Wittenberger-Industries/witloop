---
type: Research Note
title: Contract tests for ship verification honesty
description: How existing unittest modules pin skill/charter text and the 1.16.x bump, and the single test plan for this feature (no live checker).
feature: 0003-blast-radius-proof
timestamp: 2026-08-27
valid_until: 2026-09-26
---

# Contract tests: pin skill text, not a live checker

## Responsibility Map

Plugin markdown (skills, agent charter, gate references) plus `tests/`. No frontend or backend app layer.

## How the repo already pins contracts

All claims below are `[VERIFIED: tests/*.py read 2026-08-27]` unless tagged otherwise.

### Pattern A: load files as text, never import the plugin

`tests/test_bug_fix_checker.py` opens with:

> Independently loads agents/wit-code-checker.md and skills/ship/SKILL.md as text.
> Does not import other repo modules (several run checks on import).

`tests/test_work_type_release.py` repeats the same rule for `scripts/validate.py`.

Helpers copied per module (no `tests/` package, no `from tests.foo import`):

- `ROOT = Path(__file__).resolve().parents[1]`
- `load(path)` → `read_text(encoding="utf-8")` or AssertionError
- `frontmatter(text)` → split on `---`
- `markdown_tables(text)` / `_split_row` when a coverage matrix is the pin
- Section slices by heading: `text[text.index("### Testing") : text.index("### Verification")]`

`python -m unittest discover -s tests` is the repo-map suite command `[VERIFIED: .wit/repo-map.md]`. A new `tests/test_*.py` is picked up with no extra wiring.

### Pattern B: exact table cells prove BLOCKER without Task

`CheckerBugFixMatrixTests.test_additive_rows_blocker_for_omissions` is the template for "missing row is a checker BLOCKER":

1. Parse the first markdown table whose header contains item + plan + result + severity (`bug_fix_matrix()`).
2. Compare a frozen `BUG_FIX_ROWS` tuple of dicts (`item`, `plan`, `result`, `severity`) cell-for-cell.
3. `assertIn("BLOCKER", got["severity"])`.

That is the cheapest proof the charter will fail a missing row. The test never dispatches `wit-code-checker`, never mocks Task, never writes `verification.md`.

`test_bug_fix_matrix` returns **the first** matching table `[VERIFIED: tests/test_bug_fix_checker.py bug_fix_matrix]`. A new table with the same four header words *before* the bug-fix matrix would steal that parse and fail `len(rows) == 5`.

### Pattern C: heading slices on ship SKILL.md (PR template)

`ShipBugFixEvidenceTests` does not open a generated `PR.md`. It slices the **template inside** `skills/ship/SKILL.md`:

- `## 5 · PR description` then `### Summary` … `### Acceptance criteria`
- `### Testing` … `### Verification`
- `### Verification` … `### Risk & rollout`

`ShipRulesInventoryTests` pins a conditional heading with `(?m)^## Rules inventory\s*$` plus "Do not require it for every PR".

The fenced ````markdown` PR body in ship:5 is the template tests should search; sibling research owns the exact new heading string. This note does not name one.

### Pattern D: one RELEASE constant owns the 1.16.x bump

`tests/test_work_type_release.py`:

```
RELEASE = "1.16.0"
MARKETPLACE_CATALOG = "0.2.0"
```

`ManifestLockstepTests.test_three_plugin_versions_are_exactly_1_15_0` (name is stale from 1.15.0) `json.loads` three files and asserts each wit version equals `RELEASE`:

- `.claude-plugin/plugin.json` `version`
- `.codex-plugin/plugin.json` `version`
- `.claude-plugin/marketplace.json` plugin `name == "wit"` `version`

Marketplace **catalog** `metadata.version` stays `"0.2.0"`, not the plugin patch `[VERIFIED: test_work_type_release.py + marketplace.json]`.

`scripts/validate.py` also checks the three plugin versions agree, but it **runs the whole gate and `sys.exit` at import** `[VERIFIED: scripts/validate.py lines 62-110 and 374-385]`. Tests must keep reading those JSON files themselves. `test_validate_portability.py` and `test_plugin_root.py` only `Path.read_text` validate.py. `test_work_type_release.py` even asserts its own source does not `import validate`.

### Pattern E: overview vs architecture vs README

| File | Current version string | Existing test |
|---|---|---|
| `.wit/overview.md` | `Version \`1.16.0\` in the three plugin manifests` | `test_overview_routes_work_types_at_1_15_0`: `assertIn(RELEASE, text)` and `assertNotIn("1.14.1", text)` |
| `.wit/architecture.md` | caption: work-type routing `(1.15.0)`, PLUGIN_ROOT `(1.16.0)` | **does not** `assertIn(RELEASE, …)` |
| `README.md` | frontmatter `v1.16.0` and `Current release is **1.16.0**` | `test_work_type_docs.py` does **not** pin the version |
| `.wit/repo-map.md` | lockstep wording, no `1.16.0` | no version digit pin |

`EM_DASH = "\u2014"` is hunted in `test_work_type_release.py` and `test_work_type_docs.py`, not in `test_bug_fix_checker.py`. New shipped-text tests should hunt it on the files they own.

## Do not extend the bug-fix matrix

The checker bug-fix table is gated `When Work type is bug-fix` `[VERIFIED: agents/wit-code-checker.md]`. This feature's safety row applies to **every behavior PR**, plus docs-only `n/a`. Putting it in `BUG_FIX_ROWS` would:

- wrongly skip feature PRs
- force an edit to `len(rows) == 5` in `test_additive_rows_blocker_for_omissions`

Keep that tuple at five rows. Land the new rule in result-mode **outside** that gated table (prose, or a table whose headers do not match item/plan/result/severity).

## Recommendation (exactly one test plan)

### 1. Bump version in the existing release module only

In `tests/test_work_type_release.py` set `RELEASE = "1.16.1"`. Same commit: three manifests to `1.16.1`, overview `Version \`1.16.1\``. Leave `MARKETPLACE_CATALOG = "0.2.0"`.

Optionally replace the leftover `assertNotIn("1.14.1")` on overview with `assertNotIn("1.16.0")` so overview cannot claim both currents. Do not put `assertNotIn("1.16.0")` on architecture: `1.16.0` there is the PLUGIN_ROOT history line.

**Architecture does not need `1.16.1`.** Do not add `assertIn(RELEASE, architecture)`. Do not rewrite the PLUGIN_ROOT `(1.16.0)` caption to 1.16.1.

**README** currently states 1.16.0 with no test pin. Bump the two user-facing strings in the same release commit so docs match manifests. Do not add a new README version assertion (that would be a new pin `test_work_type_docs.py` never made).

Do not duplicate lockstep tests in a new module. Do not import `scripts/validate.py`.

### 2. New module for the feature (do not pile onto bug-fix or release)

Add `tests/test_ship_safety_fact.py`, unittest, stdlib, copy `load` / `frontmatter` / (if needed) `markdown_tables` locally. Docstring: independently loads the files below as text; does not import other repo modules; does not dispatch a checker.

**Files to Read** (paths the skills already load; no new always-loaded file):

- `skills/ship/SKILL.md` (PR template + ship:1 gate invocation)
- `agents/wit-code-checker.md` (result mode)
- `skills/rpa/references/verification-gate.md`
- `skills/ship/references/verification-gate.md` (iron law already lives here)

Do not create a second gate file. If plan later adds a new reference that always-loaded skills must `${PLUGIN_ROOT}`-point at, that is a **serial** task after the file exists (`validate.py` check 3 resolves those paths `[VERIFIED: scripts/validate.py docstring item 3]`). Default: edit the four files above so no wiring task is required.

Do not extend `test_work_type_docs.py` unless plan also edits `docs/design-notes/ship.md` / `wit-code-checker.md` (runtime never loads those).

### 3. Strings and tables to assert (heading text comes from sibling)

Do not invent a PR.md section title here. Assert the sibling's heading once it exists, plus these tokens that the brief already requires:

**Checker result mode** (slice around `**\`result\`**` / result-mode, **outside** the bug-fix `When Work type is bug-fix` block):

- missing row, or writeup with none of `command` / `unproven` / `n/a` → **BLOCKER**
- honest `unproven` → **INFO**
- `n/a` plus a docs-only reason → **INFO**
- taxonomy remains `BLOCKER` / `WARNING` / `INFO`
- the D3 cluster `PASS / CONCERNS / FAIL / WAIVED` is absent as a severity list (do **not** `assertNotIn("PASS")` globally: RPA gate already says "verdict is PASS" in English `[VERIFIED: skills/rpa/references/verification-gate.md]`)

If sibling lands a table, freeze a `SAFETY_FACT_ROWS` (or equivalent) tuple like `BUG_FIX_ROWS`. Headers must not steal `bug_fix_matrix()`.

**Ship SKILL.md** (slice `### Testing` / `### Verification` / the fenced PR template under `## 5 · PR description`):

- one safety-fact row is required for behavior PRs
- proof is a command run **this session**, or the word `unproven`
- extra named checks that were not run are listed `unproven`, never omitted
- docs-only may use `n/a` with a reason
- `unproven` does not skip repo-map gate commands (`pytest` / `validate.py` when configured)
- `assertNotIn(EM_DASH, text)` on this file

**RPA verification-gate.md:** the same tokens / the same checker mapping (pointer or repeated rule). Still one gate; still `${PLUGIN_ROOT}/agents/wit-code-checker.md` result mode.

**Ship verification-gate.md:** keep the iron law ("command actually run in this session"). If sibling adds an explicit pointer at the PR row, assert that pointer; do not require the plugin version string in this file.

**Self-check in the new module** (copy from `test_work_type_release.py`): this file's source does not `import validate` / `from validate import`.

### 4. What "proves BLOCKER" means in CI

Green tests mean: if a human or agent follows the charter and template, a missing or writeup-only row is classified BLOCKER. They do not execute the checker. That is the same honesty level as today's bug-fix matrix tests.

## Don't-hand-roll

| Problem | Don't build | Use instead | Why |
|---|---|---|---|
| Prove checker BLOCKER | Live Task / fake verification.md | Charter string + optional table cells | `test_bug_fix_checker.py` |
| Three-manifest 1.16.1 | New lockstep class | `RELEASE` in `test_work_type_release.py` | Single pin; validate.py already agrees on import-unsafe path |
| Shared test helpers | `tests/helpers.py` | Copy `load` / `frontmatter` | No test imports another test module |
| New safety-fact.md | Extra always-loaded ref | Edit existing ship/RPA/checker files | Avoid PLUGIN_ROOT serial wiring; brief: no second gate |

## Assumptions Log

| Claim | Why assumed | Load-bearing? |
|---|---|---|
| Exact PR.md heading string | Sibling charter owns headings | no (tests assert whatever that note names) |
| README version bump without a new assertion is enough | `test_work_type_docs.py` never pinned `1.16.0` | no |
| Architecture caption stays `1.16.0` for PLUGIN_ROOT | Existing architecture test ignores `RELEASE` | no |

## Risks / unknowns

- A new result-mode table with Item / Plan / Result / Severity headers **before** the bug-fix table breaks `bug_fix_matrix()`. Put new rules in prose or distinct headers, after that table if a table is required.
- `assertNotIn("PASS")` on RPA/ship text would false-fail. Ban the D3 four-name list, not the English word.
- Overview `assertNotIn("1.16.0")` is safe; the same assert on architecture is not.
- `validate.py` on import exits the process. Never `import` it from tests.
- New `${PLUGIN_ROOT}/...` targets must exist before the pointer lands or `validate.py` check 3 fails.

## Dependency Legitimacy

None added.

## Citations (repo)

- `tests/test_bug_fix_checker.py`
- `tests/test_work_type_release.py`
- `tests/test_work_type_docs.py`
- `tests/test_validate_portability.py`
- `scripts/validate.py` (read as text only)
- `agents/wit-code-checker.md` result-mode bug-fix table
- `skills/ship/SKILL.md` ship:5 PR template
- `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.claude-plugin/marketplace.json` (wit `1.16.0`; catalog `0.2.0`)
- `.wit/overview.md`, `.wit/architecture.md`
