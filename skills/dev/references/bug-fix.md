---
type: Reference
title: "Bug-fix route: repro contract, evidence, narrow-fix bypass"
description: "On-demand overlay for Work type bug-fix: repro-focused brainstorm, pre-plan systematic-debugging, mandatory plan and checker, fail-closed narrow-fix gate bypass, and same-surface proof."
timestamp: 2026-08-25
tags: [dev, bug-fix, reference]
---

# Bug-fix route: repro contract, evidence, narrow-fix bypass

This file is enough to decide when loaded alone.

Load when Work type is bug-fix. Feature / missing Work type = today's loop; never consult Gate bypass.
missing Work type = feature. `--auto` stays separate from the narrow-fix bypass.

Phase order: brainstorm repro, research debug, plan+checker, then gate/bypass, then build.

## 1. Brainstorm specialization

Keep `brief.md` and the four must-asks. Reinterpret them for bug-fix (do not add a second conversation):

1. **Scope**: the symptom, the named surface, and explicit non-goals (no drive-by refactor, no extra work type).
2. **Behavior**: expected vs actual, with a concrete trigger. This is the WHAT of the bug, not the root cause.
3. **Acceptance**: the original repro fails, then passes, on the same named surface. Name the root cause and the smallest justified fix in the eventual result (acceptance of the run, not a guessed HOW).
4. **Hard constraints**: compatibility, public-behavior freeze when the user wants a narrow fix, must-reuse.

Brainstorm never skipped. `--auto` still does not skip brainstorm. Delegation to
`superpowers:brainstorming` is unchanged (dialogue method only; wit still writes `brief.md`). Stamp stays
`brainstorm via superpowers:brainstorming` or `brainstorm via wit fallback (superpowers absent)`, plus
`, dialogue` / `, self-answered (headless)`.

Persist a `## Repro contract` section inside `brief.md` (not a new dossier type):

- **Surface:** exact command, test node, or UI path (the same string later phases reuse)
- **Trigger:** steps
- **Observed / expected**
- **Force strategy** if intermittent

Feature brainstorm must-asks stay untouched when Work type is missing or `feature`.

## 2. Systematic-debugging (research evidence, before approach fan-out)

Before approach fan-out, delegate to `superpowers:systematic-debugging` when present; otherwise run the
inline hypothesis-and-test fallback. Stamp exactly
`debug via superpowers:systematic-debugging` or
`debug via wit fallback (systematic-debugging absent)`.

Reproduce on the brief **Surface** before any fix. Force the trigger if needed. Write `research/repro.md`
(type: Research Note: hypotheses ruled out, surviving mechanism, commands) and `.logs/repro-before.txt`
(redirected per the output house rule). Durable stamps use THE SAME surface string:

- `- <ts> **Update** repro failed on <surface>`
- later `- <ts> **Update** repro passed on <surface>`

A bug that will not reproduce does not enter build; record a blocker.

Keep the existing `debug (any phase)` path for later task failures. No new debug agent.

Research fan-out after evidence: usually one `[repo-question]` leftover at most (smallest justified fix
given this mechanism).

## 3. Plan and plan-mode checker

Plan + plan-mode checker ALWAYS run. Narrow plans small (typically 1-3 tasks). First Verify is the Surface
(or a cheap automated stand-in that is that surface). Red and green stay inside that task. Still write
`spec.md` / `tasks.md` / `pitfalls.md`. Still commit the dossier on main
(`docs(<slug>): feature dossier (design gate)`).

`spec.md` acceptance criteria name the surface, the fail-then-pass requirement, the root cause, and the
smallest fix. Same-surface fail then pass. Add a regression test when practical; if not practical,
`spec.md` must record an explicit impracticality reason.

## 4. Narrow-fix predicate (FAIL-CLOSED)

Bypass the human ask and gate-summary render only. Always stamp `design gate opened` first so timing span1
closes.

All must be true (any missing field = false). Bypass is refused when any conjunct is missing. Then use the
existing interactive or `--auto` gate.

1. Work type exactly bug-fix (never feature, never missing). Work type is exactly `bug-fix` (never `feature`, never missing).
2. Root cause from runtime evidence: `repro failed on <surface>` exists and `research/repro.md` names the surviving mechanism.
3. Public behavior unchanged: no advertised command, skill contract, CLI flag, user-visible default, or published API/schema change.
4. Architecture unchanged: no new module, dependency, layer, or external service; nothing ADR-worthy.
5. Blast radius = files tasks.md names; no silent extra surface.
6. Plan-mode checker has no BLOCKER. WARNINGs are allowed and must be copied into the bypass block.
7. Smallest evidence-backed fix (the smallest change the evidence justifies; a belt-and-suspenders extra is not a narrow fix).

`--auto` stays separate. If the predicate holds, use the bypass stamp (justified skip). NEVER reuse `design gate auto-approved (--auto)`. If the predicate fails under `--auto`, keep today's auto-approve path.

## 5. Audit stamp and Gate bypass block

Always stamp `design gate opened` first:

`- <ts> **Update** design gate opened`

Then, if the predicate holds, do not ask. Write the structured `## Gate bypass` block and:

`- <ts> **Update** design gate bypassed (narrow-fix): <one-line reason>, phase = build`

```text
## Gate bypass
- **Status:** narrow-fix
- **Public behavior unchanged:** yes
- **Architecture unchanged:** yes
- **Root cause:** <mechanism>
- **Why skip:** <one line>
- **Checker (plan mode):** PASS | N WARNINGs (<list>)
- **Surface:** <exact surface string>
```

Build precondition: interactive/auto-approve stamp **or** (Work type bug-fix AND `## Gate bypass` Status
`narrow-fix` AND a `design gate bypassed (narrow-fix)` log line). Feature path never consults this block.

Keep-alive re-print: treat a recorded bypass like `--auto` (no second paste). Persistence was armed at the
brainstorm handoff.

## 6. Build, same-surface proof, reopen

After the fix task, run the **same** Surface command again, redirected to `.logs/repro-after.txt`, and stamp
`repro passed on <surface>` using THE SAME surface string as the failing stamp. Wrong-surface or
inconclusive is not a pass.

When a cheap local test exists, that test is the surface. When a test would be expensive,
integration-heavy, or unclear, keep the original surface and add an automated regression test when
practical; if not practical, spec.md must say why.

Do not split failing-repro and fix into two commits; red and green stay in one task.

If build discovers an architecture or public-contract change, revoke the bypass and reopen the existing design gate (existing mid-run amend). Do not keep a narrow-fix skip once the change is no longer narrow.
