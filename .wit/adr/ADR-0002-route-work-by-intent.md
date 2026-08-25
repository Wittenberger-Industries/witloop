---
type: ADR
title: Route dev work by intent with read-only and bug-fix overlays
description: Deduce work type before dev writes state, then early-exit investigations or overlay the existing feature loop.
feature: 0003-work-type-routing
status: accepted
timestamp: 2026-08-25
---

# ADR-0002: Route dev work by intent with read-only and bug-fix overlays

- **Status:** accepted
- **Date:** 2026-08-25
- **Deciders:** wit research (autonomous); design gate approved 2026-08-25
- **Feature:** 0003-work-type-routing

## Context

`/wit:dev` currently treats every request as a feature that opens a dossier and proceeds toward a PR.
That adds feature ceremony to confirmed defects and cannot answer read-only architecture questions
without leaving the loop. Witloop must add those paths without copying pstack's sticky 22-playbook
router, adding a fifth command, requiring MCPs, or changing the existing feature contract.

The route decision must happen before any write-capable scan or feature-folder setup because an
investigation promises no repository mutation. Bug fixes still need resume, planning, checker, TDD,
shipping, and durable proof, so a separate implementation pipeline would duplicate load-bearing state.

## Decision

We will:

1. Deduce `feature`, `bug-fix`, or `investigation` from semantic user intent before write-capable dev
   setup. `--kind feature|bug-fix|investigation` overrides deduction. Invalid values stop. Mixed or
   unclear intent defaults to an announced `feature`.
2. Route investigations through an on-demand read-only reference. Prefer an installed `how` skill
   through the existing discovery union; use a portable cited fallback otherwise. The chat reply is
   the only artifact. No scan write, dossier, gate, keep-alive, branch, or PR occurs.
3. Stamp `Work type:` in feature and bug-fix dossiers. Missing stamps remain `feature` for backwards
   compatibility. Route-specific procedure stays in on-demand references, not the always-loaded dev
   body.
4. Overlay bug fixes on the existing brainstorm, research, plan, checker, build, and ship phases.
   Research reproduces and isolates the root cause before a fix is planned. The same surface must fail
   before and pass after.
5. Permit a distinct `design gate bypassed (narrow-fix)` outcome only when a fail-closed record proves
   the change restores an existing public contract, changes no architecture, dependency, or interface,
   has no plan-mode BLOCKER, and is the smallest fix justified by runtime evidence. This is not
   `--auto`; missing evidence keeps the normal gate.
6. Keep `wit-code-checker` as the only review-agent contract. Add only bug-fix coverage rows; preserve
   its report markers, caps, modes, and tools.

## Consequences

- **Positive:** read-only questions no longer create state; bugs gain reproduce-first evidence while
  reusing the mature feature pipeline; ambiguous requests remain safely on the feature path.
- **Negative / costs:** the work-type and narrow-bypass contracts touch hotspot rules, timing parsers,
  progress templates, and checker coverage. Semantic deduction is protocol-tested rather than a pure
  function over arbitrary language.
- **Follow-ups:** roadmap candidate 3 may reuse the `understand` capability inside active feature
  research. Performance and forensics work types remain later candidates.

## Alternatives considered

- **Keyword-only classifier helper:** easy to unit-test, but brittle across phrasing and languages and
  weaker than the requested intent deduction.
- **New `/wit:investigate` or bug-fix command:** breaks the four-command surface and duplicates entry
  behavior.
- **Reuse feature ceremony for investigations:** violates the read-only, no-dossier result.
- **Skip planning and checker for bug fixes:** weakens coverage and breaks build's gate precondition.
- **Copy pstack's playbook router:** imports Cursor-specific machinery and conflicts with Witloop's
  spec-driven state machine.

## Citations

1. `skills/dev/SKILL.md` dev:1-2: current setup, flag parsing, and feature-folder classification.
2. `references/workflow.md` "Contracts": phase order and two-gate contract.
3. `skills/research/references/integrations.md`: optional-skill detection, delegation, and capture.
4. `skills/build/SKILL.md` precondition: plan plus a recorded gate outcome.
5. Local pstack 0.14.3 `skills/poteto-mode/playbooks/bug-fix.md` and `investigation.md`: methods
   borrowed without the sticky router.
