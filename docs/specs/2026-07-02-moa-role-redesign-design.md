---
type: Design Spec
title: "MoA — rename tiered-model roles to wi's actual dispatched agents"
description: Replace the confusing orchestrator/execution/checker/reviewer role names in .wi/moa.md with the three real dispatch targets (wi-code-checker, wi-researcher, wi-task-runner), fold the standalone cross-provider "reviewer" into wi-code-checker's result-mode path, and give each role a clear, non-arbitrary tiering default.
status: accepted
timestamp: 2026-07-02
tags: [moa, models, reference, config]
---

# MoA — rename tiered-model roles to wi's actual dispatched agents

## Problem

`references/moa.md` (issue #12, `ed6f14a`) splits model tiers across four roles — `orchestrator`,
`execution`, `checker`, `reviewer` — but only `orchestrator` and `checker` name something real. `execution`
is silently shared by two unrelated agents (`wi-researcher` and `wi-task-runner`), and `reviewer` is a
fourth concept bolted on beside `checker` even though both do the same job (goal-backward verification) —
`reviewer` just happens to run cross-provider over a diff. The result: presets are hard to reason about,
and there's no default logic for *why* a role gets the tier it does.

## Goals

- Every row in the `## Roles` table names a real dispatch target: `orchestrator` (informational),
  `wi-code-checker`, `wi-researcher`, `wi-task-runner`.
- `wi-code-checker` absorbs the standalone `reviewer` concept — cross-provider is its own **result-mode**
  path, not a separate agent.
- Each role's default tier follows an explainable rule, not an arbitrary preset value:
  - `wi-code-checker`: same-family fallback tier, **never below the orchestrator's own tier** (smart:
    top-of-family `fable`; simple: matches orchestrator, `opus`).
  - `wi-researcher`: one Claude tier below the orchestrator, computed once at first-run setup.
  - `wi-task-runner`: scales with preset (smart → `opus`, simple → `sonnet`).
- No runtime behavior regression: PLAN-mode checks, RESULT-mode cross-provider review + fallback, per-wave
  gating, and the max-2-review-round cap all keep working exactly as today.

## Non-goals

- No back-compat parsing of the old `execution`/`checker`/`reviewer` schema — the feature is one commit
  old (`ed6f14a`), so a stale `.wi/moa.md` from before this change is a one-time regenerate, not a
  migration path to build.
- No change to *how* cross-provider calls work (`_call_openai`/`_call_anthropic`, exit codes, the
  BLOCKER/WARNING/INFO fallback ladder, the 2-round cap) — only to how the config names and resolves the
  role that uses them.
- PLAN-mode checker stays same-family only (see Design §2) — extending `moa_review.py` to handle a
  spec/tasks-shaped (non-diff) prompt for cross-provider PLAN checks is out of scope.

## Design

### 1 · `## Roles` table

| Role | smart | simple | Notes |
|------|-------|--------|-------|
| `orchestrator` | `fable` | `opus` | informational only — session model, set via `/model`; wi warns once on mismatch, never blocks |
| `wi-code-checker` | `fable` | `opus` | same-family fallback tier; never below `orchestrator`'s tier |
| `wi-researcher` | `opus` | `sonnet` | one Claude tier below `orchestrator` (`fable→opus→sonnet→haiku`, floor at `haiku`) |
| `wi-task-runner` | `opus` | `sonnet` | scales with preset |

Presets still only *pre-fill* — every cell stays individually overridable via `## Per-agent overrides`.

### 2 · `wi-code-checker` absorbs the old "reviewer"

- **PLAN mode** (pre-gate, before a diff exists — verifies spec/task coverage): always dispatched via the
  Agent tool at the `wi-code-checker` role's Claude tier. No cross-provider path here (see Non-goals).
- **RESULT mode** (ship, plus per-wave when `check_points: per-wave`): if `## Cross-provider config`
  names a provider and its API key is present, verification runs via `moa_review.py` against the diff —
  functionally identical to today's `reviewer` mechanics (same prompt, same PASSED/ISSUES verdict, same
  2-round cap). If cross-provider is unconfigured or the call fails (exit 2 or 3), fall back to the
  Agent-dispatched `wi-code-checker` Claude tier — this is the *same* fallback ladder that exists today,
  just documented as `wi-code-checker` degrading to its own same-family tier rather than "reviewer
  degrading to checker."

### 3 · `## Reviewer provider` → `## Cross-provider config`

Same fields, `provider | base_url | model | api_key_env`, plus `review_points` renamed `check_points`
(`at-finish | per-wave`) to match the retired "reviewer" terminology. `provider: none` disables
cross-provider entirely — PLAN and RESULT mode both stay same-family, exactly like the `simple` preset
today.

### 4 · `moa_review.py` changes

- `PROVIDER_DEFAULTS` key `review_points` → `check_points`; `_section(body, "Reviewer provider")` →
  `_section(body, "Cross-provider config")`.
- `reviewer_enabled(cfg)` → `cross_provider_configured(cfg)`, same not-in-`("", "none", "off", "disabled")`
  check, now read from the `wi-code-checker` cross-provider config rather than a `reviewer` role cell.
- `model_for(agent, cfg)` splits the old two-branch lookup into three direct role reads:
  ```python
  def model_for(agent, cfg):
      if not cfg:
          return "inherit"
      if agent in cfg.get("overrides", {}):
          return cfg["overrides"][agent]
      return cfg.get("roles", {}).get(agent, "inherit")
  ```
  (Roles are now keyed by the literal agent name, so no more `if agent in ("wi-code-checker", "checker")`
  special-casing — the bare `"checker"` alias is dropped along with the old schema.)

### 5 · First-run setup + dispatch call-sites

`dev`/`rpa` step-2 setup wording updates to ask about the new table (still: *"MoA models: smart, simple,
or custom?"*, `--auto` → simple preset). At setup time, `wi-researcher`'s literal is computed once
(`step_down(orchestrator_tier)`) and written into the table — dispatch itself stays a plain table read,
no runtime tier-stepping logic. `research`/`build`/`ship`/`rpa` SKILL.md dispatch descriptions update their
role-name references (`execution` → `wi-researcher`/`wi-task-runner` per call-site; `reviewer` →
`wi-code-checker` cross-provider path) but keep the same call shape (`model_for(agent, cfg)` at each
`Agent(...)` dispatch).

### 6 · Migration

Clean break. An old-schema `.wi/moa.md` (rows named `execution`/`checker`/`reviewer`) simply won't
populate `wi-code-checker`/`wi-researcher`/`wi-task-runner` rows under the new `model_for()` — those
dispatches silently fall back to `inherit` (today's documented "no config" behavior), which is safe, just
under-tiered. Fix is to delete/regenerate `.wi/moa.md` via first-run setup. Not automated since the feature
predates any real external adoption.

## Testing

- `tests/test_moa_config.py` updates: `parse_moa_config` fixtures use the new table headings and role
  names; `model_for` cases cover `wi-code-checker`/`wi-researcher`/`wi-task-runner` plus the
  per-agent-override precedence; `cross_provider_configured` replaces `reviewer_enabled` cases (including
  `provider: none`).
- No new runtime tests needed for the fallback ladder — exit-code handling in `moa_review.py` is
  unchanged, only its config surface moved.
