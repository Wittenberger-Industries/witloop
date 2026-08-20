---
type: Learning
title: First-class Cursor host via a capability table (learnings)
description: WHEN calling ensure_logdir.py → AVOID the feature folder (target .logs)
feature: 0001-cursor-capability-table
timestamp: 2026-08-19
tags: [cursor, powershell, posix, capability-table]
---

# First-class Cursor host via a capability table (learnings)

## What didn't work
Calling `ensure_logdir.py` on `.wit/features/<slug>/` wrote a `*` gitignore that hid the whole dossier from `git status`. The helper is correct; the argument was the feature folder instead of `.logs`.

PowerShell `>` on a Python script writes UTF-16 LE. Later UTF-8 readers (`check_tokens.py`, `gh pr create --body-file`) then see a BOM or garbled body. The two-arg `strip_frontmatter.py <in> <out>` path exists so ship never needs that redirect.

## Non-obvious decisions
Host probe order is env (if a wit root) then walk-up from cwd then marketplace cache. Cache-first would bind a stale Cursor marketplace copy when the session is opened on this source checkout.

## Gotchas / patterns to reuse
- WHEN calling `ensure_logdir.py` → AVOID the feature folder as `<dir>` → BECAUSE it writes `*` into that folder's `.gitignore` and the dossier vanishes from git
- WHEN capturing a command on PowerShell → DO write the log from Python (or `strip_frontmatter.py` two-arg) → BECAUSE `>` is UTF-16 LE and wit ledgers/PR bodies are UTF-8
- WHEN adding a capability-table pointer to a hotspot (`workflow.md`, `wit-directory.md`) → DO retarget leftover host-named ship commands in the same hunk → BECAUSE a file loaded alone still decides if it names `token_report.py` / `/goal` as the mechanism
