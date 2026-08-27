---
type: PR Description
title: Ship verification honesty
description: Safety fact at ship
feature: 0003-blast-radius-proof
timestamp: 2026-08-27
---

## feat: Ship verification honesty (v1.16.1)

### Summary

Ship must name one safety fact on every behavior PR: a command run this session that would fail if
the claim is false, or the word `unproven`. Extra named non-gate checks that were not run are listed
`unproven`, never omitted. Docs-only PRs use `n/a` with a reason. The checker treats a missing or
writeup-only row as BLOCKER. Honest `unproven` and valid `n/a` are INFO. Version lockstep 1.16.1.

Task-runners never wait on the user. Architecture is `## TASK BLOCKED` with the question in Notes.
Every generation ends on a last-line marker. Build continues the DAG in the same turn.

pstack contributed the one-fact-plus-real-run. D3 contributed unknown-never-silent-PASS. Witloop
keeps BLOCKER / WARNING / INFO and does not adopt PASS / CONCERNS / FAIL / WAIVED.

### Acceptance criteria
- [x] `### Safety fact` between Testing and Verification with Claim / Proof / optional Not-run (verified by `python -m unittest tests.test_ship_safety_fact`)
- [x] Checker result-mode BLOCKER for missing heading, omitted row, or writeup-only Proof; INFO for honest `unproven` and valid docs-only `n/a` (verified by `tests.test_ship_safety_fact.CheckerSafetyFactTests`)
- [x] Absent `PR.md` is not a miss; checker still writes the Safety fact row (verified by charter pin + this PR copies that row)
- [x] `unproven` cannot skip repo-map / RPA gate commands; no sixth Run step (verified by `tests.test_ship_safety_fact`)
- [x] RPA pointer uses the same rows and heading; no D3 severity cluster (verified by `tests.test_ship_safety_fact.RpaSafetyFactTests`)
- [x] Manifests, `RELEASE`, and overview lockstep at 1.16.1; catalog 0.2.0; architecture `(1.16.0)` caption kept (verified by `python -m unittest tests.test_work_type_release tests.test_work_type_docs`)
- [x] Runner never yields: architecture is `## TASK BLOCKED`; every generation ends on a last-line marker; failed Verify is not a user prompt; AUTH-GATE stays the only human pause (verified by `tests.test_task_runner_no_yield`)
- [x] Build continues the DAG same turn: no wrap-up, no backgrounded runner, no ended turn while tasks remain except AUTH-GATE or design-gate AskQuestion; Grok pulls at the wave gate (verified by `tests.test_task_runner_no_yield`)

### Changes
- Always-on Safety fact table in `wit-code-checker` after the bug-fix matrix
- Unconditional `### Safety fact` in the ship:5 template, ship:8 checkbox, gate honesty paragraph
- RPA verification-gate pointer (no `skills/rpa/SKILL.md` edit)
- Lockstep 1.16.1 (owner-directed patch; constitution prefers minor)
- Task-runner never addresses the user; last-line marker every generation; architecture is `## TASK BLOCKED`
- Build no-yield: same-turn tick/commit/dispatch; no backgrounded runners; Grok pull at wave gate

### Testing
- Format: `n/a - not configured`
- Lint: `n/a - not configured`
- Typecheck: `n/a - not configured`
- Tests: `python -m unittest discover -s tests` → 306 OK
- Structure / CI-equivalent: `python scripts/validate.py` → exit 0 on tracked files (local scan also hits untracked `docs/skill-ideas/`, not in this PR)

### Safety fact
- Claim: the loaded checker charter, ship PR template, ship/RPA gate files, 1.16.1 lockstep, task-runner no-yield charter, and build same-turn DAG continuation encode the locked contract.
- Proof: `python -m unittest tests.test_ship_safety_fact tests.test_task_runner_no_yield tests.test_work_type_release tests.test_work_type_docs tests.test_bug_fix_checker.CheckerBugFixMatrixTests tests.test_bug_fix_checker.CheckerPreservedContractTests tests.test_bug_fix_checker.ShipBugFixEvidenceTests tests.test_bug_fix_checker.ShipRulesInventoryTests` (this session; 87 tests, OK)

