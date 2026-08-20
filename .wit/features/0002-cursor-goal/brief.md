---
type: Brief
title: Cursor native /goal keep-alive
description: Cursor keep-alive is model-judged /goal; bump 1.14.1.
feature: 0002-cursor-goal
timestamp: 2026-08-20
---

# Brief: Cursor native /goal keep-alive

## What the user wants
Cursor now has native `/goal` (`CreateGoal` / `UpdateGoal`). After 1.14.0 shipped Cursor as keep-alive `none`, 1.14.1 puts Cursor on `model_judged_goal` with Grok: print the same one-line `/goal`; paste is the go; `cursor-tools.md` names `CreateGoal` and `UpdateGoal`. Version skip of 1.14.0 was the original hope; 1.14.0 already merged as #90, so this is the patch.

## Acceptance (in the user's words)
- Cursor keep-alive print is `/goal`, not none.
- `cursor-tools.md` names `CreateGoal` and `UpdateGoal`.
- Tests select `model_judged_goal` for Cursor and Grok.
- Three manifests **1.14.1**.

## Scope & non-goals
- In: Cursor `keep_alive` cell, keep-alive templates, cursor-tools mechanism, tests, validate.py anchors, glossary/ADR amendment, version bump, host copy.
- Out: rebuilding the capability table; Autopilot; `/loop` as keep-alive; new enum; token scrape.

## Constraints
- Reuse `model_judged_goal`. No fifth host fork. No em-dashes. Manifest lockstep.
