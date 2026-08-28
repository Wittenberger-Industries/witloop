---
type: Research Note
title: "Smallest DESC_CAP check for the three plugin JSON descriptions"
description: Place a 7a-json loop next to SKILL 7a; pin live lengths plus Codex in the existing lockstep test; do not require identical texts or a subprocess fixture.
feature: 0005-marketplace-json-cap
timestamp: 2026-08-28
valid_until: 2026-09-27
---

# Smallest DESC_CAP check for plugin JSON descriptions

## Responsibility Map

Plugin-manifest / structure-gate layer only (this repo is not a frontend/backend app). The check lives in `scripts/validate.py`; the unittest lives in `tests/test_work_type_release.py`. Wording of the three description strings is out of this charter.

## What must stay true

- Each of the three plugin `description` fields is `<= DESC_CAP` (1024). [VERIFIED: brief.md]
- `python scripts/validate.py` remains the structure gate. [VERIFIED: constitution.md Testing; repo-map.md]
- Five advertised `/wit:` commands, five host names, and `keep-alive` stay pinned; do not delete or loosen those asserts. [VERIFIED: tests/test_work_type_release.py:86-104; constitution.md Testing]
- Patch 1.16.3; three-manifest version lockstep. [VERIFIED: brief.md]
- Do not import `scripts/validate.py` from tests (it runs checks on import). [VERIFIED: tests/test_work_type_release.py:4-5, 184-187]

## Live lengths (this session)

| Field | Chars | vs 1024 |
| --- | --- | --- |
| `.claude-plugin/marketplace.json` `plugins[name=wit].description` | 1357 | +333 |
| `.claude-plugin/plugin.json` `description` | 1396 | +372 |
| `.codex-plugin/plugin.json` `description` | 1396 | +372 |
| marketplace `metadata.description` (out of scope) | 210 | under |

[VERIFIED: python json.loads this session; matches research/repro.md]

`plugin.json` text == Codex text today; neither equals the marketplace wit description. [VERIFIED: equality check this session]

## Prior art in this repo

### DESC_CAP / 7a (the pattern to copy)

`DESC_CAP = 1024` at `scripts/validate.py:326`. Check 7a walks `skills/**/SKILL.md` and `references/skill-aliases/**/SKILL.md` via `_fm_desc`, and errors when `len(desc) > DESC_CAP`. [VERIFIED: scripts/validate.py:326-331]

It does **not** walk `.claude-plugin/*.json` or `.codex-plugin/plugin.json`. Check 1 only `json.loads` those files and compares versions. Lint scope 7c includes `.claude-plugin/*.json` for dead strings, not length, and does **not** include `.codex-plugin/`. [VERIFIED: scripts/validate.py:62-103, 351-357]

### SKILL unittest (the test pattern to copy)

`tests/test_work_type_routing.py::test_dev_and_alias_descriptions_under_cap_with_conservative_tells` reads `DESC_CAP = (\d+)` from validate.py **source**, asserts `cap == 1024`, then `assertLessEqual(len(desc), cap)` on **live** SKILL files. It does not subprocess validate.py and does not use an over-cap fixture. [VERIFIED: tests/test_work_type_routing.py:243-255]

### Lockstep pin (must not weaken)

`tests/test_work_type_release.py::test_manifest_descriptions_keep_five_commands_and_five_hosts` loops **only** `(plugin["description"], wit["description"])` and asserts:

- all five `HOSTS` (`Claude Code`, `Codex CLI`, `Copilot CLI`, `Grok Build`, `Cursor`)
- `/wit:setup`, `/wit:scan`, `/wit:dev`, `/wit:rpa`, `/wit:add-issues`
- `keep-alive`
- not `/wit:investigate`, not `/wit:how`, not em-dash

[VERIFIED: tests/test_work_type_release.py:86-104]

Codex `description` is **not** in that loop. Codex is loaded for version lockstep only. [VERIFIED: tests/test_work_type_release.py:72-84 vs 86-90]

### Why a subprocess over-cap fixture does not fit

