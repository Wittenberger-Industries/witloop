---
type: Verification
title: Verification - Ship verification honesty (plan mode)
description: Revised plan can execute; constitution minor-bump vs owner-locked 1.16.1 remains for the design gate.
feature: 0003-blast-radius-proof
status: issues-found
timestamp: 2026-08-27
---

# Verification - Ship verification honesty (plan mode)

**Mode:** plan (round 2 of 2). Work type: feature (bug-fix overlay rows not required).
**Question:** will this plan, built exactly as written, deliver the feature?
**Verdict:** yes, it can execute. Round-1 F1/F2/F4 are closed. Remaining F3 (constitution minor vs owner-locked patch 1.16.1) is WARNING for the human design gate. This is the last plan-mode round; do not re-check.

## Coverage matrix

| Item | Covering task | Wired? | Notes |
|---|---|---|---|
| AC1 `### Safety fact` between Testing and Verification; Claim / Proof (`command` \| `unproven` \| `n/a`) / Not-run | Task 2 inserts template + copy-the-row + ship:8 box; `ShipSafetyFactTests` | yes | Task 2 Verify also re-runs `ShipBugFixEvidenceTests` so fail-then-pass stays inside Testing |
| AC2 result-mode BLOCKER missing heading / omitted matrix row / writeup-only; INFO honest unproven and valid docs-only `n/a`; BLOCKER `n/a` on runtime-behavior diff; plan-mode skip; every shipping work type | Task 1 always-on table after the bug-fix table; `CheckerSafetyFactTests` | yes | "Always-on" is the not-work-type-gated pin (opposite of the bug-fix gate). Docs-only paths pinned in Task 1 Do |
| AC3 absent `PR.md` is not a miss; checker still writes the Safety fact row into `verification.md` | Task 1 Do: write-the-row fallback, not a miss | yes | Round-1 partial language is now explicit |
| AC4 unproven cannot skip repo-map / RPA gate commands; no sixth Run step | Task 2 gate paragraph; Task 3 RPA "does not skip" | yes | Iron-law file stays at five Run steps |
| AC5 RPA pointer uses the same checker rows and the same `PR.md` heading; no D3 verdict list | Task 3 pointer; Task 2 heading (RPA reuses ship:5); Task 3 four-name-cluster ban | yes | `skills/rpa/SKILL.md` already loads this gate; Task 3 correctly does not edit it |
| AC6 manifests / `RELEASE` / overview lockstep 1.16.1; catalog 0.2.0; architecture `(1.16.0)` caption kept | Task 4 | yes | Verify is `tests.test_work_type_release` + `tests.test_work_type_docs`. Architecture.md is not in Files (keep). Catalog pin already in `ManifestLockstepTests` |
| Constitution: stdlib tests, no em dashes, TDD, tests in `tests/` | Tasks 1-3 red-then-green in one sitting; em-dash `assertNotIn` on edited files | yes | Round-1 TDD shape violation is gone |
| Constitution: agent charter additive; do not change markers / tools / loop unless spec names it | Task 1 Do: do not change tools, last-line markers, or the 2-round loop | yes | Spec names the new result-mode rows. Task 1 Verify re-runs `CheckerPreservedContractTests` |
| Constitution: hotspots serial (`skills/ship/SKILL.md`) | Task 2 only | yes | Wave 1 file sets (Task 1 vs Task 4) are disjoint writers |
| Constitution: three-manifest lockstep | Task 4 | yes | |
| Constitution: behavior/artifact changes bump **minor**; patch is relocation/compression | Task 4 sets patch `1.16.1` per spec Rollout owner lock | **violates** | Explicit, not silent. See F3. Gate waives or the owner lock stands |
| Constitution: rule-text PR rules inventory | existing ship:5 conditional `## Rules inventory` | n/a (ship, not build) | This diff will be rule text; no extra task needed |
| Constitution Simplicity | (4) over-build hunt | pass | No new always-loaded file, no new dep, no second gate, no `verify-report.md` |
| ADR-0001 capability table | standing; not re-litigated | n/a | No host if-tree, no new adapter |
| ADR-0002 work types; checker remains the single review agent; preserve markers/tools; bug-fix table stays five gated rows | Task 1 table **after** (not merged); Task 3 does not add a work type or a second agent | yes | Additive always-on rows are the same pattern as ADR-0002, not a re-open of decision 6. `CheckerBugFixMatrixTests` in Task 1 Verify |
| ADR-0003 generic `${PLUGIN_ROOT}` | no new `${PLUGIN_ROOT}` target | yes | Learning applied by avoidance |
| Glossary **Safety fact** | Tasks 1-2 (result-mode rows + `PR.md` heading); plan-mode carve-out in Task 1 | yes | Honor point is at ship |
| Glossary **Unproven** | Tasks 1-3 (INFO, not skip, not WAIVED) | yes | |
| Pitfall: first-pass absent `PR.md` | Task 1 | yes | |
| Pitfall: bug_fix_matrix theft | Task 1 (table after, not before, not merged) | yes | `bug_fix_matrix()` returns the first matching table; Verify includes `CheckerBugFixMatrixTests` (`len(rows) == 5`) |
| Pitfall: Testing slice breakage | Task 2 keep fail-then-pass strings in Testing; Task 2 Verify re-runs `ShipBugFixEvidenceTests` | yes | Slice `### Testing`:`### Verification` will include the new heading; asserts are positive |
| Pitfall: unproven skips the suite | Tasks 1-3 | yes | |
| Pitfall: token collision `n/a` vs `n/a - not configured` | Task 2 Do: both phrases, tests assert both | yes | Round-1 F4 closed |
| Pitfall: WARNING as hidden WAIVED | Task 1 INFO for honest unproven | yes | |
| Pitfall: INFO-only `## ISSUES FOUND` | Task 1 leave markers | yes | |
| Pitfall: `assertNotIn("PASS")` | Task 3 ban four-name cluster, not the word PASS | yes | RPA line still says "verdict is PASS" |
| Pitfall: architecture 1.16.0 caption | Task 4 Do: do not change it | yes | |
| Pitfall: new PLUGIN_ROOT file | no new always-loaded file | yes | |
| Pitfall: shared test module serializes 1→2→3 | Depends on 1, then 2; Wave 1 is 1+4 | yes | `tests/test_ship_safety_fact.py` is appended per task so red+green stay in one sitting |
| Learning `0003-work-type-routing` (serial wiring after new always-loaded files) | honored by avoidance | n/a | No new file an always-loaded skill must `${PLUGIN_ROOT}`-point at; Tasks 1-3 edit existing ship / checker / RPA gate paths. The new unittest module is not always-loaded |

