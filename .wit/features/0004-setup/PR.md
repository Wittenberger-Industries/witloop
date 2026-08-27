---
type: PR Description
title: /wit-setup first-run
description: Fifth command owns first-run
feature: 0004-setup
timestamp: 2026-08-27
---

## feat: /wit-setup first-run (v1.16.2)

### Summary

`/wit:setup` is a fifth advertised command. It owns first-run: repo docs, constitution, plugin
offer, models preset, and a keep-or-skip tokens ledger. `/wit:scan` is refresh-only (bare invoke
is silent `--refresh`). Missing `.wit/repo-map.md` at scan, dev, or rpa runs setup first.
`ledger: skip` in project `.wit/models.md` means no tokens.md init, finalize, token table, or
ship:8 `check_tokens.py`. Version lockstep 1.16.2. ADR-0004.

### Acceptance criteria

- [x] Setup skill is user-invocable and owns first-run; `--auto` writes simple plus `ledger | on`  (verified by `python -m unittest tests.test_setup`)
- [x] Scan is refresh-only; missing `repo-map.md` runs setup  (verified by `python -m unittest tests.test_setup`)
- [x] Dev and rpa invoke setup on a missing map; investigation and add-issues do not  (verified by `python -m unittest tests.test_setup`)
- [x] `ledger: skip` is fail-closed `on` unless exact skip; honor sites skip init/finalize/table/gate  (verified by `python -m unittest tests.test_setup`)
- [x] Five advertised commands; manifests and `RELEASE` 1.16.2; catalog 0.2.0; plugin-root tell stays scan  (verified by `python -m unittest tests.test_work_type_release tests.test_work_type_docs tests.test_setup`)

### Changes

- New `skills/setup/SKILL.md` and `references/skill-aliases/wit-setup/`.
- Scan shrinks to `--refresh` A/B/C; missing map runs setup.
- Models first-run and `## Token ledger` live in setup; resolve-once stays at feature seed.
- Ship/build/research/rpa honor `ledger: skip` without teaching `check_tokens.py` a `--skip` flag.

### Testing

- Format: `n/a - not configured`
- Lint: `n/a - not configured`
- Typecheck: `n/a - not configured`
- Tests: `python -m unittest discover -s tests` → 369 OK (after advertised-scan retarget). Ship:1
  was 357 OK before those pins. Lockstep slice:
  `python -m unittest tests.test_setup tests.test_work_type_release tests.test_work_type_docs` → 92 OK.
- Plugin structure: `python scripts/validate.py` on the tracked tree → OK. Local working-tree
  validate fails OKF on untracked `docs/skill-ideas/` drafts (not in this PR).

### Safety fact

- Claim: skill-and-doc contract plus unittest string pins (setup owns first-run; scan refresh-only
  at the skill and on advertised surfaces; ledger skip honored; five-command 1.16.2 lockstep).
- Proof: this-session `python -m unittest discover -s tests` (369 OK). Also
  `python -m unittest tests.test_setup tests.test_work_type_release tests.test_work_type_docs` (92 OK).
- Not-run: none

### Verification

Result-mode checker: no BLOCKER. WARNINGs 1-3 (advertised scan-as-bootstrap, glossary directory
tell, leftover scan first-run pointers) were fixed at ship:3 and pinned in `tests/test_setup.py`
`AdvertisedScanRetargetTests`. Remaining INFOs: MoA ledger has no skip clause (research listed
recommended, not required; no covering AC); owner-directed patch 1.16.2 vs constitution minor.
Learnings: `0003-work-type-routing` honored; `0003-blast-radius-proof` not triggered.

### Risk & rollout

Patch 1.16.2. Revert this PR to restore 1.16.1. Recopy `~/.agents/skills/wit-setup` on
Copilot/Codex/Grok. No feature flag. PR #94 already merged; this branch was rebased onto master.

### Decisions

- [ADR-0004](../../adr/ADR-0004-setup-owns-first-run.md): fifth command owns first-run; scan is
  refresh-only; ledger toggle in `.wit/models.md`.

## Rules inventory

This PR changes rule text (skills and references agents load). Constitution: public skill contract
needs an ADR (ADR-0004 accepted). Three-manifest lockstep 1.16.2. Plugin-root tell stays
`skills/scan/SKILL.md`. No new always-loaded PLUGIN_ROOT file. Agent charters untouched.

Loaded-alone:

- `skills/setup/SKILL.md`: first-run owner; `--auto` simple plus ledger on; tell is missing
  `repo-map.md`.
- `skills/scan/SKILL.md`: refresh only; missing map runs setup.
- `skills/dev/SKILL.md` / `skills/rpa/SKILL.md`: invoke setup; no models.md write; ledger skip
  honored at report/init.
- `skills/ship/SKILL.md` / `skills/build/SKILL.md` / `skills/research/SKILL.md`: skip means do not
  init, finalize, print the token table, or run ship:8 `check_tokens.py`.
- `references/models.md`: `## Token ledger`; interactive write omits the heading until setup:7.
- `references/skill-aliases/wit-scan/SKILL.md`: refresh, not bootstrap.
- Host maps: alias copy is setup's bootstrap; Copilot invoke list includes `/wit setup`.
