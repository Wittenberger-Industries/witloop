---
type: Research Note
title: "Research questions: work-type routing"
description: Load-bearing repository questions that determine the implementation design.
feature: 0003-work-type-routing
timestamp: 2026-08-25
---

# Research questions: work-type routing

1. **[repo-question] Classification seam:** Where can Witloop infer or override `feature`, `bug-fix`,
   and `investigation` before feature-folder classification while leaving the existing feature path
   unchanged?
2. **[repo-question] Investigation route:** How should a read-only investigation invoke installed
   understanding skills or a portable fallback, produce citations, and exit without `.wit/` state or a
   PR?
3. **[repo-question] Bug-fix route:** How can a reproduce-first bug-fix flow reuse Witloop's existing
   phases, record a justified narrow-fix design-gate bypass, and enforce failing-then-passing
   same-surface proof?
