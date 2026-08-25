---
type: Verification
title: Verification - Work-type routing for bug fixes and investigations (plan mode)
description: Plan underspecifies resume, always-announce, and the investigation capture exception; remaining gaps are wave-safety and verify pins.
feature: 0003-work-type-routing
status: issues-found
timestamp: 2026-08-25
---

# Verification: 0003-work-type-routing (plan mode)

**Question:** will this plan, built exactly as written, deliver the feature?
**Verdict:** no. Three locked decisions have no covering Do/Files evidence in Task 1. Several wave-safety and verification pins are incomplete.

Applicable learnings: none (progress.md `applicable learnings: none`).

## Coverage matrix

| Item | Source | Covering task | Evidence | Status |
|------|--------|---------------|----------|--------|
| AC1 semantic deduce `feature\|bug-fix\|investigation`; `--kind` wins; invalid stops; mixed → announced `feature` | spec.md:39-41 | Task 1 | Do names semantic deduction, `--kind`, invalid stop, mixed/unclear → announced `feature`; Verify `tests.test_work_type_routing` | PARTIAL — see F1 (always-announce) |
| AC2 resolve before scan/model/folder writes; investigation exits; feature/bug-fix continue folder classifier | spec.md:42-44 | Tasks 1, 2 | Task 1 Do "before write-capable dev setup" + hook-order tests; Task 2 deny-list + early exit | COVERED |
| AC3 stamp `Work type:`; missing = `feature`; resume does not re-deduce unless `--kind` | spec.md:45-47 | Task 1 | Do stamps optional `Work type:` and missing=`feature`. Resume/no-re-deduce is not in any Do; `feature-folder-cases.md` not in Files | **GAP** F2 |
| AC4 investigation: no `.wit/` state/branch/commit/keep-alive/PR; `how`/`why` optional; 2-explorer fallback; citations + `## Sources` | spec.md:48-52 | Task 2 (+ Task 1 integrations) | Task 2 Do names exit, delegation, cap, citations, deny-list. Standing `integrations.md` capture-into-`.wit/` rule is not excepted | **GAP** F3 |
| AC5 bug-fix brainstorm repro contract; research systematic-debugging or fallback; root cause recorded | spec.md:53-56 | Task 3 | Do: repro-contract brainstorm, pre-plan systematic-debugging, root-cause evidence; Files include brainstorm + research SKILL.md | COVERED |
| AC6 plan + plan-mode checker always; narrow-fix bypass only when every conjunct is recorded | spec.md:57-61 | Task 3 | Do: mandatory plan/checker path, fail-closed predicate, "test every predicate conjunct", bypass refusal | COVERED |
| AC7 distinct `design gate bypassed (narrow-fix)` stamp + audit block; fail closed; `--auto` separate; feature never bypasses | spec.md:62-64 | Tasks 3, 5 | Task 3: structured Gate bypass block, stamp distinction, `--auto`/feature unchanged. Full stamp string lives in spec, not Task 3 Do | COVERED (see W2) |
| AC8 same-surface fail-then-pass; PR names root cause + smallest fix; regression or impracticality; result-mode omission = BLOCKER | spec.md:65-68 | Tasks 3, 4 | Task 3 same-surface + regression-or-rationale; Task 4 additive checker rows + ship PR evidence + charter markers preserved | COVERED |
| AC9 all three timing parsers count bypass as build/ship span start; approved/auto-approved unchanged | spec.md:69-71 | Task 5 | Do: allow-list in `_ledger.py`, `token_report.py`, `grok_token_report.py`; failing bypass fixture first; existing spans unchanged | COVERED (see W2) |
| AC10 four commands; five-host table; feature default; agent markers; seven-file dossier | spec.md:72-74 | Tasks 1, 4, 6 | Task 1 four-command + feature behavior; Task 4 marker/tool/caps pin; Task 6 four-command/five-host wording. No task Verify runs `unittest discover` | COVERED (see I2) |
| AC11 version `1.15.0` lockstep; user docs; source memory; rules inventory in `PR.md` | spec.md:75-77 | Task 6 | Do: bump 1.14.1→1.15.0, docs, inventory "prepare". Verify is only `validate.py` (parity, not the number or inventory) | PARTIAL — see W4 |
| Brief: always announce selected work type + `--kind` override; never ask; never route silently | brief.md:17-18 | Task 1 | Do announces only the ambiguous-`feature` default | **GAP** F1 |
| Brief: `--kind feature\|bug-fix\|investigation` wins | brief.md:14-15 | Task 1 | Do parse `--kind` | COVERED |
| Brief: investigation read-only, no dossier/gate/build/PR | brief.md:20-21 | Task 2 | Do + deny-list | COVERED (F3 for integrations capture) |
| Brief: bug-fix names root cause + smallest fix; same-surface fail then pass; regression when practical | brief.md:35-37 | Tasks 3, 4 | Do + checker/ship | COVERED |
| Brief: existing feature brainstorm/design/build/ship preserved | brief.md:38 | Tasks 1, 3 | missing-Work-type=`feature`; unchanged-feature tests | COVERED |
| Brief: no fifth command, no new review agent, no required MCP, no RPA/add-issues change | brief.md:44-46 | Tasks 1, 2, 4, 6 | four-command tests; checker additive-only; no rpa/add-issues Files | COVERED |
| Brief: five-host via capability table/adapters | brief.md:50 | Tasks 1, 6 | alias `--kind` pass-through; five-host wording. NL description tells not tasked | COVERED (see W3) |
| ADR-0002.1 semantic deduce before write-capable setup; `--kind`; invalid stop; mixed → announced feature | ADR-0002:32-34 | Task 1 | Do matches, minus always-announce | PARTIAL F1 |
| ADR-0002.2 investigation on-demand; installed `how` else portable fallback; chat-only; no scan write/dossier/gate/keep-alive/PR | ADR-0002:35-37 | Tasks 1, 2 | Task 1 hook before writes; Task 2 route | PARTIAL F3 |
| ADR-0002.3 stamp `Work type:`; missing=`feature`; procedure on-demand not in always-loaded body | ADR-0002:38-40 | Task 1 | work-types.md + thin SKILL prelude | COVERED (resume still F2) |
| ADR-0002.4 overlay existing phases; reproduce + isolate root cause before plan; same surface fail then pass | ADR-0002:41-43 | Task 3 | overlay Do; Files brainstorm/research/build/workflow | COVERED |
| ADR-0002.5 distinct bypass stamp; fail-closed; not `--auto` | ADR-0002:44-47 | Tasks 3, 5 | predicate + distinct stamp + parser allow-list | COVERED |
| ADR-0002.6 single `wit-code-checker`; additive rows only; preserve markers/caps/modes/tools | ADR-0002:48-49 | Task 4 | Do additive-only + contract-test preserved markers | COVERED |
| ADR rejected: keyword-only classifier helper | ADR-0002:64 | Task 1 (honor) | Plan does **not** add `classify_work_type.py`. Do says semantic. Tests name "examples", not an anti-keyword pin | honored (see I1) |
| Glossary **Work type** (not task type / route kind) | glossary.md:22-23 | Task 1 | stamp `Work type:`; flag remains `--kind` | COVERED |
| Constitution: TDD, tests in `tests/test_*.py` | constitution.md:32-35 | all tasks | header + per-task Verify | COVERED |
| Constitution: no new dep unless ladder + spec | constitution.md:25-28, 37-39 | spec.md:105 | Dependencies none; no new helper script in tasks | COVERED |
| Constitution: agent charters additive only | constitution.md:41 | Task 4 | explicit preserve tools/modes/caps/markers | COVERED |
| Constitution: hotspots serial | constitution.md:42 | waves | Task 1 `dev/SKILL.md`; Task 3 `build/SKILL.md`+`workflow.md`; Task 4 `ship/SKILL.md`; not parallel | COVERED |
| Constitution: behavior change = minor lockstep | constitution.md:48 | Task 6 | 1.14.1→1.15.0 three manifests | COVERED (W4 pin) |
| Constitution: rule-text PR inventory | constitution.md:51 | Task 6 | "Prepare … for ship's `PR.md`"; ship:5 template has no inventory section | PARTIAL W4 |
| Simplicity (prohibitive): no extra abstraction/dep | constitution.md:24-30 | (4) over-build | Three on-demand refs match spec Design. No keyword helper, no `check_narrow_fix.py`. Task 6 file count is the AC11 doc surface | PASS |
| Pitfall: classified after a write | pitfalls.md:11-13 | Tasks 1, 2 | hook-order + deny-list | COVERED |
| Pitfall: mixed intent exits read-only | pitfalls.md:14-16 | Task 1 | mixed → announced `feature` | COVERED |
| Pitfall: "file a bug" stolen by bug-fix | pitfalls.md:17-19 | Task 1 | trigger examples + four-command tests | COVERED |
| Pitfall: feature path regresses | pitfalls.md:19-21 | Tasks 1, 3 | missing-Work-type + unchanged-feature tests | COVERED |
| Pitfall: optional skill required | pitfalls.md:22-24 | Task 2 | fallback + no-install; `plugin-bootstrap.md` not in Files (omission preserves current set) | COVERED |
| Pitfall: read-only depends on host flag | pitfalls.md:25-27 | Task 2 | portable deny-list + exit-state check | COVERED |
| Pitfall: false narrow-fix bypass | pitfalls.md:28-30 | Task 3 | conjunctive record + BLOCKER veto. **Mid-build reopen not in Task 3 Do** | PARTIAL W2 |
| Pitfall: `--auto` confused with bypass | pitfalls.md:31-33 | Tasks 3, 5 | distinct-stamp tests | COVERED |
| Pitfall: timing parser drift | pitfalls.md:34-36 | Task 5 | three implementations + shared fixture intent | COVERED |
| Pitfall: raw repro pruned | pitfalls.md:37-39 | Tasks 3, 4 | durable stamps, spec, checker, PR | COVERED |
| Pitfall: checker charter damaged | pitfalls.md:40-42 | Task 4 | additive-only marker tests | COVERED |
| Pitfall: manifest/docs mismatch | pitfalls.md:43-45 | Tasks 1, 6 | alias tests + 1.15.0 bump | COVERED (W4) |
| Learning: none applicable | progress.md:45 | — | no hook to honor | n/a |

