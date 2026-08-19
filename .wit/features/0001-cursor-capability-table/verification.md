---
type: Verification
title: Verification - First-class Cursor host via a capability table (plan mode)
description: Plan will deliver as written; no BLOCKERs. Residual WARNING is the Task 5/6 context-window ceiling.
feature: 0001-cursor-capability-table
status: issues-found
timestamp: 2026-08-19
---

# Verification (plan mode, round 2)

Question: will this plan, built exactly as written, deliver the feature? **Yes.** Round-1 BLOCKERs F1–F3 and WARNINGs F4–F9, F11 are now tasked and verified. One WARNING remains (task-window ceiling). Round 2 is the last checker pass; remaining findings go to the human design gate.

Applicable learnings: none (progress.md `applicable learnings: none`).

## Round-1 disposition

| R1 | Was | Round-2 |
|----|-----|---------|
| F1 host probe every slug | BLOCKER | **Closed.** Task 7 Do names `claude\|codex\|copilot\|grok\|cursor`, plugin-root order, forbids copying this feature's Cursor stamp; Verify greps `Host: claude` in `skills/dev/SKILL.md`. |
| F2 Copilot / unknown Host | BLOCKER | **Closed.** Task 5 routes `cursor`, `copilot`, `codex`, missing Host, and any unknown slug to unavailable; Files + Verify include copilot/grok/cursor maps. |
| F3 ship log-dir `mkdir -p` | BLOCKER | **Closed.** Task 5 owns `skills/ship/SKILL.md` ship:8 `ensure_logdir.py`; Verify greps that file. Task 3 explicitly does not edit ship. |
| F4 `strip_frontmatter` stdout + `>` | WARNING | **Closed.** Spec Interfaces and Task 3/5 use `<in.md> <out.md>` and forbid shell `>`. |
| F5 models grok-else-claude | WARNING | **Closed.** Task 6 retargets host detection to stamped `Host:`; Verify greps `Host:` in `references/models.md`. |
| F6 paste `/goal` go-signal | WARNING | **Closed.** Task 7 replaces that sentence; Verify greps it empty in dev/research. |
| F7 plugin-bootstrap no Verify | WARNING | **Closed.** Task 6 Verify requires `plugin marketplace add` only in a non-Cursor branch. |
| F8 adapter ship:6 one-liners | WARNING | **Closed.** Task 5 Files/Verify cover grok/copilot/cursor maps. |
| F9 `_ledger` vs `test_timing_report` | WARNING | **Closed.** Task 5 Verify includes `tests.test_timing_report`. |
| F10 Task 6 ceiling | WARNING | **Remains** (and Task 5 is now in the same band). See F1 below. |
| F11 ship/SKILL.md clobber | WARNING | **Closed.** Exclusive ownership: Task 5 owns ship; Task 7 Files omit it and say do not edit. |
| F12 missing spec greps | INFO | **Partial.** `if cursor` and `/goal` go-signal greps added. Residuals in F2. |
| F13 research nits | INFO | **Partial.** Stale `cursor-grok-4.5-high` is not in this tree's `AGENTS.md`. Residuals in F3. |

## Coverage matrix

