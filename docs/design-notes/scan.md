---
type: Design Notes
title: "scan: design rationale (maintainer notes)"
description: The "why" behind scan/SKILL.md's rules, relocated out of the loaded skill by #41 (v1.9.1); the runtime never reads this file; each entry is anchored to the section it explains.
timestamp: 2026-08-27
tags: [scan, design-notes, context-budget]
---

# scan: design rationale (maintainer notes)

`skills/scan/SKILL.md` is loaded wholesale at scan time, and two of the files it may touch
(`constitution.md`, `repo-map.md`) then sit in the orchestrator's context for entire later runs, so
the skill carries rules only. The rationale lives here, anchored by section. When editing the skill,
keep this file in sync: a rule whose "why" is deleted instead of relocated loses its guard against
future "simplification". First-run write of those files is setup (`docs/design-notes/setup.md`).

## Intro

- **Mission.** scan is the cheap drift-check: re-verify `.wit/` facts so later phases still trust
  them. It does not create a `.wit/` from scratch. Setup owns that one-time groundwork.
- **Why bare invoke is silent `--refresh`:** after the split, scan has one job. A mandatory flag for
  the only remaining job is ceremony. `--refresh` stays as a synonym so `dev`'s auto-stale caller
  does not change.
- **Why missing `repo-map.md` → run setup and then stop:** scan must not keep a first-document body.
  Telling the user to type setup is a dead end. Chaining refresh after setup just wrote the map is a
  second empty commit. `.wi/` with no `.wit/` is the same tell; the rename lives in setup.
- **Why `--refresh` re-verifies instead of re-documenting:** repos move on without wit (humans commit,
  dependencies change, modules appear), and `dev` auto-invokes the refresh at feature start, so it must
  stay cheap; re-documenting is the expensive path and mostly churns prose.

## `--refresh` A (drift check)

- **Why facts, not prose:** the refresh verifies exactly what a later phase would trust (commands,
  stack, structure) and touches only what drifted; anything more re-opens the full documentation pass
  that `--refresh` exists to avoid.
- **Why unchanged config means commands stand:** re-running the suite "to check" costs minutes and
  proves nothing a config diff didn't already; the `--version`/`--help` probe is the fallback only when
  reading the config is inconclusive.
- **Why diagram updates are structural-only:** the mermaid is a module/dependency map, not a change log;
  churn inside existing nodes doesn't change the picture.
- **Why mermaid traps live in A.3:** refresh still edits `architecture.md`. The two parser traps plus
  reserved-word IDs used to sit under the first-write templates; those templates moved to setup, so
  "rules above" would dangle. A.3 carries the list so refresh never loads setup to draw a diagram.
- **Why the config/lock enumeration was trimmed from the skill:** the stack-detection cookbook is the
  canonical list (pyproject, package.json, lockfiles, CI workflows, tool configs); repeating it in the
  skill invited drift between the two lists.
- **What `check_mermaid.py` catches (relocated catch-list):** reserved-word node IDs, unquoted
  special-char labels, unbalanced `subgraph`/`end`, unclosed fence; when `mmdc` (mermaid-cli) is
  installed it also does a true render. The skill mandates only "fix every error; never save a diagram
  that doesn't pass".

## `--refresh` B (memory hygiene)

- **Why the index target (roughly 30 lines):** learnings recall is via the index (wit-directory.md);
  every phase reads it per feature, so the compounding memory only stays useful if it stays lean.
- **Why promote-then-tombstone:** a standing rule belongs in its source of truth, where every phase
  already looks; the tombstone keeps the index honest about where the learning went, and deleting the
  detail file keeps the knowledge in exactly one place.
- **Why ADRs are never pruned:** they are the project's decision history; superseding with a new ADR
  preserves the trail a future maintainer follows.
- **Timing note (lag, not drift):** ship commits a feature's learnings on the feature branch, so main's
  `learnings.md` lacks in-flight features' lines until their PRs merge; wit-directory.md tells
  `scan --refresh` to read that as normal lag, not drift.

## `--refresh` C (report; the lean-file warning)

- **Why the ~150-line ceiling is worth a warning line:** `constitution.md` and `repo-map.md` are held in
  the orchestrator's context for entire runs (workflow.md's context budget), so overweight there is paid
  on every turn. The ceiling itself is wit-directory.md's lean-file rule; scan only surfaces breaches.
  Setup warns at first write; refresh warns again if the files grew.
