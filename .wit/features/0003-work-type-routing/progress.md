---
type: Feature Progress
title: Work-type routing for bug fixes and investigations
description: Route bug-fix and read-only investigation requests through purpose-built Witloop paths.
feature: 0003-work-type-routing
status: build
timestamp: 2026-08-25
---

# Feature: Work-type routing for bug fixes and investigations

- **Slug:** 0003-work-type-routing
- **Created:** 2026-08-25
- **Phase:** build
- **Gate mode:** interactive
- **Flow:** dev
- **Worktree:** /workspace
- **Branch:** cursor/pstack-feature-roadmap-e671
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
- 2026-08-25T18:15:21+00:00 **Decision** ambiguous intent defaults to announced `feature` classification with override guidance
- 2026-08-25T18:18:19+00:00 **Decision** classifier deduces all three work types from intent; no constraints beyond roadmap defaults
- 2026-08-25T18:19:33+00:00 **Update** brief.md written and confirmed; glossary updated; awaiting handoff
- 2026-08-25T18:21:15+00:00 **Update** phase = research
- 2026-08-25T18:21:15+00:00 **Update** research engine engaged (wit 1.14.1)
- 2026-08-25T18:21:15+00:00 **Update** applicable learnings: none
- 2026-08-25T18:27:56+00:00 **Decision** approach = ADR-0002 semantic work-type router with read-only investigation and bug-fix phase overlays
- 2026-08-25T18:27:56+00:00 **Update** phase = plan
- 2026-08-25T18:29:58+00:00 **Update** plan via superpowers:writing-plans
- 2026-08-25T18:29:58+00:00 **Update** spec.md, tasks.md, and pitfalls.md written; plan self-review passed
- 2026-08-25T18:37:48+00:00 **Reflection** plan-mode checker found unmapped always-announce, resume, and investigation capture-exception decisions - earlier catch: plan
- 2026-08-25T18:37:48+00:00 **Update** plan checker round 1: 3 BLOCKERs fixed; warning pins folded into tasks
- 2026-08-25T18:41:23+00:00 **Update** plan checker round 2: no BLOCKER; one validate warning fixed in Task 2
- 2026-08-25T18:41:23+00:00 **Update** design gate opened
- 2026-08-25T19:10:32+00:00 **Update** design gate approved, phase = build
- 2026-08-25T19:10:32+00:00 **Update** build engine engaged (wit 1.14.1)
- 2026-08-25T19:10:32+00:00 **Update** worktree via superpowers: using-git-worktrees; Cloud Agent checkout already isolated on PR branch, so no second worktree
- 2026-08-25T19:20:16+00:00 **Update** Task 1 done: work-type routing foundation
- 2026-08-25T19:20:16+00:00 **Update** Task 1 tokens unavailable Duration unavailable
- 2026-08-25T19:22:00+00:00 **Update** Wave 2 dispatched: tasks 2, 3, 5
- 2026-08-25T19:30:45+00:00 **Update** Task 2 done: read-only investigation exit
- 2026-08-25T19:30:45+00:00 **Update** Task 2 tokens unavailable Duration unavailable
- 2026-08-25T19:30:45+00:00 **Update** Task 3 done: reproduce-first bug-fix overlay
- 2026-08-25T19:30:45+00:00 **Update** Task 3 tokens unavailable Duration unavailable
- 2026-08-25T19:30:45+00:00 **Update** Task 5 done: timing parsers accept gate bypass
- 2026-08-25T19:30:45+00:00 **Update** Task 5 tokens unavailable Duration unavailable
- 2026-08-25T19:30:45+00:00 **Reflection** Tasks 2 and 3 omitted SKILL.md pointers so they could run in parallel - earlier catch: plan
- 2026-08-25T19:30:45+00:00 **Update** added Task 8 to wire plugin-root pointers; Wave 3 is tasks 4 and 8
- 2026-08-25T19:35:00+00:00 **Update** Task 4 done: bug-fix checker and ship proof
- 2026-08-25T19:35:00+00:00 **Update** Task 4 tokens unavailable Duration unavailable

## Tasks (mirrored from tasks.md once planned)
- [x] 1. Add the work-type routing foundation
- [x] 2. Add the read-only investigation exit
- [x] 3. Overlay the reproduce-first bug-fix lifecycle
- [x] 4. Enforce bug-fix proof in checker and ship
- [x] 5. Keep timing reports compatible with gate bypass
- [ ] 6. Document work-type routing
- [ ] 7. Update source memory and release 1.15.0
- [ ] 8. Wire on-demand investigation and bug-fix pointers

## Decisions / blockers
- Roadmap seed: route `feature | bug-fix | investigation`; preserve the two-gate feature contract, four advertised commands, cross-host adapters, and the single `wit-code-checker` review contract.
- User selected both routes for the first release; additional work types remain out of scope.
- Route selection is automatic by default, with an explicit user override for ambiguous requests.
- Investigation is a read-only exit: no `.wit/` feature dossier, brainstorm, design gate, build, or PR.
- Bug fixes always run a repro-focused brainstorm. A narrow fix with no public behavior or architecture change may skip the design gate when the reason is recorded; all other fixes keep it.
- Every bug-fix result names the root cause and smallest justified fix, shows the original repro fail and then pass on the same surface, and adds an automated regression test when practical.
- `/wit:dev` accepts one extensible `--kind` flag; the default remains intent classification.
- Ambiguous requests default to `feature`; Witloop announces the classification and the `--kind` override instead of asking or choosing silently.
- Intent deduction covers `feature`, `bug-fix`, and `investigation`. Hard constraints remain five-host compatibility, no fifth command, no required MCP, one checker agent, and unchanged feature behavior.
- Canonical term: **Work type**. The selected work type precedes feature-folder classification.
- Research chose semantic intent deduction over a keyword-only helper. Investigation exits before write-capable setup; bug fixes reuse all existing phases with a fail-closed narrow-fix bypass.
