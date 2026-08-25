---
type: Spec
title: Work-type routing for bug fixes and investigations
description: Deduce dev work type, early-exit read-only investigations, and run evidence-led bug fixes through the existing loop.
feature: 0003-work-type-routing
timestamp: 2026-08-25
---

# Spec: Work-type routing for bug fixes and investigations

## Summary

`/wit:dev` will deduce whether a request is a `feature`, `bug-fix`, or `investigation` before it
writes repository state. An explicit `--kind` overrides deduction. Investigations return a cited
read-only answer and stop. Bug fixes reuse the existing phase machine with reproduce-first evidence
and a fail-closed narrow-fix design-gate bypass.

The design follows ADR-0002. Existing feature requests, RPA, add-issues, host capability behavior, and
the single checker-agent contract remain unchanged.

## Goals

- Route all three work types from user intent through the existing `/wit:dev` entry.
- Preserve a fully read-only investigation path with optional `how` / `why` delegation.
- Make bug fixes prove the root cause and the same-surface failing-then-passing result.
- Reuse the existing dossier, plan, checker, TDD, build, ship, and keep-alive contracts.
- Keep route-specific procedure out of the always-loaded dev body.

## Non-goals

- New advertised commands or named agents.
- Refactoring, performance, prototype, visual-parity, or other work types.
- Required MCPs, pstack, Graphite, or Cursor-only mechanics.
- A keyword-only runtime classifier or a new application dependency.
- Changes to `/wit:rpa`, `/wit:add-issues`, or existing feature semantics.

## Acceptance criteria

1. `/wit:dev` semantically deduces `feature`, `bug-fix`, or `investigation`; valid `--kind` wins,
   invalid values stop with the valid set, and mixed/unclear intent becomes an announced `feature`.
   → verified by: `python -m unittest tests.test_work_type_routing`
2. Work type resolves before scan/model/folder writes. `investigation` loads the read-only route and
   exits; `feature` and `bug-fix` continue through the existing folder-state classifier.
   → verified by: `python -m unittest tests.test_work_type_routing tests.test_investigation_route`
3. Feature and bug-fix dossiers stamp `Work type:`; a missing stamp means `feature`, and resuming does
   not re-deduce unless `--kind` is supplied.
   → verified by: `python -m unittest tests.test_work_type_routing`
4. An investigation creates no `.wit/` state, branch, commit, keep-alive, or PR; it delegates to
   installed `how` when present, optionally uses installed `why` for motivation, otherwise uses a
   portable read-only fallback capped at two explorers, and returns code/git/web citations plus
   sources.
   → verified by: `python -m unittest tests.test_investigation_route`
5. A bug-fix brainstorm records a repro surface, trigger, observed result, and expected result.
   Research invokes installed `systematic-debugging` or the inline fallback before planning and
   records the root cause.
   → verified by: `python -m unittest tests.test_bug_fix_route`
6. Plan and plan-mode checker always run for bug fixes. The human design gate may be bypassed only
   when every narrow-fix condition is recorded: bug-fix work type, failing repro and root cause,
   restored existing public contract, unchanged architecture/dependencies/interfaces, named finite
   blast radius, no checker BLOCKER, and smallest evidence-backed fix.
   → verified by: `python -m unittest tests.test_bug_fix_route`
7. Narrow-fix bypass uses the distinct `design gate bypassed (narrow-fix)` stamp and structured audit
   block. Missing evidence fails closed; `--auto` remains separate; feature design gates never bypass.
   → verified by: `python -m unittest tests.test_bug_fix_route tests.test_timing_report`
8. Bug-fix build and ship require the same named surface to fail before and pass after, the PR to name
   the root cause and smallest fix, and either a regression test or an explicit impracticality reason.
   The result-mode checker treats a missing contract item as a BLOCKER.
   → verified by: `python -m unittest tests.test_bug_fix_route tests.test_bug_fix_checker`
9. All timing parsers count the narrow-fix bypass as the build/ship span start without changing
   approved or auto-approved timing.
   → verified by: `python -m unittest tests.test_timing_report`
10. The four advertised commands, five-host capability table, existing feature default, agent report
    markers, and seven-file done dossier remain intact.
    → verified by: `python scripts/validate.py && python -m unittest discover -s tests`
11. The behavior change ships as version `1.15.0` in all three manifests, with user docs, source-repo
    memory, and a before/after rules inventory in `PR.md`.
    → verified by: `python -m unittest tests.test_work_type_docs tests.test_work_type_release && python scripts/validate.py`

## Design

ADR-0002 owns the public decision. `skills/dev/SKILL.md` gets one read-only prelude that parses flags,
deduces and announces work type, then points to on-demand procedure:

- `skills/dev/references/work-types.md`: precedence, examples, stamp and resume rules.
- `skills/dev/references/investigation.md`: optional-skill delegation, fallback, citation contract,
  read-only deny-list, and early exit.
- `skills/dev/references/bug-fix.md`: repro contract, systematic-debugging evidence, narrow-fix
  predicate, same-surface proof, and phase pointers.

Investigation exits before write-capable setup. Feature and bug-fix then enter today's host probe,
scan/model setup, and folder-state classifier. `progress.md` gains an optional `Work type:` field.

Bug-fix procedure overlays, rather than replaces, brainstorm, research, plan, checker, build, and ship.
`integrations.md` adds `understand` and pre-fix debugging delegation. The checker receives additive
bug-fix matrix rows only. Timing parser allow-lists gain the distinct bypass stamp.

## Interfaces & data changes

- **Skill interface:** `/wit:dev <request> [--auto] [--kind feature|bug-fix|investigation]`.
- **Progress schema:** optional `Work type: feature|bug-fix`; optional `## Gate bypass` for narrow bug
  fixes. Missing Work type is `feature`.
- **Investigation output:** chat reply only, with route mode and `## Sources`.
- **Bug-fix evidence:** ephemeral repro note/logs; durable progress stamps, spec criteria, checker
  verdict, and PR excerpts.
- **Dependencies / config / env:** none.

## Test plan

- **Contract tests:** routing precedence, hook order, alias pass-through, read-only deny-list,
  integrations rows, bug-fix predicate, backwards compatibility, version/docs markers.
- **Unit tests:** all three timing parsers recognize the bypass stamp and preserve existing spans.
- **Full gate:** repository validator and all unittest modules.
- **Manual:** not applicable; this plugin behavior is a prompt contract and has no UI or executable
  classifier. Tests inspect the exact independently loaded rules.

## Rollout & back-out

- Release as `1.15.0`.
- Back out by reverting the routing references, thin pointers, progress extensions, parser allow-list,
  tests, docs, and manifest bump together. Existing dossiers remain readable because missing Work type
  always means `feature`.

## Open questions

- None. Research assumptions are resolved by the fail-closed rules above.

## Citations

1. ADR-0002: work-type and overlay decision.
2. `skills/dev/SKILL.md`, `references/workflow.md`, and `skills/build/SKILL.md`: current phase and gate
   contracts.
3. pstack 0.14.3 `bug-fix.md`, `investigation.md`, and `how/SKILL.md`: methods adapted without the
   sticky router.
