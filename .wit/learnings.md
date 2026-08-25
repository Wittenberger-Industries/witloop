---
type: Learnings Index
title: Learnings index (Witloop)
description: One line + hook per feature; phases read this, then open a detail file only when its hook fits.
timestamp: 2026-08-19
---

# Learnings index

- [First-class Cursor host via a capability table](learnings/0001-cursor-capability-table.md): WHEN calling ensure_logdir.py → AVOID the feature folder (target .logs) · process: checker 2/2 rounds, remote-fix 1
- [Work-type routing](learnings/0003-work-type-routing.md): WHEN parallel tasks create files the always-loaded skill must plugin-root-point at → DO add a serial wiring task after those files exist · process: plan checker 2/2 rounds, Task 8 pointer-wiring gap
