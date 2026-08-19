---
type: Research Note
title: Load-bearing unknowns
description: Dispatch plan for 0001-cursor-capability-table research.
feature: 0001-cursor-capability-table
timestamp: 2026-08-19
---

# Questions

1. `[repo-question]` Where does the capability table live, and how do always-loaded SKILL bodies cite capabilities instead of host if-trees? (table-placement)
2. `[repo-question]` How does ship:6 pick token parsers today, and what is the smallest dispatcher that given `Host: cursor` writes unavailable, never runs `token_report.py`, and still fills Duration from `progress.md`? (token-dispatcher)
3. `[repo-question]` How do keep-alive, skill discovery, ask, subagent dispatch, and models currently branch on host names, and how does the Cursor row fill those capabilities? (cursor-adapter)
4. `[repo-question]` Which POSIX snippets in this repo fail on PowerShell, and which tiny Python helpers (the `now.py` pattern) must ride along to unblock Cursor-on-Windows? (posix-helpers)
