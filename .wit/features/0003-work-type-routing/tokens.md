---
type: Token Ledger
title: "Token ledger: 0003-work-type-routing"
description: Exact per-subagent token usage + the orchestrator total (finalized by ship pre-PR).
feature: 0003-work-type-routing
timestamp: 2026-08-25
---

# Token ledger: 0003-work-type-routing

Append a row the moment each subagent's completion notification arrives; the figure
exists only there and is NOT retrievable later. Duration comes from the notification's
elapsed time or the orchestrator's own dispatch/arrival stamps (OS clock); write
`unavailable` when unknown, never an estimate. ship finalizes the Orchestrator section.

| Phase | Source | Tokens | Duration | Basis |
|-------|--------|--------|----------|-------|
| research | Research classification seam | unavailable | unavailable | Cursor completion exposed no usage or elapsed time |
| research | Research investigation route | unavailable | unavailable | Cursor completion exposed no usage or elapsed time |
| research | Research bug-fix route | unavailable | unavailable | Cursor completion exposed no usage or elapsed time |
| plan check R1 | Check work-type plan | unavailable | unavailable | Cursor completion exposed no usage or elapsed time |
| plan check R2 | Recheck work-type plan | unavailable | unavailable | Cursor completion exposed no usage or elapsed time |
| build | Task 1 work-type routing | unavailable | unavailable | Cursor completion exposed no usage or elapsed time |
| build | Task 2 investigation exit | unavailable | unavailable | Cursor completion exposed no usage or elapsed time |
| build | Task 3 bug-fix overlay | unavailable | unavailable | Cursor completion exposed no usage or elapsed time |
| build | Task 5 timing bypass stamp | unavailable | unavailable | Cursor completion exposed no usage or elapsed time |
| build | Task 4 bug-fix checker | unavailable | unavailable | Cursor completion exposed no usage or elapsed time |
| build | Task 8 route pointers | unavailable | unavailable | Cursor completion exposed no usage or elapsed time |
| build | Task 6 work-type docs | unavailable | unavailable | Cursor completion exposed no usage or elapsed time |
| build | Task 7 release 1.15.0 | unavailable | unavailable | Cursor completion exposed no usage or elapsed time |
| orchestrator | main thread, all phases | (see Orchestrator section) | n/a (see below) | finalized by finalize_tokens.py; unavailable if the host has no local usage field or the parse fails: never substitute or estimate |

**Subagents (exact): 0.**
**Σ compute: unavailable across 0 dispatches.**
**Autonomous wall-clock (excl. manual steps): 1h09m39s.**

## Orchestrator

Orchestrator: unavailable for this run

- host: cursor
- NOTE: this host exposes no local orchestrator usage field; Duration totals come from progress.md Log stamps. Never a dashboard scrape.
