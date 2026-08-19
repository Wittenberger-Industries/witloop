---
type: Feature Progress
title: First-class Cursor host via a capability table
description: Make Cursor a first-class wit host by adding a capability table and filling the Cursor row.
feature: 0001-cursor-capability-table
status: ship
timestamp: 2026-08-19
---

# Feature: First-class Cursor host via a capability table

- **Slug:** 0001-cursor-capability-table
- **Created:** 2026-08-19
- **Phase:** ship
- **Gate mode:** interactive
- **Flow:** dev
- **Worktree:** D:/ClaudeCowork/wi-plugin/wi-plugin-wit-0001-cursor-capability-table
- **Branch:** wit/0001-cursor-capability-table
- **Host:** cursor
- **Plugin root (resolved):** D:/ClaudeCowork/wi-plugin/wi-plugin-wit-0001-cursor-capability-table

## Capabilities (resolved)
- keep_alive=none · tokens=unavailable · ask=AskQuestion · subagent=Task wit-* when listed else inline agents/*.md · shell=Python scripts (POSIX or PowerShell) · skill_invoke=plugin skills + natural-language auto-trigger

## Model routing (resolved)
- resolved 2026-08-19T13:01:45+03:00 from .wit/models.md (preset: custom)
- orchestrator=cursor-grok-4.6-xhigh (informational) · checker=cursor-grok-4.6-xhigh · researcher=cursor-grok-4.6-xhigh · task-runner=cursor-grok-4.6-xhigh · rpa-build=cursor-grok-4.6-xhigh
- cross-provider=none · MoA=none

## Log
- 2026-08-19T13:01:45+03:00 **Created** feature, phase = brainstorm
- 2026-08-19T13:01:45+03:00 **Update** brainstorm via superpowers:brainstorming, dialogue
- 2026-08-19T13:01:45+03:00 **Decision** model routing: custom, every role = cursor-grok-4.6-xhigh, cross-provider none
- 2026-08-19T13:04:51+03:00 **Decision** PR shape: one PR, capability table + Cursor as the fully filled first row
- 2026-08-19T13:04:51+03:00 **Decision** POSIX-to-Python helpers ride along to unblock Cursor-on-Windows
- 2026-08-19T13:04:51+03:00 **Update** brief.md written; awaiting user confirm
- 2026-08-19T13:06:18+03:00 **Update** phase = research
- 2026-08-19T13:06:18+03:00 **Update** research engine engaged (wit 1.13.4)
- 2026-08-19T13:06:18+03:00 **Update** applicable learnings: none
- 2026-08-19T13:16:23+03:00 **Update** phase = plan
- 2026-08-19T13:16:23+03:00 **Update** plan via superpowers:writing-plans
- 2026-08-19T13:16:23+03:00 **Decision** approach = ADR-0001 capability table; Cursor first row; finalize_tokens.py; keep-alive none; walk-up before cache
- 2026-08-19T13:36:49+03:00 **Update** design gate opened
- 2026-08-19T13:52:00+03:00 **Update** design gate approved, phase = build
- 2026-08-19T13:52:00+03:00 **Update** build engine engaged (wit 1.13.4)
- 2026-08-19T13:52:00+03:00 **Update** worktree via superpowers
- 2026-08-19T13:52:00+03:00 **Update** task 1 done (Self-Check PASS)
- 2026-08-19T14:11:06+03:00 **Update** wave 2 done: tasks 2, 3, 4, 6 (Self-Check PASS)
- 2026-08-19T14:11:06+03:00 **Update** task 5 done (Self-Check PASS)
- 2026-08-19T14:11:06+03:00 **Update** task 7 done (Self-Check PASS)
- 2026-08-19T14:11:06+03:00 **Update** task 8 done (Self-Check PASS); all tasks ticked
- 2026-08-19T14:33:42+03:00 **Update** phase = ship (ship engine engaged (wit 1.14.0))
- 2026-08-19T14:33:42+03:00 **Update** verification via superpowers:verification-before-completion
- 2026-08-19T14:45:31+03:00 **Update** review via wit-code-checker + superpowers:requesting-code-review[inline]
- 2026-08-19T14:45:31+03:00 **Update** review round 1: no BLOCKER; F1/F2/F5 WARNINGs fixed (finalize_tokens + keep-alive cells in workflow/wit-directory; RPA probe fields)
- 2026-08-19T14:45:31+03:00 **Update** docs-sync: architecture, overview, repo-map for Cursor host + capability table
- 2026-08-19T14:52:50+03:00 **Update** review round 2: CHECK PASSED (F1/F2/F5 closed)
- 2026-08-19T14:52:50+03:00 **Update** learnings captured
- 2026-08-19T14:52:50+03:00 **Update** PR.md written
- 2026-08-19T14:55:11+03:00 **Update** PR opened: https://github.com/Wittenberger-Industries/witloop/pull/90
- 2026-08-19T14:57:11+03:00 **Reflection** validate: test_encode_drops_drive_colon_and_separators failed on Linux CI because Path("D:/...").resolve() is not a Windows drive path - earlier catch: none

## Tasks (mirrored from tasks.md once planned)
- [x] 1. Capability table, probe template, workflow pointer
- [x] 2. cursor-tools.md + bootstrap listings
- [x] 3. POSIX helpers
- [x] 4. Keep-alive keyed by capability
- [x] 5. Token dispatcher
- [x] 6. Skill discovery + plugin-bootstrap + models cursor column
- [x] 7. SKILL body pointers + validate.py retarget
- [x] 8. Manifest bump and host copy

## Decisions / blockers
- Source issue: https://github.com/Wittenberger-Industries/witloop/issues/89
- Cursor-first: optimize the Cursor row and adapter; capability table is the shape so the next host is a row, not a fork
- Session is the Witloop source repo (not a clone)
