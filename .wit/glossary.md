---
type: Glossary
title: "Glossary: Witloop"
description: Canonical project domain terms and the aliases to avoid.
timestamp: 2026-08-27
---

# Glossary: Witloop

**Capability table:** A matrix of harness capabilities (`plugin_root`, `subagent`, `keep_alive`, `tokens`, `ask`, `shell`, `skill_invoke`) with one column per host. Skills read stamped capabilities, not product names.
_Avoid_: host if-tree, fifth-host fork, Cursor special case

**Host probe:** Resolve-once detection of the running harness, stamped as `Host:` and `Plugin root (resolved):` in `progress.md`. Later phases read that block and never re-guess.
_Avoid_: host detection, harness sniff

**Keep-alive none:** A `keep_alive` capability value meaning wit prints no `/goal` and no Autopilot relaunch because the chat already persists. Optional `/loop` may be documented. Not Cursor's value (Cursor is model-judged `/goal` as of 1.14.1).
_Avoid_: Cursor Autopilot

**Model-judged /goal:** The `keep_alive` family for Grok Build and Cursor: user pastes a one-line `/goal`; the agent registers it and self-completes after judging the done-condition (`update_goal` on Grok; `CreateGoal` then `UpdateGoal` on Cursor). Not Claude/Codex's hard predicate.
_Avoid_: Cursor Autopilot, keep-alive none on Cursor

**Work type:** The intent class `feature`, `bug-fix`, or `investigation` that selects a Witloop execution path before feature-folder classification.
_Avoid_: task type, route kind

**Safety fact:** The one claim a change is safe because of. At ship it is proven by a command run this session, marked `unproven`, or `n/a` for a docs-only PR. A green suite does not replace it.
_Avoid_: blast-radius writeup, gate verdict, CONCERNS

**Unproven:** An honest, visible row meaning a named safety fact or extra check was not exercised this session. Not a silent PASS, not a skipped repo-map gate command, and not a WAIVED fail.
_Avoid_: CONCERNS, waived, skipped

**Setup:** The advertised first-run command (`/wit:setup`). It creates `.wit/` and writes repo docs, constitution, models, and the tokens ledger toggle. Missing `.wit/` at scan / dev / rpa runs this first.
_Avoid_: first-run scan, bootstrap scan

**Scan:** Refresh of an already-written `.wit/` map (`--refresh`, including stale auto-refresh). It does not create a project from scratch.
_Avoid_: setup, bootstrap
