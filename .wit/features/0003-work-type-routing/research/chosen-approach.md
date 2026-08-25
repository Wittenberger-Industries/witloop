---
type: Research Note
title: "Chosen approach: thin work-type router with phase overlays"
description: Reconciled design for semantic work-type deduction, read-only investigations, and evidence-led bug fixes.
feature: 0003-work-type-routing
timestamp: 2026-08-25
valid_until: 2026-09-24
---

# Chosen approach: thin work-type router with phase overlays

## Decision

Add one semantic work-type decision before any write-capable `/wit:dev` setup:

1. Resolve the plugin root and parse `--auto` / `--kind` in memory.
2. `--kind` wins. Otherwise the orchestrator deduces intent using conservative rules and examples.
   Mixed or unclear intent becomes an announced `feature`.
3. `investigation` loads an on-demand read-only reference and exits without scan writes, a dossier,
   gates, keep-alive, or PR.
4. `feature` and `bug-fix` continue through the existing host probe, scan, model setup, and
   feature-folder classifier. Their dossier stamps `Work type:`; a missing stamp means `feature`.

Keep the semantic deduction in the skill contract, not a keyword-only script. The orchestrator already
understands the user's request, and a fixed English tell table would be less faithful to "deduce intent."
Contract tests pin precedence, examples, announcement, hook order, and backwards compatibility.

## Investigation overlay

`skills/dev/references/investigation.md` owns the exit. It uses the existing skill-discovery union and
delegates to installed `how` when present; motivational questions may also use installed `why`.
Otherwise Witloop runs a portable read-only explorer/explainer fallback, capped at two explorers for a
cross-cutting question. The cited chat reply is the only artifact.

`integrations.md` gains an `understand` capability and an explicit exception to its normal
capture-into-`.wit/` rule. The route does not add a command, agent, MCP requirement, or install offer.

## Bug-fix overlay

`skills/dev/references/bug-fix.md` specializes the existing phase machine:

- Brainstorm adds a concrete repro contract: surface, trigger, observed result, expected result.
- Research invokes installed `systematic-debugging`, or the existing inline fallback, before choosing
  a fix. It records the failing surface and root cause.
- Plan and plan-mode checker always run.
- The human design gate may be bypassed only for a fail-closed narrow fix that restores an existing
  public contract, changes no architecture/dependency/interface, has no checker BLOCKER, and is the
  smallest fix supported by the evidence. The structured reason and distinct
  `design gate bypassed (narrow-fix)` stamp are mandatory.
- Build and ship reuse the existing task-runner, TDD, verification, checker, and PR flow. The same
  named surface must fail before and pass after. Missing regression coverage needs an explicit
  impracticality reason.

Timing parsers and the build precondition accept the distinct bypass stamp. Feature and `--auto` gate
behavior remain unchanged.

## Rejected

- **Keyword-only classifier script:** testable but brittle, language-bound, and weaker than semantic
  intent deduction.
- **A fifth command or hidden investigation skill:** expands the advertised surface and competes with
  optional `how`.
- **Parallel bug-fix playbook:** duplicates dossier, plan, checker, build, and ship behavior.
- **Skip directly from repro to build:** weakens plan-mode coverage and breaks build preconditions.

## Risks carried to plan

- The investigation hook must run before scan or feature-folder writes.
- Invalid `--kind` must stop with valid values; it must not silently infer.
- The narrow-fix predicate must fail closed and remain distinct from `--auto`.
- All three timing parsers must recognize the bypass stamp.
- Agent charter edits must be additive and leave report markers and tools unchanged.
- The behavior change requires a minor version bump with three-manifest parity.
