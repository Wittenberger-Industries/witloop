---
type: Verification
title: Verification - Work-type routing for bug fixes and investigations (plan mode)
description: Round 2 - F1-F3 and prior warning pins are mapped; one residual wave-2 validate gap remains.
feature: 0003-work-type-routing
status: issues-found
timestamp: 2026-08-25
---

# Verification: 0003-work-type-routing (plan mode, round 2)

**Question:** will this plan, built exactly as written, deliver the feature?
**Verdict:** yes on locked decisions F1-F3 and the round-1 warning pins, with one residual wave-safety WARNING.

Applicable learnings: none (progress.md `applicable learnings: none`).

## Round-1 disposition

| ID | Round-1 issue | Now | Evidence |
|----|---------------|-----|----------|
| F1 | Always-announce missing from Task 1 Do | **fixed** | tasks.md:22-24 exact announce line; contract-test inferred/override/default |
| F2 | Resume does not re-deduce unless `--kind` | **fixed** | tasks.md:17 `feature-folder-cases.md`; tasks.md:25-26 stamp honor + override wins; contract-test resume |
| F3 | Investigation capture-into-`.wit/` exception unowned | **fixed** | tasks.md:26-28 `understand` + pre-fix debug + chat-only exception; independently loaded integrations tests |
| W1 | Wave 1 dangling `${CLAUDE_PLUGIN_ROOT}` + Verify omitted `validate.py` | **mostly fixed** | tasks.md:24 point only at `work-types.md`; Task 1 Verify includes `validate.py`. Residual: Task 2 still omits it (W1r) |
| W2 | `design gate opened` then bypass; workflow skip cell; mid-build reopen | **fixed** | tasks.md:53-59 exact stamp after opened; skip never/feature vs recorded narrow-fix; revoke and reopen; test reopen path |
| W3 | Description/alias tells and `--kind` pass-through | **fixed** | tasks.md:28-29 conservative fix/investigation tells; "file a bug" stays add-issues; `--kind` beside `--auto` |
| W4 | `1.15.0` and rules inventory not runnable | **fixed** | Task 4 inventory heading + tests (tasks.md:68-71); Task 7 pins exactly `1.15.0` (tasks.md:99-103); spec AC11 verify line names both new modules |
| W5 | Task 6 was 13 files | **fixed** | split Task 6 docs vs Task 7 memory+release. Task 1 is 8 files at the ceiling (I2) |
| W6 | Semantic tests could accept a keyword table | **fixed** | tasks.md:30-31 orchestrator judgment, not a keyword-only runtime classifier |
| I2 | AC8 verify omitted `test_bug_fix_checker` | **fixed** | spec.md:68 both modules |

## Coverage matrix

