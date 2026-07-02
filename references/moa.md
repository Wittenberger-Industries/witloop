---
type: Reference
title: "MoA — tiered model assignments for wi's dispatched agents"
description: "Configurable Mixture-of-Agents: orchestrator on the best model, wi sub-agents on cheaper tiers, an independent cross-provider reviewer at checkpoints. Config in .wi/moa.md, set up on first run."
timestamp: 2026-07-02
tags: [moa, models, reference]
---

# MoA — tiered model assignments for wi's dispatched agents

Orchestration (planning, routing, synthesis) wants the best model; delegated execution is usually
simpler and runs fine on cheaper tiers. wi's MoA support splits the two, plus an optional **independent
reviewer** — ideally a *different provider/architecture* (different training, different blind spots) —
that code-reviews the finished work. Scope: **wi-dispatched agents only** (researcher, task-runner,
checker, RPA build delegations); wi never re-models other plugins' or the user's own agents.

**The orchestrator model is informational.** A plugin cannot set the session model — the user picks it
with `/model`. wi records the intended tier and, at run start, **warns once** if the session model is
below it (e.g. config says `fable`, session runs `haiku`); it never blocks.

## The config file — `.wi/moa.md`

Project-level, persisted, read at every dispatch point. Template (fill from a preset, then let the user
override any cell):

```markdown
---
type: MoA Config
title: MoA model assignments — <project>
description: Per-role model assignments for wi-dispatched agents (preset: smart | simple | custom).
preset: <smart | simple | custom>
timestamp: <YYYY-MM-DD>
---

# MoA model assignments

## Roles
| Role | Model | Notes |
|------|-------|-------|
| orchestrator | <fable\|opus\|sonnet\|haiku> | informational — session model, set via /model; wi warns on mismatch |
| execution | <opus\|sonnet\|haiku\|inherit> | default for every wi-dispatched sub-agent |
| checker | <tier\|inherit> | the goal-level checker agent (plan/result mode) |
| reviewer | <provider model id \| none> | independent MoA code review; provider below. `none` disables it |

## Reviewer provider
| Key | Value |
|-----|-------|
| provider | <openai \| anthropic> |
| base_url | <https://api.openai.com/v1> |
| model | <gpt-5> |
| api_key_env | <OPENAI_API_KEY> |
| review_points | <at-finish \| per-wave> |

## Per-agent overrides
| Agent | Model |
|-------|-------|
| <researcher \| task-runner \| checker \| rpa-build> | <tier> |
```

Claude tiers are the Agent-dispatch tokens `fable | opus | sonnet | haiku`, plus `inherit` (= the session
model). The reviewer model is the *provider's* model id.

## Presets

| Role | **smart** | **simple** |
|------|-----------|------------|
| orchestrator | fable | opus |
| execution | opus | sonnet |
| checker | inherit | inherit |
| reviewer | gpt-5 (openai) | none |

**smart** = top-tier orchestration, strong execution, cross-architecture review. **simple** = lean
pass-through, no reviewer. Presets only *pre-fill* the table — every cell stays individually overridable.

## First-run setup (dev / rpa entry points)

When `.wi/moa.md` is **absent** at a wi entry skill (dev step 2, rpa step 2): **interactive** → ask once
— *"MoA models: smart, simple, or custom?"* — pre-fill from the chosen preset, confirm the per-role rows
(and any per-agent override), write the file. **`--auto`** → write the **simple** preset and log it as an
assumption. Either way the file persists and is **never re-asked** (edit `.wi/moa.md` to change it). When
the file exists, skip setup entirely — just apply it.

## Dispatch rule (build, research, ship, rpa)

At every wi Agent dispatch, resolve the model as **per-agent override → role → `inherit`** (the
`checker` agent reads the `checker` role; everything else reads `execution`) and pass it as the
dispatch's model parameter. No `.wi/moa.md` → everything inherits, exactly wi's pre-MoA behavior.
**Fallback:** a configured model that errors as unavailable at dispatch time → re-dispatch with
`inherit` and note it in `progress.md`; never stall a run on a model assignment.

## The MoA reviewer (independent code review at checkpoints)

Not a per-tool-call interceptor (rejected as cost-prohibitive — see issue #12's scope revision): the
reviewer is an **independent third-party code review of the finished work**, run by ship §2 — and, when
`review_points: per-wave`, additionally at each build wave-end gate over that wave's diff. Mechanics:

1. Produce the diff (`git diff <base>...HEAD` for at-finish; the wave's commits for per-wave) to a temp
   file, plus context: `spec.md` (or `sdd.md` §13) and the relevant constitution rules.
2. Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/ship/scripts/moa_review.py --config .wi/moa.md
   --diff <patch> --context <spec> --out .wi/goals/<slug>/moa-review.md`.
3. Exit `0` = `## REVIEW PASSED`; `1` = `## ISSUES FOUND` — treat findings like checker findings:
   BLOCKER → fix (loop back to build), WARNING/INFO → address or record. **Max 2 review→fix rounds**
   (the issue's revision cap); whatever remains after round 2 is surfaced, with severity, in `PR.md`'s
   Verification section. `3` = no API key in `api_key_env` → **fall back** to dispatching a checker-tier
   Claude agent with the same review charter (log `moa review via fallback (<reason>)`); `2` = config or
   API error → same fallback. The reviewer works alone — the orchestrator hands it the diff and takes
   back findings; it does not steer the review.
4. `moa-review.md` is **ephemeral** like `verification.md`: distill the verdict into `PR.md`, prune at
   close-out.

Reviewer `none` (simple preset) → skip this section entirely; ship's existing self-review + checker
still run — MoA review is a layer on top, never a replacement.
