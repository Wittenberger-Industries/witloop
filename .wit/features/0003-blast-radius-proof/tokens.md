---
type: Token Ledger
title: "Token ledger: 0003-blast-radius-proof"
description: Exact per-subagent token usage + the orchestrator total (finalized by ship pre-PR).
feature: 0003-blast-radius-proof
timestamp: 2026-08-27
---

# Token ledger: 0003-blast-radius-proof

Append a row the moment each subagent's completion notification arrives; the figure
exists only there and is NOT retrievable later. Duration comes from the notification's
elapsed time or the orchestrator's own dispatch/arrival stamps (OS clock); write
`unavailable` when unknown, never an estimate. ship finalizes the Orchestrator section.

| Phase | Source | Tokens | Duration | Basis |
|-------|--------|--------|----------|-------|
| orchestrator | main thread, all phases | (see Orchestrator section) | n/a (see below) | finalized by finalize_tokens.py; unavailable if the host has no local usage field or the parse fails: never substitute or estimate |
| research | researcher: insertion-seams | unavailable | unavailable | Host tokens cell unavailable; no notification counts |
| research | researcher: contract-tests | unavailable | unavailable | Host tokens cell unavailable; no notification counts |
| plan | checker: plan-mode round 1 | unavailable | unavailable | Host tokens cell unavailable; no notification counts |
| plan | checker: plan-mode round 2 | unavailable | unavailable | Host tokens cell unavailable; no notification counts |
| build | task-runner: task 4 | unavailable | unavailable | Host tokens cell unavailable; no notification counts |
| build | task-runner: task 1 (interrupted; parent takeover) | unavailable | unavailable | Host tokens cell unavailable; user-backgrounded then interrupted |
| build | parent: task 1 | unavailable | unavailable | Host tokens cell unavailable; implemented in orchestrator session |
| build | parent: task 2 | unavailable | unavailable | Host tokens cell unavailable; implemented in orchestrator session |
| build | parent: task 3 | unavailable | unavailable | Host tokens cell unavailable; implemented in orchestrator session |
| ship | checker: result-mode | unavailable | unavailable | Host tokens cell unavailable; no notification counts |

**Subagents (exact): 0.**
**Σ compute: unavailable across 0 dispatches.**
**Autonomous wall-clock (excl. manual steps): 31m17s.**

## Orchestrator

Orchestrator: unavailable for this run

- host: cursor
- NOTE: this host exposes no local orchestrator usage field; Duration totals come from progress.md Log stamps. Never a dashboard scrape.