## Findings

### F1 — BLOCKER — Always-announce is not in any task Do

**Mode:** plan
**Evidence:** brief.md:17-18 (announce selected work type + override; never ask; never route silently); spec.md:82-83 (prelude "deduces and announces"); tasks.md:20-25 (Task 1 Do announces only mixed/unclear → `feature`).

Built exactly as written, inferred `bug-fix` / `investigation` / plain `feature` may route with no one-line announcement. That is silent routing, which the brief forbids.

**Plan edit (Task 1 Do):** after resolve, always print `Work type: <type> (<source>). Override: --kind feature|bug-fix|investigation`. Never ask which type. Never continue without that line. Contract-test inferred, `--kind`, and ambiguous-default cases.

### F2 — BLOCKER — AC3 resume does not re-deduce unless `--kind`

**Mode:** plan
**Evidence:** spec.md:45-47; ADR-0002:38-39; classification-seam resume rule (load-bearing); tasks.md:20-25 (stamp + missing=`feature` only); `references/feature-folder-cases.md` resume (lines 19-27) is not in any Files list.

Today resume re-enters from `progress.md` with no Work type field (`feature-folder-cases.md:23-27`). Task 1 never says: detect in-flight match, honor stamped `Work type:`, skip deduction unless this invocation has `--kind`. A task-runner can re-classify every entry. An in-flight bug-fix can become `feature` or `investigation` on resume.

