---
type: Pitfalls
title: "Pitfalls: work-type routing for bug fixes and investigations"
description: Failure modes for intent routing, read-only exit, gate bypass, evidence, and backwards compatibility.
feature: 0003-work-type-routing
timestamp: 2026-08-25
---

# Pitfalls: work-type routing for bug fixes and investigations

- **Investigation classified after a write:** scan, model setup, or feature-folder creation would break
  the read-only contract before the route exits. Prevented by: task 1 hook-order tests and task 2
  deny-list tests.
- **Mixed intent exits read-only:** "explain this, then change it" could lose requested work if
  investigation wins. Prevented by: task 1's conservative mixed/unclear default to announced `feature`
  plus `--kind` override.
- **Issue filing stolen by bug-fix triggers:** "file a bug" belongs to add-issues, while "fix this bug"
  belongs to dev. Prevented by: task 1 trigger examples and four-command contract tests.
- **Feature path changes accidentally:** moving setup or gate rules for every request could regress the
  existing product. Prevented by: tasks 1 and 3 missing-Work-type=`feature` and unchanged-feature tests.
- **Optional skill treated as required:** investigation could fail when pstack, `how`, `why`, or MCPs
  are absent. Prevented by: task 2 full-union detection, mandatory fallback, and no-install tests.
- **Read-only promise depends on a host flag:** not every host exposes `readonly: true`. Prevented by:
  task 2's portable deny-list and exit-state check; host flags are only extra defense.
- **False narrow-fix bypass:** an architectural or public-contract change could skip human review.
  Prevented by: task 3's conjunctive fail-closed record, checker BLOCKER veto, and mid-build gate reopen.
- **`--auto` confused with evidence-based bypass:** reusing the auto-approved stamp would erase why the
  gate was skipped. Prevented by: tasks 3 and 5 distinct-stamp tests.
- **Timing parser drift:** adding bypass to only one parser makes host reports disagree. Prevented by:
  task 5's shared fixture against all three implementations.
- **Raw repro evidence pruned:** `.logs/` and research notes disappear at ship, losing trust in the
  result. Prevented by: tasks 3 and 4 durable progress stamps, spec criteria, checker verdict, and PR
  excerpts.
- **Checker charter contract damaged:** edits could alter markers, caps, or tools while adding bug-fix
  rows. Prevented by: task 4 additive-only tests for all sensitive charter markers.
- **Manifest or docs mismatch:** behavior may ship under `1.14.1` or one host alias may omit `--kind`.
  Prevented by: tasks 1 and 7 alias tests, parity validation, and the `1.15.0` lockstep bump.