## Round 1 follow-up

| ID | Round 1 | Round 2 |
|---|---|---|
| F1 BLOCKER separate red Task 1 / unowned Wave 2 Verify classes | tasks.md Task 1 was fail-only; production tasks omitted the test file | **closed.** Tasks 1-3 each own test class + production files, failing asserts first then implement. Shared module is serial (1→2→3). Task 4 is lockstep with no red safety-fact tests |
| F2 WARNING docs-only path list unpinned | "n/a on a runtime path" / "per spec" | **closed.** Task 1 Do enumerates `skills/`, `agents/`, `scripts/`, `tests/`, `references/`, `.claude-plugin/`, `.codex-plugin/`, `AGENTS.md` |
| F3 WARNING constitution minor vs patch 1.16.1 | spec locked 1.16.1 | **open.** Now an explicit owner-directed lock in spec Rollout and Task 4 Do ("do not retarget 1.17.0"). Still a constitution conflict for the human gate |
| F4 WARNING token-collision pin claimed but not tasked | pitfalls pointed at old Task 3; Do lists omitted the phrases | **closed.** Task 2 Do: Testing `n/a - not configured` vs Safety fact `n/a`; tests assert both |

## Findings

### F3 - WARNING - Constitution minor bump vs owner-locked patch 1.16.1

**Mode:** plan (round 2; same finding as round 1, now an explicit owner lock)
**Evidence:**
- `.wit/constitution.md` Git & shipping: "Behavior/artifact changes bump **minor**; pure relocation/compression bumps **patch**."
- This change adds a public `PR.md` heading and new checker BLOCKER rows (behavior/artifact).
- `spec.md` Rollout: "Patch 1.16.1. The owner directed a 1.16.x patch even though the constitution prefers minor for behavior/artifact changes. Do not retarget 1.17.0."
- `tasks.md` Task 4 Do: same owner lock; `RELEASE = "1.16.1"`.

**Why not BLOCKER:** the version number is an owner-directed spec lock, not a silent down-scope of the safety-fact behavior. The plan can execute at 1.16.1. The design gate must waive the minor-bump rule (or the owner lock stands as a recorded exception). Do not retarget 1.17.0 inside this plan round.

## Silent scope-reduction

No `v1` / stub / wire-later downgrade of a locked Proof token, INFO-vs-WARNING mapping, or "no sixth Run step". Roadmap harvest text (unproven → WARNING; every AC PASS/unproven/waived) is correctly **not** implemented (spec Non-goals). Tasks 1-3 say "failing asserts first" then production edits; that is TDD, not a red-only task.

## Over-build

No new dependency, no new always-loaded file, no second gate, no `verify-report.md`, no D3 vocabulary, no fourth work type. Design-notes edits are required by those files' own sync rule. Ship:1 pointer sentence is loaded-alone constitution, not gold-plating. Task 4 is six files, inside the 5-8 ceiling. Tasks 1-3 are 3 / 4 / 2 files.

## Pre-mortem

Assume build stalls mid-implementation:

- **Task 1 table order vs first-table parse:** `bug_fix_matrix()` in `tests/test_bug_fix_checker.py` returns the first Item/Plan/Result/Severity table. A copied helper that also takes the first table would miss the Safety fact rows if they sit after, and putting them first would fail `CheckerBugFixMatrixTests` (`len(rows) == 5`). Task 1 Verify includes that class, so the stall is in-task and recoverable (parse the later table / find by row name; keep a blank line so tables do not merge).
- **Task 2 heading slice:** `ShipBugFixEvidenceTests` slices `### Testing` to `### Verification`. Inserting `### Safety fact` enlarges that slice; Task 2 keeps fail-then-pass strings in Testing and re-runs that class. New tests that slice Testing→Safety fact must not match a prose `` `### Safety fact` `` before the fenced template (empty slice). Recoverable in Task 2.
- **Shared file:** `tests/test_ship_safety_fact.py` is not a hidden overlap. Waves put Task 4 beside Task 1; Tasks 2 and 3 are later serial waves. Wave-end (`skills/build/SKILL.md`) runs the full suite at each boundary; after Wave 1 only `CheckerSafetyFactTests` exists in the new module, which is green if Task 1 completed.

No missing dependency edge. No untestable Verify (all named unittest classes exist today except the new module, which each of Tasks 1-3 creates/appends).

## Applicable learning

`0003-work-type-routing`: WHEN parallel tasks create files the always-loaded skill must plugin-root-point at → DO add a serial wiring task after those files exist.

Honored: the plan creates no such file. `tests/test_ship_safety_fact.py` is not always-loaded. Tasks 1-3 only edit existing ship / checker / RPA gate paths.

## Line-level findings

n/a (plan mode)

## CHECK PASSED / ISSUES FOUND

One WARNING remains (F3). No BLOCKERs. Escalated to the design gate (plan-mode round budget exhausted).
