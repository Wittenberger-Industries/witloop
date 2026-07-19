---
type: Design Spec
title: "Learnings lifecycle: coverage, causal format, counters, polish (issues #78-#80, #83)"
description: >
  Accepted design for PR1 of the 2026-07-19 workflow review: close the learnings recall→enforcement
  gap, standardize causal lesson bullets, add evidence counters + enforced-by retirement, and land
  three polish one-liners. Approach: literal skill/agent text edits only. Ships as v1.13.1.
status: accepted
timestamp: 2026-07-19
tags: [learnings, checker, ship, scan, research, polish, design]
---

# Learnings lifecycle (issues #78, #79, #80, #83)

## Summary

Ship one PR (`v1.13.1`) that makes learnings a first-class, enforceable part of wit's loop:

1. **#78** - Checker coverage matrix includes applicable learnings (research stamps them; dispatches pass them).
2. **#79** - Causal `WHEN → DO/AVOID → BECAUSE` bullet format for new lessons.
3. **#80** - Index counters `(seen: N, last: …)`, reinforce-not-duplicate, promote/retire on evidence.
4. **#83** - Three polish lines: test-level rule, checker pre-mortem, waiver pointer.

Later PRs (out of this spec): **#81** Reflection lines (`v1.13.2`), **#82** process-drift telemetry (`v1.13.3`), then a **full dry-run feature** after #82.

## Problem

Learnings are recalled (research §1a) but never enforced. Freeform bullets are hard to apply. Recurrence is not counted, so promotion is guesswork, and structurally-enforced lessons never retire. Three small polish gaps ride along when the same files are open.

## Goals / non-goals

**In:** Additive skill/agent markdown edits listed below; version bump `1.13.0 → 1.13.1`; `scripts/validate.py` green; close #78 #79 #80 #83 on merge.

**Out:** New agents, new gates, new scripts, fixture/pytest for prose, live dry-run in this PR, issues #81/#82, migrating existing freeform learnings.

## Approach (locked)

**Literal skill edits** - edit priority files exactly as the issues specify. No Python parsers; agents apply the conventions.

## Behavior by issue

### #78 - Coverage matrix

- After research §1a settled-check, stamp:  
  `- <ts> **Update** applicable learnings: <slug: ~10-word hook; …> | none`
- research §2 and ship §2 pass that progress.md line into the checker dispatch.
- wit-code-checker matrix inputs gain "applicable learning named in the dispatch" (both modes).  
  Plan/diff hits a lesson's context and ignores its action → **WARNING** (hook + task # / `file:line`).  
  Promoted-to-constitution lessons stay **BLOCKER** via the existing constitution row.
- verification.md shows a Learnings row (or explicit "none applicable").
- ship §4: violated-again → sharpen existing hook, do not duplicate (pairs with #80).

### #79 - Causal format

- ship §4 detail template: keep three headings; guidance line + one example causal bullet.
- Index hooks: compress to `WHEN <context> → AVOID <action>` where natural.
- scan --refresh B1: dedupe on matching WHEN-context.

### #80 - Counters + retirement

- ship §4: match existing hook → increment `(seen: N, last: NNNN-<slug>)`, optional sharpen, current feature line `reinforces <earlier-slug>'s <hook>`, no new detail file.
- scan B2: promote at `seen ≥ 3` (≥ 2 if rule-shaped); constitution still user-confirmed.
- scan B3: second trigger `→ enforced by <check> (<date>)` after verifying the check exists; delete detail file.
- wit-directory learnings-recall: one clause on counters.

### #83 - Polish

1. spec-template Test plan: cheapest level rule; never assert the same thing at two levels.
2. wit-code-checker plan mode: pre-mortem bullet (untestable Verify / hidden parallel overlap / missing dependency edge).
3. ship §2 + §5: waived/deferred WARNING needs roadmap.md line or issue pointer; PR.md Verification shows it.

## Files

| File | Changes |
|------|---------|
| `skills/research/SKILL.md` | §1a stamp; §2 dispatch inputs |
| `agents/wit-code-checker.md` | matrix row; plan-mode pre-mortem |
| `skills/ship/SKILL.md` | §2 dispatch + waiver; §4 format/counters/sharpen; §5 Verification |
| `skills/scan/SKILL.md` | B1 WHEN-dedupe; B2 thresholds; B3 enforced-by |
| `skills/research/references/wit-directory.md` | counters clause |
| `skills/plan/references/spec-template.md` | test-level rule |
| `.claude-plugin/plugin.json`, `marketplace.json`, `.codex-plugin/plugin.json` | `1.13.1` |
| `docs/roadmap.md` | queue note for #78-#83 |

## Acceptance (this PR)

- [ ] Matrix + dispatch + stamp wording landed per #78
- [ ] Causal template + B1 WHEN-dedupe per #79
- [ ] Counters / reinforce / B2 / B3 / wit-directory per #80
- [ ] Three polish lines per #83
- [ ] Version `1.13.1` on all three manifests; `python scripts/validate.py` green
- [ ] Issues #78 #79 #80 #83 closed by the PR
- [ ] No dry-run in this PR (deferred until after #82)

## Packaging (program)

| PR | Issues | Version |
|----|--------|---------|
| 1 (this) | #78 #79 #80 #83 | 1.13.1 |
| 2 | #81 | 1.13.2 |
| 3 | #82 | 1.13.3 |
| after 3 | full dry-run feature | - |
