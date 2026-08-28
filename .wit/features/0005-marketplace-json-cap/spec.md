---
type: Spec
title: Marketplace plugin descriptions under 1024 chars
description: Cap the three plugin JSON description fields at DESC_CAP, shrink live copy, ship 1.16.3.
feature: 0005-marketplace-json-cap
timestamp: 2026-08-28
---

# Spec: Marketplace plugin descriptions under 1024 chars

## Summary
1.16.2 plugin `description` fields exceed the 1024-character marketplace/install ceiling (marketplace wit 1357; plugin.json and Codex 1396). `DESC_CAP` already caps SKILL.md descriptions; it does not walk the three JSON manifests. Extend that same cap, shorten the three strings so they still name the five commands, five hosts, and keep-alive, and bump lockstep version to 1.16.3.

## Goals
- Each of the three plugin `description` fields is ≤ 1024 characters.
- `python scripts/validate.py` fails a future over-cap the same way it fails an over-cap SKILL.md description.
- Manifest versions, `RELEASE`, overview, and README lockstep at 1.16.3.

## Non-goals
- A whole-file size cap on marketplace.json.
- SKILL.md or agent description changes.
- Minifying JSON or dropping keywords.
- Identical prose across the three descriptions (version lockstep only).
- Fixing untracked `docs/skill-ideas/` OKF failures (pre-existing; not this bug).
- Refactoring validate.py section 1 to share parsed JSON.

## Acceptance criteria  (each must be testable)
1. **Surface fail-then-pass.** Given current 1.16.2 texts over 1024, `python scripts/validate.py` does not report a plugin-description-cap error (repro-before). After the fix, live lengths are ≤ 1024 and validate.py reports no `plugin description is` error. → verified by: `.logs/repro-before.txt` vs `.logs/repro-after.txt` on surface `python scripts/validate.py` (pass = no plugin-description-cap line + lengths ≤ 1024; exit code may still be 1 from out-of-scope skill-ideas OKF).
2. **Root cause.** The surviving mechanism is: `DESC_CAP` 7a walks only SKILL.md, not the three JSON plugin descriptions. → verified by: `research/repro.md`; 7a-json exists in `scripts/validate.py`.
3. **Smallest fix.** One sibling 7a-json loop using the existing `DESC_CAP`, shortened live descriptions, and lockstep 1.16.3. No new checker, no fixture ROOT, no identity pin. → verified by: diff is those files; no new `tests/test_*.py`; no second cap constant.
4. **Regression test.** The lockstep description test keeps every host/command/`keep-alive` pin, adds Codex to the loop, pins `DESC_CAP` from validate.py source, and asserts live `len(desc) <= cap`. A source-anchor requires `: plugin description is` in validate.py. → verified by: `python -m unittest tests.test_work_type_release.ManifestLockstepTests.test_manifest_descriptions_keep_five_commands_and_five_hosts`
5. **Advertised copy.** Each of the three descriptions still contains the five `/wit:` commands, five host names, `keep-alive`, and `refreshes the map`; none contain `documents and bootstraps` or an em-dash. → verified by: that same unittest plus `python -m unittest tests.test_setup.AdvertisedScanRetargetTests.test_manifests_say_scan_refreshes_not_bootstraps`.
6. **Version lockstep.** Three plugin versions, `RELEASE`, overview, and README current-release tells are 1.16.3. Marketplace catalog `metadata.version` stays `0.2.0`. → verified by: `python -m unittest tests.test_work_type_release`

## Design
Reuse `DESC_CAP = 1024` in `scripts/validate.py`. Immediately after the SKILL 7a loop, add a 7a-json block that reads `.claude-plugin/plugin.json` `description`, `.codex-plugin/plugin.json` `description`, and marketplace `plugins[name=wit].description` (not `metadata.description`). Error shape: `{rel}: plugin description is {n} chars (> {DESC_CAP}-char cap)`. Invalid JSON: skip (section 1 already reported). Missing/non-str description: skip.

Tests stay in `tests/test_work_type_release.py`. Do not import or subprocess validate.py. Do not require the three strings to be identical.

Shortened copy may share one paragraph (678-char draft in tasks.md) as long as every pin still matches.

No ADR: nothing hard to reverse.

## Interfaces & data changes
- **APIs / signatures:** none. validate.py CLI unchanged; new error strings only when a description exceeds DESC_CAP.
- **Data / schema:** none. Marketplace catalog version stays 0.2.0. Plugin versions 1.16.2 → 1.16.3.
- **Config / env:** none.
- **Dependencies:** none.

## Test plan
- **Level rule:** unit + the existing structure gate. Do not add a validate.py subprocess fixture.
- **Unit:** lockstep description pins + live length + source-anchor; version lockstep; setup advertised-copy phrase pin.
- **Integration / e2e:** `python scripts/validate.py` on the live tree; ignore skill-ideas OKF noise when judging this bug.
- **Edge cases:** invalid JSON already handled by section 1; do not add a required-key check for description.

## Rollout & back-out
Patch release 1.16.3. Revert the PR to restore 1.16.2. No migration.

## Open questions
- None.

## Citations
[1] `.wit/features/0005-marketplace-json-cap/research/repro.md`: lengths and missing 7a-json.
[2] `.wit/features/0005-marketplace-json-cap/research/desc-cap-check.md`: chosen check shape.
[3] `scripts/validate.py` 7a SKILL loop: pattern to copy.
