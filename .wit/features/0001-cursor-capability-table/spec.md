---
type: Spec
title: First-class Cursor host via a capability table
description: Stamp host capabilities once, fill the Cursor row, and stop guessing in later phases.
feature: 0001-cursor-capability-table
timestamp: 2026-08-19
---

# Spec: First-class Cursor host via a capability table

## Summary
Cursor becomes a documented wit host. A capability x host table is the source of host behavior; Cursor is the first fully filled column. A Cursor `/wit:dev` (or natural-language equivalent) stamps `Host: cursor` and a resolved plugin root, prints keep-alive `none`, and at ship writes an unavailable orchestrator without invoking `token_report.py`. See ADR-0001.

## Goals
- Skills branch on stamped capabilities, not product-name if-trees in always-loaded SKILL bodies.
- Cursor is optimal: probe, `cursor-tools.md`, keep-alive none, tokens unavailable, `AskQuestion`, plugin-cache skill discovery, named-or-inline Task, `cursor` model column, Python helpers on PowerShell.
- Existing Claude / Codex / Copilot / Grok paths stay green.

## Non-goals
- Scraping Usage dashboard / Admin API into the ledger.
- Changing the phase machine, artifact formats, or agent charter contracts.
- Cursor-specific procedure in always-loaded SKILL bodies beyond a pointer.
- Gemini CLI / OpenCode / Factory Droid hosts.
- Treating Cursor Autopilot as wit keep-alive.
- Moving worktrees to `.wit/worktrees/`.
- A full POSIX-to-Python rewrite.

## Acceptance criteria  (each must be testable)
1. A Cursor run of `/wit:dev` stamps `Host: cursor` and `Plugin root (resolved):` plus `## Capabilities (resolved)` in `progress.md`; later phases read that block.  →  verified by: `progress.md` template in wit-directory.md contains those fields; grep of `skills/{dev,scan,rpa}/SKILL.md` for the probe pointer; this feature's own `progress.md` already shows `Host: cursor`.
2. `references/cursor-tools.md` exists and is listed from `AGENTS.md`, README, and `validate.py`'s portability file check (alongside the existing three tool maps). `references/capabilities.md` exists and is in that check.  →  verified by: `python scripts/validate.py` and a unittest that the portability tuple includes both files.
3. `finalize_tokens.py --write` given `Host: cursor` (or no Claude transcript) writes `Orchestrator: unavailable for this run` and does not bind a foreign `~/.claude` session; Duration totals still fill from `progress.md`. An all-unavailable ledger still passes `check_tokens.py`.  →  verified by: `tests/test_finalize_tokens.py` (plant `HOME/.claude`, assert `token_report.py` not invoked; duration filled).
4. Keep-alive print on Cursor is the `none` template, never Claude `/goal` and never Copilot Autopilot flags.  →  verified by: `tests/test_keep_alive.py` selects `none` for Cursor and asserts the block has no `/goal` and no `autopilot`.
5. `AskUserQuestion` in scan/brainstorm/research/plugin-bootstrap maps to Cursor `AskQuestion` via `cursor-tools.md`.  →  verified by: grep `AskQuestion` in `references/cursor-tools.md`; SKILL bodies cite the `ask` capability rather than a new Cursor fork.
6. Skill presence checks search Cursor's plugin cache before stamping `(skill absent)`.  →  verified by: unittest of `discover_skills.py` (or the documented search-order helper) that a fake `~/.cursor/plugins/cache/.../skills` dir counts as present.
7. Dispatch uses named `Task` types when they appear in the session list, otherwise inlines `agents/*.md`. Missing named types is not a hard failure.  →  verified by: `cursor-tools.md` + `worktrees-and-subagents.md` named-vs-inline contract; grep that SKILL bodies do not `exit 1` on missing `wit-*` types.
8. Skills that need a capability cite `references/capabilities.md` (**the capability table**), not a new `if cursor` / `if grok` fork in always-loaded SKILL bodies.  →  verified by: `python scripts/validate.py` after retargeting the `autopilot`/`grok` body-string checks; grep `skills/{dev,research,plan,build,ship}/SKILL.md` for `if cursor` is empty.
9. `.wit/models.md` / `references/models.md` platform map documents a `cursor` column; a Cursor dispatch reads the resolved concrete model id.  →  verified by: `tests/test_models_config.py` cursor-host mapping (extend `PlatformMapTest`).
10. `ensure_logdir.py` and `strip_frontmatter.py` exist beside `now.py` and are the instructed side-effect path for log-dir and PR-body strip.  →  verified by: unit tests for both CLIs; grep that workflow.md / ship PR-body recipe name the scripts.

