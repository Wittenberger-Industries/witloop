---
type: Plan
title: "wi:rpa auto-publish implementation plan"
description: Task-by-task plan to add a gate-approved publish decision (none/feed/deploy) and a post-gate ship publish action to wi:rpa.
timestamp: 2026-06-16
tags: [rpa, publish, orchestrator, plan]
---

# wi:rpa auto-publish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `wi:rpa` can publish a verified, PR'd build to a connected Orchestrator tenant — the design gate approves `Publish: none | feed | deploy` (+ folder, prod-guarded), and ship delegates the push to `uipath-solution`, best-effort and hands-off-safe.

**Architecture:** A prose + delegation change, not code. The design gate gains one approval (`Publish:`), recorded in `progress.md`; the verify-&-ship step gains a post-gate publish action that runs only on an already-green build with the PR open, checks the `uip` tenant connection, and delegates `pack`/`publish`/`deploy`/`activate` to `uipath-solution`. The constitution carries the default; the progress template and verification-gate docs document the field and the post-gate boundary.

**Tech Stack:** Markdown skills with OKF frontmatter; `python scripts/validate.py` (manifests, frontmatter, `${CLAUDE_PLUGIN_ROOT}` resolution, fence/newline balance); `git`. No new scripts/tests — like the numbered-goal-dirs feature.

**Spec:** `docs/specs/2026-06-16-rpa-auto-publish-design.md` (read first — the gate decision, ship execution, guards, and acceptance criteria 1–9).

---

## File Structure

All edits are to existing files.
- **Modify** `skills/rpa/SKILL.md` — step 5 (gate approval gains the publish decision) + step 7 (new post-gate publish action).
- **Modify** `skills/rpa/references/rpa-constitution-template.md` — a `Publish:` default + prod-approval rule.
- **Modify** `skills/rpa/references/rpa-directory.md` — add the `Publish:` field to the `progress.md` template.
- **Modify** `skills/rpa/references/verification-gate.md` — note publish is a post-gate ship action.
- **Modify** the three manifests + `README.md` — version bump + a Roadmap bullet.

Each task ends green on `python scripts/validate.py` and is one commit.

---

## Task 1: rpa/SKILL.md — gate decision + post-gate publish action

**Files:**
- Modify: `skills/rpa/SKILL.md` (step 5 gate; step 7 verify-&-ship)

- [ ] **Step 1: Add the publish decision to the step-5 gate**

Replace exactly:
```
   ground**), recorded in `progress.md` (`Build paradigm:`). `--auto` records and proceeds on the constitution default (XAML-only). On
```
With:
```
   ground**), recorded in `progress.md` (`Build paradigm:`). **Also approve the publish decision** —
   `Publish: none | feed | deploy` (+ target folder for `deploy`): `none` = build to PR only; `feed` =
   pack + publish the package(s) to the connected tenant's feed; `deploy` = `feed` + deploy/activate as a
   Process in that folder; a **prod** folder must be explicitly approved here (never auto-selected),
   recorded in `progress.md` (`Publish:`). `--auto` records and proceeds on the constitution defaults
   (paradigm XAML-only; publish per the constitution, default `none`). On
```

- [ ] **Step 2: Add the post-gate publish action to step 7**

Replace exactly:
```
   the gate; update its `.wi/learnings.md` index line), and the **token report (`tokens.md` — finalized
   before the dossier commit, mandatory)**.
   **Ship is dev-shaped — map its artifacts to the RPA ones:** gate → the RPA verification gate above;
```
With:
```
   the gate; update its `.wi/learnings.md` index line), and the **token report (`tokens.md` — finalized
   before the dossier commit, mandatory)**.
   **Publish to the tenant (if approved) — after the PR is open.** If `progress.md` `Publish: ≠ none` and
   `uip` is authenticated to the `orchestrator.md` tenant, delegate to **`uipath-solution`**: `pack` +
   `publish` the package(s) to the feed, and for `deploy` also `deploy` + `activate` as a Process in the
   gate-approved folder. **Not connected** → skip, and record in `progress.md` that publish was approved
   but no tenant is connected (recovery: `uip cloud login`) — not a failure; the PR shipped. **On error** →
   record the exact recovery `uip`
   command in `progress.md` and report; never fail the run over publish. A **prod** target needs the gate's
   explicit approval, and publish is **post-gate** — it never runs on a red build. Record the published
   package name + version (+ folder) into `orchestrator.md` and the final report.
   **Ship is dev-shaped — map its artifacts to the RPA ones:** gate → the RPA verification gate above;
```

- [ ] **Step 3: Validate**

Run: `python scripts/validate.py`
Expected: `[OK] all checks passed` (exit 0). If it fails on fences/frontmatter/`${CLAUDE_PLUGIN_ROOT}`, fix before committing.

- [ ] **Step 4: Commit**

```bash
git add skills/rpa/SKILL.md
git commit -m "feat(rpa): gate-approved publish decision + post-gate tenant publish"
```

---

## Task 2: supporting docs — constitution default, progress field, gate note

**Files:**
- Modify: `skills/rpa/references/rpa-constitution-template.md` (Publish default)
- Modify: `skills/rpa/references/rpa-directory.md` (progress.md template field)
- Modify: `skills/rpa/references/verification-gate.md` (post-gate note)

- [ ] **Step 1: Add the `Publish:` default to the constitution's "Framework & approach"**