| Item | Source | Covering task | Evidence | Status |
|------|--------|---------------|----------|--------|
| AC1 semantic deduce; `--kind` wins; invalid stops; mixed → announced `feature` | spec.md:39-41 | Task 1 | Do: semantic deduction, `--kind`, invalid stop, mixed→`feature`, always-announce | COVERED |
| AC2 resolve before writes; investigation exits; others folder-classify | spec.md:42-44 | Tasks 1, 2 | Task 1 before write-capable + hook order; Task 2 deny-list/exit | COVERED |
| AC3 stamp `Work type:`; missing=`feature`; resume no re-deduce unless `--kind` | spec.md:45-47 | Task 1 | stamp, missing default, resume honor, override wins; Files include `feature-folder-cases.md` | COVERED |
| AC4 investigation: no `.wit/` state; `how`/`why`; 2-explorer fallback; citations | spec.md:48-52 | Tasks 1, 2 | Task 2 route + deny-list; Task 1 chat-only capture exception so integrations.md cannot order a dossier write | COVERED |
| AC5 repro-contract brainstorm; systematic-debugging; root cause | spec.md:53-56 | Task 3 | Do + brainstorm/research Files | COVERED |
| AC6 plan+checker always; fail-closed conjuncts | spec.md:57-61 | Task 3 | mandatory plan/checker; every conjunct tested | COVERED |
| AC7 distinct `design gate bypassed (narrow-fix)`; fail closed; `--auto` separate; feature never bypasses | spec.md:62-64 | Tasks 3, 5 | exact stamp after `design gate opened`; workflow skip wording; `--auto` separate | COVERED |
| AC8 same-surface; PR root cause+smallest fix; regression or rationale; result-mode BLOCKER | spec.md:65-68 | Tasks 3, 4 | overlay + additive checker rows + ship PR evidence; both test modules | COVERED |
| AC9 three parsers count bypass as span2 start; approved/auto-approved unchanged | spec.md:69-71 | Task 5 | all three parser Files; failing bypass fixture first | COVERED |
| AC10 four commands; five-host table; feature default; markers; seven-file dossier | spec.md:72-74 | Tasks 1, 4, 6, 7 | four-command tests; checker markers; docs wording; release pin | COVERED |
| AC11 `1.15.0` lockstep; user docs; source memory; rules inventory in `PR.md` | spec.md:75-77 | Tasks 4, 6, 7 | heading in ship template; docs tests; version+parity pin; ship fills inventory from diff | COVERED |
| Brief always-announce + override; never silent | brief.md:17-18 | Task 1 | exact announce sentence; never ask or route silently | COVERED |
| Brief `--kind` wins | brief.md:14-15 | Task 1 | parse `--kind` | COVERED |
| Brief investigation read-only | brief.md:20-21 | Task 2 | deny-list | COVERED |
| Brief bug-fix proof | brief.md:35-37 | Tasks 3, 4 | same-surface + checker/ship | COVERED |
| Brief existing feature path preserved | brief.md:38 | Tasks 1, 3 | missing stamp=`feature`; feature compatibility tests | COVERED |
| Brief no fifth command / new agent / required MCP / RPA/add-issues | brief.md:44-46 | Tasks 1, 2, 4, 6 | four-command; checker additive-only; no rpa/add-issues Files | COVERED |
| Brief five-host via capability table | brief.md:50 | Tasks 1, 6 | alias `--kind`; description tells; five-host wording | COVERED |
| ADR-0002.1 semantic deduce before writes | ADR-0002:32-34 | Task 1 | Do matches including announce | COVERED |
| ADR-0002.2 investigation chat-only; no scan write | ADR-0002:35-37 | Tasks 1, 2 | hook + deny-list + capture exception | COVERED |
| ADR-0002.3 stamp; missing=`feature`; on-demand procedure | ADR-0002:38-40 | Task 1 | work-types.md; SKILL body points only there | COVERED |
| ADR-0002.4 overlay; root cause before plan; same surface | ADR-0002:41-43 | Task 3 | overlay Do | COVERED |
| ADR-0002.5 fail-closed distinct bypass; not `--auto` | ADR-0002:44-47 | Tasks 3, 5 | predicate + exact stamp + parsers | COVERED |
| ADR-0002.6 single checker; additive rows; preserve markers/caps/tools | ADR-0002:48-49 | Task 4 | additive-only + marker tests | COVERED |
| ADR rejected keyword-only helper | ADR-0002:64 | Task 1 | no helper script; contract-test against keyword-only classifier | COVERED |
| Glossary **Work type** | glossary.md:22-23 | Task 1 | stamp `Work type:`; flag remains `--kind` | COVERED |
| Constitution TDD / tests in `tests/test_*.py` | constitution.md:32-35 | all | header + per-task Verify | COVERED |
| Constitution no new dep | constitution.md:25-28, 37-39 | spec.md:105 | none | COVERED |
| Constitution agent charters additive | constitution.md:41 | Task 4 | preserve tools/modes/caps/markers | COVERED |
| Constitution hotspots serial | constitution.md:42 | waves | `dev` W1; `build`+`workflow` W2 Task 3; `ship` W3 | COVERED |
| Constitution minor lockstep | constitution.md:48 | Task 7 | exactly `1.15.0` three manifests | COVERED |
| Constitution rule-text inventory | constitution.md:51 | Tasks 4, 7 | template heading + ship fills from diff | COVERED |
| Simplicity (prohibitive) | constitution.md:24-30 | (4) | no extra runtime/agent/command; Task 6/7 split is the AC11 surface | PASS |
| Pitfall: classified after a write | pitfalls.md:11-13 | Tasks 1, 2 | hook-order + deny-list | COVERED |
| Pitfall: mixed intent → investigation | pitfalls.md:14-16 | Task 1 | mixed → announced `feature` | COVERED |
| Pitfall: "file a bug" stolen | pitfalls.md:17-19 | Task 1 | tells + four-command; add-issues verbs kept | COVERED |
| Pitfall: feature path regresses | pitfalls.md:19-21 | Tasks 1, 3 | missing stamp + compatibility | COVERED |
| Pitfall: optional skill required | pitfalls.md:22-24 | Task 2 | fallback; bootstrap omission keeps current install set | COVERED |
| Pitfall: host readonly flag | pitfalls.md:25-27 | Task 2 | portable deny-list | COVERED |
| Pitfall: false narrow-fix bypass | pitfalls.md:28-30 | Task 3 | conjuncts + BLOCKER veto + mid-build reopen now in Do | COVERED |
| Pitfall: `--auto` vs bypass | pitfalls.md:31-33 | Tasks 3, 5 | distinct stamps | COVERED |
| Pitfall: parser drift | pitfalls.md:34-36 | Task 5 | three implementations | COVERED |
| Pitfall: raw repro pruned | pitfalls.md:37-39 | Tasks 3, 4 | durable stamps/PR | COVERED |
| Pitfall: checker charter damaged | pitfalls.md:40-42 | Task 4 | additive-only marker tests | COVERED |
| Pitfall: manifest/docs mismatch | pitfalls.md:43-45 | Tasks 1, 6, 7 | alias tests; docs tests; `1.15.0` pin (pitfall still says "task 6" for the bump — I1) | COVERED |
| Learning: none applicable | progress.md:45 | — | no hook to honor | n/a |

