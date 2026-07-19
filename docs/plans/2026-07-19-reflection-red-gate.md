---
type: Plan
title: "Stamped failure Reflection at every red gate (#81)"
description: "Append a stamped Reflection Log line before every red-path fix loop; ship §4 treats Reflections as mandatory compound candidates. Ships as wit v1.13.2."
timestamp: 2026-07-19
tags: [plan, ship, build, reflection, verification-gate]
---

# Stamped failure Reflection (#81) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** At every red (local gate, review BLOCKER, remote checks), append one stamped Reflection line to `progress.md` before fixing; ship §4 treats those lines as mandatory compound candidates. Ship as wit `v1.13.2`.

**Architecture:** Literal additive edits to three skill/reference files. Format uses a hyphen (not em-dash) for the earlier-catch clause per roadmap standing rule.

**Tech Stack:** Markdown skills; `scripts/validate.py`.

**Design:** Issue #81 body; packaging already locked (PR2 of the 2026-07-19 set).

## Global Constraints

- Version bump: `1.13.1` → `1.13.2` on all three manifests together.
- No em-dashes in shipped text, commits, or PR bodies. Issue's `— earlier catch:` becomes `- earlier catch:`.
- No new agents, gates, or scripts.
- No live dry-run in this PR (deferred to post-#82 full dry-run; name that on roadmap).
- Additive only on hotspot files (`ship/SKILL.md`, `build/SKILL.md`, verification-gate).

## File map

| File | Change |
|------|--------|
| `skills/ship/references/verification-gate.md` | Step 0 on red: write Reflection, then existing options |
| `skills/ship/SKILL.md` | §2 BLOCKER loop entry; §8 remote red; §4 compound consumption |
| `skills/build/SKILL.md` | §3 plan-wrong note → Reflection format |
| Three manifests + `docs/roadmap.md` | `1.13.2`; queue update |

## Format (verbatim for all write sites)

```markdown
- <ts> **Reflection** <check that failed>: <what went wrong, one clause> - earlier catch: <phase | none>
```

`<ts>` = full OS-clock ISO stamp. Green runs write none. Remote re-run flakes write none (once per distinct failure only).

---

### Task 1: verification-gate red path step 0

**Files:**
- Modify: `skills/ship/references/verification-gate.md` (`## When the gate is red`)
- Test: grep + `python scripts/validate.py`

- [ ] **Step 1: Add step 0 before existing options**

Replace the red section so writing the Reflection is mandatory first:

```markdown
## When the gate is red

Stop. A red gate is information, not an obstacle to route around. **Before any fix option**, append one
stamped Log line to the feature's `progress.md`:

`- <ts> **Reflection** <check that failed>: <what went wrong, one clause> - earlier catch: <phase | none>`

(`<ts>` from the OS clock; `earlier catch` is the phase that should have caught it - research, plan,
build, or `none`.) Then options, in order of preference:

1. Fix the code (loop back to the build phase for the failing task).
2. If a test is genuinely wrong, change it **deliberately** and say why in the PR; never delete a test
   just to go green.
3. If the failure shows the plan was wrong, amend `spec.md`/`tasks.md` and rebuild the affected part.
```

- [ ] **Step 2: Verify**

```powershell
Select-String -Path skills/ship/references/verification-gate.md -Pattern "\*\*Reflection\*\*"
Select-String -Path skills/ship/references/verification-gate.md -Pattern "earlier catch:"
python scripts/validate.py
```

- [ ] **Step 3: Commit**

```powershell
git add skills/ship/references/verification-gate.md
git commit -m "feat(ship): Reflection line before local red-gate fixes"
```

---

### Task 2: ship §2 / §8 / §4 Reflection wiring

**Files:**
- Modify: `skills/ship/SKILL.md` (§2 BLOCKER→build loop; §8 remote red; §4 Compound)
- Test: grep + validate

- [ ] **Step 1: §2 - Reflection on BLOCKER loop entry**

Where BLOCKER sends the feature back to build, require a Reflection line as part of loop entry (before the fix round), same format as Task 1.

- [ ] **Step 2: §8 - Reflection on remote checks red**

In the **Red** bullet under remote checks, require one Reflection per distinct failure before the fix loop; a re-run flake gets none.

- [ ] **Step 3: §4 - mandatory compound input**

In Compound, after the harvest bar / before or within the harvest guidance, add:

```markdown
`progress.md` **Reflection** lines from this run are mandatory candidate lessons. A Reflection that
repeats a previous feature's reflection (visible via the learnings index) is called out as recurring -
prime promotion material for the counters lifecycle.
```

- [ ] **Step 4: Verify**

```powershell
Select-String -Path skills/ship/SKILL.md -Pattern "\*\*Reflection\*\*"
Select-String -Path skills/ship/SKILL.md -Pattern "mandatory candidate lessons"
Select-String -Path skills/ship/SKILL.md -Pattern "earlier catch:"
python scripts/validate.py
```

- [ ] **Step 5: Commit**

```powershell
git add skills/ship/SKILL.md
git commit -m "feat(ship): Reflection on review/remote red; compound harvest"
```

---

### Task 3: build §3 plan-wrong note → Reflection format

**Files:**
- Modify: `skills/build/SKILL.md` (§3 When a task fails)
- Test: grep + validate

- [ ] **Step 1: Replace the plan-wrong note**

Change the sentence about noting plan-wrong in progress.md to use the Reflection format (adds `earlier catch:` attribution). Keep the amend-spec/tasks behavior.

Example replacement for the plan-wrong clause:

```markdown
If the failure reveals the **plan** was wrong, stop and amend: append a stamped Reflection line to
`progress.md` (`- <ts> **Reflection** <check that failed>: <what went wrong, one clause> - earlier catch: plan`),
update `spec.md`/`tasks.md`, and continue; never let code silently drift from the spec.
```

- [ ] **Step 2: Verify**

```powershell
Select-String -Path skills/build/SKILL.md -Pattern "\*\*Reflection\*\*"
python scripts/validate.py
```

- [ ] **Step 3: Commit**

```powershell
git add skills/build/SKILL.md
git commit -m "feat(build): plan-wrong failures use Reflection Log format"
```

---

### Task 4: version 1.13.2, roadmap, PR

**Files:**
- Modify: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (wit plugin), `.codex-plugin/plugin.json`
- Modify: `docs/roadmap.md`
- Create: this plan under `docs/plans/` (already being written); optional mirror under `docs/superpowers/plans/`
- PR via `gh`

- [ ] **Step 1: Bump to `1.13.2`** on all three manifests (not marketplace catalog `0.2.0`).

- [ ] **Step 2: Roadmap** - mark #81 shipping as v1.13.2; leave #82 + full dry-run (incl. #81 dry-run AC) for v1.13.3. Name deferred dry-run AC with a pointer.

- [ ] **Step 3: validate.py** green.

- [ ] **Step 4: Commit** plan + version + roadmap.

- [ ] **Step 5: Push and open PR** with temp `--body-file`:

```
## Summary
- Stamped Reflection Log line before every red-path fix (local gate, review BLOCKER, remote checks)
- build §3 plan-wrong notes use the same format
- ship §4 treats Reflection lines as mandatory compound candidates (recurring call-out)
- Version bump 1.13.1 → 1.13.2

Closes #81

## Test plan
- [ ] python scripts/validate.py green
- [ ] Grep confirms Reflection + earlier catch in verification-gate, ship, build
- [ ] Dry-run AC deferred to post-#82 full dry-run (roadmap pointer)
```

Branch: `feat/reflection-red-gate-81`.

---

## Self-review

1. Spec coverage: three red paths + §4 consumption + build clause + version → Tasks 1-4.
2. Em-dash: format uses hyphen `- earlier catch:`.
3. Dry-run deferred with roadmap pointer.