## Design
ADR-0001. New `references/capabilities.md` is the matrix. `references/cursor-tools.md` fills the Cursor column (tool map, keep-alive none, tokens unavailable, marketplace vs cache, named-vs-inline). `workflow.md` adds **the capability table** named rule and points log-dir at `ensure_logdir.py`. `keep-alive.md` becomes four capability-keyed templates. `skills/ship/scripts/finalize_tokens.py` is the only ship:6 token CLI; it dispatches to existing `token_report.py` / `grok_token_report.py` or the unavailable+duration path. `skills/research/scripts/discover_skills.py` (or equivalent stdlib helper) unions known skill roots. `references/models.md` adds a `cursor` column. Plugin-bootstrap offers Cursor marketplace / cache, not Claude `/plugin`, when `Host: cursor`. Three manifests bump to **1.14.0**.

Host probe writes into `progress.md` (wit-directory template):

```
- **Host:** <slug>
- **Plugin root (resolved):** <path>
## Capabilities (resolved)
- keep_alive=<cell> · tokens=<cell> · ask=<cell> · subagent=<cell> · shell=<cell> · skill_invoke=<cell>
```

Plugin-root order: env (valid wit root) → walk-up from cwd → host cache.

## Interfaces & data changes
- **APIs / signatures:** `python skills/ship/scripts/finalize_tokens.py --write <tokens.md> [--progress <progress.md>]`; `ensure_logdir.py <dir>` (feature `.logs/` or `.wit/issues`); `strip_frontmatter.py <in.md> <out.md>` writes UTF-8 and must not be used with shell `>`; `discover_skills.py` search-order helper.
- **Data / schema:** `progress.md` gains Host / Plugin root / Capabilities (resolved). Additive. Reversible (ignore unknown headings).
- **Config / env:** still `CLAUDE_PLUGIN_ROOT` when it is a wit root; empty on Cursor is expected.
- **Dependencies:** none added (stdlib only).

## Test plan
- **Level rule:** unit tests for scripts and markdown contract greps; `validate.py` as the plugin-structure gate; no e2e harness in this PR.
- **Unit:** finalize_tokens Cursor path; keep-alive `none` selection; discover_skills cache hit; models cursor column; ensure_logdir; strip_frontmatter; validate.py portability list.
- **Integration / e2e:** none (a real Cursor `/wit:dev` after merge is the quality-sensitive follow-up, not a gate in this PR).
- **Edge cases:** planted `HOME/.claude` must not bind; unstamped Host → unavailable; all-unavailable ledger passes `check_tokens.py`; PowerShell `mkdir -p` not required for log dir.

## Rollout & back-out
- Minor bump 1.13.4 → 1.14.0 (behavior + artifacts). Revert the PR. No data migration. Claude hosts that forget to stamp `Host:` get unavailable tokens until they stamp `claude`.

## Open questions
- None blocking the gate. Codex/Copilot `ask` cell labels are copied from their existing tool maps, not invented. Remaining PowerShell `>` UTF-16 on redirected logs is a pitfall, not a third helper.

## Citations
[1] [Issue #89](https://github.com/Wittenberger-Industries/witloop/issues/89)
[2] ADR-0001
[3] `docs/plans/2026-07-19-learnings-lifecycle-dryrun.md`
