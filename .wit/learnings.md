---
type: Learnings Index
title: Learnings index (Witloop)
description: One line + hook per feature; phases read this, then open a detail file only when its hook fits.
timestamp: 2026-08-28
---

# Learnings index

- [First-class Cursor host via a capability table](learnings/0001-cursor-capability-table.md): WHEN calling ensure_logdir.py → AVOID the feature folder (target .logs) · process: checker 2/2 rounds, remote-fix 1
- [Work-type routing](learnings/0003-work-type-routing.md): WHEN parallel tasks create files the always-loaded skill must plugin-root-point at → DO add a serial wiring task after those files exist · process: plan checker 2/2 rounds, Task 8 pointer-wiring gap
- [Ship verification honesty](learnings/0003-blast-radius-proof.md): WHEN adding a second coverage table to the checker → AVOID placing it before the bug-fix matrix; reinforces 0003-work-type-routing's serial-wiring hook · process: checker 2/2 rounds, parent takeover task 1
- [/wit-setup first-run](learnings/0004-setup.md): WHEN a new advertised command takes over first-run copy → DO retarget README cells, manifests, and the old alias in the same sitting · process: advertised-copy retarget at ship
- [Marketplace plugin descriptions under 1024 chars](learnings/0005-marketplace-json-cap.md): WHEN judging a validate.py repro → AVOID treating exit 1 as the named bug · process: clean