- `ROOT = Path(__file__).resolve().parent.parent` is baked in; there is no argv/fixture root. [VERIFIED: scripts/validate.py:53]
- Tests that mention validate.py refuse to import it and refuse to temp-rename live files in a parallel wave. [VERIFIED: tests/test_work_type_release.py:4-5; tests/test_validate_portability.py:1-4]
- Existing validate.py tests are source-anchors or live-file asserts, not CLI subprocess of validate.py.

### 0004 advertised-copy learning

WHEN advertised copy moves, retarget README cells, **plugin/marketplace descriptions**, and the old alias in the same sitting; lockstep tests pin **names and order**, not identical prose. [VERIFIED: .wit/learnings/0004-setup.md; .wit/learnings.md hook]

`tests/test_setup.py::test_manifests_say_scan_refreshes_not_bootstraps` already walks all three JSON paths for a phrase pin (`refreshes the map`), not identity. [VERIFIED: tests/test_setup.py:582-586]

## Options (honest)

| Option | What | Reject because |
| --- | --- | --- |
| A (chosen) | 7a-json next to 7a using the same `DESC_CAP`; extend the existing lockstep test | — |
| B | Length check in section 1 (JSON manifests) | `DESC_CAP` lives at 7a; moving it or duplicating 1024 splits the pattern the brief says to mirror. Bigger validate.py diff. |
| C | New test module + subprocess fixture / import validate.py | New file (YAGNI). Import runs the whole gate. Fixture needs a fake ROOT. Parallel-wave unsafe if temp-renaming live manifests. Weakens nothing but costs more than the SKILL pattern. |
| D | Require `plugin.json` description == marketplace == Codex | They are already not identical (marketplace vs plugin). Identity is not a lockstep pin today. Would force one wording and fight independent shortening. |

## Decision (exactly one)

**Extend check 7a with a 7a-json loop; extend `test_manifest_descriptions_keep_five_commands_and_five_hosts` in place.**

### `scripts/validate.py`

1. Keep the single `DESC_CAP = 1024`. Do not add a second constant.
2. After the SKILL 7a loop (after line 331), add a **7a-json** block that:
   - reads `.claude-plugin/plugin.json` top-level `description`
   - reads `.codex-plugin/plugin.json` top-level `description`
   - reads `.claude-plugin/marketplace.json` **only** `plugins[name=wit].description`
   - **does not** cap `metadata.description` (210 chars today; out of scope)
3. If the value is a `str` and `len(desc) > DESC_CAP`, append an error in the SKILL shape:
   `{rel}: plugin description is {len(desc)} chars (> {DESC_CAP}-char cap)`
   (distinct from `SKILL description is` so a source-anchor can pin the new gate).
4. Invalid JSON: `continue` / `pass` (section 1 already reported it).
5. Missing / non-str description: skip (do not add a new required-key check). The unittest already KeyErrors if the three fields vanish.
6. No helper function (one caller; constitution: no abstraction until a second caller).
7. Docstring check 7: add that the three plugin JSON `description` fields use the same cap. One sentence; do not invent a new numbered check.

Do **not** put this on lint_scope 7c (that is dead-string scan, and it omits Codex).

### `tests/test_work_type_release.py` (do not weaken the pin)

