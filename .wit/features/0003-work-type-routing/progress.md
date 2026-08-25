---
type: Feature Progress
title: Work-type routing for bug fixes and investigations
description: Route bug-fix and read-only investigation requests through purpose-built Witloop paths.
feature: 0003-work-type-routing
status: brainstorm
timestamp: 2026-08-25
---

# Feature: Work-type routing for bug fixes and investigations

- **Slug:** 0003-work-type-routing
- **Created:** 2026-08-25
- **Phase:** brainstorm
- **Gate mode:** interactive
- **Flow:** dev
- **Worktree:** -
- **Branch:** -
- **Host:** cursor
- **Plugin root (resolved):** /workspace

## Capabilities (resolved)
- keep_alive=model_judged_goal · tokens=unavailable · ask=AskQuestion · subagent=Task wit-* when listed else inline agents/*.md · shell=Python scripts (POSIX or PowerShell) · skill_invoke=plugin skills + natural-language auto-trigger

## Model routing (resolved)
- resolved 2026-08-25T18:00:59+00:00 from .wit/models.md (preset: custom)
- orchestrator=cursor-grok-4.6-xhigh (informational) · checker=cursor-grok-4.6-xhigh · researcher=cursor-grok-4.6-xhigh · task-runner=cursor-grok-4.6-xhigh · rpa-build=cursor-grok-4.6-xhigh
- cross-provider=none · MoA=none

## Log
- 2026-08-25T18:00:59+00:00 **Created** feature from roadmap row 1, phase = brainstorm
- 2026-08-25T18:00:59+00:00 **Update** brainstorm via superpowers:brainstorming, dialogue
- 2026-08-25T18:00:59+00:00 **Decision** roadmap slug = work-type-routing; no feature dependencies
- 2026-08-25T18:06:05+00:00 **Decision** scope includes both bug-fix and read-only investigation routes
- 2026-08-25T18:06:54+00:00 **Decision** routes auto-detect from intent and accept an explicit override

## Tasks (mirrored from tasks.md once planned)

## Decisions / blockers
- Roadmap seed: route `feature | bug-fix | investigation`; preserve the two-gate feature contract, four advertised commands, cross-host adapters, and the single `wit-code-checker` review contract.
- User selected both routes for the first release; additional work types remain out of scope.
- Route selection is automatic by default, with an explicit user override for ambiguous requests.
