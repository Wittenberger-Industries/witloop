---
type: Plan
title: "#65 centralize MoA + tiered-routing mechanics; skills carry a trigger + pointer"
description: "Move the restated MoA proposer/aggregator/layers mechanics and the routing resolve-once/first-run mechanics out of the five always-loaded skill bodies into references/moa.md + references/models.md (loaded on demand), leaving each skill a trigger + pointer. No behavior change; a points:none run dispatches identically to before."
feature: 65-centralize-moa-routing
timestamp: 2026-07-12
tags: [plan, performance, context-budget, models]
---

# #65 centralize MoA + tiered-routing mechanics

## Problem (issue AC)

`references/moa.md` and `references/models.md` already hold the full MoA + tiered-routing contract, but
the always-loaded `SKILL.md` bodies restate the dispatch mechanics on top of pointing at them. That text
is paid for on every turn, and MoA is off by default (`points: none`), so for the common case it
describes a path that never fires. Reduce each skill to a trigger + pointer; the mechanics live only in
the on-demand references.

## Approach: move-then-compress (never delete without a home)

1. **Move the skill-only mechanics into the references first** (the ones that lived only in a skill body):
   - `moa.md` Research point: the proposer charter inputs, and that the synthesis's dissent feeds the
     ADR rejected-alternatives + the design-gate `Rejected:` line.
   - `moa.md` Review point: proposers get the IDENTICAL result-mode prompt (both passes + the line-review
     template); the aggregator dedupes / keeps MAX severity / verifies against the repo before dropping a
     false positive; a full MoA pass counts as one review round (cross-provider layer + max-2-rounds loop
     unchanged).
   - `models.md` First-run setup: the warn-once-on-tier-mismatch is now stated at the apply step so the
     dev/rpa pointer is self-complete.
2. **Compress each skill body to a trigger + pointer**, keeping only the condition that tells the
   orchestrator WHEN to load the reference, the pointer, and any genuinely skill-specific wiring:
   - `research/SKILL.md`: routing dispatch line + the MoA research-point block.
   - `ship/SKILL.md`: the MoA review-point block + a light trim of the cross-provider layer recipe.
   - `build/SKILL.md`: the task-runner resolve-once/unavailable-model restatement.
   - `dev/SKILL.md` + `rpa/SKILL.md`: the first-run-setup restatement.

## What stays (binding)

- Every trigger stays in the skill (the orchestrator must know when to reach for the reference).
- Contract log strings unchanged and still emittable: `approach via MoA (...)`, `review via MoA (...)`,
  `+ MoA (<N> proposers, <L> layers, aggregator <tier>)`, `cross-provider layer skipped (<reason>)`.
- No behavior change: a `points: none` run dispatches identically to origin/main.
- Charters untouched (the charter-edit exceptions are spent).

## Result

Always-loaded skill bodies: ~9,241 -> ~8,951 words (-290, paid every turn). On-demand `moa.md`:
+114 words (loaded only when a run resolves routing or dispatches MoA; MoA off by default, so most runs
never load it). `models.md`: +one clause.

## Verification

- `python scripts/validate.py` + `pytest tests/` green.
- Independent adversarial removed-behavior audit: **SAFE** - every removed clause maps to a reference
  line, all triggers + contract strings intact, `points: none` identical to origin/main.
- Grep-confirmed: each evicted mechanic present in a reference and absent from the skill bodies.
