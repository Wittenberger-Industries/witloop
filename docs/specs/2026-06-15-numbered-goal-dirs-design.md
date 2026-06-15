---
type: Design Spec
title: Numbered goal directories — a global ordinal prefix on the goal slug
description: New goals get a zero-padded global ordinal prefix (0001-<name>) at creation, mirroring ADR-NNNN, so implementation order is visible in the directory listing, branch names, and PRs.
status: accepted
timestamp: 2026-06-15
tags: [goals, slug, ordering, convention, dev, rpa, adr]
---

# Numbered goal directories

## Problem

wi goal directories are named by kebab `<slug>` only (`.wi/goals/tokens-md-guardrails/`), so a
`.wi/goals/` listing gives no sense of the order goals were implemented. The project already numbers ADRs
globally (`ADR-NNNN-*`) precisely so the decision sequence is legible; goals lack the same affordance.

## Goals

- Every newly created goal gets a zero-padded global ordinal prefix **as part of its slug** — `<slug>`
  becomes `NNNN-<name>` (e.g. `0001-tokens-md-guardrails`) — so creation order (≈ implementation order)
  is visible in the directory listing, the `wi/<slug>` branch name, and the PR.
- Mirror the existing `ADR-NNNN` convention: global, monotonic, 4-digit, assigned at creation, never
  renumbered.
- Minimal blast radius: only the slug-**derivation** step changes; the ~93 templated `<slug>` references
  across the skills keep working because the number rides inside `<slug>`.
- Apply uniformly to the **dev** flow and the **rpa** flow.

## Non-goals

- **Renumbering or renaming existing goals** — would break their branches, open PRs, and cross-references.
  Legacy unnumbered goals stay as-is.
- **A deterministic next-number helper script** — numbering is a one-shot at-creation step that cannot be
  silently skipped (you must name the directory to create it), and "highest + 1" is the same trivial
  computation the ADR flow already does in prose. A script would be over-engineering and inconsistent with
  `ADR-NNNN`.
- **Pre-numbering roadmap rows** — rows stay name-only; the number is assigned when the goal folder is
  first created.
- **Completion-order numbering** — impractical (would require renaming on completion). Creation order is
  the legible, stable proxy for implementation order in wi's sequential workflow.

## Design

### The change (approach B — the ordinal is part of the slug)

At goal creation, after deriving the kebab name, prefix the next global 4-digit ordinal so `<slug>`
becomes `NNNN-<name>`. Because the number lives **inside** `<slug>`, every downstream
`.wi/goals/<slug>/` path, `wi/<slug>` branch, `/goal` keep-alive condition, and cross-reference is
unchanged — only the derivation changes.

### Numbering (mirrors `ADR-NNNN`)

- **Global** across the project's `.wi/goals/`, **monotonic**, **4-digit** zero-padded, assigned **once at
  creation**, **never renumbered**.
- Next number = (highest **numeric** `NNNN` prefix among existing `.wi/goals/*/` directories) + 1; `0001`
  if none exist. Non-numeric (legacy) directory names contribute nothing to the max.
- Model-computed by scanning `.wi/goals/` — the same way the next `ADR-NNNN` is computed by reading the
  ADR log. No script.

### Where it changes (2 prose edits + 2 doc updates)

1. `skills/dev/SKILL.md` step 2 — "Derive a kebab-case `<slug>`" becomes: derive the kebab name, then
   prefix the next global 4-digit ordinal so `<slug>` = `NNNN-<name>`.
2. `skills/rpa/SKILL.md` — the same at its PDD→goal-open step (where the rpa slug is derived).
3. `skills/research/references/wi-directory.md` — document the convention in the Conventions section and
   show a `0001-<slug>` directory in the `.wi/` layout tree.
4. `skills/rpa/references/rpa-directory.md` — document the convention and show a numbered goal dir in its
   layout tree.

### Backward compatibility

Existing unnumbered goal directories are left exactly as-is (renaming would break their branches, PRs, and
references). The next-number scan ignores non-numeric prefixes, so the first numbered goal in a legacy
project starts at `0001`; numbered and unnumbered directories coexist, and order is visible for everything
created after adoption.

### Interactions with the existing dev step-2 logic

- **Resume:** an in-flight goal keeps its existing (already-numbered) directory — never renumber on resume.
- **Done-slug collision:** the global ordinal already makes every directory unique, so the existing `-2`
  suffix rule becomes a rarely-needed readability fallback rather than the collision guard. Keep it; note
  the relegation.
- **Roadmap match:** the row's name gets its number when the goal folder is first created (roadmap rows
  stay name-only).

## Acceptance criteria

1. `dev/SKILL.md` step 2 instructs deriving `<slug>` = `NNNN-<kebab-name>`, where `NNNN` = highest existing
   numeric `.wi/goals/` prefix + 1 (else `0001`), 4-digit zero-padded, assigned at creation.
2. `rpa/SKILL.md`'s goal-open step instructs the same derivation from the PDD.
3. `wi-directory.md` documents the convention (global, monotonic, 4-digit, at creation, never renumbered)
   and its `.wi/goals/` layout example shows a `0001-<slug>` directory.
4. `rpa-directory.md` documents the convention and shows a numbered goal directory in its layout.
5. The backward-compat rule (don't renumber existing; ignore non-numeric prefixes; first numbered = `0001`)
   is stated in `wi-directory.md`.
6. The resume / done-collision / roadmap interactions are stated correctly where the slug is derived
   (`dev/SKILL.md` step 2).
7. No `<slug>` template reference elsewhere is broken (the number rides inside `<slug>`); no
   `${CLAUDE_PLUGIN_ROOT}` reference is broken.
8. `python scripts/validate.py` passes; the `NNNN` / 4-digit / `0001` wording is consistent across all
   edited files.
9. Version bumped `0.10.4 → 0.10.5` across the three manifests; a README Roadmap "shipped" bullet is added.

## Verification

No unit tests — this is a prose naming convention like `ADR-NNNN`. Verify by `python scripts/validate.py`
(frontmatter, `${CLAUDE_PLUGIN_ROOT}` resolution, fence balance) plus a manual read confirming the four
skill/reference files agree on the convention and the layout examples show `0001-<slug>`. Sanity-trace the
numbering by hand: a `.wi/goals/` containing `0001-a` and `0002-b` yields next = `0003`; an empty one
yields `0001`.

## Rollout

Single PR. Version bump to `0.10.5` + a README Roadmap "shipped" bullet. Run `validate.py` and the
file-tail check (this repo's truncation hazard) before commit. No migration: existing goals keep their
names; numbering applies to goals created from adoption onward.
