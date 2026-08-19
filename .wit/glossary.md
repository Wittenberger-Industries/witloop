---
type: Glossary
title: "Glossary: Witloop"
description: Canonical project domain terms and the aliases to avoid.
timestamp: 2026-08-19
---

# Glossary: Witloop

**Capability table:** A matrix of harness capabilities (`plugin_root`, `subagent`, `keep_alive`, `tokens`, `ask`, `shell`, `skill_invoke`) with one column per host. Skills read stamped capabilities, not product names.
_Avoid_: host if-tree, fifth-host fork, Cursor special case

**Host probe:** Resolve-once detection of the running harness, stamped as `Host:` and `Plugin root (resolved):` in `progress.md`. Later phases read that block and never re-guess.
_Avoid_: host detection, harness sniff

**Keep-alive none:** The Cursor keep-alive capability: the chat already persists, so wit prints no `/goal` and no Autopilot relaunch. Optional `/loop` may be documented; Cursor Autopilot is not this.
_Avoid_: Cursor Autopilot, Claude /goal on Cursor
