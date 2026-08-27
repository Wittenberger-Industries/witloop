---
type: Brief
title: "/wit-setup first-run"
description: A fifth advertised command that owns first-run; scan becomes refresh-only; models and a tokens ledger toggle live in setup.
feature: 0004-setup
timestamp: 2026-08-27
---

# Brief: /wit-setup first-run

## What the user wants

Initial setup is one command. `/wit-setup` (Claude `/wit:setup`, Copilot/Grok `/wit-setup`, Codex
`$wit-setup`) is a new advertised entry point. It does everything that is first-run today: what
`/wit-scan` currently writes on a new project, plus model routing, plus a project-level tokens
ledger choice.

If `.wit/` is missing, `/wit:dev` and `/wit:rpa` (and a refresh-only `/wit:scan` that has nothing to
refresh) run setup first, then continue. `/wit:add-issues` does not.

`/wit-scan` stays user-facing. It only refreshes: `--refresh` by hand, and the existing stale-map
auto-refresh from later phases. It does not document a repo from scratch. No repo-map → tell the
user to run setup.

Models: the smart / simple / custom question that today fires on first `/wit:dev` or `/wit:rpa`
moves into setup. The file is still `.wit/models.md`, committed where written.

Tokens: setup asks once whether this project keeps a `tokens.md` ledger or skips it. Skip means
later phases do not init, finalize, or print a token table, and `check_tokens.py` is not a ship
gate. Keep means today's ledger, including honest `unavailable` on hosts that cannot measure.
`--auto` writes the simple models preset and `ledger: on` (Claude still measures). The toggle lives
in `.wit/models.md` as `ledger: on | skip`.

Example: a new Cursor checkout with no `.wit/`. User types `/wit:dev "add a button"`. Setup runs:
repo-map, constitution, plugin/alias offer, models question, ledger question, commit. Then dev
continues. Later `/wit-scan` only drift-checks.

## Acceptance (in the user's words)

- `/wit-setup` exists and is advertised next to scan, dev, rpa, add-issues.
- Missing `.wit/` at scan / dev / rpa runs setup first. add-issues does not.
- Scan first-run (repo-map, overview, architecture, constitution, greenfield commands, plugin and
  alias offer, `.wi` rename, commit) lives in setup, not in scan.
- `/wit-scan` is refresh-only (manual and auto-stale). No repo-map → send the user to setup.
- Model first-run is not in dev or rpa.
- Setup asks keep-or-skip `tokens.md`. Skip skips the ledger for the rest of the project.
- Manifests lockstep at 1.16.2.

## Scope & non-goals

- In: new `skills/setup/SKILL.md` and design notes; move scan first-run into it; shrink scan to
  `--refresh`; retarget models first-run; `ledger: on | skip` in `.wit/models.md`; ship/build/research/rpa
  honor skip; fifth advertised command plus `wit-setup` aliases; README / AGENTS / contract tests;
  ADR-0004 for the new public command; three-manifest 1.16.2.
- Out: auto-setup from add-issues; worktree policy question; keep-alive override; MoA wizard;
  changing Cursor `/goal` into a scheduler; folding setup back into scan; retarget 1.17.0;
  putting this work on PR #94.

## Constraints

- Patch release 1.16.2 (all three manifests together). Owner directed 1.16.x.
- New PR, stacked on 1.16.1 (PR #94) if that is still unmerged.
- Keep the four other entry points; scan remains user-facing as refresh.
- No em dashes in shipped text.
- Do not add a new always-loaded `${PLUGIN_ROOT}` target; project state stays in `.wit/models.md`.
- Host probe stays per session in `progress.md`, not a project file.

## Approach preferences (optional, non-binding)

- Move scan's first-run text into setup (not an orchestrator that still calls scan's old body).
- Tokens toggle in `.wit/models.md`, not a second `.wit/setup.md`.
- `--auto` on setup: simple preset + ledger on.

## Open questions for research

- Exact heading and key name in `.wit/models.md` for `ledger: on | skip`, and the cheapest string
  pins so skip is observable without a live ship run.
- Whether `/wit-scan` with no flags on an already-scanned repo is silent `--refresh` or requires
  `--refresh` on the command line.
