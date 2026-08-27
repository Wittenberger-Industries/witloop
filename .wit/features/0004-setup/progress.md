---
type: Feature Progress
title: "/wit-setup first-run"
description: Fifth advertised command owns first-run; scan is refresh-only; models and ledger toggle live in setup.
feature: 0004-setup
status: build
timestamp: 2026-08-27
---

# Feature: /wit-setup first-run

- **Slug:** 0004-setup
- **Created:** 2026-08-27
- **Phase:** build
- **Gate mode:** interactive
- **Flow:** dev
- **Work type:** feature
- **Worktree:** - (branch in current checkout)
- **Branch:** wit/0004-setup
- **Host:** cursor
- **Plugin root (resolved):** D:/ClaudeCowork/wi-plugin/wi-plugin

## Capabilities (resolved)
- keep_alive=model_judged_goal · tokens=unavailable · ask=AskQuestion · subagent=Task wit-* when listed else inline agents/*.md · shell=Python scripts (POSIX or PowerShell) · skill_invoke=plugin skills + natural-language auto-trigger

## Model routing (resolved)
- resolved 2026-08-27T22:21:21+03:00 from .wit/models.md (preset: custom)
- orchestrator=cursor-grok-4.6-xhigh (informational) · checker=cursor-grok-4.6-xhigh · researcher=cursor-grok-4.6-xhigh · task-runner=cursor-grok-4.6-xhigh · rpa-build=cursor-grok-4.6-xhigh
- cross-provider=none · MoA=none

## Log
- 2026-08-27T22:21:21+03:00 **Created** feature, phase = brainstorm
- 2026-08-27T22:21:21+03:00 brainstorm via superpowers:brainstorming, dialogue
- 2026-08-27T22:21:21+03:00 **Update** base: stacked on wit/0003-blast-radius-proof (PR #94 unmerged; 1.16.2 follows 1.16.1)
- 2026-08-27T22:22:51+03:00 **Update** phase = research
- 2026-08-27T22:22:51+03:00 research engine engaged (wit 1.16.1)
- 2026-08-27T22:22:51+03:00 **Update** applicable learnings: 0003-work-type-routing: WHEN parallel tasks create files the always-loaded skill must plugin-root-point at → DO add a serial wiring task after those files exist; 0003-blast-radius-proof: WHEN adding a second coverage table to the checker → AVOID placing it before the bug-fix matrix

- 2026-08-27T22:32:59+03:00 **Update** phase = plan
- 2026-08-27T22:32:59+03:00 plan via superpowers:writing-plans
- 2026-08-27T22:52:56+03:00 **Update** design gate approved, phase = build
- 2026-08-27T22:52:56+03:00 build engine engaged (wit 1.16.1)
- 2026-08-27T22:52:56+03:00 worktree via superpowers (already on wit/0004-setup; isolate in place)
- 2026-08-27T22:52:56+03:00 tdd via superpowers:test-driven-development
- 2026-08-27T23:02:42+03:00 **Update** task 1 done

## Tasks (mirrored from tasks.md once planned)
- [x] 1. Setup skill plus five-command lockstep
- [ ] 2. Scan is refresh-only
- [ ] 3. Alias and bootstrap copy list
- [ ] 4. Dev/rpa invoke setup; models first-run moves
- [ ] 5. Honor ledger skip

## Decisions / blockers
- Fifth advertised command. Scan stays user-facing as refresh-only.
- Missing `.wit/repo-map.md` → setup first from scan / dev / rpa. add-issues does not auto-run setup.
- Move scan first-run text into setup (not call-through).
- Models first-run and `ledger: on | skip` live in setup; toggle in `.wit/models.md`.
- `--auto`: simple preset + ledger on. No worktree / keep-alive / MoA questions.
- Version 1.16.2. New PR, not #94. ADR-0004 for the public command.
