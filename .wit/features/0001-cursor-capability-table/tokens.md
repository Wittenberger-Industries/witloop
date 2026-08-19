---
type: Token Ledger
title: "Token ledger: 0001-cursor-capability-table"
description: Exact per-subagent token usage + the orchestrator total (finalized by ship pre-PR).
feature: 0001-cursor-capability-table
timestamp: 2026-08-19
---

# Token ledger: 0001-cursor-capability-table

Append a row the moment each subagent's completion notification arrives; the figure
exists only there and is NOT retrievable later. Duration comes from the notification's
elapsed time or the orchestrator's own dispatch/arrival stamps (OS clock); write
`unavailable` when unknown, never an estimate. ship finalizes the Orchestrator section.

| Phase | Source | Tokens | Duration | Basis |
|-------|--------|--------|----------|-------|
| research | researcher: table-placement | unavailable | unavailable | exact (Cursor: no local usage field) |
| research | researcher: token-dispatcher | unavailable | unavailable | exact (Cursor: no local usage field) |
| research | researcher: cursor-adapter | unavailable | unavailable | exact (Cursor: no local usage field) |
| research | researcher: posix-helpers | unavailable | unavailable | exact (Cursor: no local usage field) |
| plan | checker: plan-mode round 1 | unavailable | unavailable | exact (Cursor: no local usage field) |
| plan | checker: plan-mode round 2 | unavailable | unavailable | exact (Cursor: no local usage field) |
| build W1 | task-runner: task 1 | unavailable | unavailable | exact (Cursor: no local usage field) |
| build W2 | task-runner: task 2 | unavailable | unavailable | exact (Cursor: no local usage field) |
| build W2 | task-runner: task 3 | unavailable | unavailable | exact (Cursor: no local usage field) |
| build W2 | task-runner: task 4 | unavailable | unavailable | exact (Cursor: no local usage field) |
| build W2 | task-runner: task 6 | unavailable | unavailable | exact (Cursor: no local usage field) |
| build W3 | task-runner: task 5 | unavailable | unavailable | exact (Cursor: no local usage field) |
| build W4 | task-runner: task 7 | unavailable | unavailable | exact (Cursor: no local usage field) |
| build W5 | task-runner: task 8 | unavailable | unavailable | exact (Cursor: no local usage field) |
| orchestrator | main thread, all phases | (see Orchestrator section) | n/a (see below) | parsed by token_report.py; unavailable if the parse fails: never substitute or estimate |

**Subagents (exact): <sum>.**
**Σ compute: <dur> across <n> dispatches.**
**Autonomous wall-clock (excl. manual steps): <dur>.**

## Orchestrator

_PENDING: ship replaces this section during the dossier tidy (BEFORE the dossier commit and the PR) by running `python ${CLAUDE_PLUGIN_ROOT}/skills/ship/scripts/token_report.py --write <this file>` on Claude Code; on a non-Claude host the platform tool map names the finalizer (Grok Build: `grok_token_report.py --write`, references/grok-tools.md). It parses the session data, fills the duration totals from the ledger rows + progress.md phase spans, and appends the exact per-subagent split. That parsed figure is the only reliable orchestrator measure; if the parse fails it writes `Orchestrator: unavailable for this run`; never a substitute, estimate, or invented figure. A tokens.md still reading PENDING after ship is a defect._
