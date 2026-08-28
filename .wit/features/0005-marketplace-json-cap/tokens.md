---
type: Token Ledger
title: "Token ledger: 0005-marketplace-json-cap"
description: Exact per-subagent token usage + the orchestrator total (finalized by ship pre-PR).
feature: 0005-marketplace-json-cap
timestamp: 2026-08-28
---

# Token ledger: 0005-marketplace-json-cap

Append a row the moment each subagent's completion notification arrives; the figure
exists only there and is NOT retrievable later. Duration comes from the notification's
elapsed time or the orchestrator's own dispatch/arrival stamps (OS clock); write
`unavailable` when unknown, never an estimate. ship finalizes the Orchestrator section.

| Phase | Source | Tokens | Duration | Basis |
|-------|--------|--------|----------|-------|
| research | researcher: desc-cap-check | unavailable | unavailable | exact (completion notification) |
| plan | checker: plan mode | unavailable | unavailable | exact (completion notification) |
| build W1 | task-runner: task 1 | unavailable | unavailable | exact (completion notification) |
| ship | checker: result mode | unavailable | unavailable | exact (completion notification) |
| orchestrator | main thread, all phases | (see Orchestrator section) | n/a (see below) | finalized by finalize_tokens.py; unavailable if the host has no local usage field or the parse fails: never substitute or estimate |

**Subagents (exact): 0.**
**Σ compute: unavailable across 0 dispatches.**
**Autonomous wall-clock (excl. manual steps): 15m48s.**

## Orchestrator

Orchestrator: unavailable for this run

- host: cursor
- NOTE: this host exposes no local orchestrator usage field; Duration totals come from progress.md Log stamps. Never a dashboard scrape.