Replace exactly:
```
- **Prefer Integration Service connectors / APIs over UI** where one exists — for maintainability
  (selectors break, APIs are stable). **UI automation is valid** when there's no API or the interaction is
  inherently UI; flag UI steps in the SDD as higher-maintenance.   (confirm)
```
With:
```
- **Prefer Integration Service connectors / APIs over UI** where one exists — for maintainability
  (selectors break, APIs are stable). **UI automation is valid** when there's no API or the interaction is
  inherently UI; flag UI steps in the SDD as higher-maintenance.   (confirm)
- **Publish (default `none`):** after a green build + PR, wi can publish to a connected Orchestrator tenant
  — `none` (no push, default), `feed` (publish the package to the tenant feed), or `deploy` (`feed` +
  deploy/activate as a Process in a folder). The design gate confirms it each run; `--auto` uses this
  default. **No production-folder deploy without explicit approval at the gate.**   (confirm)
```

- [ ] **Step 2: Add the `Publish:` field to the `progress.md` template**

In `skills/rpa/references/rpa-directory.md`, replace exactly:
```
- **Build paradigm:** xaml-only   <!-- xaml-only (pure activities, NO Invoke Code) | coded-allowed (.cs) — user-approved at the design gate -->
```
With:
```
- **Build paradigm:** xaml-only   <!-- xaml-only (pure activities, NO Invoke Code) | coded-allowed (.cs) — user-approved at the design gate -->
- **Publish:** none   <!-- none | feed (publish package to tenant feed) | deploy (feed + deploy/activate to a folder) — approved at the design gate; prod folder needs explicit approval -->
```

- [ ] **Step 3: Add the post-gate note to the verification gate**

In `skills/rpa/references/verification-gate.md`, replace exactly:
```
The bar a built UiPath solution must clear before it ships. It uses UiPath's own tooling via the `uip`
CLI / the `uipath-platform` skill — wi doesn't invent checks. Run every command **non-interactively and
time-bounded** (a hands-off run must never stall on a prompt; a hang is a blocker to surface).
```
With:
```
The bar a built UiPath solution must clear before it ships. It uses UiPath's own tooling via the `uip`
CLI / the `uipath-platform` skill — wi doesn't invent checks. Run every command **non-interactively and
time-bounded** (a hands-off run must never stall on a prompt; a hang is a blocker to surface).

**Publishing is not part of this gate.** Pushing the package to a tenant (`progress.md` → `Publish: feed |
deploy`) is a separate, **post-gate** ship action that runs only on an already-green build with the PR open
(see rpa/SKILL.md step 7) — it never gates "done" and never runs on a red build.
```

- [ ] **Step 4: Validate**

Run: `python scripts/validate.py`
Expected: `[OK] all checks passed` (exit 0).

- [ ] **Step 5: Commit**

```bash
git add skills/rpa/references/rpa-constitution-template.md skills/rpa/references/rpa-directory.md skills/rpa/references/verification-gate.md
git commit -m "docs(rpa): Publish default in constitution, progress field, post-gate note"
```

---

## Task 3: version bump, README, and full verification

**Files:**
- Modify: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json` (`0.10.5 → 0.11.0`)
- Modify: `README.md` (Roadmap bullet)

- [ ] **Step 1: Bump version 0.10.5 → 0.11.0 in all three manifests**

In each file, change `"version": "0.10.5"` to `"version": "0.11.0"` (one occurrence per file):
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `.codex-plugin/plugin.json`

- [ ] **Step 2: Add the README Roadmap bullet**

`README.md` has a `## Roadmap` section whose current first bullet begins `- **Numbered goal directories** (v0.10.5) shipped —`. Insert this NEW bullet as the **first** item under `## Roadmap`, immediately before that bullet:
```
- **rpa tenant publish** (v0.11.0) shipped — `wi:rpa` can publish a verified, PR'd build to a connected
  Orchestrator tenant: the design gate approves `Publish: none | feed | deploy` (+ folder, prod-guarded),
  and ship delegates `pack`/`publish`/`deploy`/`activate` to `uipath-solution` — best-effort, hands-off-safe.
  Next: Maestro flow as a build paradigm. Design and plan in `docs/specs/` and `docs/plans/`.
```

- [ ] **Step 3: Full verification (paste real output)**

```bash
python scripts/validate.py
```
Expected: `[OK] all checks passed` (exit 0; manifests still valid JSON after the bump).

File-tail check for truncation (this repo's known hazard):
```bash
for f in skills/rpa/SKILL.md skills/rpa/references/rpa-constitution-template.md skills/rpa/references/rpa-directory.md skills/rpa/references/verification-gate.md README.md; do echo "== $f =="; tail -c 100 "$f"; echo; done
```
Confirm every tail ends on a complete line.

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/plugin.json .claude-plugin/marketplace.json .codex-plugin/plugin.json README.md
git commit -m "chore: release 0.11.0 — rpa tenant publish"
```

---

## Done-when

- `python scripts/validate.py` passes.
- `rpa/SKILL.md` step 5 gate approves `Publish: none|feed|deploy` (+ folder, prod-guarded) into `progress.md`; step 7 publishes post-PR via `uipath-solution` when `Publish ≠ none` and `uip` is connected — connection-skip and errors are best-effort + recorded, never failing the run.
- The constitution carries a `Publish:` default (`none`) + prod rule; the `progress.md` template has the `Publish:` field; `verification-gate.md` states publish is post-gate.
- Version is `0.11.0` across the three manifests with a README Roadmap bullet (which also seeds Feature B).
