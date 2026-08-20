---
type: Feature Progress
title: Cursor native /goal keep-alive
description: Flip Cursor keep_alive to model_judged_goal and bump 1.14.1.
feature: 0002-cursor-goal
status: done
timestamp: 2026-08-20
---

# Feature: Cursor native /goal keep-alive

- **Slug:** 0002-cursor-goal
- **Created:** 2026-08-20
- **Phase:** done
- **Gate mode:** interactive
- **Flow:** dev
- **Worktree:** D:\ClaudeCowork\wi-plugin\wi-plugin-wit-0002-cursor-goal
- **Branch:** wit/0002-cursor-goal
- **Host:** cursor
- **Plugin root (resolved):** D:\ClaudeCowork\wi-plugin\wi-plugin-wit-0002-cursor-goal

## Capabilities (resolved)
- keep_alive=model_judged_goal · tokens=unavailable · ask=AskQuestion

## Model routing (resolved)
- resolved 2026-08-20T14:37:50+03:00 from .wit/models.md (preset: custom)
- orchestrator=cursor-grok-4.6-xhigh (informational) · checker=cursor-grok-4.6-xhigh · researcher=cursor-grok-4.6-xhigh · task-runner=cursor-grok-4.6-xhigh

## Log
- 2026-08-20T14:37:50+03:00 **Created** feature on origin/master after 0001 shipped as 1.14.0 (#90)
- 2026-08-20T14:37:50+03:00 **Decision** Cursor keep_alive = model_judged_goal; CreateGoal/UpdateGoal in cursor-tools.md; bump 1.14.1
- 2026-08-20T14:37:50+03:00 **Update** build engine engaged (wit 1.14.0)
- 2026-08-20T14:43:14+03:00 **Update** phase = ship
- 2026-08-20T14:43:14+03:00 **Update** PR https://github.com/Wittenberger-Industries/witloop/pull/91 · remote checks: 1/1 green
- 2026-08-20T14:43:14+03:00 **Update** phase = done

## Tasks (mirrored)
- [x] 1. Invert tests and flip Cursor keep-alive to model_judged_goal
- [x] 2. Adapter, validate.py, glossary, ADR, manifests, host copy

## Decisions / blockers
- 0001 merged as #90 / 1.14.0 with keep-alive none; this feature is the 1.14.1 follow-up, not a rebuild.
