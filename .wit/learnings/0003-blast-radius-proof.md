---
type: Learning
title: Ship verification honesty (learnings)
description: A second Item/Plan/Result/Severity table before the bug-fix matrix steals bug_fix_matrix().
feature: 0003-blast-radius-proof
timestamp: 2026-08-27
tags: [checker, ship, tests]
---

# Ship verification honesty (learnings)

## What didn't work

- WHEN adding a second Item/Plan/Result/Severity table to `agents/wit-code-checker.md` → AVOID placing it before the bug-fix matrix → BECAUSE `bug_fix_matrix()` in `tests/test_bug_fix_checker.py` returns the first matching table (`len(rows) == 5`).

## Non-obvious decisions

- Honest `unproven` is INFO, not WARNING. WARNING implies a waiver pointer (hidden WAIVED).
- WHEN ship:2 runs before `PR.md` exists → DO still write the Safety fact row into `verification.md` → BECAUSE a missing heading is not a BLOCKER on the first pass.

## Gotchas / patterns to reuse

- WHEN Testing and Safety fact both need an `n/a` token → DO keep Testing as `n/a - not configured` and Safety fact Proof as `n/a` → BECAUSE one substring would collide.
- WHEN banning D3 verdict names in RPA text → AVOID `assertNotIn("PASS")` globally → BECAUSE the RPA gate already says `verdict is PASS`.