### Verification
Result-mode checker: `## CHECK PASSED`. All eight ACs wired. No BLOCKER / WARNING / INFO findings. Line-level: ready to merge. Safety fact row was written while `PR.md` was absent (not a miss); this section is the copy.

### Risk & rollout
Patch 1.16.1. The owner directed a 1.16.x patch even though the constitution prefers minor for
behavior/artifact changes. Do not retarget 1.17.0. Revert the PR to restore 1.16.0 behavior.
No feature flag.

### Decisions
No new ADR (nothing hard to reverse). Standing ADR-0001 / ADR-0002 / ADR-0003 unchanged.
Learning `0003-work-type-routing` honored by not adding an always-loaded `${PLUGIN_ROOT}` target.

## Rules inventory

Rule-text diff. Each file still decides correctly if loaded alone.

| File | Before | After |
|---|---|---|
| `agents/wit-code-checker.md` | Bug-fix matrix only (five gated rows). Glossary Safety fact / Unproven had no result-mode honor point. | Second always-on result-mode table after the bug-fix table. Plan-mode skip / carve-out. Absent `PR.md` writes the row, not a miss. Loaded alone: still one review agent, same tools, same last-line markers, same 2-round loop. |
| `skills/ship/SKILL.md` | PR template jumped Testing → Verification. No Safety fact checkbox. | Unconditional `### Safety fact`. Copy-the-row at ship:5. ship:1 honesty pointer. ship:8 legal-Proof box. Loaded alone: still runs ship:2 before ship:5; Testing still holds fail-then-pass. |
| `skills/ship/references/verification-gate.md` | Iron law + five Run steps. | Honesty paragraph: green suite is not the safety fact; unproven does not skip configured commands; no sixth Run step. `n/a - not configured` stays a Testing phrase. Loaded alone: still five Run steps in the same order. |
| `skills/rpa/references/verification-gate.md` | Checker dispatch with no Safety fact pointer. | Pointer: same charter rows, same `### Safety fact` via ship:5, unproven does not skip restore/validate/Analyzer/paradigm. No D3 `PASS / CONCERNS / FAIL / WAIVED` list. Loaded alone: `verdict is PASS` still means the checker verdict. |
| `agents/wit-task-runner.md` | Architecture was `STOP and ask` (human wait). A generation could end without a last-line marker. | Architecture is `## TASK BLOCKED` with the question in Notes. Every generation ends on exactly one marker. Failed Verify is not a user prompt. AUTH-GATE stays the only human pause. Loaded alone: same tools, same ~15-line report, same 3-attempt cap, same landmines, same three markers. |
| `skills/build/SKILL.md` | After a report: tick/commit/dispatch next wave, but a parent wrap-up or backgrounded runner could end the turn with unticked tasks. | No yield while the DAG has work: same-turn tick/commit/dispatch; no wrap-up; no backgrounded `wit-task-runner`; Grok pull at wave gate. AUTH-GATE and design-gate AskQuestion remain the only pauses. Loaded alone: still one committer, still wave-end gate, still 3-attempt cap. |
| `skills/build/references/worktrees-and-subagents.md` | Skeleton asked for a short report with no last-line marker. | Skeleton requires `## TASK COMPLETE` / `## TASK BLOCKED` / `## TASK AUTH-GATE`; never address the user. |
| `references/grok-tools.md` | Tokens already pulled at wave gate; runners could still `background: true`. | Do not spawn a runner with `background: true`; pull `get_command_or_subagent_output` at each wave gate. |
| `references/cursor-tools.md` | Task dispatch with no background ban. | Do not set `run_in_background` on a `wit-task-runner`. `/goal` is a done-lock, not a scheduler. |

`skills/rpa/SKILL.md` was not edited; it already loads this gate file.