Edit `test_manifest_descriptions_keep_five_commands_and_five_hosts` only (plus `RELEASE = "1.16.3"` as the sibling version lockstep already owned by this file — not this charter's wording task).

1. **Keep every existing assert** (hosts, five `/wit:` commands, `keep-alive`, banned investigate/how, em-dash).
2. **Add Codex to the loop** — change the tuple to `(plugin["description"], wit["description"], codex["description"])`. Load `codex` the same way the version test already does. This does not loosen a pin; it applies the same pins to the third field this feature will rewrite. 0004 already treats all three manifests as advertised-copy surfaces. [VERIFIED: Codex omitted today at :90]
3. **Live-file length, SKILL-test style:** read `DESC_CAP = (\d+)` from `scripts/validate.py` source, `assertEqual(cap, 1024)`, and `assertLessEqual(len(desc), cap)` for each of the three strings. Do **not** hardcode 1024 only in the test while leaving the constant unpinned.
4. **Source-anchor the new gate** (the SKILL test never had to, because 7a already existed): `assertIn(": plugin description is", validate_src)` so CI cannot ship shortened live files while 7a-json was never added. This is still not a subprocess. Pattern: `tests/test_validate_portability.py` and `ValidateSourceAnchorTests`.
5. **Do not** `assertEqual` plugin vs marketplace vs Codex text.
6. **Do not** change `test_work_type_routing.py` (that test is SKILL/alias tells + DESC_CAP for skills; leave it).
7. **Do not** add a new `tests/test_*.py`.
8. **Do not** import or subprocess `validate.py`.

TDD order: add the length (+ Codex-in-loop) asserts first (red on 1357/1396). Plan/build then shortens the three strings (out of this charter) until the pin+length test is green. Then add 7a-json so `python scripts/validate.py` is the structure gate for a future over-cap.

### Identical text?

**No.** Marketplace wit description is already a different string from plugin.json/Codex. Lockstep is version + advertised **names**, not one shared paragraph. Requiring identity would be a new constraint, would shrink the wording budget, and is not needed to keep the five-command / five-host pins.

Codex matching plugin.json today is historical, not a test pin. After shortening they **may** stay equal (least surprise, copy-paste) but the test must not require it.

### Subprocess over-cap fixture?

**No.** Live-file length like the SKILL test, plus a source-anchor that 7a-json exists. validate.py cannot point at a temp tree without rewriting ROOT (out of scope).

## Don't-Hand-Roll

| Problem | Don't build | Use instead | Why |
| --- | --- | --- | --- |
| Cap plugin JSON descriptions | New checker module / second cap constant | Existing `DESC_CAP` + 7a-json | Brief: mirror 7a |
| Prove over-cap fails | Temp-rename manifests; import validate.py | Live `assertLessEqual` + source-anchor | ROOT is `__file__`-relative; import runs the whole gate |
| Keep commands/hosts | Rewrite or drop lockstep asserts | Same test, same asserts, add Codex to the tuple | Constitution: don't weaken tests |
| Three texts in lockstep | `assertEqual` across files | Phrase pins already in test_setup + command/host pins | 0004: names, not identical prose |

## Files this charter says to change

| File | Change |
| --- | --- |
| `scripts/validate.py` | 7a-json after 7a; docstring check 7 sentence |
| `tests/test_work_type_release.py` | Codex in pin loop; DESC_CAP + live length; source-anchor; `RELEASE` bump is sibling |

Out of this charter (same feature, not this question): shorten the three JSON description strings; bump the three manifest versions to 1.16.3; overview/README version tells.

## Risks / unknowns (plan must consume)

- After shortening, the five-command / five-host / keep-alive pins still have to fit in 1024. That is a wording budget problem for plan/build, not a check-shape problem. If a pin string is dropped to make the cap, that is a failed task, not a test change.
- `test_overview_routes_work_types_at_1_16_2` and `RELEASE` in the same file must move to 1.16.3 with the manifests; forgetting the constant is a known lockstep miss.
- Untracked `docs/skill-ideas/` OKF failures already exit 1 from validate.py; they are not this bug and must not be "fixed" in this diff.
- 7a-json re-parses JSON already parsed in section 1. Harmless (section 1 already re-parses). Do not refactor section 1 to share a parsed dict (blast radius).

## Assumptions Log

| Claim | Why assumed | Load-bearing? |
| --- | --- | --- |
| Host marketplaces also ceiling plugin `description` at 1024 (same number as agent-skills SKILL.md) | Brief mandates 1024 and "mirror DESC_CAP"; this session did not fetch host schema docs (repo-question mode) | No — implementation uses repo `DESC_CAP` regardless of vendor docs |
| Codex may diverge from plugin.json after shortening | Today they are equal; no test requires equality | No — recommendation is not to add an identity pin |

No load-bearing `[ASSUMED]` rows.

## Dependency Legitimacy

None added. Stdlib `json` + existing unittest.

## Hard-to-reverse?

No. Adding a length check and a unittest assert is a patch; revert is delete the loop and the extra asserts.
