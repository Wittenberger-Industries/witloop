---
type: Brief
title: Ship verification honesty
description: Require a proven or unproven safety fact at ship, and never silent-PASS an unmeasured extra check.
feature: 0003-blast-radius-proof
timestamp: 2026-08-27
---

# Brief: Ship verification honesty

## What the user wants

At ship, a behavior PR cannot look green on a writeup. It must name **one safety fact** (the claim
the change is safe because of) and either a command run **this session** that would fail if that
claim is false, or the word `unproven`. A green test suite does not replace that row.

Named extra checks that are not repo-map gate commands (visual, perf, anything similar) and were
not run this session are listed as `unproven`. They are never omitted so the PR looks complete.

Docs-only PRs (no runtime behavior) use `n/a` with a short reason instead of inventing a fact.

pstack's contribution is the one-fact-plus-real-run (or honest unproven). D3's contribution is
unknown-never-silent-PASS. Witloop keeps BLOCKER / WARNING / INFO. It does not adopt D3's
PASS / CONCERNS / FAIL / WAIVED names.

Ship writes the rows into `PR.md`. Checker result-mode treats a missing row, or prose with no
command / `unproven` / `n/a`, as BLOCKER. Tests cover the skill text, the PR template, and the
checker charter. The same row applies on the RPA verification gate.

Example: a skill change that claims `validate.py` rejects leftover `${CLAUDE_PLUGIN_ROOT}` names
that command (or a unittest) in Testing plus a Safety fact line pointing at it. If the cheap
proof does not exist, the line says `unproven` and why.

## Acceptance (in the user's words)

- Every behavior PR names one safety fact and a this-session command, or `unproven`.
- Extra named checks that were not run appear as `unproven`, never disappear.
- Docs-only PRs may use `n/a` with a reason.
- Checker result-mode BLOCKER if that row is missing or is writeup-only.
- Repo-map gate commands still run under the existing iron law. Unproven is not a way to skip
  pytest or `validate.py` when they are configured.
- Manifests lockstep at 1.16.1.

## Scope & non-goals

- In: `skills/ship/` (gate + `PR.md` template), `agents/wit-code-checker.md` result mode,
  RPA verification-gate pointer, tests, three-manifest 1.16.1, roadmap row 4 marked done at ship.
- Out: D3 PASS / CONCERNS / FAIL / WAIVED vocabulary; a new `verify-report.md`; pstack arena /
  multi-model blast radius; changing user-accepted red CI (`progress.md` only, as today);
  verification-map (roadmap row 2); a fifth advertised command.

## Constraints

- Patch release 1.16.1 (all three manifests together).
- Keep `wit-code-checker` as the single review agent and BLOCKER / WARNING / INFO.
- No em dashes in shipped text.
- Must reuse the existing ship / RPA gate files; do not add a second gate.

## Approach preferences (optional, non-binding)

- Prefer a short `### Safety fact` block in `PR.md` over a fourth verdict vocabulary.
- Map checker: missing/writeup-only → BLOCKER; honest `unproven` → INFO (visible, not a fail);
  `n/a` with a docs-only reason → INFO.

## Open questions for research

- Exact `PR.md` heading and the cheapest test shape that proves a missing row is a checker BLOCKER
  without a live subagent (skill/charter string tests, same style as existing ship tests).
