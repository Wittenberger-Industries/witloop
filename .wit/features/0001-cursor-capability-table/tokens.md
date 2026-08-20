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
| ship | checker: result-mode round 1 | unavailable | unavailable | exact (Cursor: no local usage field) |
| ship | checker: result-mode round 2 | unavailable | unavailable | exact (Cursor: no local usage field) |
| orchestrator | main thread, all phases | (see Orchestrator section) | n/a (see below) | finalized by finalize_tokens.py; unavailable if the host has no local usage field or the parse fails: never substitute or estimate |

**Subagents (exact): 0.**
**Σ compute: unavailable across 0 dispatches.**
**Autonomous wall-clock (excl. manual steps): 1h33m42s.**

## Orchestrator

Orchestrator: unavailable for this run

- host: cursor
- NOTE: this host exposes no local orchestrator usage field; Duration totals come from progress.md Log stamps. Never a dashboard scrape.
