---
type: Plan
title: "Numbered goal directories implementation plan"
description: Task-by-task plan to add a global ordinal prefix to the goal slug (0001-<name>) at creation, across the dev and rpa flows.
timestamp: 2026-06-15
tags: [goals, slug, ordering, plan]
---

# Numbered goal directories Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** New goals get a zero-padded global ordinal prefix as part of the slug (`0001-<name>`), assigned at creation and mirroring `ADR-NNNN`, so `.wi/goals/` lists in implementation order — visible in the directory, the `wi/<slug>` branch, and the PR.

**Architecture:** A prose convention change, not code. Only the slug-*derivation* step changes (dev step 2; the rpa ingest step); because the ordinal lives inside `<slug>`, the ~93 templated `<slug>` references are untouched. Two directory-reference docs document the convention and show `0001-<slug>` in their layout trees. No new scripts or unit tests — verification is `scripts/validate.py` + a read-back, exactly as the existing `ADR-NNNN` convention is maintained.

**Tech Stack:** Markdown skills with OKF frontmatter; `python scripts/validate.py` (manifests, frontmatter, `${CLAUDE_PLUGIN_ROOT}` resolution, fence/newline balance); `git`.

**Spec:** `docs/specs/2026-06-15-numbered-goal-dirs-design.md` (read first — problem, the ADR-mirrored numbering rule, backward-compat, and acceptance criteria 1–9).

---

## File Structure

All edits are to existing files; nothing is created except this plan's commits.
- **Modify** `skills/dev/SKILL.md` — step 2 slug derivation + the done-collision bullet.
- **Modify** `skills/rpa/SKILL.md` — step 2 gains a "derive the numbered run-slug first" pointer.
- **Modify** `skills/rpa/references/ingest.md` — §1 gains the authoritative run-slug derivation.
- **Modify** `skills/research/references/wi-directory.md` — layout tree + Slugs convention.
- **Modify** `skills/rpa/references/rpa-directory.md` — layout tree + a numbered-run-slug convention bullet.
- **Modify** the three manifests + `README.md` — version `0.10.4 → 0.10.5` + a Roadmap bullet.

Each task ends green on `python scripts/validate.py` and is one commit.

---

## Task 1: dev/SKILL.md — number the slug at derivation

**Files:**
- Modify: `skills/dev/SKILL.md` (step 2 derivation line; the done-collision bullet)

- [ ] **Step 1: Edit the derivation line**

Replace exactly:
```
   asked. Derive a kebab-case `<slug>`, then **check before creating**:
```
With:
```
   asked. Derive a kebab-case name, then prefix the **next global 4-digit ordinal** so `<slug>` =
   `NNNN-<name>` (e.g. `0001-stripe-webhooks`) — mirroring `ADR-NNNN`: the ordinal is global across
   `.wi/goals/`, monotonic, assigned **once at creation, never renumbered** (next = highest existing
   `.wi/goals/` ordinal + 1, else `0001`; legacy unnumbered goals are left as-is and ignored by the scan;
   a resumed goal keeps its number; a roadmap row's name is numbered when its folder is first created).
   Then **check before creating**:
```

- [ ] **Step 2: Edit the done-collision bullet**

Replace exactly:
```
   - Slug collides with a **done** goal: suffix the new one (`<slug>-2`); a finished dossier is history,
     not a scratch folder.
```
With:
```
   - Slug collides with a **done** goal: the global ordinal already makes the new folder unique (it gets
     the next number), so the kebab name may safely repeat across ordinals; only add a `-2` suffix to
     disambiguate identical names when scanning. A finished dossier is history, not a scratch folder.
```

- [ ] **Step 3: Validate**

Run: `python scripts/validate.py`
Expected: `[OK] all checks passed` (exit 0). If it fails on fences/frontmatter/`${CLAUDE_PLUGIN_ROOT}`, fix before committing.

- [ ] **Step 4: Commit**

