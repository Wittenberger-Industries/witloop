---
type: Research Note
title: Chosen approach
description: Reconciled HOW for 0001-cursor-capability-table.
feature: 0001-cursor-capability-table
timestamp: 2026-08-19
valid_until: 2026-09-18
---

# Chosen approach

**We will** introduce a capability x host table in `references/capabilities.md`, stamp `Host:` plus resolved capability cells into `progress.md` at scan/dev/rpa entry, and fill Cursor as the first complete adapter (`references/cursor-tools.md`). Skills cite the table and read stamped cells. They do not gain new `if cursor` / `if grok` forks.

Locked from research:

1. Table lives in `references/capabilities.md`, not inside `workflow.md` (lean-file). `workflow.md` adds the named rule **the capability table**.
2. `finalize_tokens.py --write` is the only ship:6 token command. `Host: cursor` writes `Orchestrator: unavailable for this run`, never calls `token_report.py`, still fills Duration from `progress.md`. Unstamped Host fail-safes to unavailable.
3. `keep-alive.md` is keyed by capability (`predicate_goal` / `model_judged_goal` / `relaunch` / `none`). Cursor prints `none`.
4. Plugin-root order (Cursor-first dogfood): env if it is a wit root; walk-up from cwd; then host plugin cache. Source checkout wins over marketplace cache.
5. Ask maps to Cursor `AskQuestion` (`id`, `prompt`, `options[{id,label}]`, optional `allow_multiple`).
6. Subagent: named `Task` `wit-*` when listed, else inline `agents/*.md`.
7. Skill discovery unions session list, Claude registry, `~/.cursor/plugins/cache/**/skills`, Copilot install dir, `~/.agents/skills/`.
8. `references/models.md` gains a `cursor` column. Concrete ids: `cursor-grok-4.6-xhigh`, `composer-2.5-fast`, `inherit`.
9. POSIX helpers this PR: `ensure_logdir.py` and `strip_frontmatter.py` beside `now.py`. No worktree path change. No full POSIX rewrite.
10. `validate.py` lists `cursor-tools.md` and `capabilities.md`. Retarget SKILL-body `autopilot`/`grok` string checks to citation of the capability table / keep-alive file.

ADR-0001 records (1)-(4) as hard-to-reverse.