**Plan edit (Task 1 Do + Files):** add stamp and resume rules to `skills/dev/references/work-types.md`. On in-flight match, do not re-deduce unless `--kind` is present; `--kind` wins over the stamp. If that detection stays in `references/feature-folder-cases.md`, add that file to Task 1 Files and a one-line "do not re-deduce Work type" rule. Contract-test: stamped `bug-fix` resume without `--kind` stays `bug-fix`; `--kind feature` on resume wins; missing stamp stays `feature`.

### F3 — BLOCKER — Investigation capture-into-`.wit/` exception is not tasked

**Mode:** plan
**Evidence:** spec.md:48-50 (no `.wit/` state); ADR-0002:35-37; `skills/research/references/integrations.md:62-66` (standing rule: capture every delegate result into `.wit/`); Task 1 Do "Add shared integrations rows" (tasks.md:22) does not name the exception; Task 2 Files are only `investigation.md` + `tests/test_investigation_route.py` (tasks.md:30-31).

Independently loaded integrations.md will still order a dossier write after `how`/`why`. Task 2's deny-list cannot amend a file it does not own. That breaks AC4 even if investigation.md is perfect.

**Plan edit (Task 1 Do, same Files):** add an `understand` capability row (`how` required when installed; `why` optional for motivational questions; artifact = chat reply) **and** an explicit investigation exception to capture-into-`.wit/`. Contract-test that integrations.md loaded alone does not order `.wit/` writes for this route. Do not give Task 2 `integrations.md` (wave-1 ownership already).

