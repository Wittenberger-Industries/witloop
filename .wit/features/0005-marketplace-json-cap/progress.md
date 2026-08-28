---
type: Feature Progress
title: "Marketplace plugin descriptions under 1024 chars"
description: Cap marketplace.json, plugin.json, and Codex plugin description fields at 1024 characters and ship 1.16.3.
feature: 0005-marketplace-json-cap
status: build
timestamp: 2026-08-28
---

# Feature: Marketplace plugin descriptions under 1024 chars

- **Slug:** 0005-marketplace-json-cap
- **Created:** 2026-08-28
- **Phase:** build
- **Gate mode:** interactive
- **Flow:** dev
- **Work type:** bug-fix
- **Worktree:** D:/ClaudeCowork/wi-plugin/wi-plugin-wit-0005-marketplace-json-cap
- **Branch:** wit/0005-marketplace-json-cap
- **Host:** cursor
- **Plugin root (resolved):** D:/ClaudeCowork/wi-plugin/wi-plugin-wit-0005-marketplace-json-cap

## Capabilities (resolved)
- keep_alive=model_judged_goal · tokens=unavailable · ask=AskQuestion · subagent=Task wit-* when listed else inline agents/*.md · shell=Python scripts (POSIX or PowerShell) · skill_invoke=plugin skills + natural-language auto-trigger

## Model routing (resolved)
- resolved 2026-08-28T10:55:32+03:00 from .wit/models.md (preset: custom · ledger: on)
- orchestrator=cursor-grok-4.6-xhigh (informational) · checker=cursor-grok-4.6-xhigh · researcher=cursor-grok-4.6-xhigh · task-runner=cursor-grok-4.6-xhigh · rpa-build=cursor-grok-4.6-xhigh
- cross-provider=none · MoA=none

## Log
- 2026-08-28T10:55:32+03:00 **Created** feature, phase = brainstorm
- 2026-08-28T10:55:32+03:00 brainstorm via superpowers:brainstorming, dialogue
- 2026-08-28T10:59:01+03:00 **Update** phase = research
- 2026-08-28T10:59:01+03:00 research engine engaged (wit 1.16.2)
- 2026-08-28T10:59:01+03:00 debug via superpowers:systematic-debugging
- 2026-08-28T10:59:01+03:00 **Update** repro failed on python scripts/validate.py
- 2026-08-28T10:59:01+03:00 **Update** applicable learnings: 0001-cursor-capability-table: WHEN calling ensure_logdir.py → AVOID the feature folder (target .logs); 0004-setup: WHEN advertised copy moves → DO retarget README cells, manifests, and the old alias in the same sitting
- 2026-08-28T11:04:34+03:00 **Update** phase = plan
- 2026-08-28T11:04:34+03:00 plan via superpowers:writing-plans
- 2026-08-28T11:14:49+03:00 **Update** design gate opened
- 2026-08-28T11:14:49+03:00 **Update** design gate bypassed (narrow-fix): DESC_CAP 7a-json plus shortened live copy, no public contract or architecture change, phase = build
- 2026-08-28T11:14:49+03:00 build engine engaged (wit 1.16.2)
- 2026-08-28T11:14:49+03:00 worktree via superpowers
- 2026-08-28T11:20:19+03:00 **Update** task 1 done
- 2026-08-28T11:20:19+03:00 **Update** repro passed on python scripts/validate.py

## Gate bypass
- **Status:** narrow-fix
- **Public behavior unchanged:** yes
- **Architecture unchanged:** yes
- **Root cause:** DESC_CAP 7a walks only SKILL.md; the three JSON plugin descriptions have no length check
- **Why skip:** smallest evidence-backed patch; checker PASS; advertised commands unchanged
- **Checker (plan mode):** PASS
- **Surface:** python scripts/validate.py

## Tasks (mirrored from tasks.md once planned)
- [x] 1. Cap JSON plugin descriptions at DESC_CAP

## Decisions / blockers
- Cap surface: marketplace.json wit plugin `description` AND `.claude-plugin/plugin.json` / `.codex-plugin/plugin.json` descriptions (same 1024 cap on each). Not the whole marketplace.json file.
- Approach: 7a-json sibling loop using existing DESC_CAP; live-file length test in test_work_type_release.py; no ADR.
