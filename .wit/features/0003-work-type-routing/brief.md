---
type: Brief
title: Work-type routing for bug fixes and investigations
description: Route feature, bug-fix, and investigation requests from intent while preserving each path's contract.
feature: 0003-work-type-routing
timestamp: 2026-08-25
---

# Brief: Work-type routing for bug fixes and investigations

## What the user wants

`/wit:dev` should deduce whether a request is a `feature`, `bug-fix`, or `investigation` and route it
through behavior suited to that work. Users may override the deduction with
`--kind feature|bug-fix|investigation`.

Ambiguous intent defaults to `feature`. Witloop announces the selected work type and shows the
override instead of asking another question or routing silently.

An investigation is read-only. It returns a cited explanation or recommendation and creates no
feature dossier, brainstorm, design gate, build, or PR.

A bug fix starts from a reproduced symptom. It uses a repro-focused brainstorm and runtime evidence
to identify the root cause and ship the smallest justified change. Narrow fixes that change neither
public behavior nor architecture may skip the design gate when Witloop records why. Other fixes keep
the gate.

## Acceptance (in the user's words)

- Intent is classified across all three work types, not only bug fixes and investigations.
- `--kind feature|bug-fix|investigation` wins over automatic classification.
- Ambiguous intent is announced as `feature` with override guidance.
- Investigation returns a cited answer without changing product files, creating a dossier, or
  opening a PR.
- Bug-fix output names the root cause and smallest justified fix.
- The original bug repro fails before the fix and passes afterward on the same surface.
- An automated regression test is added when practical.
- Existing feature requests keep their current brainstorm, design, build, and ship behavior.

## Scope & non-goals

- In: intent classification, explicit `--kind` override, investigation exit, and scientific bug-fix
  flow.
- Out: refactoring, performance, prototype, and other work types.
- Out: a fifth advertised command, a dedicated `/wit:how`, a new review agent, Graphite workflows,
  required MCP integrations, or changes to RPA and add-issues.

## Constraints

- Work on all five documented hosts through the capability table and adapters.
- Keep `wit-code-checker` as the single review-agent contract.
- Preserve existing `feature` behavior.
- Require no MCP or external plugin; optional skills may be delegated to when present.
- Follow repository release policy for behavior changes and keep manifest versions in lockstep.

## Approach preferences (optional, non-binding)

- Infer work type from the user's intent by default.
- Borrow pstack's reproduce-first and cited-investigation methods without copying its sticky router.
- Keep the classifier and route entry points thin; put route-specific procedure in on-demand
  references.

## Open questions for research

- Which intent tells and precedence rules minimize false bug-fix or investigation classifications?
- Where should route-specific procedures live so existing feature behavior stays unchanged?
- How should the narrow-fix design-gate bypass be represented and tested without weakening the
  normal gate?