## Wave safety

| Wave | Tasks | Shared Files | Intermediate green? |
|------|-------|----------------|---------------------|
| 1 | 1 | — | At risk: see W1 |
| 2 | 2, 3, 5 | none | File-disjoint. Stamp string is shared via spec AC7 (`design gate bypassed (narrow-fix)`); Task 5 allow-list substring `design gate bypassed` matches. |
| 3 | 4 | — | Depends on 3. OK |
| 4 | 6 | — | Depends on 2, 4, 5 (3 transitive via 4). OK |

Hotspot serial rule holds: `dev/SKILL.md` (wave 1), `build/SKILL.md`+`workflow.md` (wave 2 Task 3), `ship/SKILL.md` (wave 3).

### W1 — WARNING — Wave 1 can fail `validate.py`; dangling route pointers

**Mode:** plan
**Evidence:** spec.md:81-88 (prelude points at `investigation.md` and `bug-fix.md`); Task 1 Do "point to route references" (tasks.md:21); those files are created in Tasks 2 and 3; `scripts/validate.py:140-150` requires every `${CLAUDE_PLUGIN_ROOT}/…` path to exist; Task 1 also rewrites `skills/dev/SKILL.md`, whose load-bearing strings `self-answered (headless)` and `fails this check` are gated at `scripts/validate.py:185-187`; Task 1 Verify is only `tests.test_work_type_routing` (tasks.md:26); `scripts/validate.py` is in Task 1 Files with no Do item.

**Plan edit:** Task 1 points only at `work-types.md` (created in-task). Tasks 2 and 3 add the `${CLAUDE_PLUGIN_ROOT}` pointers when those files exist. Name the `validate.py` anchors in Task 1 Do or drop it from Files. Add `python scripts/validate.py` to Task 1 and Task 3 Verify (Task 3 edits `skills/brainstorm/SKILL.md`, same headless-only anchors at validate.py:182-184).

### W2 — WARNING — Narrow-fix overlay omits three fail-closed details

**Mode:** plan
**Evidence:**
- pitfalls.md:28-30 claims "mid-build gate reopen"; Task 3 Do (tasks.md:45-49) does not mention revoke-and-reopen.
- `references/workflow.md:49` `May skip when` is `never`; Task 3 Do "Keep `--auto` and normal feature gates unchanged" can be read as leaving that cell untouched, so independently loaded workflow.md still forbids bypass.
- bug-fix research: still emit `design gate opened` so span1 closes; Task 3 does not require it; Task 5 then treats missing `opened` as existing None (test_timing_report.py:61-65). Narrow-fix research+plan wall-clock becomes `unavailable`.

**Plan edit (Task 3 Do):** (1) quote the stamp `design gate bypassed (narrow-fix)` and still emit `design gate opened` first; (2) set workflow.md design-gate `May skip when` to never for feature, recorded narrow-fix only for bug-fix; (3) if build finds architecture/public-contract change, revoke bypass and re-open the gate (existing mid-run amend).