| Item | Source | Covering task | Wired? | Notes |
|------|--------|---------------|--------|-------|
| AC1 stamp `Host:` + `Plugin root (resolved):` + `## Capabilities (resolved)`; later phases read it | spec.md AC1 | Task 1 (template); Task 7 (scan/dev/rpa probe + pointer); Task 5 (reads `Host:`); Task 6 (models read stamp); Task 7 (go-signal from stamped `keep_alive`) | Yes | Detection is prose (tool surface / which adapter applies) plus the five slugs, not a telltale table. Enough to implement; see F3. Scan has no feature `progress.md` (F3). |
| AC2 `cursor-tools.md` + `capabilities.md` listed from AGENTS, README, validate.py | spec.md AC2 | Task 2 | Yes | Portability tuple + unittest. |
| AC3 `finalize_tokens.py --write` on Cursor writes unavailable; no `token_report.py`; Duration from progress; all-unavailable ledger passes | spec.md AC3 | Task 5 | Yes | Cursor / Copilot / Codex / missing / unknown → unavailable; Claude and Grok delegated; `test_tokens_guardrail` in Verify. |
| AC4 keep-alive `none` on Cursor; no `/goal`; no Autopilot | spec.md AC4 | Task 4 (templates); Task 7 (bodies + go-signal) | Yes | Spec verify-by is `test_keep_alive`. Ship still names `/goal` and Autopilot in armed-loop close-out (F3); that path is gated on an armed loop, which Cursor `none` does not arm. |
| AC5 AskUserQuestion → Cursor `AskQuestion` in scan/brainstorm/research/plugin-bootstrap | spec.md AC5 | Task 2 (`AskQuestion` in cursor-tools.md); Task 7 (scan/brainstorm/research cite `ask`) | Yes | plugin-bootstrap keeping the Claude tool *name* is the locked adapter-map. Field names `id`/`prompt`/`options` are spec/chosen-approach, not Task 2 Do (F3). |
| AC6 skill presence searches Cursor plugin cache before `(skill absent)` | spec.md AC6 | Task 6 | Yes | `discover_skills.py` + integrations.md order. plugin-bootstrap marketplace Verify is now a grep. |
| AC7 named `Task` types when listed, else inline; missing types not fatal | spec.md AC7 | Task 2 (cursor-tools.md); Task 7 (worktrees-and-subagents.md) | Yes | Do states non-fatal. Verify still does not grep `exit 1` (F2). |
| AC8 cite `capabilities.md`, no new `if cursor` / `if grok` in always-loaded bodies | spec.md AC8 | Task 7 (pointer + grep); Task 5 (ship:6 is one CLI, no host if-tree) | Yes | `plan/SKILL.md` and `build/SKILL.md` are in the AC8 grep set, not in Task 7 Files; today they have no host if-trees. |
| AC9 `cursor` column; Cursor dispatch reads concrete model id | spec.md AC9 | Task 6 | Yes | Column + stamp-driven detection + `PlatformMapTest`. |
| AC10 `ensure_logdir.py` + `strip_frontmatter.py`; workflow.md / ship PR-body name them | spec.md AC10 | Task 3 (helpers, workflow.md, add-issues); Task 5 (ship:7/8) | Yes | Task 5 Verify greps `ensure_logdir.py` in ship, not `strip_frontmatter.py` (F2). Do still requires ship:7 two-arg strip. |
| ADR-0001.1 matrix in `references/capabilities.md`; SKILL bodies cite it and read stamped cells | ADR-0001 | Task 1; Task 7; Task 5/6 consumers | Yes | Cite + stamped `keep_alive` / `Host:` reads are tasked. |
| ADR-0001.2 probe once at scan/dev/rpa; plugin-root env → walk-up → cache; cwd-as-wit-root beats cache | ADR-0001 | Task 1 (template); Task 2 (order in cursor-tools.md); Task 7 (execute + stamp every slug) | Yes | Order matches the ADR, not the five-step adapter-research variant (cache before walk-up). ADR wins. |
| ADR-0001.3 `finalize_tokens.py` only ship:6 command; any `tokens=unavailable` host (+ missing Host) writes sentinel; no `token_report.py`; Duration from progress | ADR-0001 | Task 5 | Yes | Copilot/Codex/unknown included. `codex-tools.md` is not in Task 5 Files; SKILL default is the dispatcher so Codex needs no map override (F3). |
| ADR-0001.4 keep-alive.md keyed by capability; Cursor is `none` | ADR-0001 | Task 4 | Yes | Optional `/loop` in Task 4 Do. |
| Cursor is the first fully filled column / `cursor-tools.md` | ADR-0001 | Task 1; Task 2 | Yes | |
| Glossary: Capability table | glossary.md | Task 1; Task 7 | Yes | |
| Glossary: Host probe | glossary.md | Task 1; Task 7 | Yes | Same Task 7 recipe as ADR-0001.2. |
| Glossary: Keep-alive none | glossary.md | Task 4; Task 7 | Yes | |
| Pitfall: validate.py tripwires | pitfalls.md | Task 7 (retarget in the same task as SKILL edits) | Yes | |
| Pitfall: Claude Host stamp | pitfalls.md | Task 7 | Yes | Prevention text is now in Task 7 Do + Verify. |
| Pitfall: foreign transcript bind | pitfalls.md | Task 5 | Yes | Plant `HOME/.claude`; assert `token_report.py` not invoked on `Host: cursor`. |
| Pitfall: all-unavailable ledger | pitfalls.md | Task 5 | Yes | Duration fill + `test_tokens_guardrail`. |
| Pitfall: Grok finalize still SystemExit | pitfalls.md | Task 5 | Yes | Delegate `grok` unchanged; `test_grok_token_report` in Verify. |
| Pitfall: source repo vs marketplace cache | pitfalls.md | Task 2 (document); Task 7 (execute walk-up-before-cache) | Yes | Pitfall "prevented by" still names only Task 2; Task 7 now runs the order. |
| Pitfall: host prose in SKILL bodies | pitfalls.md | Task 7; Task 5 (ship tokens) | Yes | Pointer-only; constitution Simplicity. Residual host names in ship close-out (F3). |
| Pitfall: PowerShell UTF-16 logs | pitfalls.md | none (YAGNI) | Honored | Deliberate non-task; no third helper. |
| Pitfall: named Task types flicker | pitfalls.md | Task 7 | Yes | |
| Pitfall: Auth & security none | pitfalls.md | n/a | Honored | |
| Constitution: TDD + tests in `tests/` | constitution.md Testing | Tasks 1–6 say TDD; Verifies are unittests | Yes | |
| Constitution: `validate.py` + unit suite before ship | constitution.md Git | Task 7; Task 8 | Yes | |
| Constitution: three manifests lockstep; behavior bump minor | constitution.md Git | Task 8 (1.13.4 → 1.14.0) | Yes | |
| Constitution: stdlib only / Simplicity ladder | constitution.md | spec Dependencies; all scripts stdlib | Yes | No new dep. Verified as prohibition in over-build. |
| Constitution: ADR for capability table | constitution.md Architecture | ADR-0001 exists; Task 1 implements | Yes | |
| Constitution: agent charters unchanged | constitution.md Architecture | no task edits `agents/*.md` | Honored | Spec non-goal. |
| Constitution: host procedure in `references/` | constitution.md Simplicity | Task 2; Task 7 | Yes | Prohibition, not a mapping row. |
| Constitution: hotspots serial | constitution.md Architecture | Waves 1→2→3→4→5 | Yes | workflow.md: Task 1 then 3. validate.py: Task 2 then 7. ship/SKILL.md: Task 5 only. wit-directory.md: Task 1 only. |
| Constitution: no dashboard scrape; Autopilot not keep-alive; no Gemini row; no charter rewrite | constitution.md Out of scope | no such tasks | Honored | |
| Learnings | progress.md | n/a | Honored | none applicable. |

