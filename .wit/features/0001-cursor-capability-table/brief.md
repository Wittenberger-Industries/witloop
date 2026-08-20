---
type: Brief
title: First-class Cursor host via a capability table
description: What the user wants from this feature, in plain terms (the WHAT, not the HOW).
feature: 0001-cursor-capability-table
timestamp: 2026-08-19
---

# Brief: First-class Cursor host via a capability table

## What the user wants
Witloop already runs a full `/wit:dev` loop inside Cursor, but Cursor is not a documented host. A Cursor run must stamp **Host: cursor** and a resolved plugin root once, then every later phase reads that stamp instead of guessing. Skills branch on a **capability table** (plugin_root, subagent, keep_alive, tokens, ask, shell, skill_invoke), not on product-name if-trees.

Cursor is the first fully filled row and the adapter we optimize in this PR:

- Plugin root resolves even when `CLAUDE_PLUGIN_ROOT` is empty (Cursor cache or walk-up to this source repo).
- Keep-alive is **none**: this chat persists; never print Claude `/goal` or Copilot Autopilot flags; Cursor Autopilot is not wit persistence. Optional `/loop` may be documented for `Phase=done`.
- Tokens: orchestrator is `unavailable` (no local usage field). Duration totals still fill from `progress.md`. Ship must not run Claude's `token_report.py` against a foreign transcript. Dashboard scrape is forbidden.
- Ask maps to Cursor `AskQuestion`.
- Subagent: named `Task` types `wit-*` when the session list has them; otherwise inline `agents/*.md`. Missing named types is not a hard failure.
- Skill presence searches Cursor's plugin cache before stamping `(skill absent)`.
- Model routing has a `cursor` column; this repo already resolves every role to `cursor-grok-4.6-xhigh`.
- Shell: scripts are Python. Tiny helpers ride along so Cursor-on-Windows (PowerShell) is unblocked (`mkdir -p` / awk-class side effects).

`references/cursor-tools.md` is the Cursor adapter. New Cursor-specific prose does not land in the five always-loaded SKILL bodies; those files cite the capability table.

Concrete example: a Cursor `/wit:dev` (or natural-language equivalent) on this Windows machine stamps `Host: cursor`, prints the none keep-alive block, and at ship writes `Orchestrator: unavailable for this run` while still filling Duration. `python scripts/validate.py` and `pytest tests/` stay green.

## Acceptance (in the user's words)
- A Cursor run stamps `Host: cursor` and a resolved plugin root in `progress.md`; later phases read that block.
- `references/cursor-tools.md` exists and is listed from `AGENTS.md`, README, and `validate.py`'s portability file check.
- Ship finalize on Cursor writes the unavailable Orchestrator sentinel (or an explicitly labeled dashboard paste) and does not invoke `token_report.py`; Duration still fills; all-unavailable ledgers still pass `check_tokens.py`.
- Keep-alive print on Cursor is the none (or documented `/loop`) template, never Claude `/goal` and never Copilot Autopilot.
- `AskUserQuestion` in scan/brainstorm/research/plugin-bootstrap maps to Cursor `AskQuestion`.
- Skill presence checks search Cursor's plugin cache before `(skill absent)`.
- Dispatch uses named `Task` types when present, otherwise inlines charters.
- Skills that need a capability cite the capability table, not a new `if cursor` / `if grok` fork in always-loaded SKILL bodies.
- Tests cover: validate.py requires `cursor-tools.md`; token finalizer given `Host: cursor` writes unavailable and does not bind a foreign `~/.claude` session; keep-alive template selection for the Cursor capability.
- `.wit/models.md` platform map documents a `cursor` column; a Cursor dispatch reads the resolved concrete model id.
- POSIX-to-Python helpers that unblock Cursor-on-Windows ship in this PR.

## Scope & non-goals
- In: capability table; host probe; `cursor-tools.md` as first consumer; token dispatcher; keep-alive as a capability keyed by `none` for Cursor; skill discovery union including `~/.cursor/plugins/cache/**/skills`; models `cursor` column; inline-dispatch contract; tiny Python helpers for Windows shell side effects; tests + README/AGENTS/validate wiring.
- Out: scraping Usage dashboard / Admin API into the ledger; changing the phase machine, artifact formats, or agent charter contracts; Cursor-specific procedure in always-loaded SKILL bodies beyond a pointer; Gemini CLI / OpenCode / Factory Droid hosts; treating Cursor Autopilot as keep-alive; moving worktrees to `.wit/worktrees/` (separate issue).

## Constraints
- One PR. Cursor-first: the Cursor row is complete and optimal; other hosts become table rows, not new forks.
- This is the Witloop source repo, not a clone.
- Every wit dispatch in this run uses `cursor-grok-4.6-xhigh`.
- Ledger rule: exact or `unavailable`, never a guessed scrape.
- No em-dashes. Three-manifest version bump together. `validate.py` + unit suite green. File tails intact after markdown edits.
- Superpowers supplies dialogue/plan/build method; wit artifacts (`brief.md`, spec, tasks, PR) always win.

## Approach preferences (optional, non-binding)
- Capability table in `references/workflow.md` (or a small sibling), with `cursor-tools.md` filling the Cursor row.
- One `finalize_tokens.py --write` (or ship:6 dispatch) that picks the parser from `Host:`.
- Keep-alive.md becomes a table keyed by capability (`predicate_goal` / `model_judged_goal` / `relaunch` / `none`).

## Open questions for research
- Exact file for the capability table (workflow.md vs a sibling) if size would break the lean-file rule.
- Which POSIX snippets actually fail on PowerShell in this repo and therefore must become helpers in this PR vs stay documented.
