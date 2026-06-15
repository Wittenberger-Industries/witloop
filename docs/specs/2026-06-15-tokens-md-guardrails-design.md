---
type: Design Spec
title: Harder guardrails for tokens.md — scaffold, script-write, blocking ship gate
description: Make the per-goal token ledger impossible to silently skip — a deterministic scaffold, a script that writes the orchestrator total into the file, and a structural close-out gate that blocks the PR on a genuine skip.
status: accepted
timestamp: 2026-06-15
tags: [tokens, ship, build, research, rpa, guardrail, dossier]
---

# Harder guardrails for tokens.md

## Problem

`tokens.md` — the per-goal token ledger (one of the seven dossier files) — **sometimes
never gets fully written**. It has four skip points, each a prose instruction the
orchestrating model can quietly drop while juggling its real work:

1. **Scaffold** — created lazily "on the first delegation if absent"; if that append is
   skipped, no file is ever created.
2. **Live subagent rows** — appended during research and build the moment each
   completion notification arrives. The count exists *only* in that notification.
3. **Finalize** (ship §5.3) — today the agent runs `token_report.py`, sees the report in
   the console, and is *supposed* to hand-copy it over the `## Orchestrator` PENDING
   block. Ship already warns "printing to the console does not count as done" — i.e. this
   copy step is a known, observed skip.
4. **Verify** (ship §8) — a soft close-out checkbox the agent can tick from memory.

**Hard constraint (verified):** subagent token counts are **not recoverable after the
fact**. A probe of every transcript under `~/.claude/projects/` for this project found
zero `isSidechain:true` usage records — the harness does not persist subagent usage in
any summable, attributable form. So the live append (point 2) is the *only* capture point
for subagent counts; a ship-time script can **detect a missing row but never reconstruct
its number**. The orchestrator total, by contrast, *is* recoverable — `token_report.py`
parses the main-thread transcript's per-turn `usage`.

## Goals

- A skipped or half-written `tokens.md` **cannot ship silently** — it fails a structural
  gate at close-out and the keep-alive loop is forced to complete it before the PR opens.
- Finalize becomes **one deterministic command** that writes the file itself — no manual
  stdout-copy to skip.
- The file **always exists** with the right skeleton from the first delegation.
- An honest *can't-measure* (transcript unparseable → `Orchestrator: unavailable for this
  run`) still ships — the gate blocks a **skip**, never an honest measurement failure.
- Applies uniformly to **both** the dev flow and the rpa flow.

## Non-goals

- **Recovering missed subagent rows** — impossible; the harness has discarded the number.
  The gate proves the file is present and structurally finalized, not that every subagent
  that ran got a row.
- **A per-row completeness heuristic** (e.g. cross-checking row count against `tasks.md`).
  Explicitly declined: the ledger is a cost *estimate*, not an audit.
- **Changing the live-append model** — it remains the only capture point for subagent
  counts; we back it with a gate rather than replace it.
- **Any harness change** — the gate works purely via a script exit code wired to
  `Phase=done` / the keep-alive condition through skill prose.

## Design

### Two small scripts (stdlib-only python3, no new dependencies)

**`skills/ship/scripts/token_report.py`** — add a `--write <tokens.md>` mode. It parses
the transcript exactly as today, then instead of only printing:
- replaces the `## Orchestrator` **PENDING** block in place with the parsed figures, or
  with `Orchestrator: unavailable for this run` when the parse fails (never PENDING, never
  a fabricated or substituted number);
- recomputes the `**Subagents (exact): N.**` line by summing the integer Tokens cells of
  the ledger rows;
- still prints the report to stdout (so close-out can read the figure back).
- **Exit:** `0` when the section was written (including the `unavailable` case — the
  *write* succeeded). Non-zero only if the file does not exist (message: run
  `check_tokens.py --init` first) or cannot be written. File creation is **not** this
  script's job — it finalizes an existing ledger.

**`skills/ship/scripts/check_tokens.py`** — new, two modes:
- `--init <path>`: write the template **only if the file is absent**; exact byte-for-byte
  no-op if it already exists (idempotent). Template = OKF frontmatter (`type: Token
  Ledger`), the ledger table header, the static `| orchestrator | main thread, all phases
  | … |` guidance row, the `**Subagents (exact): <sum>.**` placeholder, and the `##
  Orchestrator` PENDING block — matching the canonical template in `wi-directory.md`.