```bash
git add skills/dev/SKILL.md
git commit -m "feat(dev): number goal slugs with a global ordinal at creation (NNNN-<name>)"
```

---

## Task 2: rpa flow — number the run-slug at ingest

**Files:**
- Modify: `skills/rpa/SKILL.md` (step 2 pointer)
- Modify: `skills/rpa/references/ingest.md` (§1 authoritative derivation)

- [ ] **Step 1: Add the pointer in rpa/SKILL.md step 2**

Replace exactly:
```
2. **Register inputs & components, ingest the PDD.** Follow
   `${CLAUDE_PLUGIN_ROOT}/skills/rpa/references/ingest.md`: catalog the supporting files in the repo (API
   refs, CSV/mapping tables, sample data, screenshots) into `.wi/inputs.md`; detect reusable components
   into `.wi/components.md`; convert the PDD to `pdd.md` with markitdown (skip if it's already Markdown).
```
With:
```
2. **Register inputs & components, ingest the PDD.** Follow
   `${CLAUDE_PLUGIN_ROOT}/skills/rpa/references/ingest.md`: derive the **numbered run-slug** first
   (`NNNN-<name>` — the next global 4-digit ordinal, mirroring `ADR-NNNN`; see ingest.md §1); catalog the
   supporting files in the repo (API refs, CSV/mapping tables, sample data, screenshots) into
   `.wi/inputs.md`; detect reusable components into `.wi/components.md`; convert the PDD to `pdd.md` with
   markitdown (skip if it's already Markdown).
```

- [ ] **Step 2: Add the authoritative derivation in ingest.md §1**

Replace exactly:
```
## 1. Convert the PDD → `pdd.md`

- If the PDD is `.docx`/`.pdf`/`.pptx`: `markitdown <pdd> -o .wi/goals/<slug>/pdd.md`.
```
With:
```
## 1. Derive the run-slug, then convert the PDD → `pdd.md`

- **Derive `<slug>` first** — it's the goal-folder name used everywhere below: a kebab name from the
  PDD/solution, **prefixed with the next global 4-digit ordinal** (`NNNN-<name>`, e.g. `0001-invoices`),
  mirroring `ADR-NNNN`: global across `.wi/goals/`, monotonic, assigned once at creation, never renumbered.
  Next = highest existing `.wi/goals/` ordinal + 1 (else `0001`); legacy unnumbered runs are left as-is.
- If the PDD is `.docx`/`.pdf`/`.pptx`: `markitdown <pdd> -o .wi/goals/<slug>/pdd.md`.
```

- [ ] **Step 3: Validate**

Run: `python scripts/validate.py`
Expected: `[OK] all checks passed` (exit 0).

- [ ] **Step 4: Commit**

```bash
git add skills/rpa/SKILL.md skills/rpa/references/ingest.md
git commit -m "feat(rpa): derive a numbered run-slug at ingest (NNNN-<name>)"
```

---

## Task 3: document the convention in the directory references

**Files:**
- Modify: `skills/research/references/wi-directory.md` (layout tree + Slugs convention)
- Modify: `skills/rpa/references/rpa-directory.md` (layout tree + a numbered-run-slug bullet)

- [ ] **Step 1: Update the wi-directory.md layout tree**

Replace exactly:
```
    └── <slug>/             # one folder per goal (feature), slug is kebab-case
```
With:
```
    └── 0001-<slug>/        # one folder per goal; NNNN- global ordinal (creation order) + kebab slug
```

- [ ] **Step 2: Update the wi-directory.md Slugs convention**

Replace exactly:
```
- **Slugs** are short, kebab-case, derived from the feature: "Add Stripe webhooks" -> `stripe-webhooks`.
```
With:
```
- **Slugs** are short, kebab-case, derived from the feature, **prefixed with a global 4-digit ordinal
  assigned at creation**: "Add Stripe webhooks" -> `0001-stripe-webhooks`. The prefix mirrors `ADR-NNNN`
  (global across `.wi/goals/`, monotonic, **never renumbered**) so `.wi/goals/` lists in implementation
  order; next number = highest existing `.wi/goals/` ordinal + 1 (else `0001`). Legacy unnumbered goals
  are left as-is and contribute nothing to the max.
```

