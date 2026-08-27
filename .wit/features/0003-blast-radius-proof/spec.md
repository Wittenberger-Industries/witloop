---
type: Spec
title: Ship verification honesty
description: Require a proven or unproven safety fact at ship, and never silent-PASS an unmeasured extra check.
feature: 0003-blast-radius-proof
timestamp: 2026-08-27
---

# Spec: Ship verification honesty

## Summary

Ship must name one safety fact on every behavior PR: a command run this session that would fail if
the claim is false, or the word `unproven`. Extra named non-gate checks that were not run are listed
`unproven`, never omitted. Docs-only PRs use `n/a` with a reason. The checker treats a missing or
writeup-only row as BLOCKER. Honest `unproven` and valid `n/a` are INFO. Version lockstep 1.16.1.

pstack contributed the one-fact-plus-real-run. D3 contributed unknown-never-silent-PASS. Witloop
keeps BLOCKER / WARNING / INFO and does not adopt PASS / CONCERNS / FAIL / WAIVED.

## Goals

- A behavior PR cannot look green on a writeup alone.
- A green test suite does not replace the safety-fact row.
- Repo-map (and RPA) gate commands still run; `unproven` cannot skip them.
- Contract tests pin the charter and template without a live checker dispatch.

## Non-goals

- D3 PASS / CONCERNS / FAIL / WAIVED names, or mapping unproven to WARNING (that is a waiver).
- A new `verify-report.md` or a sixth verification-gate run step.
- pstack arena / multi-model blast radius.
- Changing user-accepted red CI (stays `progress.md` only).
- Roadmap row 2 (verification-map) or inventing unnamed visual/perf rows on every PR.
- A fourth work type for docs-only.
- Reordering ship:2 (checker) after ship:5 (`PR.md`).

## Acceptance criteria  (each must be testable)

1. The ship:5 `PR.md` template has an unconditional `### Safety fact` heading between `### Testing`
   and `### Verification`, with Claim, Proof (`command` | `unproven` | `n/a`), and optional Not-run
   bullets.  →  verified by: `python -m unittest tests.test_ship_safety_fact`
2. Checker result mode, for every shipping work type: missing heading (when `PR.md` exists), omitted
   matrix row, or writeup-only Proof is BLOCKER; honest `unproven` is INFO; valid docs-only `n/a` is
   INFO; `n/a` on a runtime-behavior diff is BLOCKER. Plan mode skips these rows.  →  verified by:
   `python -m unittest tests.test_ship_safety_fact`
3. When `PR.md` is absent (first ship:2), missing heading is not a miss; the checker still writes the
   Safety fact row into `verification.md`.  →  verified by: charter string in
   `tests.test_ship_safety_fact`
4. Configured repo-map / RPA gate commands cannot be skipped via `unproven`. Iron law gains no sixth
   run step.  →  verified by: `python -m unittest tests.test_ship_safety_fact`
5. RPA verification-gate pointer uses the same checker rows and the same `PR.md` heading; no copied
   D3 verdict list.  →  verified by: `python -m unittest tests.test_ship_safety_fact`
6. Manifests, `RELEASE`, and overview lockstep at 1.16.1. Marketplace catalog stays 0.2.0.
   Architecture keeps the historical 1.16.0 PLUGIN_ROOT caption.  →  verified by:
   `python -m unittest tests.test_work_type_release`

## Design

No new always-loaded file (avoids a serial PLUGIN_ROOT wiring task). Edit:

- `skills/ship/SKILL.md` - template, copy-the-row at ship:5, ship:8 checkbox
- `skills/ship/references/verification-gate.md` - honesty paragraph; unproven does not skip
- `agents/wit-code-checker.md` - glossary carve-out in plan mode; result-mode table **after** the
  bug-fix table (same four-column idea; first table stays the five bug-fix rows)
- `skills/rpa/references/verification-gate.md` - pointer only
- `docs/design-notes/ship.md` and `docs/design-notes/wit-code-checker.md` - rationale
- `tests/test_ship_safety_fact.py` - new contract tests
- `tests/test_work_type_release.py` `RELEASE = "1.16.1"` plus three manifests, overview, README

**Docs-only tell:** `n/a` is valid only when Proof is `n/a` plus a reason **and** `git diff --stat`
does not touch `skills/`, `agents/`, `scripts/`, `tests/`, `references/`, `.claude-plugin/`,
`.codex-plugin/`, or `AGENTS.md`. README / `docs/` / `.wit/roadmap.md` may be `n/a`.

**Sequencing:** checker at ship:2 may lack `PR.md`; that is not BLOCKER. Ship:5 copies the matrix
row into `### Safety fact`. Re-entry with an existing `PR.md` requires the heading.

**Learnings applied:** 0003-work-type-routing (serial wiring after new always-loaded files) → no new
`${PLUGIN_ROOT}` target; edit existing files only.

## Interfaces & data changes

- **APIs / signatures:** none
- **Data / schema:** `PR.md` template gains `### Safety fact` (additive public shape)
- **Config / env:** none
- **Dependencies:** none

## Test plan

- **Level rule:** unittest string/table pins; never a live Task.
- **Unit:** `tests/test_ship_safety_fact.py` plus existing `test_work_type_release.py` RELEASE bump.
- **Integration / e2e:** none
- **Edge cases:** first-pass absent `PR.md`; `n/a` on a skill diff; Testing `n/a - not configured`
  vs Safety fact `n/a`; do not `assertNotIn("PASS")` globally on RPA text; do not put a new
  Item/Plan/Result/Severity table **before** the bug-fix matrix.

## Rollout & back-out

- Patch 1.16.1. The owner directed a 1.16.x patch even though the constitution prefers minor for
  behavior/artifact changes. Do not retarget 1.17.0. Revert the PR to restore 1.16.0 behavior.
- No feature flag.

## Open questions

- None. Docs-only path list is locked in Design.

## Citations

[1] pstack `skills/blast-radius/SKILL.md`: one safety fact, prove by running code or mark unproven.
[2] D3 `d3-dev/phase-09-verify.md`: unknown targets are never silent PASS; WAIVED is out of this spec.
[3] `.wit/features/0003-blast-radius-proof/research/insertion-seams.md`
[4] `.wit/features/0003-blast-radius-proof/research/contract-tests.md`
[5] `tests/test_bug_fix_checker.py` additive BLOCKER rows without a live checker.
