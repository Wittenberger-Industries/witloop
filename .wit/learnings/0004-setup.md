---
type: Learning
title: /wit-setup first-run (learnings)
description: Advertised copy and models-template heading can skip the ledger ask after a first-run text move.
feature: 0004-setup
timestamp: 2026-08-27
tags: [setup, scan, advertised-commands, ledger]
---

# /wit-setup first-run (learnings)

## What didn't work

Moving scan procedure 1-7 into `skills/setup/SKILL.md` left the README scan table cell, three
manifest descriptions, and `wit-scan`'s alias describing scan as bootstrap. Lockstep tests pin
command names and table order, not that cell body.

## Non-obvious decisions

PR #94 squash-merged while 0004 was stacked on the original 0003 commits. `origin/master...HEAD`
still contained 0003 until a non-interactive `git rebase --onto origin/master <last-0003-sha>`.

## Gotchas / patterns to reuse

- WHEN a new advertised command takes over first-run copy → DO retarget the README command-table
  cell, plugin/marketplace descriptions, and the old command's alias in the same sitting as the
  skill move → BECAUSE lockstep tests pin names and order, not the scan cell body
- WHEN first-run writes `.wit/models.md` from a template that already contains `## Token ledger`
  → DO omit that heading until the ledger question (setup:7) → BECAUSE a present heading skips
  the keep-or-skip ask
- WHEN a stacked branch's base squash-merges → DO rebase `--onto origin/master` from the last
  stacked SHA before opening the next PR → BECAUSE three-dot vs master still lists the pre-squash
  commits
