---
type: Learning
title: Work-type routing (learnings)
description: WHEN parallel tasks create files the always-loaded skill must plugin-root-point at → DO add a serial wiring task after those files exist
feature: 0003-work-type-routing
timestamp: 2026-08-25
tags: [work-type, validate, parallel-waves]
---

# Work-type routing (learnings)

## What didn't work
Wave 2 created `investigation.md` and `bug-fix.md` in parallel, so neither task could edit `skills/dev/SKILL.md`. Task 1 also forbade `${CLAUDE_PLUGIN_ROOT}` pointers at files that did not exist yet (`validate.py` check 3). The always-loaded prelude therefore could not load the routes until a later serial task wired them.

## Non-obvious decisions
Work type is a semantic orchestrator judgment, not a keyword script. Investigation must exit before scan writes. Narrow-fix bypass is fail-closed and is not `--auto`.

## Gotchas / patterns to reuse
- WHEN two parallel tasks create files the always-loaded skill must `${CLAUDE_PLUGIN_ROOT}`-point at → DO keep those pointers out of the parallel wave and add a serial wiring task after the files exist → BECAUSE `validate.py` fails on missing refs and file overlap would serialize the wave anyway
- WHEN adding a design-gate skip → DO stamp `design gate opened` first, then a distinct bypass phrase, and extend every timing parser's allow-list in the same change → BECAUSE span1 and span2 key on those exact phrases
