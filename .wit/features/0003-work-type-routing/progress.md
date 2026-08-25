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
- 2026-08-25T18:08:26+00:00 **Decision** investigations return a cited answer with no dossier, gates, or PR
- 2026-08-25T18:09:47+00:00 **Decision** narrow bug fixes may skip the design gate after a repro-focused brainstorm
- 2026-08-25T18:12:15+00:00 **Decision** bug fixes require failing-then-passing same-surface evidence and practical regression coverage
- 2026-08-25T18:13:48+00:00 **Decision** explicit route override = `--kind feature|bug-fix|investigation`

## Tasks (mirrored from tasks.md once planned)

## Decisions / blockers
- Roadmap seed: route `feature | bug-fix | investigation`; preserve the two-gate feature contract, four advertised commands, cross-host adapters, and the single `wit-code-checker` review contract.
- User selected both routes for the first release; additional work types remain out of scope.
- Route selection is automatic by default, with an explicit user override for ambiguous requests.
- Investigation is a read-only exit: no `.wit/` feature dossier, brainstorm, design gate, build, or PR.
- Bug fixes always run a repro-focused brainstorm. A narrow fix with no public behavior or architecture change may skip the design gate when the reason is recorded; all other fixes keep it.
- Every bug-fix result names the root cause and smallest justified fix, shows the original repro fail and then pass on the same surface, and adds an automated regression test when practical.
- `/wit:dev` accepts one extensible `--kind` flag; the default remains intent classification.