- `<path>` (verify — the gate): exit `0` **iff** all hold, else exit non-zero printing the
  first failing check:
  - the file exists;
  - frontmatter is present and parseable with `type: Token Ledger`;
  - **≥1 data row** — a table row whose Tokens cell is an integer (the static orchestrator
    row and any `<n>` placeholder do **not** count, so this forces ≥1 real appended row);
  - the Subagents sum line is a filled integer (not the literal `<sum>`);
  - the `## Orchestrator` section is **resolved** — contains parsed figures **or** the
    `unavailable for this run` sentinel, and **not** `PENDING`.

*Assumption:* every wi goal that reaches ship has delegated ≥1 subagent (research
dispatches researchers, build dispatches task-runners, rpa dispatches per unit), so the
"≥1 data row" rule never blocks a legitimate run. A hypothetical zero-delegation goal is
out of scope; if one ever arises, the fix is an explicit "no delegation this run" marker
the gate accepts — not softening the rule.

*Boundary rationale:* transcript parsing (`token_report.py`) stays separate from file
lifecycle + verification (`check_tokens.py`); each script keeps one purpose.

### Wiring into the flow

| Where | Change |
|---|---|
| **research** (autonomous-phase start) | run `check_tokens.py --init <path>` so the file exists before the first researcher row; keep the per-completion row append. |
| **build** (start) | defensive `check_tokens.py --init <path>` if absent (covers skipped/resumed research); keep the per-runner row append. rpa build mirrors this. |
| **ship §5.3** (finalize, before the dossier commit) | replace "run the script, then write its output into `tokens.md`" with a single `python3 …/token_report.py --write <path>` (orchestrator section + Subagents sum in one command). |
| **ship §8** (close-out) | the soft `tokens.md` checkbox becomes `python3 …/check_tokens.py <path>`; a **non-zero exit blocks `progress.md` Phase = done**, so a keep-alive loop keeps working the goal instead of opening the PR. |
| **rpa** verification gate | the prose "tokens.md present" / "tokens.md written" checks become the same `check_tokens.py <path>` call. |

## Acceptance criteria

1. `check_tokens.py --init P` on an absent `P` writes a ledger whose frontmatter is
   `type: Token Ledger` and that contains the table header, the static orchestrator row,
   the `<sum>` placeholder, and a `## Orchestrator` PENDING block.
2. `check_tokens.py --init P` on an existing `P` leaves it byte-for-byte unchanged.
3. `token_report.py --write P` against a parseable transcript replaces PENDING with the
   parsed figures, sets `**Subagents (exact): N.**` to the integer sum of the data rows,
   still prints the report, and exits 0.
4. `token_report.py --write P` when the transcript cannot be parsed writes `Orchestrator:
   unavailable for this run` (no PENDING, no fabricated number) and exits 0.
5. `token_report.py --write P` when `P` is absent exits non-zero and does not create `P`.
6. `check_tokens.py P` exits 0 on a finalized ledger (real figure **or** `unavailable`),
   and exits non-zero — naming the first failing check — when `P` is missing, has no
   integer-token data row, has an unfilled `<sum>`, or still shows `PENDING`.
7. `ship/SKILL.md` §5.3 calls `token_report.py --write`; §8 calls `check_tokens.py` and
   states that a non-zero exit blocks `Phase = done`.
8. `research/SKILL.md` and `build/SKILL.md` call `check_tokens.py --init` at the points
   above; `research/references/wi-directory.md` documents the three script calls
   (`--init`, `--write`, verify) alongside the template.
9. `rpa/SKILL.md`, `rpa/references/build-uipath.md`, `rpa/references/verification-gate.md`,
   and `rpa/references/rpa-constitution-template.md` route their tokens.md check through
   `check_tokens.py`.
10. Both scripts are stdlib-only python3; unit tests for criteria 1–6 pass via
    `python -m unittest`; `python scripts/validate.py` still passes.
11. Plugin version bumped `0.10.3 → 0.10.4` across the three manifests; a README /
    release-notes line records the guardrail.

## Testing

A new `tests/` directory with stdlib `unittest` (no new dependency, no test runner to
install): `python -m unittest discover tests`. Cases cover criteria 1–6, including a small
fixture transcript (`usage` records) for the parseable case and an empty/garbage file for
the `unavailable` case. The skill prose changes (criteria 7–9) are verified by
`scripts/validate.py` (frontmatter/manifest) plus a manual read.

## Rollout

Standard single-PR change. Version bump to `0.10.4`, README/release-notes line, run
`scripts/validate.py`, and the usual file-tail check before commit (this repo has a
history of truncated writes). No migration: existing in-flight `tokens.md` files already
match the template the scripts expect.
