---
type: Learning
title: Marketplace plugin descriptions under 1024 chars (learnings)
description: WHEN judging a validate.py repro → AVOID treating exit 1 as the named bug
feature: 0005-marketplace-json-cap
timestamp: 2026-08-28
tags: [validate, marketplace, description-cap]
---

# Marketplace plugin descriptions under 1024 chars (learnings)

## What didn't work
`python scripts/validate.py` on the parent checkout exited 1 because untracked `docs/skill-ideas/` files fail OKF. That hid the real signal: zero `plugin description is` errors while the three JSON fields were 1357/1396.

## Non-obvious decisions
validate.py `ROOT` is `__file__`-relative. A temp-tree over-cap fixture cannot point the gate at fake manifests without rewriting ROOT. Live-file `len(desc) <= DESC_CAP` plus a source-anchor for `: plugin description is` is the SKILL-test pattern.

## Gotchas / patterns to reuse
- WHEN judging a validate.py repro → AVOID treating a non-zero exit as the named bug → BECAUSE OKF walks `docs/**` including untracked local files
- WHEN capping JSON plugin descriptions → DO a sibling 7a-json loop, live-file length, and a source-anchor → AVOID importing validate.py or a fixture ROOT
