---
type: ADR
title: Branch on a capability table; Cursor is the first filled row
description: Skills read stamped host capabilities, not product-name if-trees; Cursor is the first complete column.
feature: 0001-cursor-capability-table
status: accepted
timestamp: 2026-08-19
---

# ADR-0001: Branch on a capability table; Cursor is the first filled row

- **Status:** accepted
- **Date:** 2026-08-19
- **Deciders:** wit research (autonomous); design gate approved 2026-08-19
- **Feature:** 0001-cursor-capability-table

## Context
Witloop now has four documented hosts (Claude, Codex, Copilot, Grok) plus a fifth in real use (Cursor) that is not a documented host. Each new host copied a `*-tools.md` and added special cases in keep-alive, ship:6, `models.md`, and `validate.py`. Cursor already completed a `/wit:dev` loop, but ship could still run Claude's `token_report.py` against a leftover transcript, and keep-alive print could emit `/goal` or Autopilot flags that Cursor does not have. Adding Cursor as another named fork would not scale (Gemini/OpenCode later). The constitution names a host capability table as an ADR trigger.

## Decision
We will:

1. Own the capability x host matrix in `references/capabilities.md`. Rows are capabilities (`plugin_root`, `subagent`, `keep_alive`, `tokens`, `ask`, `shell`, `skill_invoke`). Columns are hosts (`claude`, `codex`, `copilot`, `grok`, `cursor`). Adapters fill cells. Always-loaded SKILL bodies cite **the capability table** and then read stamped cells in `progress.md`.
2. Probe the host once at scan/dev/rpa entry. Stamp `Host:`, `Plugin root (resolved):`, and `## Capabilities (resolved)` into `progress.md`. Later phases never re-guess. Plugin-root order: (a) `CLAUDE_PLUGIN_ROOT` if it is a wit root, (b) walk-up from cwd to `skills/` + `.claude-plugin/`, (c) host plugin cache. Cwd-as-wit-root beats marketplace cache so this source repo dogfoods itself.
3. Make `finalize_tokens.py --write` the only ship:6 token command. It picks a parser from `Host:`. Cursor (and any host whose `tokens` cell is `unavailable`) writes `Orchestrator: unavailable for this run` and must not invoke `token_report.py`. Duration totals still fill from `progress.md`. Unstamped Host fail-safes to unavailable.
4. Key `keep-alive.md` by `keep_alive` capability (`predicate_goal` / `model_judged_goal` / `relaunch` / `none`), not by product name. Cursor and Grok share `model_judged_goal` (one printable `/goal` template). Host register/complete tools live in adapters: Grok `update_goal`; Cursor `CreateGoal` then `UpdateGoal`. `none` remains a valid value for a future host; it is not Cursor's. (Amended 2026-08-20 in 0002-cursor-goal after Cursor gained native `/goal`; 1.14.0 had shipped Cursor as `none`.)

Cursor is the first fully filled column and the adapter we optimize in this change (`references/cursor-tools.md`). Other hosts become rows filled from existing adapters, not new if-trees.

## Consequences
- **Positive:** the next host is a table row plus an adapter file. Cursor stops binding Claude transcripts and prints the same model-judged `/goal` family as Grok, with CreateGoal/UpdateGoal named only in the adapter. Source-repo dogfood resolves plugin root to this tree.
- **Negative / costs:** every host must stamp `Host:` (Claude included) or token finalize fail-safes to unavailable. `validate.py` must stop requiring `autopilot`/`grok` inside SKILL bodies. Orchestrators must load `capabilities.md` once when they need a cell.
- **Follow-ups:** Gemini/OpenCode/Factory are later rows. Worktree path under `.wit/worktrees/` stays a separate issue. Remaining POSIX (`>` UTF-16 on PowerShell) is a pitfall, not a third helper this PR.

## Alternatives considered
- **Fifth host fork only** (`cursor-tools.md` plus more string checks): ships Cursor faster, repeats the Grok (#43) pattern. Rejected as the long-term shape.
- **Matrix inside `workflow.md`:** mixes phase contracts with host identity and would break the ~150-line lean-file rule.
- **Skills look up `*-tools.md` by `Host:`:** still a product-name if-tree.
- **Scrape Cursor Usage dashboard into the ledger:** violates the ledger rule (exact or `unavailable`). Rejected.

## Citations
[1] [Issue #89](https://github.com/Wittenberger-Industries/witloop/issues/89): acceptance criteria and Cursor harness review (2026-08-13).
[2] `docs/plans/2026-07-19-learnings-lifecycle-dryrun.md`: Cursor dry-run; inline roles; token_report.py bind.
[3] `docs/specs/2026-07-12-grok-build-platform-design.md`: fourth-host adapter pattern to generalize, not copy.
