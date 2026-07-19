---
type: Plan
title: "Process-drift telemetry across features (#82)"
description: "Close-out process: clause on learnings index lines; scan --refresh trend pass proposes amendments at >=3 shared frictions. Ships as wit v1.13.3; full dry-run follows merge."
timestamp: 2026-07-19
tags: [plan, ship, scan, process-drift, learnings]
---

# Process-drift telemetry (#82) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** At ship close-out, append `process: clean` or a friction clause to the feature's learnings-index line; scan --refresh B step 5 trends those clauses and proposes amendments when >=3 features share friction. Ship as wit `v1.13.3`.

**Architecture:** Literal additive skill/reference edits only. One-line telemetry, no scores. Refresh proposes, never self-applies constitution changes.

**Tech Stack:** Markdown skills; `scripts/validate.py`.

## Global Constraints

- Version bump: `1.13.2` → `1.13.3` on all three manifests together.
- No em-dashes in shipped text, commits, or PR bodies.
- No new agents, gates, or scripts.
- Index stays ~30-line readable (suffixes are single-line).
- Full dry-run is AFTER this PR merges (separate follow-up in the same session or next); roadmap names deferred dry-run ACs (#79/#81).
- Hotspot files: single branch (`ship/SKILL.md`, `wit-directory.md`, `scan/SKILL.md`).

## File map

| File | Change |
|------|--------|
| `skills/ship/SKILL.md` | §8 after close-out checklist: write `process:` suffix on index line |
| `skills/scan/SKILL.md` | B new step 5 trend pass; renumber if needed (Target stays; insert before Glossary or after Target) |
| `skills/research/references/wit-directory.md` | Optional `process:` suffix clause on learnings recall |
| Manifests + roadmap | `1.13.3` |

## Format

On the feature's learnings-index line, append either:
- ` · process: clean`
- ` · process: checker 2/2 rounds, remote-fix 1, task 3 debug pass, frontend stamp missing`

Vocabulary = countable facts already in `progress.md` (no judgment, no scores).

---

### Task 1: ship §8 close-out process: clause

**Files:**
- Modify: `skills/ship/SKILL.md` (§8, after the close-out checklist / before or with Phase = done)
- Test: grep + validate

- [ ] **Step 1: Add close-out process telemetry**

After the checklist (when all boxes green, before or as part of setting Phase = done), require updating the feature's `.wit/learnings.md` index line with the `process:` suffix. If the line was already written in ship:4, append the suffix to it now (idempotent: do not duplicate `process:`).

```markdown
**Process telemetry (after the checklist, before Phase = done):** append a compact clause to this
feature's learnings-index line in `.wit/learnings.md`:
` · process: clean` when the run did not strain the process, or
` · process: <friction>` naming countable facts already in `progress.md` (examples: `checker 2/2 rounds`,
`remote-fix 1`, `task 3 debug pass`, `frontend stamp missing`). No judgment, no scores. If the index
line already has a `process:` suffix, leave it (do not duplicate).
```

- [ ] **Step 2: Verify**

```powershell
Select-String -Path skills/ship/SKILL.md -Pattern "process: clean"
Select-String -Path skills/ship/SKILL.md -Pattern "Process telemetry"
python scripts/validate.py
```

- [ ] **Step 3: Commit**

```powershell
git add skills/ship/SKILL.md
git commit -m "feat(ship): process: clause on learnings index at close-out"
```

---

### Task 2: scan --refresh B step 5 trend pass

**Files:**
- Modify: `skills/scan/SKILL.md` (`### B · Memory hygiene`)
- Test: grep + validate

- [ ] **Step 1: Add step 5 after Target (step 4)**

```markdown
5. **Process-drift trend:** scan index lines' `process:` clauses. The same friction appearing in
   ~3 features (or more) → surface it in the refresh report with a concrete proposed amendment
   (example: "checker round budget too small for this repo - raise to 3 in constitution?" /
   "remote checks flaky - add the CI wait note to repo-map?"). Propose, never self-apply;
   constitution stays user-owned. Fewer than 3 shared frictions → stay silent on process drift.
```

Keep steps 1-4 unchanged. Glossary/ADR notes after B stay.

- [ ] **Step 2: Optionally mention process-drift counts in section C report** one clause if useful (not required if step 5 already says "refresh report").

- [ ] **Step 3: Verify**

```powershell
Select-String -Path skills/scan/SKILL.md -Pattern "Process-drift trend"
Select-String -Path skills/scan/SKILL.md -Pattern "Propose, never self-apply"
python scripts/validate.py
```

- [ ] **Step 4: Commit**

```powershell
git add skills/scan/SKILL.md
git commit -m "feat(scan): process-drift trend pass on refresh B"
```

---

### Task 3: wit-directory process: suffix clause

**Files:**
- Modify: `skills/research/references/wit-directory.md` (Learnings recall bullet)
- Test: grep + validate

- [ ] **Step 1: Document optional process: suffix**

Append to the Learnings recall bullet:

```markdown
Index lines may also carry an optional ` · process: clean` or ` · process: <friction>` suffix written
at ship close-out; tidy/checklist treat it as part of the line, not a stray.
```

- [ ] **Step 2: Verify**

```powershell
Select-String -Path skills/research/references/wit-directory.md -Pattern "process: clean"
python scripts/validate.py
```

- [ ] **Step 3: Commit**

```powershell
git add skills/research/references/wit-directory.md
git commit -m "docs: document process: suffix on learnings index lines"
```

---

### Task 4: version 1.13.3, roadmap, PR

**Files:** three manifests; `docs/roadmap.md`; this plan; PR

- [ ] **Step 1:** Bump to `1.13.3` on all three manifests.
- [ ] **Step 2:** Roadmap: #82 shipping as v1.13.3; note full dry-run (incl. deferred #79/#81 dry-run ACs) runs immediately after merge.
- [ ] **Step 3:** validate.py green.
- [ ] **Step 4:** Commit plan + version + roadmap.
- [ ] **Step 5:** Push + `gh pr create` with temp body-file; Closes #82.

Branch: `feat/process-drift-telemetry-82`.

---

## Self-review

1. Close-out write + scan trend + wit-directory + version covered.
2. Threshold `>= 3` / `~3` as in issue; propose never apply.
3. Dry-run after merge, not in this PR.