### W3 — WARNING — Cross-host auto-trigger phrases are not tasked

**Mode:** plan
**Evidence:** `skills/dev/SKILL.md:4-8` description is feature-shaped only; `references/skill-aliases/wit-dev/SKILL.md:4-7,19-20` forwards `--auto` only; Task 1 tests "description cap" and "alias pass-through" but does not require adding bug-fix/investigation NL tells. Cursor loads from `description`; Copilot/Grok/Codex from the alias.

`--kind` pass-through is implied by "alias pass-through" and should be spelled as `--auto` and `--kind`. Without description tells, "fix this crash" / "how does X work" may never load `/wit:dev` on description-driven hosts (add-issues or pstack `how` win).

**Plan edit (Task 1 Do):** expand `dev` + `wit-dev` descriptions with conservative bug-fix and investigation tells under the 1024-char cap; alias sentence passes `--kind` next to `--auto`; keep "file a bug" on add-issues.

### W4 — WARNING — AC11 inventory and `1.15.0` are not runnable Verify

**Mode:** plan
**Evidence:** spec.md:75-77; Task 6 Verify `python scripts/validate.py` (tasks.md:84) checks three-way parity, not the number `1.15.0`; ship:5 template (`skills/ship/SKILL.md:210-245`) has no rules-inventory section; Task 6 Do "Prepare" does not name an in-repo artifact; Task 4 owns `skills/ship/SKILL.md` and does not mention inventory.

**Plan edit:** Task 6 Verify asserts all three manifests equal `1.15.0` and that README/AGENTS mention `--kind` and the investigation exit. Either Task 4 extends the ship:5 template with a rules-inventory heading for rule-text PRs, or Task 6 Verify asserts a committed inventory draft the ship phase will paste.

### W5 — WARNING — Task-unit ceilings

**Mode:** plan
**Evidence:** Task 1 = 7 files (routing + alias + template + integrations + validate.py + tests) — at the 5-8 ceiling, multi-concern. Task 3 = 6 files across brainstorm, research, build, and workflow — sprawling multi-phase overlay. Task 6 = 13 files (tasks.md:74-79).

**Plan edit:** split Task 6 into docs/source-memory vs manifest bump+inventory pin. Consider splitting Task 3's workflow/build precondition from the brainstorm/research overlay if a runner cannot hold both.

### W6 — WARNING — Semantic deduction tests may accept a keyword table

**Mode:** plan
**Evidence:** ADR-0002:64 rejects a keyword-only helper; spec.md:34 non-goal; Task 1 Do says "semantic" (tasks.md:20) but Verify list is "precedence, examples, hook order…" (tasks.md:23-24). Protocol tests of example mappings can go green on an exclusive-tell table, which is the rejected helper in markdown form.

**Plan edit (Task 1 Verify):** assert independently loaded `work-types.md` + the prelude instruct semantic intent deduction, name all three classes, and do not present a keyword-only runtime classifier. Keep conservative examples as illustrations, not as the classifier.

## Over-build (Simplicity)

No extra runtime, agent, command, or dependency. The omitted `classify_work_type.py` / `check_narrow_fix.py` helpers match ADR + spec. No finding.

## Pre-mortem

If the build stalls: Task 1 rewrites `dev:1-2`, drops validate.py headless-only strings, and stays green because Verify never runs `validate.py` (W1). Task 3 ships bypass in `bug-fix.md` while workflow.md still says design-gate may skip `never` (W2). Resume re-deduces and an in-flight bug-fix exits investigation (F2). Investigation delegates to `how` and integrations.md captures into `.wit/` (F3).

## Info

- **I1.** `research/classification-seam.md` still recommends a stdlib tell-table helper and classify at the start of current `dev:2` (after scan). ADR-0002, chosen-approach.md, spec.md, and Task 1 Do supersede that. Task-runners must not rebuild from that note.
- **I2.** spec AC8 `verified by` names `tests.test_bug_fix_route`; Task 4 adds `tests.test_bug_fix_checker.py`. Point AC8 at both modules.
- **I3.** Learnings: none applicable; no honor/ignore finding.