- [ ] **Step 3: Update the rpa-directory.md layout tree**

Replace exactly:
```
    └── <run-slug>/          # one /wi:rpa run = one PDD -> solution
```
With:
```
    └── 0001-<run-slug>/     # one /wi:rpa run = one PDD -> solution; NNNN- global ordinal (creation order)
```

- [ ] **Step 4: Add a numbered-run-slug bullet to rpa-directory.md Conventions**

Replace exactly:
```
## Conventions

- **Project-level files persist & compound** across runs:
```
With:
```
## Conventions

- **Run-slugs are numbered** — `NNNN-<name>` (a global 4-digit ordinal assigned at creation, mirroring
  `ADR-NNNN`; next = highest existing `.wi/goals/` ordinal + 1, else `0001`, never renumbered), so runs
  list in implementation order. Same convention as the dev flow (`wi-directory.md`).
- **Project-level files persist & compound** across runs:
```

- [ ] **Step 5: Validate**

Run: `python scripts/validate.py`
Expected: `[OK] all checks passed` (exit 0).

- [ ] **Step 6: Commit**

```bash
git add skills/research/references/wi-directory.md skills/rpa/references/rpa-directory.md
git commit -m "docs(wi): document numbered goal/run directories in the layout references"
```

---

## Task 4: version bump, README, and full verification

**Files:**
- Modify: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json` (`0.10.4 → 0.10.5`)
- Modify: `README.md` (Roadmap bullet)

- [ ] **Step 1: Bump version 0.10.4 → 0.10.5 in all three manifests**

In each file, change `"version": "0.10.4"` to `"version": "0.10.5"` (one occurrence per file):
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `.codex-plugin/plugin.json`

- [ ] **Step 2: Add the README Roadmap bullet**

`README.md` has a `## Roadmap` section whose current first bullet begins `- **tokens.md guardrails** (v0.10.4) shipped —`. Insert this NEW bullet as the **first** item under `## Roadmap`, immediately before that bullet:
```
- **Numbered goal directories** (v0.10.5) shipped — new goals get a global 4-digit ordinal prefix as part
  of the slug (`0001-<name>`, mirroring `ADR-NNNN`), so `.wi/goals/` lists in implementation order — visible
  in the directory, the branch name, and the PR. dev + rpa; existing goals untouched. Design and plan in
  `docs/specs/` and `docs/plans/`.
```

- [ ] **Step 3: Full verification (paste real output)**

```bash
python scripts/validate.py
```
Expected: `[OK] all checks passed` (exit 0; manifests still valid JSON after the bump).

File-tail check for truncation (this repo's known hazard):
```bash
for f in skills/dev/SKILL.md skills/rpa/SKILL.md skills/rpa/references/ingest.md skills/research/references/wi-directory.md skills/rpa/references/rpa-directory.md README.md; do echo "== $f =="; tail -c 100 "$f"; echo; done
```
Confirm every tail ends on a complete line.

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/plugin.json .claude-plugin/marketplace.json .codex-plugin/plugin.json README.md
git commit -m "chore: release 0.10.5 — numbered goal directories"
```

---

## Done-when

- `python scripts/validate.py` passes.
- `dev/SKILL.md` step 2 and `rpa` ingest §1 derive `<slug>` = `NNNN-<name>` with the highest-existing-+1 rule (else `0001`); the done-collision bullet notes the ordinal makes `-2` a fallback.
- `wi-directory.md` and `rpa-directory.md` document the convention and show a `0001-<slug>` directory in their trees.
- Version is `0.10.5` across the three manifests with a README Roadmap bullet.
- A grep for the convention keyword is consistent: `NNNN` / `0001` / "4-digit" wording matches across all edited files.
