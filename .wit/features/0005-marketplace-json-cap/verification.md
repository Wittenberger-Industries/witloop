---
type: Verification
title: Verification - Marketplace plugin descriptions under 1024 chars (plan mode)
description: Plan covers all six ACs, bug-fix rows, pitfalls, and both learnings; no silent down-scope.
feature: 0005-marketplace-json-cap
status: passed
timestamp: 2026-08-28
---

# Verification (plan mode)

Work type: **bug-fix**. Question: will this plan, built exactly as written, deliver the feature?

**Verdict:** yes. One TDD task wires the cap, the three live strings, lockstep 1.16.3, and the named surface. No BLOCKER / WARNING / INFO.

## Coverage matrix

| Item | Covering task | Result |
| --- | --- | --- |
| AC1 Surface fail-then-pass (`python scripts/validate.py`; before = no plugin-description-cap line while over 1024; after = lengths ≤ 1024 and no `plugin description is`; exit 1 OKF allowed) | Task 1 Verify (tasks.md:29) names that surface string; step 2 is the cheap red stand-in (length unittest). Before-stamp already at `.logs/repro-before.txt`. Spec AC1 (spec.md:28). | covered |
| AC2 Root cause: DESC_CAP 7a walks SKILL.md only; 7a-json must exist | Spec AC2 + `research/repro.md` surviving mechanism (repro.md:33-35). Task 1 step 3 adds 7a-json (tasks.md:21). Source-anchor in the same test (tasks.md:17). | covered |
| AC3 Smallest fix: sibling 7a-json, same `DESC_CAP`, shortened copy, lockstep 1.16.3; no new checker, no fixture ROOT, no identity pin | Task 1 Do forbids import/subprocess, new test module, section-1 refactor, identity assert (tasks.md:15-17, 21, 23). Files list is exactly those surfaces (tasks.md:14). | covered |
| AC4 Regression: lockstep description test keeps host/command/`keep-alive` pins, adds Codex, pins `DESC_CAP` from source, `len(desc) <= cap`, `: plugin description is` | Task 1 steps 1-2 (tasks.md:17-19). Verify runs `tests.test_work_type_release` including `test_manifest_descriptions_keep_five_commands_and_five_hosts` (tasks.md:29). | covered |
| AC5 Advertised copy: five `/wit:` commands, five hosts, `keep-alive`, `refreshes the map`; no `documents and bootstraps`; no em-dash | Task 1 step 1 keeps every existing assert; step 4 canned paragraph (tasks.md:23-25). Measured: 678 chars; all pins present; no em-dash; no `/wit:investigate` / `/wit:how`. Verify also runs `test_manifests_say_scan_refreshes_not_bootstraps` (tasks.md:29). | covered |
| AC6 Version lockstep 1.16.3 (three plugins, `RELEASE`, overview, README); catalog `metadata.version` stays `0.2.0` | Task 1 step 5 (tasks.md:27). `RELEASE = "1.16.3"`; version test renamed `_1_16_3`; overview test renamed + `assertNotIn("1.16.2")`. Catalog pin already in `test_three_plugin_versions_*` (test_work_type_release.py:84). README frontmatter + "Current release is **1.16.2**" sentence named. | covered |
| Bug-fix: Repro contract / named surface | Task 1 Verify: `Surface string for logs: python scripts/validate.py` (tasks.md:29). Matches brief.md:33 and repro.md:12. | covered |
| Bug-fix: Root cause recorded | spec.md:29; research/repro.md:33-35. | covered |
| Bug-fix: Same-surface fail-then-pass | Task 1 includes the verify on that surface (tasks.md:29). Research before + post-fix Validate judgment (no cap line + lengths). Unittest red/green stay in the same task (tasks.md:15, 19, 29). | covered |
| Bug-fix: Smallest justified fix | spec.md:30; Task 1 is the evidence-backed minimum (mirror 7a, no new module). | covered |
| Bug-fix: Regression test | Task 1 [test] extends `test_manifest_descriptions_keep_five_commands_and_five_hosts`. No impracticality out needed. | covered |
| Pitfall: weakened pin (drop host/command/`keep-alive`) | Task 1 keeps every existing assert and adds Codex to the same loop (tasks.md:17); canned paragraph contains every pin. | covered |
| Pitfall: advertised copy drift (`scan` bootstraps) | Task 1 keeps `refreshes the map`, forbids `documents and bootstraps` (tasks.md:23); Verify runs the 0004 phrase test. | covered |
| Pitfall: skill-ideas OKF / exit 1 | Task 1 Verify judges cap-line absence + live lengths, not the whole OKF list (tasks.md:29); spec.md:24, 28. | covered |
| Pitfall: lockstep miss (RELEASE/overview/README) | Task 1 Files include those four plus three manifests (tasks.md:14, 27); overview `assertNotIn("1.16.2")`. | covered |
| Pitfall: import validate.py | Task 1 Do forbids import/subprocess (tasks.md:15); length is live-file + source-anchor. | covered |
| Pitfall: identity pin | Task 1 may copy the paragraph; must not `assertEqual` across files (tasks.md:23). | covered |
| Glossary Setup / Scan | Canned paragraph: setup is first-run; scan `refreshes the map`; missing repo-map runs setup first. Honored by Task 1 step 4. | covered |
| Glossary Model-judged /goal / Keep-alive none | Paragraph names keep-alive families (Claude/Codex predicate `/goal`; Grok and Cursor model-judged `/goal`; Copilot relaunch). Not Autopilot. | covered |
| Glossary Safety fact / Unproven | Plan-mode carve-out; honor at ship. | skip (plan) |
| Runtime State Inventory | Not a rename/migration. | n/a |
| ADRs | Dispatch: none apply. | n/a |
| Constitution: stdlib / no new dep | No new dependency. Reuse `DESC_CAP` + unittest. | covered (no extra task) |
| Constitution: no em-dash | Task 1 canned paragraph (measured: none) + existing `EM_DASH` assert kept. | covered |
| Constitution: TDD; don't weaken tests | Task 1 red-then-green; existing pins kept; Codex added (strengthens). | covered |
| Constitution: three-manifest version lockstep | Task 1 step 5. | covered |
| Constitution: Simplicity (no helper, fewest files, no interface-of-one) | Prohibitive; see over-build. Task 1: no helper, no new file, no second cap constant. | n/a (hunt 4) |
| Constitution: Git bump **minor** for behavior | Brief/spec lock **patch 1.16.3** (owner-directed, same 1.16.x pattern as 0004). Not treated as a miss. | noted |
| Constitution: ship-gate `validate.py` exit 0 | Pre-existing untracked `docs/skill-ideas/` OKF; spec non-goal. Task 1 judges this bug's signal. Full exit 0 is outside this plan. | noted (pitfall) |
| Learning 0001-cursor-capability-table: WHEN calling ensure_logdir.py → AVOID the feature folder (target `.logs`) | Plan never calls `ensure_logdir.py` on the feature folder. Pitfalls.md:18 and spec AC1 target `.wit/features/0005-marketplace-json-cap/.logs/` (dir exists; `.gitignore` is `*`; `repro-before.txt` present). Honored. | honored (no covering task required) |
| Learning 0004-setup: WHEN advertised copy moves → DO retarget README cells, manifests, and the old alias in the same sitting | Full WHEN is a command taking over first-run copy. This plan compresses in-place, does not relocate scan/setup copy. Manifests rewritten with every command/host pin; 0004 phrase test in Verify; README cells and `wit-scan` alias unchanged (and already refresh-not-bootstrap). Honored; does not hit the move-copy hook. | honored (no covering task required) |

