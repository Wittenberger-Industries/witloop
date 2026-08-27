---
type: Pitfalls
title: "Pitfalls: Ship verification honesty"
description: Failure modes that apply to this change, each with a preventing task.
feature: 0003-blast-radius-proof
timestamp: 2026-08-27
---

# Pitfalls: Ship verification honesty

- **First-pass absent PR.md:** If the charter treats missing `### Safety fact` as BLOCKER when
  `PR.md` does not exist yet, every ship:2 fails. Prevented by: Task 1 (absent-file fallback;
  checker still writes the row into `verification.md`).
- **bug_fix_matrix theft:** A new table with Item / Plan / Result / Severity **before** the bug-fix
  table makes `test_bug_fix_checker.py` parse the wrong rows. Prevented by: Task 1 (new table after
  the bug-fix table).
- **Testing slice breakage:** `test_bug_fix_checker.py` slices `### Testing` to `### Verification`.
  Inserting `### Safety fact` between them enlarges that slice; fail-then-pass strings must still
  live in it. Prevented by: Task 2 (keep those strings in the Testing section; new tests slice
  Testing→Safety fact).
- **Unproven skips the suite:** An agent could mark pytest `unproven` instead of running it.
  Prevented by: Tasks 2 and 3 (iron-law / RPA "unproven does not skip" sentences) plus Task 1
  runtime-path pins.
- **Token collision:** Safety fact `n/a` vs Testing `n/a - not configured`. Prevented by: Task 2
  (distinct phrases; tests assert both).
- **WARNING as hidden WAIVED:** Mapping unproven to WARNING requires a waiver pointer.
  Prevented by: Task 1 (INFO for honest unproven).
- **INFO-only ISSUES FOUND:** Honest unproven still prints `## ISSUES FOUND`. Do not change markers.
  Prevented by: Task 1 (leave PASSED/ISSUES markers; pitfalls note only).
- **assertNotIn PASS:** Would fail RPA "verdict is PASS". Prevented by: Task 3 (ban the four-name
  D3 cluster, not the word PASS).
- **Architecture 1.16.0:** Overview may drop current 1.16.0; architecture PLUGIN_ROOT caption must
  keep 1.16.0. Prevented by: Task 4.
- **New PLUGIN_ROOT file:** A new always-loaded reference needs a serial wiring task.
  Prevented by: no new always-loaded file (learnings applied).
- **Shared test module serializes 1→2→3:** `tests/test_ship_safety_fact.py` is appended per task so
  red+green stay in one sitting. Prevented by: Depends on edges (not a parallel wave).
