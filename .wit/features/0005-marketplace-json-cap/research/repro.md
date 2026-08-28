---
type: Research Note
title: "Repro: plugin descriptions over 1024 with no validate.py guard"
description: Evidence that DESC_CAP applies only to SKILL.md; the three plugin JSON descriptions exceed 1024 and are not flagged.
feature: 0005-marketplace-json-cap
timestamp: 2026-08-28
valid_until: 2026-09-27
---

# Repro: plugin descriptions over 1024

**Surface:** `python scripts/validate.py`
**Log:** `.wit/features/0005-marketplace-json-cap/.logs/repro-before.txt`

## Observed (this session)

- marketplace.json wit `description`: 1357 chars (333 over)
- `.claude-plugin/plugin.json` `description`: 1396 chars (372 over)
- `.codex-plugin/plugin.json` `description`: 1396 chars (372 over)
- marketplace.json whole file: 2184 chars (not in scope; brief caps fields, not the file)
- `DESC_CAP = 1024` in `scripts/validate.py` is applied only to `skills/**/SKILL.md` and skill-alias SKILL.md (comment 7a)
- validate.py output this session: 20 FAIL issues, all `docs/skill-ideas/**` OKF frontmatter. Zero issues mention plugin/marketplace description length.

Unrelated confounder: untracked `docs/skill-ideas/` files fail OKF and make validate.py exit 1. That is not this bug. The missing-guard evidence is the absence of a description-cap error while the three fields are over 1024.

## Hypotheses ruled out

- Whole-file 1024 cap: user chose field-level cap on the three plugin descriptions.
- Skill description cap broken: SKILL.md 7a still exists and tests pin DESC_CAP at 1024 (`tests/test_work_type_routing.py`).
- Manifests missing description keys: all three parse and have long strings.
- Host-specific marketplace schema: same three files are already in the lockstep set.

## Surviving mechanism

Plugin `description` strings grew across host/command releases (five hosts, five `/wit:` commands, keep-alive, RPA process dump) with no JSON-side length check. `DESC_CAP` never walks `.claude-plugin/*.json` or `.codex-plugin/plugin.json`. Marketplace/install validation (Copilot and Claude plugin description ceilings) is therefore only caught by humans, not CI.

## Pattern to reuse

Extend the existing `DESC_CAP` check to the three plugin description fields. `tests/test_work_type_release.py` already loads those manifests and requires five commands + five hosts + keep-alive in the two plugin descriptions. Shrink the prose, keep those pins, bump lockstep to 1.16.3.

## Commands

```
python scripts/validate.py
python -c "measure plugin description lengths"
```