## Findings

None.

## Silent scope-reduction

No v1/stub/mock/wire-later against locked decisions. Explicit non-goals (whole-file cap, SKILL.md, minify, identity pin, skill-ideas OKF, section-1 refactor, subprocess fixture) stay named, not quiet. Skipping missing/non-str description is the locked AC3 edge; the unittest KeyErrors if a field vanishes.

## Over-build (Simplicity)

No extra dependency, no new `tests/test_*.py`, no second cap constant, no helper, no identity assert, no fixture ROOT. Codex-in-loop and README/overview 1.16.3 are AC4/AC6, not extras. One task / one wave matches bug-fix red-and-green-in-one-task.

## Pre-mortem

- **Untestable Verify:** `python scripts/validate.py` stays exit 1 on skill-ideas OKF. Task 1 Verify already judges stdout substring + lengths, not exit 0. A runner that requires exit 0 would stall; the plan line to follow is tasks.md:29, not `sys.exit`.
- **File overlap / missing edge:** Wave 1 is Task 1 only. No parallel overlap.
- **Ceiling:** Task 1 names 7 files (inside ~5-8). Acceptable; splitting would break same-task red/green.
- **README host pin:** `tests.test_work_type_docs.ReadmeUserDocsTests.test_advertised_hosts_exclude_codex` requires README "four hosts" and no "Codex". Task 1 only retargets the version token in that sentence (tasks.md:27). Not a plan gap if followed; Task Verify does not run that module (ship suite will).

## Line-level

Skipped (plan mode).
