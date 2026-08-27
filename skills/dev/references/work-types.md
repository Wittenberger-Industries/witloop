---
type: Reference
title: "Work types: semantic deduction before write-capable setup"
description: "How /wit:dev semantically deduces feature, bug-fix, or investigation, announces the result, and honors --kind plus resume stamps."
timestamp: 2026-08-25
tags: [dev, work-type, routing, reference]
---

# Work types: semantic deduction before write-capable setup

Work type is a **semantic orchestrator judgment** of the user's intent. It is not a keyword-only runtime classifier;
do not add a keyword-only helper. Deduce before any write-capable setup (host probe, scan, models, feature folder).
This file is enough to decide when loaded alone.

## Types and conservative tells

- **feature** - new behavior, construction, design-and-build. Conservative tells: "build me",
  "I want a feature", "add `<capability>`", implement, support new behavior.
- **bug-fix** - repair a confirmed defect. Conservative tells: "fix this bug", "why does X fail",
  broken, crash, regression, a repro to repair. Do not steal "file a bug" (that stays add-issues).
- **investigation** - read-only explanation, no change request. Conservative tells: "how does X work",
  "explain this architecture", a walk-through with no edit.

## Precedence

1. Valid `--kind feature|bug-fix|investigation` wins. Source: `kind`. Tells are ignored.
2. Invalid `--kind` **stops** with that valid set. Do not infer. Do not continue.
3. Semantic deduction of a single clear type. Source: `inferred`.
4. Mixed, unclear, or mixed-intent ("explain this then change it") becomes an announced `feature`.
   Source: `ambiguous-default`. Never ask. Never route silently.

Precedence: `--kind` > inferred > ambiguous-default.

## Always announce

Always print exactly this one line (never silent, never a question):

Work type: <type> (<source>). Override: --kind feature|bug-fix|investigation

Source labels are `kind`, `inferred`, or `ambiguous-default`.

## Resume and stamp

Feature and bug-fix dossiers stamp optional `Work type: feature|bug-fix`. Investigation never seeds a
folder. On resume, honor the stamp without re-deduction unless `--kind` is present; the override
wins. A missing Work type: stamp means feature.

## After announce

- **investigation:** load `${PLUGIN_ROOT}/skills/dev/references/investigation.md` and exit.
  No host probe, scan, models, or feature-folder writes.
- **bug-fix:** continue through host probe, scan, models, and the folder classifier
  (`new / resume / in-flight-overlap / done-collision / roadmap-row`). After the folder classifier,
  load `${PLUGIN_ROOT}/skills/dev/references/bug-fix.md`.
- **feature:** continue through host probe, scan, models, and the folder classifier
  (`new / resume / in-flight-overlap / done-collision / roadmap-row`). Do not load bug-fix.md.
