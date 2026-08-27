---
type: Spec
title: "/wit-setup first-run"
description: Fifth advertised command owns first-run; scan is refresh-only; ledger skip lives in .wit/models.md.
feature: 0004-setup
timestamp: 2026-08-27
---

# Spec: /wit-setup first-run

## Summary

`/wit:setup` is a fifth advertised command. It owns first-run: repo docs, constitution, plugin and
alias offer, models preset, and a keep-or-skip tokens ledger. `/wit:scan` only refreshes. Missing
`.wit/repo-map.md` at scan, dev, or rpa runs setup first. add-issues and investigation do not.
Version lockstep 1.16.2. ADR-0004.

## Goals

- One sitting creates a usable `.wit/` including models and a ledger choice.
- Scan stays a cheap refresh, still user-facing.
- Old repos without a ledger key keep today's tokens.md behavior.

## Non-goals

- Auto-setup from add-issues.
- Worktree, keep-alive, or MoA questions.
- Making Cursor `/goal` a scheduler.
- Folding setup back into scan, or hiding scan.
- A new always-loaded `${PLUGIN_ROOT}` file or `.wit/setup.md`.
- Retarget 1.17.0. This work is not PR #94.

## Acceptance criteria  (each must be testable)

1. `skills/setup/SKILL.md` exists, is user-invocable (no `user-invocable: false`), and owns first-run
   (repo-map/constitution/plugin offer, models question, ledger question). `--auto` writes simple plus
   `ledger | on`.  →  verified by: `python -m unittest tests.test_setup`
2. Scan SKILL.md is refresh-only. Bare `/wit-scan` is silent `--refresh`. Missing `repo-map.md` **runs
   setup** (does not merely tell; does not re-doc in scan). Setup writes the map; scan does not chain a
   refresh after that.  →  verified by: `python -m unittest tests.test_setup`
3. Dev:1 and rpa:2 invoke setup when `repo-map.md` is missing; they do not write models.md; they still
   resolve-once into `progress.md`. Investigation does not invoke setup. add-issues does not.
   Absent `models.md` after a map exists still runs setup's models+ledger slice (upgrade hole).
   →  verified by: `python -m unittest tests.test_setup`
4. `.wit/models.md` may contain `## Token ledger` with key `ledger` values `on` | `skip`. Absent or
   not-exact-`skip` is `on`. Skip: no `--init`, no finalize, no token table, no ship:8 `check_tokens.py`.
   →  verified by: `python -m unittest tests.test_setup`
5. Five advertised commands. README table is setup, scan, dev, rpa, add-issues. `USER_COMMANDS` is
   filesystem-alpha including `setup`. Alias `references/skill-aliases/wit-setup/` exists. Manifests
   and `RELEASE` lockstep 1.16.2. Catalog 0.2.0. Architecture entry subgraph includes setup.
   Plugin-root tell stays `skills/scan/SKILL.md`.  →  verified by:
   `python -m unittest tests.test_work_type_release tests.test_work_type_docs tests.test_setup`

## Design

ADR-0004. Copy the add-issues pattern: new skill directory plus flat alias; no command registry in
validate.py. Move scan procedure 1-7 into setup (text move, not a wrapper). Scan keeps `--refresh`
A/B/C; copy mermaid-trap rules into that remaining body. models.md heading becomes setup's first-run;
add `## Token ledger`. Honor skip in ship/build/research/rpa and the seven-file / RPA dossier lists.
Stamp `· ledger: <on|skip>` on the resolved-routing first bullet. Learning 0003-work-type-routing:
create `skills/setup/SKILL.md` in the same task that updates four-command pins so the suite stays
green. Host Grok advertises `/wit-setup` (bare `/setup` may clash).

**Locked from research (not open):**
- Tell is missing `repo-map.md`, not missing `.wit/` (add-issues may mkdir `.wit/issues/`).
- Bare scan with no flags is silent `--refresh`.
- Setup does not seed `## Model routing (resolved)`; that stays at feature seed.
- Fail-closed ledger default is `on`.
- No mid-run ledger toggle.

## Interfaces & data changes

- **APIs / signatures:** fifth slash command `/wit:setup` and aliases `/wit-setup` / `$wit-setup`.
- **Data / schema:** optional `## Token ledger` table in project `.wit/models.md`.
- **Config / env:** none
- **Dependencies:** none

## Test plan

- **Level rule:** unittest string pins; never a live Task.
- **Unit:** `tests/test_setup.py` plus existing advertised-command tests.
- **Integration / e2e:** none
- **Edge cases:** absent ledger key; `models.md` absent with map present; investigation skip;
  add-issues does not call setup; architecture `(1.16.0)` PLUGIN_ROOT caption if still present.

## Rollout & back-out

- Patch 1.16.2. Owner directed 1.16.x. Do not retarget 1.17.0. Revert the PR to restore 1.16.1.
- Stacked on PR #94 until that merges; retarget onto master afterward.
- No feature flag. Recopy `~/.agents/skills/wit-setup` on Copilot/Codex/Grok.

## Open questions

- None. Research locks above.

## Citations

[1] ADR-0004
[2] `.wit/features/0004-setup/research/fifth-command-seams.md`
[3] `.wit/features/0004-setup/research/move-surface.md`
[4] `.wit/features/0004-setup/research/ledger-skip.md`
[5] Learning `0003-work-type-routing` serial wiring after new skill files
