---
type: ADR
title: "Advertise /wit:setup as the first-run command"
description: Fifth advertised command owns first-run; scan is refresh-only; project ledger toggle lives in .wit/models.md.
feature: 0004-setup
status: accepted
timestamp: 2026-08-27
---

# ADR-0004: Advertise /wit:setup as the first-run command

- **Status:** accepted
- **Date:** 2026-08-27
- **Deciders:** wit research (autonomous); design gate confirms
- **Feature:** 0004-setup

## Context

First-run is split. Scan writes `.wit/` (repo-map, constitution, plugin offer). Models.md is asked
later, on first `/wit:dev` or `/wit:rpa`. Tokens.md is always created even on hosts that cannot
measure. The advertised surface is four commands. The owner wants one first-run command, a project
choice to skip the token ledger, and scan kept as a refresh. ADR-0002 rejected a fifth *work-type*
command (`/wit:how`); it did not freeze advertised-command cardinality at four.

## Decision

We will advertise `/wit:setup` (aliases `/wit-setup` / `$wit-setup`) as a fifth user-invocable
command. It owns first-run: current scan bootstrap plus models preset plus `ledger: on | skip` in
project `.wit/models.md`. `/wit:scan` remains user-facing and is `--refresh` only (bare invoke is
silent refresh). Missing `.wit/repo-map.md` at scan / dev / rpa runs setup first. add-issues does
not. Investigation still skips setup. Absent `ledger` (or any value other than exact `skip`) is
`on`. `--auto` on setup writes the simple preset and `ledger | on`. Plugin-root detection still
keys on `skills/scan/SKILL.md`. No new always-loaded `${PLUGIN_ROOT}` file.

## Consequences

- **Positive:** One sitting configures wit. Scan stays cheap. Old repos keep today's ledger.
- **Negative / costs:** Five advertised commands; Grok's bare `/setup` may clash with a builtin
  (branded `/wit-setup` is the advertised form); existing `~/.agents/skills/` needs a recopy for
  the new alias.
- **Follow-ups:** Move scan procedure 1-7 into setup; shrink scan; retarget models.md First-run;
  honor skip in ship/build/research/rpa dossier rules; lockstep 1.16.2.

## Alternatives considered

- **Fold models and ledger into scan:** rejected; owner chose a new entry point.
- **Setup orchestrates scan's old body:** rejected; owner chose a text move.
- **Hide scan (`user-invocable: false`):** rejected; owner kept manual refresh.
- **Tokens skip as a host capability:** rejected; this is a project toggle, not Cursor vs Claude.
- **New `.wit/setup.md` or PLUGIN_ROOT file:** rejected; one store in `.wit/models.md`.

## Citations

[1] `.wit/features/0004-setup/research/fifth-command-seams.md`: copy add-issues; two tuple orders.
[2] `.wit/features/0004-setup/research/move-surface.md`: repo-map.md tell; silent refresh.
[3] `.wit/features/0004-setup/research/ledger-skip.md`: `## Token ledger` / `ledger` / fail-closed `on`.
[4] `.wit/adr/ADR-0002-route-work-by-intent.md`: no fifth work-type command; cardinality not frozen.
