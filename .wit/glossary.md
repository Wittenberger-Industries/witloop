---
type: Glossary
title: "Glossary: Witloop"
description: Canonical project domain terms and the aliases to avoid.
timestamp: 2026-08-20
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
