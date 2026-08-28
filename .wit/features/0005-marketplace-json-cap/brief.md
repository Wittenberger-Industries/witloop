---
type: Brief
title: Marketplace plugin descriptions under 1024 chars
description: Each plugin description field in marketplace.json, plugin.json, and the Codex manifest stays at or under 1024 characters, enforced, shipped as 1.16.3.
feature: 0005-marketplace-json-cap
timestamp: 2026-08-28
---

# Brief: Marketplace plugin descriptions under 1024 chars

## What the user wants
The three plugin `description` fields (`.claude-plugin/marketplace.json` wit entry, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`) must stay at or under 1024 characters. 1.16.2 is over that limit (marketplace wit description 1357 chars; plugin.json and Codex 1396). Skill `description` fields already have this cap; these three do not. Version ships as **1.16.3**.

## Acceptance (in the user's words)
- Each of the three plugin `description` fields is ≤ 1024 characters.
- A description over 1024 fails the same structure gate that already caps SKILL.md descriptions.
- Manifest versions lockstep at 1.16.3.

## Scope & non-goals
- In: shorten the three description texts; add a 1024-char guard; bump the three plugin versions to 1.16.3 (patch).
- Out: a whole-file size cap on marketplace.json; SKILL.md or agent description changes; minifying JSON; dropping keywords; advertised-command or host changes.

## Constraints
- Patch 1.16.3; three-manifest version lockstep.
- No em-dashes.
- `python scripts/validate.py` remains the structure gate.
- Public advertised commands and hosts do not change (descriptions may be shorter, not fewer commands).

## Approach preferences (optional, non-binding)
- Mirror the existing SKILL.md `DESC_CAP = 1024` pattern in validate.py rather than a new checker.

## Repro contract
- **Surface:** `python scripts/validate.py`
- **Trigger:** current 1.16.2 texts (marketplace wit description 1357 chars; plugin.json and Codex 1396).
- **Observed:** over 1024; validate.py does not flag plugin/marketplace descriptions.
- **Expected:** each of the three fields ≤ 1024; validate.py errors if any exceed.
- **Force strategy:** n/a (deterministic file contents).

## Open questions for research
- None. How to word the shortened descriptions and where the tests live is for research/plan.
