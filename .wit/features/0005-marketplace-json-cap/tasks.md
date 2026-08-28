---
type: Task List
title: "Tasks: Marketplace plugin descriptions under 1024 chars"
description: One TDD task: failing lockstep length test, 7a-json, shortened descriptions, 1.16.3 lockstep.
feature: 0005-marketplace-json-cap
timestamp: 2026-08-28
---

# Tasks: Marketplace plugin descriptions under 1024 chars

> Ordered. Each task is small enough for one focused sitting and ends green.

## Task 1: Cap JSON plugin descriptions at DESC_CAP   [test]
- **Files:** `tests/test_work_type_release.py`, `scripts/validate.py`, `.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.wit/overview.md`, `README.md`
- **Do:** TDD, red then green in this task. Do not import or subprocess `scripts/validate.py`. Do not add a new test module. Do not touch `docs/skill-ideas/`. Do not refactor validate.py section 1.

  1. In `tests/test_work_type_release.py`: set `RELEASE = "1.16.3"`. Add `VALIDATE = ROOT / "scripts" / "validate.py"`. In `test_manifest_descriptions_keep_five_commands_and_five_hosts`, keep every existing host/command/`keep-alive`/banned-investigate/how/em-dash assert. Change the loop to `(plugin["description"], wit["description"], codex["description"])` (load `codex` the same way `test_three_plugin_versions_are_exactly_1_16_2` already does; rename that test to `test_three_plugin_versions_are_exactly_1_16_3`). Read `DESC_CAP = (\d+)` from `VALIDATE` source, `assertEqual(cap, 1024)`, and `assertLessEqual(len(desc), cap)` for each of the three strings. `assertIn(": plugin description is", VALIDATE.read_text(encoding="utf-8"))`. In `test_overview_routes_work_types_at_1_16_2`, rename to `_1_16_3`, keep `assertIn(RELEASE, text)`, and add `assertNotIn("1.16.2", text)`.

  2. Run `python -m unittest tests.test_work_type_release.ManifestLockstepTests.test_manifest_descriptions_keep_five_commands_and_five_hosts`. Confirm it fails because live lengths are 1357/1396, not because of a missing import or a dropped pin.

  3. In `scripts/validate.py`, keep the single `DESC_CAP = 1024`. After the SKILL 7a loop, add 7a-json: for `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` use top-level `description`; for `.claude-plugin/marketplace.json` use `plugins[name=wit].description` only (not `metadata.description`). If value is a `str` and `len(desc) > DESC_CAP`, append `{rel}: plugin description is {len(desc)} chars (> {DESC_CAP}-char cap)`. Invalid JSON: continue. Missing/non-str: skip. No helper. Docstring check 7: one sentence that the three plugin JSON description fields use the same cap.

  4. Replace each of the three plugin `description` strings with this paragraph (678 chars; pins every required phrase). They may stay identical; do not add an identity assert. Do not use an em-dash. Keep `refreshes the map`. Do not write `documents and bootstraps`.

     Witloop: opinionated spec-driven loop for Claude Code, Codex CLI, Copilot CLI, Grok Build, and Cursor. /wit:setup is first-run (repo docs, constitution, models, ledger; --auto writes simple plus ledger on); /wit:scan refreshes the map (--refresh; missing repo-map runs setup first); /wit:dev routes feature | bug-fix | investigation (--kind) then brainstorms, designs at one gate (--auto), and implements to a PR with keep-alive (Claude/Codex predicate /goal; Grok and Cursor model-judged /goal; Copilot relaunch); /wit:add-issues files GitHub issues; /wit:rpa builds UiPath from a PDD. Parallel worktrees, ADR log, token report. Soft-integrates superpowers and frontend-design.

  5. Set `"version": "1.16.3"` on `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, and the marketplace wit plugin entry. Leave marketplace `metadata.version` at `0.2.0`. In `.wit/overview.md` replace current `1.16.2` with `1.16.3`. In `README.md` frontmatter and the "Current release is **1.16.2**" sentence, move to 1.16.3. Do not edit historical 1.16.2 mentions under `.wit/features/0004-setup/`.

- **Verify:** `python -m unittest tests.test_work_type_release tests.test_setup.AdvertisedScanRetargetTests.test_manifests_say_scan_refreshes_not_bootstraps`. Then `python scripts/validate.py`: live plugin description lengths must be ≤ 1024 and stdout must not contain `plugin description is`. Do not treat skill-ideas OKF FAILs as this task failing. Surface string for logs: `python scripts/validate.py`.
- **Depends on:** -

## Waves  (derived from Depends on + Files: what build runs concurrently)
- Wave 1: task 1
