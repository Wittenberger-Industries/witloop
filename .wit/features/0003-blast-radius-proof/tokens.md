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

**Subagents (exact): <sum>.**
**Σ compute: <dur> across <n> dispatches.**
**Autonomous wall-clock (excl. manual steps): <dur>.**

## Orchestrator

_PENDING: ship replaces this section during the dossier tidy (BEFORE the dossier commit and the PR) by running `python ${PLUGIN_ROOT}/skills/ship/scripts/finalize_tokens.py --write <this file>`. That CLI reads Host: from progress.md and routes to the host parser (Claude: token_report.py; Grok: grok_token_report.py; Cursor/Copilot/Codex/unstamped/unknown: the honest unavailable sentinel plus Duration from progress.md spans). If the parse fails or the host exposes no local usage field it writes `Orchestrator: unavailable for this run`; never a substitute, estimate, invented figure, or dashboard scrape. A tokens.md still reading PENDING after ship is a defect._