## Findings

### F1 — WARNING — Task 5 and Task 6 sit at the context-window ceiling

**Mode:** plan. **Evidence:** `tasks.md` Task 6 Files (6): `discover_skills.py`, integrations.md, plugin-bootstrap.md, models.md, two test modules. Concerns: skill-discovery union, Cursor bootstrap offer, models `cursor` column **and** stamp-driven host detection. Task 5 Files (7): `finalize_tokens.py`, `_ledger.py`, `skills/ship/SKILL.md`, three tool maps, `tests/test_finalize_tokens.py`. Concerns: dispatcher routing, ship:6/7/8 POSIX recipes, adapter one-liners. Verify also runs four test modules. Ceiling ~5–8 files **or** a sprawling multi-concern change in one sitting.

Round-1 F10 is unfixed; concentrating F3/F8 into Task 5 put a second task in the same band. Built as written the feature still delivers if both sittings finish. Risk is a mid-task stall or a partial edit that drops one concern. Design gate: waive, or split Task 6 (models vs discovery) / Task 5 (dispatcher vs ship POSIX vs adapters) before build.

### F2 — INFO — A few spec verify-by greps are still not in task Verify commands

**Mode:** plan. **Evidence:** AC7 `exit 1` on missing `wit-*` is a spec verify-by line; Task 7 Verify is `validate.py` + `unittest discover` + `if cursor` + `/goal` go-signal + `Host: claude` in **dev only**. AC1's grep of `skills/{dev,scan,rpa}/SKILL.md` for the probe pointer is not in Verify (Do still names all three). AC10 ship PR-body: Task 5 Do requires `strip_frontmatter.py <in> <out>` but Verify greps `ensure_logdir.py` in `skills/ship/SKILL.md`, not `strip_frontmatter.py`.