## Findings

### W1r — WARNING — Task 2 Verify still omits `validate.py`

**Mode:** plan
**Evidence:** Task 2 Files create `skills/dev/references/investigation.md` (tasks.md:37-38); Verify is only `python -m unittest tests.test_investigation_route` (tasks.md:44). `scripts/validate.py` OKF/fence/trailing-newline checks glob `skills/**/*.md`. Wave 2 runs Task 2 in parallel with Task 3 (which does run `validate.py`), so Task 3 may not see Task 2's new file. A truncated or type-less `investigation.md` can leave wave 2 green until Task 7.

**Plan edit:** Task 2 Verify → `python -m unittest tests.test_investigation_route && python scripts/validate.py`. Name the investigation/bug-fix files in `work-types.md` as repo paths without `${CLAUDE_PLUGIN_ROOT}` so Task 1's validator stays green (Task 1 already forbids those env-var pointers from `SKILL.md`).

No BLOCKERs. Prior F1-F3 and W2-W6 are mapped with named files, TDD order, dependencies, and runnable Verify.

## Wave safety

| Wave | Tasks | Shared Files | Intermediate green? |
|------|-------|----------------|---------------------|
| 1 | 1 | — | Yes if `work-types.md` does not `${CLAUDE_PLUGIN_ROOT}`-point at not-yet-created route files (Task 1 Verify includes `validate.py`, so a dangling env-var path fails the task). |
| 2 | 2, 3, 5 | none | File-disjoint. Stamp shared via spec AC7 / Task 3 exact string; Task 5 substring `design gate bypassed` matches. Task 2 OKF not gated (W1r). |
| 3 | 4 | — | Depends on 3. OK |
| 4 | 6 | — | Depends on 2, 4, 5 (3 via 4). OK |
| 5 | 7 | — | Depends on 6. Pins `1.15.0` + `validate.py`. OK |

Hotspots stay serial: `dev/SKILL.md` wave 1; `build/SKILL.md`+`workflow.md` wave 2 Task 3; `ship/SKILL.md` wave 3.

## Over-build (Simplicity)

No extra runtime, agent, command, or dependency. Keyword helper still omitted. Task 6/7 split is the previous 13-file docs task, not new scope.

## Pre-mortem

If the build stalls: Task 2 writes `investigation.md` without OKF `type:` and stays green (W1r). Everything else now fails closed inside its own Verify (`validate.py` on Tasks 1, 3, 7; semantic/resume/announce/capture tests on Task 1; stamp+reopen on Task 3; version pin on Task 7).

## Info

- **I1.** pitfalls.md:43-45 still attributes the `1.15.0` bump to task 6; the bump lives in task 7. Prevention still holds.
- **I2.** Task 1 is 8 files (ceiling ~5-8), now including `feature-folder-cases.md` required by F2. Task 3 remains a 6-file phase overlay. Acceptable; do not split unless a runner fails to hold it.
- **I3.** `research/classification-seam.md` still recommends a tell-table helper and classify-after-scan. Task-runners follow ADR-0002 + tasks.md, not that note.
- **I4.** Learnings: none applicable.
