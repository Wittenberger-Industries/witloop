---
type: PR Description
title: Work-type routing for bug fixes and investigations
description: Route feature, bug-fix, and investigation
feature: 0003-work-type-routing
timestamp: 2026-08-25
---

## feat: Work-type routing for bug fixes and investigations

### Summary
`/wit:dev` now deduces work type (`feature`, `bug-fix`, or `investigation`) before any write-capable setup. `--kind` overrides. Investigations return a cited read-only answer and stop. Bug fixes reuse the existing phases with reproduce-first evidence and a fail-closed narrow-fix design-gate bypass. Feature behavior, four advertised commands, five-host adapters, and the single checker-agent contract stay. Plugin version **1.15.0**. ADR-0002.

### Acceptance criteria
- [x] Semantic deduce of `feature|bug-fix|investigation`; `--kind` wins; invalid stops; mixed/unclear is announced `feature` (`python -m unittest tests.test_work_type_routing`)
- [x] Work type resolves before scan/model/folder writes; investigation loads the read-only route and exits (`tests.test_work_type_routing`, `tests.test_investigation_route`)
- [x] Dossiers stamp `Work type:`; missing means `feature`; resume honors the stamp unless `--kind` (`tests.test_work_type_routing`)
- [x] Investigation creates no `.wit/` state, branch, commit, keep-alive, or PR; `how` / optional `why` / 2-explorer fallback; `## Sources` (`tests.test_investigation_route`)
- [x] Bug-fix brainstorm records a repro contract; research runs systematic-debugging or the inline fallback before planning (`tests.test_bug_fix_route`)
- [x] Plan and plan-mode checker always run; human design gate bypasses only when every narrow-fix conjunct is recorded (`tests.test_bug_fix_route`)
- [x] Distinct `design gate bypassed (narrow-fix)` stamp; `--auto` stays separate; feature never bypasses (`tests.test_bug_fix_route`, `tests.test_timing_report`)
- [x] Same-surface fail-then-pass; PR names root cause and smallest fix; regression test or impracticality rationale; result-mode BLOCKER if missing (`tests.test_bug_fix_route`, `tests.test_bug_fix_checker`)
- [x] All three timing parsers count the bypass as span2 start (`tests.test_timing_report`)
- [x] Four commands, five-host table, feature default, checker markers, seven-file dossier intact (`python scripts/validate.py`, full unittest)
- [x] Version `1.15.0` lockstep, user docs, source memory, rules inventory (`tests.test_work_type_docs`, `tests.test_work_type_release`)

### Changes
- Read-only prelude in `skills/dev/SKILL.md` plus `work-types.md`, `investigation.md`, and `bug-fix.md`
- `--kind` on the `wit-dev` alias; conservative fix/investigation tells in skill descriptions
- `understand` and pre-fix debug rows, plus a chat-only investigation exception, in `integrations.md`
- Additive bug-fix matrix rows on `wit-code-checker`; ship PR evidence and conditional Rules inventory
- Timing parsers accept `design gate bypassed` as the build/ship span start
- Manifests `1.14.1` → `1.15.0`

### Testing
- Format / lint / typecheck: `n/a - not configured`
- `python scripts/validate.py` → `[OK] all checks passed` (`.logs/gate-validate.txt`, EXIT 0)
- `python -m unittest discover -s tests` → 254 tests OK (`.logs/gate-tests.txt`, EXIT 0)
- New modules: `test_work_type_routing`, `test_investigation_route`, `test_bug_fix_route`, `test_bug_fix_checker`, `test_work_type_docs`, `test_work_type_release`; `test_timing_report` extended

### Verification
Result-mode `wit-code-checker` (feature-level + line-level, `requesting-code-review` template inline): **CHECK PASSED**. 11/11 ACs wired. ADR-0002 locked decisions wired. No BLOCKER, WARNING, or INFO findings. This dossier is Work type feature (missing stamp means feature); bug-fix matrix rows are product, not applied to this run.

### Risk & rollout
No feature flag. Install 1.15.0. Back out by reverting the routing references, thin pointers, progress extensions, parser allow-list, tests, docs, and manifest bump together. Existing dossiers stay readable: missing Work type means `feature`.

### Decisions
- [ADR-0002](../../adr/ADR-0002-route-work-by-intent.md): route dev work by intent with read-only and bug-fix overlays

## Rules inventory
| File | Before | After | Loaded-alone still decides? |
|---|---|---|---|
| `skills/dev/SKILL.md` | Every request is a feature; flags are `--auto` only | Read-only prelude deduces work type, announces it, loads investigation.md or continues; `--kind` parsed | Yes: prelude + numbered steps |
| `skills/dev/references/work-types.md` | (new) | Semantic judgment, precedence, announce, resume stamp | Yes |
| `skills/dev/references/investigation.md` | (new) | Read-only exit, how/why, deny-list, Sources | Yes |
| `skills/dev/references/bug-fix.md` | (new) | Repro contract, evidence, fail-closed bypass, same-surface proof | Yes |
| `references/skill-aliases/wit-dev/SKILL.md` | Forwards `--auto` | Forwards `--auto` and `--kind` | Yes |
| `references/feature-folder-cases.md` | Resume re-enters phase | Resume honors `Work type:` unless `--kind` | Yes |
| `skills/research/references/wit-directory.md` | No Work type field | Optional `Work type:`; missing means feature | Yes |
| `skills/research/references/integrations.md` | Capture every delegate into `.wit/` | `understand` row; investigation is chat-only; pre-fix debug row | Yes |
| `skills/brainstorm/SKILL.md` | Feature must-asks only | Bug-fix loads bug-fix.md repro contract | Yes |
| `skills/research/SKILL.md` | Gate is approve or `--auto` | Bug-fix evidence step; `design gate opened` then optional `design gate bypassed (narrow-fix)` | Yes |
| `skills/build/SKILL.md` | Gate passed = approved or `--auto` | Also accepts recorded narrow-fix bypass; reopen if the change stops being narrow | Yes |
| `references/workflow.md` | Design gate may skip: never | Never for feature; bug-fix only with recorded predicate and stamp | Yes |
| `agents/wit-code-checker.md` | Coverage matrix without bug-fix rows | Additive bug-fix BLOCKER rows when Work type is bug-fix; markers/tools unchanged | Yes |
| `skills/ship/SKILL.md` | PR template without inventory | Bug-fix PR evidence; conditional `## Rules inventory` | Yes |
| `scripts/validate.py` | Headless/self-answer anchors | Also pins the work-type announce string and `work-types.md` | Yes |