Do text still covers these. Untestable-pre-mortem only.

### F3 — INFO — Leftover host / POSIX / research nits, not silent down-scope

**Mode:** plan. **Evidence:**

- `skills/ship/SKILL.md:367` and `:430` still name Claude/Codex `/goal` and Copilot Autopilot. Task 7 no longer edits ship; Task 5 Do does not retarget those sentences. They fire only if a keep-alive loop is **armed**; Cursor `none` does not arm one.
- `references/workflow.md:13,27,49` mermaid / table still say `/goal` or Autopilot. Task 1/3 edit workflow.md and do not mention the diagram. `AGENTS.md:41-42` persistence bullet is the same three hosts; Task 2 only lists `cursor-tools.md`.
- `skills/research/references/wit-directory.md` and `references/workflow.md` still name `token_report.py` as the ship finalizer. Task 5 retargets `skills/ship/SKILL.md` and `_ledger.py` PENDING (the actual command + ledger boilerplate). Codex map is omitted from Task 5 Files; the SKILL default is `finalize_tokens.py`.
- `date -Iseconds` still leads in `skills/dev/SKILL.md:49`, `skills/ship/SKILL.md:22-23`, `wit-directory.md:128-129`. posix-helpers "must unblock" via existing `now.py`. Task 3's "same recipe block" does not reach those three lines. Spec AC10 and chosen-approach #9 do not require a third helper or a full POSIX rewrite.
- Task 2 Do names `AskQuestion` but not locked fields `id` / `prompt` / `options[{id,label}]` (chosen-approach #5).
- Scan has no feature `progress.md`; Task 7 "stamp at scan/dev/rpa entry" is live detection for plugin-bootstrap, file stamp when dev/rpa seeds `progress.md`.
- Task 4 still says "until task 8 retargets" the keep-alive Grok string; Task 7 keeps that string on purpose so `validate.py`'s keep-alive.md check stays green.

## Silent scope-reduction

No remaining silent down-scope of a locked decision. Round-1 Copilot drop, ship log-dir drop, and "copy this Cursor stamp" are reversed in Task 5/7 Do.

No `stub` / `wire later` / `TODO` / `v1` / `static for now` in `tasks.md`. Spec "no e2e", UTF-16 log YAGNI, and full POSIX rewrite non-goal are explicit.

## Over-build (constitution Simplicity)

No new dependency. No interface-of-one (helpers have two callers: workflow / ship / add-issues). Capability table covering all current hosts is required by ADR-0001, not speculative. `discover_skills.py` unioning all skill roots is spec Design. No third UTF-16 helper (YAGNI honored). `strip_frontmatter.py <in> <out>` (spec) vs research tempfile-stdout-path: spec wins; both avoid PowerShell `>` of the body.

Not over-build: Task 5/6 packing (ceiling/WARNING, F1).

## Pre-mortem (build stalls mid-plan)

1. **Untestable Verify:** AC7 `exit 1` grep and ship:7 `strip_frontmatter.py` grep (F2). Host-detection tells are not named (F3); a weak recipe could still pass `Host: claude` grep.
2. **Hidden file overlap:** Task 2 then Task 5 both own `references/cursor-tools.md` (serialized; Task 5 only adds a ship:6 one-liner). Task 2 then Task 7 both own `scripts/validate.py` (Task 7 must keep Task 2's portability tuple — stated). Wave 2 files remain disjoint. Task 5/7 ship overlap is gone.
3. **Missing Depends on:** Task 7 does not depend on Task 3 (correct: it must not rewrite POSIX or ship). Task 5 depends on 1, 2, and 3. Task 7 depends on 2, 4, 5, 6.
4. **Ceiling stall:** Task 5 or Task 6 drops a concern while Verify for the other concern is green (F1).

## Verdict

Plan mode, round 2 of 2. Matrix: 10/10 spec ACs named and wired; ADR decisions, glossary, pitfalls, constitution rows mapped. Learnings: none applicable.

BLOCKER: none.
WARNING: F1 (Task 5 and Task 6 ceilings).
INFO: F2, F3.

No further checker loop. Design gate decides whether to waive F1 (and the INFO nits) or split those tasks before build.

status: issues-found
