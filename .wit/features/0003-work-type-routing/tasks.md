---
type: Task List
title: "Tasks: work-type routing for bug fixes and investigations"
description: TDD tasks for the routing foundation, route overlays, timing compatibility, checker evidence, and release docs.
feature: 0003-work-type-routing
timestamp: 2026-08-25
---

# Tasks: work-type routing for bug fixes and investigations

> Ordered. Each task writes its failing test first, confirms the expected failure, implements the
> smallest change, and ends green.

## Task 1: Add the work-type routing foundation  [infra]
- **Files:** `skills/dev/SKILL.md`, `skills/dev/references/work-types.md`,
  `references/skill-aliases/wit-dev/SKILL.md`,
  `references/feature-folder-cases.md`,
  `skills/research/references/wit-directory.md`,
  `skills/research/references/integrations.md`, `scripts/validate.py`,
  `tests/test_work_type_routing.py`
- **Do:** Add semantic `feature|bug-fix|investigation` deduction before write-capable dev setup;
  parse `--kind`, stop on invalid values, and default mixed/unclear intent to `feature`. Always print
  `Work type: <type> (<source>). Override: --kind feature|bug-fix|investigation`; never ask or route
  silently. Point only to `work-types.md` from the always-loaded body, preserve the existing folder
  classifier, stamp optional `Work type:`, and make missing stamps mean feature. On resume honor the
  stamp without re-deduction unless `--kind` is present; the override wins. Add `understand` and
  pre-fix debug integrations plus an explicit chat-only investigation exception to the normal
  capture-into-`.wit/` rule. Expand dev and alias descriptions with conservative fix/investigation
  intent while keeping "file a bug" on add-issues, and pass `--kind` beside `--auto`. Contract-test
  semantic deduction as an orchestrator judgment rather than a keyword-only runtime classifier,
  always-announced inferred/override/default cases, resume, hook order, progress template,
  independently loaded integrations, four-command surface, description cap, and feature behavior.
- **Verify:** `python -m unittest tests.test_work_type_routing && python scripts/validate.py`
- **Depends on:** -

## Task 2: Add the read-only investigation exit  [infra]
- **Files:** `skills/dev/references/investigation.md`,
  `tests/test_investigation_route.py`
- **Do:** Write the on-demand route that exits before scan/dossier writes, delegates to installed
  `how` and optional motivational `why`, otherwise uses a portable read-only fallback capped at two
  explorers, returns cited Explain/Decide output with `## Sources`, and forbids state, keep-alive,
  branch, commit, PR, and phase-agent writes. Test delegation/fallback markers, deny-list, explorer
  cap, citation contract, and hand-back to `--kind feature|bug-fix`.
- **Verify:** `python -m unittest tests.test_investigation_route && python scripts/validate.py`
- **Depends on:** 1

## Task 3: Overlay the reproduce-first bug-fix lifecycle  [infra]
- **Files:** `skills/dev/references/bug-fix.md`, `skills/brainstorm/SKILL.md`,
  `skills/research/SKILL.md`, `skills/build/SKILL.md`, `references/workflow.md`,
  `tests/test_bug_fix_route.py`
- **Do:** Add the repro-contract brainstorm specialization, pre-plan systematic-debugging delegation
  and root-cause evidence, mandatory plan/checker path, fail-closed narrow-fix predicate, structured
  Gate bypass block, and the exact `design gate bypassed (narrow-fix)` stamp after the normal
  `design gate opened` stamp. Set workflow's skip contract to never for feature and recorded
  narrow-fix only for bug-fix. Add the build precondition, same-surface before/after proof,
  regression-test-or-rationale rule, and missing-Work-type feature default. Keep `--auto` separate.
  If build discovers an architecture or public-contract change, revoke the bypass and reopen the
  existing design gate. Test every predicate conjunct, bypass refusal, stamp distinction, phase
  ordering, reopen path, and feature compatibility.
- **Verify:** `python -m unittest tests.test_bug_fix_route && python scripts/validate.py`
- **Depends on:** 1

## Task 4: Enforce bug-fix proof in checker and ship  [test]
- **Files:** `agents/wit-code-checker.md`, `skills/ship/SKILL.md`,
  `tests/test_bug_fix_checker.py`
- **Do:** Add only the bug-fix matrix rows for named repro surface, root cause, same-surface
  fail-then-pass, smallest fix, and regression coverage or impracticality rationale. Make omissions
  BLOCKERs in the appropriate checker pass and require PR evidence at ship. Add a conditional
  `## Rules inventory` section to the ship PR template for rule-text changes. Preserve the charter's
  tools, modes, caps, and `## CHECK PASSED` / `## ISSUES FOUND` markers. Contract-test all preserved
  markers, additive rules, and inventory heading.
- **Verify:** `python -m unittest tests.test_bug_fix_checker`
- **Depends on:** 3

## Task 5: Keep timing reports compatible with gate bypass  [test]
- **Files:** `skills/ship/scripts/_ledger.py`, `skills/ship/scripts/token_report.py`,
  `skills/ship/scripts/grok_token_report.py`, `tests/test_timing_report.py`
- **Do:** Add `design gate bypassed` to the build/ship span-start allow-list in all three parsers.
  Write the failing narrow-bypass fixture first, then prove approved, auto-approved, missing-boundary,
  and negative-span behavior remains unchanged.
- **Verify:** `python -m unittest tests.test_timing_report`
- **Depends on:** 1

## Task 6: Document work-type routing  [docs]
- **Files:** `README.md`, `AGENTS.md`, `docs/design-notes/dev.md`,
  `docs/design-notes/research.md`, `docs/design-notes/build.md`,
  `docs/design-notes/ship.md`, `docs/design-notes/wit-code-checker.md`,
  `tests/test_work_type_docs.py`
- **Do:** Document the three work types, `--kind`, read-only investigation exit, bug-fix evidence and
  narrow-bypass semantics, while keeping four advertised commands and five-host wording. Preserve
  frozen archives. Contract-test README/AGENTS descriptions and the design-note ownership split.
- **Verify:** `python -m unittest tests.test_work_type_docs`
- **Depends on:** 2, 4, 5

## Task 7: Update source memory and release 1.15.0  [docs]
- **Files:** `.wit/overview.md`, `.wit/architecture.md`, `.wit/repo-map.md`,
  `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`,
  `.codex-plugin/plugin.json`, `tests/test_work_type_release.py`
- **Do:** Update source-repo memory only where behavior changed. Bump all three manifests from
  `1.14.1` to exactly `1.15.0`. Add a release contract test that pins the version, manifest parity,
  three work types, four advertised commands, and source-memory routing entry. The ship phase will
  fill its new Rules inventory section from the final diff.
- **Verify:** `python -m unittest tests.test_work_type_release && python scripts/validate.py`
- **Depends on:** 6

## Waves  (derived from Depends on + Files: what build runs concurrently)
- Wave 1: task 1
- Wave 2: tasks 2, 3, 5
- Wave 3: task 4
- Wave 4: task 6
- Wave 5: task 7
