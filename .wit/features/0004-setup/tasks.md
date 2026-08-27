---
type: Task List
title: "Tasks: /wit-setup first-run"
description: Small ordered tasks (each with files + verify) and the build waves for this feature.
feature: 0004-setup
timestamp: 2026-08-27
---

# Tasks: /wit-setup first-run

> Ordered. Each task is small enough for one focused sitting and ends green.
> plan via superpowers:writing-plans (captured in wit `tasks.md` format).

## Task 1: Setup skill plus five-command lockstep   [backend]
- **Files:** `tests/test_setup.py`, `skills/setup/SKILL.md`, `docs/design-notes/setup.md`,
  `tests/test_work_type_release.py`, `tests/test_work_type_docs.py`, `README.md`, `AGENTS.md`,
  `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (wit plugin entry only),
  `.codex-plugin/plugin.json`, `.wit/overview.md`, `.wit/architecture.md`, `.wit/repo-map.md`
- **Do:** Create `tests/test_setup.py` (failing asserts first; no `import validate`). Then
  `skills/setup/SKILL.md`: user-invocable (omit `user-invocable: false`); first-run body moved from
  scan procedure 1-7 (repo-map, constitution, greenfield, plugin offer, `.wi` rename, commit,
  report) plus models preset plus ledger question; `--auto` → simple + `ledger | on`; missing
  `repo-map.md` is the empty-project path. Description auto-triggers include "set up wit here" and
  "bootstrap wit" (moved off scan). Sync `docs/design-notes/setup.md`. Same sitting: five
  advertised commands so the glob stays green. `USER_COMMANDS = ("add-issues", "dev", "rpa", "scan",
  "setup")`. README `ADVERTISED = ("setup", "scan", "dev", "rpa", "add-issues")` (setup-first).
  AGENTS "Only setup/scan/dev/rpa/add-issues". `RELEASE = "1.16.2"` and three plugin versions.
  Overview current 1.16.2. Architecture `subgraph entry` adds setup; do not change architecture's
  `(1.16.0)` PLUGIN_ROOT caption. Catalog 0.2.0. Plugin-root tell stays `skills/scan/SKILL.md`.
  Manifest descriptions include `/wit:setup`. `assertNotIn` em dash on files this task edits.
- **Verify:** `python -m unittest tests.test_setup tests.test_work_type_release tests.test_work_type_docs`
- **Depends on:** -

## Task 2: Scan is refresh-only   [backend]
- **Files:** `tests/test_setup.py`, `skills/scan/SKILL.md`, `docs/design-notes/scan.md`,
  `references/workflow.md`, `references/capabilities.md`,
  `skills/research/references/integrations.md`, `skills/add-issues/SKILL.md`
- **Do:** Append class `ScanRefreshTests`. Shrink scan to `--refresh` A/B/C. Bare invoke (no flags)
  is silent `--refresh`. Missing `repo-map.md` → **run setup** (do not merely tell; do not re-doc
  in scan; do not chain a refresh after setup writes the map). Copy mermaid-trap rules into the
  remaining refresh body so "rules above" is not dangling. Description no longer says it
  bootstraps a new `.wit/` from scratch. One-line retarget where scan is still called first-run:
  `references/workflow.md`, `references/capabilities.md`,
  `skills/research/references/integrations.md`, `skills/add-issues/SKILL.md` (only if they name
  scan as bootstrap). Sync design notes. `assertNotIn` em dash on files this task edits.
- **Verify:** `python -m unittest tests.test_setup`
- **Depends on:** 1

## Task 3: Alias and bootstrap copy list   [docs]
- **Files:** `tests/test_setup.py`, `references/skill-aliases/wit-setup/SKILL.md`,
  `skills/scan/references/plugin-bootstrap.md`, `references/grok-tools.md`,
  `references/copilot-tools.md`, `references/codex-tools.md`
- **Do:** Append class `SetupAliasTests`. Add `wit-setup` forwarder (copy wit-scan; pass `--auto`).
  Plugin-bootstrap copy list includes `wit-setup/` (offer still runs from setup's first-run, this
  file stays the alias table). Alias description forwards to setup, not "bootstrap a folder".
  Host maps mention `/wit-setup`. Grok notes branded `/wit-setup` if
  bare `/setup` clashes. `assertNotIn` em dash on files this task edits.
- **Verify:** `python -m unittest tests.test_setup`
- **Depends on:** 2

## Task 4: Dev/rpa invoke setup; models first-run moves   [backend]
- **Files:** `tests/test_setup.py`, `skills/dev/SKILL.md`, `skills/rpa/SKILL.md`,
  `skills/dev/references/investigation.md`, `references/models.md`,
  `docs/design-notes/dev.md`, `docs/design-notes/rpa.md`
- **Do:** Append class `SetupInvokeTests`. Missing `repo-map.md` at scan (already task 2), dev, and
  rpa → run setup first (forward `--auto` when present), then continue. add-issues unchanged (assert it). Investigation still
  exits before setup. Drop models *write* from dev:1 / rpa:2; resolve-once stays. models.md
  "First-run setup" is a setup entry (plus `--auto` simple + ledger on). Heading `## Token ledger`
  with key `ledger` (`on` | `skip`); absent or not-exact-`skip` is `on`. Absent `models.md` with a
  map present → setup models+ledger slice only. Sync design notes. `assertNotIn` em dash on files
  this task edits.
- **Verify:** `python -m unittest tests.test_setup`
- **Depends on:** 1

## Task 5: Honor ledger skip   [backend]
- **Files:** `tests/test_setup.py`, `skills/ship/SKILL.md`, `skills/build/SKILL.md`,
  `skills/research/SKILL.md`, `skills/rpa/SKILL.md`, `skills/dev/SKILL.md`,
  `skills/research/references/wit-directory.md`, `skills/rpa/references/rpa-directory.md`,
  `skills/scan/references/constitution-template.md`,
  `skills/rpa/references/rpa-constitution-template.md`,
  `skills/rpa/references/verification-gate.md`,
  `skills/rpa/references/build-uipath.md`, `skills/rpa/references/build-maestro.md`
- **Do:** Append class `LedgerSkipTests`. When resolved-routing (or `.wit/models.md`) is `ledger:
  skip`: do not `--init`, do not `finalize_tokens.py`, do not print a token table, do not run
  ship:8 `check_tokens.py`. Seven-file dossier and RPA "tokens.md is mandatory" gain a skip
  carve-out. Stamp `· ledger: <on|skip>` on the wit-directory `progress.md` resolved-routing first
  bullet. Retarget remaining "scan is first-run" lines in wit-directory.md. `check_tokens.py`
  itself stays format-only (no `--skip` flag). Fail-closed: anything
  but exact `skip` is `on`. Do not support mid-run toggle. `assertNotIn` em dash on files this
  task edits. This test file still must not import validate.
- **Verify:** `python -m unittest tests.test_setup`
- **Depends on:** 4

## Waves  (derived from Depends on + Files: what build runs concurrently)
- Wave 1: task 1
- Wave 2: task 2
- Wave 3: task 3
- Wave 4: task 4
- Wave 5: task 5
