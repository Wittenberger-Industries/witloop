---
type: Task List
title: "Tasks: Ship verification honesty"
description: Small ordered tasks (each with files + verify) and the build waves for this feature.
feature: 0003-blast-radius-proof
timestamp: 2026-08-27
---

# Tasks: Ship verification honesty

> Ordered. Each task is small enough for one focused sitting and ends green.
> plan via superpowers:writing-plans (captured in wit `tasks.md` format). Round 2 after plan-mode F1.

## Task 1: Checker result-mode rows   [backend]
- **Files:** `tests/test_ship_safety_fact.py`, `agents/wit-code-checker.md`,
  `docs/design-notes/wit-code-checker.md`
- **Do:** Create `tests/test_ship_safety_fact.py` with class `CheckerSafetyFactTests` only
  (copy `load` / `frontmatter` locally; no `import validate`; no Task). Write the failing
  assertions first, then the charter. Assert: always-on result-mode rows **after** the bug-fix
  table (not before, not merged); missing heading when `PR.md` exists, omitted matrix row, or
  writeup-only Proof is BLOCKER; honest `unproven` is INFO; valid docs-only `n/a` is INFO;
  `n/a` on a runtime-behavior diff is BLOCKER; plan-mode skip; glossary carve-out for Safety fact
  and Unproven; when `PR.md` is absent the checker still **writes this row** into
  `verification.md` (not a miss). Pin the locked docs-only runtime paths in the charter and
  tests: `skills/`, `agents/`, `scripts/`, `tests/`, `references/`, `.claude-plugin/`,
  `.codex-plugin/`, `AGENTS.md`. Do not change tools, last-line markers, or the 2-round loop.
  Sync the design-notes additive subsection. `assertNotIn` em dash on files this task edits.
- **Verify:** `python -m unittest tests.test_ship_safety_fact.CheckerSafetyFactTests tests.test_bug_fix_checker.CheckerBugFixMatrixTests tests.test_bug_fix_checker.CheckerPreservedContractTests`
- **Depends on:** -

## Task 2: Ship template, gate honesty, close-out box   [backend]
- **Files:** `tests/test_ship_safety_fact.py`, `skills/ship/SKILL.md`,
  `skills/ship/references/verification-gate.md`, `docs/design-notes/ship.md`
- **Do:** Append class `ShipSafetyFactTests` to the existing test module (failing asserts first).
  Then insert unconditional `### Safety fact` between Testing and Verification in the ship:5
  template (Claim, Proof as this-session command | `unproven` | `n/a`, optional Not-run).
  Ship:5 copies the checker matrix row into that heading. Ship:8 checkbox that `PR.md` contains
  the heading and a legal Proof. One ship:1 sentence pointing at the gate paragraph. Gate file:
  honesty paragraph; `unproven` does not skip configured repo-map commands; no sixth Run step;
  Testing `n/a - not configured` stays under Testing and must not be the Safety fact `n/a` token
  (tests assert both phrases). Keep bug-fix fail-then-pass strings inside `### Testing` so
  `ShipBugFixEvidenceTests` still matches. Sync design-notes for ship:5 / INFO / no second gate.
  `assertNotIn` em dash on files this task edits. This test file still must not import validate.
- **Verify:** `python -m unittest tests.test_ship_safety_fact.ShipSafetyFactTests tests.test_bug_fix_checker.ShipBugFixEvidenceTests tests.test_bug_fix_checker.ShipRulesInventoryTests tests.test_ship_safety_fact.CheckerSafetyFactTests`
- **Depends on:** 1

## Task 3: RPA gate pointer   [backend]
- **Files:** `tests/test_ship_safety_fact.py`, `skills/rpa/references/verification-gate.md`
- **Do:** Append class `RpaSafetyFactTests` (failing asserts first). Pointer paragraph in the
  checker result-mode section: same Safety fact rows as the charter; same `### Safety fact`
  heading via ship:5; Proof is a this-session command from this gate's list or `unproven` or
  `n/a`; `unproven` does not skip restore/validate/Analyzer/paradigm. Ban the D3 four-name
  cluster `PASS / CONCERNS / FAIL / WAIVED` as a severity list (do not `assertNotIn("PASS")`
  globally). Do not edit `skills/rpa/SKILL.md`. `assertNotIn` em dash on the RPA gate file.
- **Verify:** `python -m unittest tests.test_ship_safety_fact`
- **Depends on:** 2

## Task 4: Lockstep 1.16.1   [docs]
- **Files:** `tests/test_work_type_release.py`, `.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json` (wit plugin entry only), `.codex-plugin/plugin.json`,
  `.wit/overview.md`, `README.md`
- **Do:** Set `RELEASE = "1.16.1"` and the three plugin versions. Overview current version
  1.16.1; optional `assertNotIn("1.16.0")` on overview only. Do not change architecture's
  `(1.16.0)` PLUGIN_ROOT caption. README frontmatter and "Current release" to 1.16.1. Catalog
  metadata stays 0.2.0. Owner directed patch 1.16.1 (1.16.x) even though constitution prefers
  minor for behavior; do not retarget 1.17.0.
- **Verify:** `python -m unittest tests.test_work_type_release tests.test_work_type_docs`
- **Depends on:** -

## Task 5: Runner never yields   [backend]
- **Files:** `tests/test_task_runner_no_yield.py`, `agents/wit-task-runner.md`,
  `docs/design-notes/wit-task-runner.md`, `references/models.md`
- **Do:** Create `tests/test_task_runner_no_yield.py` (failing asserts first; no `import validate`).
  Charter: retire `STOP and ask`; architecture is `## TASK BLOCKED` with the question in Notes;
  never address the user; every generation ends on exactly one last-line marker; if Verify has not
  run this generation only BLOCKED or AUTH-GATE is legal; a failed Verify is not a user prompt;
  AUTH-GATE stays the only human pause. Do not change tools, ~15-line report, Self-Check, no-commit,
  no `progress.md` writes, 3-attempt cap, or git landmines. Sync design notes. models.md cites
  `## TASK BLOCKED`. `assertNotIn` em dash on files this task edits.
- **Verify:** `python -m unittest tests.test_task_runner_no_yield.RunnerPreservedContractTests tests.test_task_runner_no_yield.RunnerNoYieldTests tests.test_task_runner_no_yield.DesignNotesNoYieldTests`
- **Depends on:** -

## Task 6: Build continues the DAG same turn   [backend]
- **Files:** `tests/test_task_runner_no_yield.py`, `skills/build/SKILL.md`,
  `skills/build/references/worktrees-and-subagents.md`, `docs/design-notes/build.md`,
  `references/grok-tools.md`, `references/cursor-tools.md`
- **Do:** Append build/skeleton/host classes to the existing test module (failing asserts first).
  Build:2 no-yield: after a runner returns, this same turn tick + commit + dispatch the next ready
  set; no user-facing wrap-up; do not background a `wit-task-runner`; do not end the parent turn
  while `tasks.md` has unticked items except AUTH-GATE or a real design-gate AskQuestion; Host grok
  pulls `get_command_or_subagent_output` at the wave gate. Skeleton last-line markers. Grok: no
  `background: true` on a runner. Cursor: no `run_in_background` on a runner. Sync design notes.
  `assertNotIn` em dash on files this task edits.
- **Verify:** `python -m unittest tests.test_task_runner_no_yield`
- **Depends on:** 5

## Waves  (derived from Depends on + Files: what build runs concurrently)
- Wave 1: tasks 1, 4
- Wave 2: task 2
- Wave 3: task 3
- Wave 4: task 5
- Wave 5: task 6
