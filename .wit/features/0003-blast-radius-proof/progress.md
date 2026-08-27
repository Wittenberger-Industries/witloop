---
type: Feature Progress
title: Ship verification honesty
description: Require a proven or unproven safety fact at ship, and never silent-PASS an unmeasured check.
feature: 0003-blast-radius-proof
status: build
timestamp: 2026-08-27
---

# Feature: Ship verification honesty

- **Slug:** 0003-blast-radius-proof
- **Created:** 2026-08-27
- **Phase:** build
- **Gate mode:** interactive
- **Flow:** dev
- **Work type:** feature
- **Worktree:** D:/ClaudeCowork/wi-plugin/wi-plugin-wit-0003-blast-radius-proof
- **Branch:** wit/0003-blast-radius-proof
- **Host:** cursor
- **Plugin root (resolved):** D:/ClaudeCowork/wi-plugin/wi-plugin-wit-0003-blast-radius-proof

## Capabilities (resolved)
- keep_alive=model_judged_goal · tokens=unavailable · ask=AskQuestion · subagent=Task wit-* when listed else inline agents/*.md · shell=Python scripts (POSIX or PowerShell) · skill_invoke=plugin skills + natural-language auto-trigger

## Model routing (resolved)
- resolved 2026-08-27T20:25:05+03:00 from .wit/models.md (preset: custom)
- orchestrator=cursor-grok-4.6-xhigh (informational) · checker=cursor-grok-4.6-xhigh · researcher=cursor-grok-4.6-xhigh · task-runner=cursor-grok-4.6-xhigh · rpa-build=cursor-grok-4.6-xhigh
- cross-provider=none · MoA=none

## Log
- 2026-08-27T20:25:05+03:00 **Created** feature, phase = brainstorm
- 2026-08-27T20:25:05+03:00 **Update** roadmap row 4 `blast-radius-proof` in-progress; scan refreshed 2026-08-27 (manifests + validate.py since last stamp; commands unchanged)
- 2026-08-27T20:25:05+03:00 brainstorm via superpowers:brainstorming, dialogue
- 2026-08-27T20:31:53+03:00 **Update** phase = research (research engine engaged (wit 1.16.0))
- 2026-08-27T20:31:53+03:00 **Update** applicable learnings: 0003-work-type-routing: WHEN parallel tasks create files the always-loaded skill must plugin-root-point at → DO add a serial wiring task after those files exist
- 2026-08-27T20:31:53+03:00 **Update** phase = plan
- 2026-08-27T20:31:53+03:00 plan via superpowers:writing-plans
- 2026-08-27T21:03:10+03:00 **Update** design gate opened
- 2026-08-27T21:03:10+03:00 **Update** design gate approved, phase = build
- 2026-08-27T21:12:44+03:00 **Update** build engine engaged (wit 1.16.0)
- 2026-08-27T21:12:44+03:00 worktree via superpowers
- 2026-08-27T21:12:44+03:00 tdd via superpowers:test-driven-development
- 2026-08-27T21:12:44+03:00 waves via superpowers:dispatching-parallel-agents + subagent-driven-development
- 2026-08-27T21:18:59+03:00 **Update** task 1 done (parent takeover after user-backgrounded runner)

## Tasks (mirrored from tasks.md once planned)
- [x] 1. Checker result-mode rows
- [ ] 2. Ship template, gate honesty, close-out box
- [ ] 3. RPA gate pointer
- [x] 4. Lockstep 1.16.1

## Decisions / blockers
- Seed: combined roadmap row 4 (pstack blast-radius + D3 unknown-never-PASS). Version target 1.16.x.
- Verdict bands: proven, unproven, or n/a (docs-only). No new WAIVED band. User-accepted red CI stays as today (`progress.md` only).
- PR must show one safety fact (this-session command or unproven) and mark any named AC/gate check that was not run as unproven, never omit it. Suite green does not replace the safety fact.
- Enforcement: ship writes those rows into `PR.md`; checker result-mode BLOCKER if a row is missing or is a writeup with no command/`unproven`/`n/a`. Tests cover both.
