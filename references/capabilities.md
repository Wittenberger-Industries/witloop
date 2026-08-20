---
type: Reference
title: "The capability table"
description: "Capability x host matrix. Skills read stamped cells in progress.md, not product-name if-trees."
timestamp: 2026-08-20
tags: [capabilities, hosts, portability, reference]
---

# The capability table

Source of host behavior. Always-loaded SKILL bodies cite **the capability table** and then
read stamped cells in `progress.md`. Adapters (`references/*-tools.md`) fill columns.
Do not add product-name if-trees in those bodies.

## Matrix

| capability | claude | codex | copilot | grok | cursor |
|---|---|---|---|---|---|
| plugin_root | native env | compat env | install or clone | resolve-once | resolve-once (env if wit root, walk-up cwd, then host cache) |
| subagent | named Agent/Task | inline spawn_agent | task / fleet | inline spawn_subagent | Task wit-* when listed else inline agents/*.md |
| keep_alive | predicate_goal | predicate_goal | relaunch | model_judged_goal | model_judged_goal |
| tokens | token_report.py | unavailable | unavailable | grok_token_report.py | unavailable |
| ask | AskUserQuestion | unknown | unknown | ask_user_question | AskQuestion |
| shell | Bash + python fallback | shell | bash | run_terminal_command | Python scripts (POSIX or PowerShell) |
| skill_invoke | plugin skills + aliases | native $skill + aliases | /wit skill + aliases | session list + Claude registry | plugin skills + natural-language auto-trigger |

`keep_alive` values: `predicate_goal` (Claude/Codex `/goal`), `model_judged_goal` (Grok and Cursor
`/goal`), `relaunch` (Copilot Autopilot), `none` (no current host; chat persists, no `/goal`).
Codex/Copilot `ask` is `unknown`: those adapters have no Ask row; do not invent a tool name.
Procedure for a cell lives in the host adapter, not here.

## Host probe

At scan / dev / rpa entry, detect the running harness once (`claude` | `codex` | `copilot` |
`grok` | `cursor`), resolve plugin root, copy that host's cells into `progress.md` as
`Host:`, `Plugin root (resolved):`, and `## Capabilities (resolved)`. Later phases read that
block and never re-guess. Every host including `claude` is stamped.

Plugin-root order: (1) `CLAUDE_PLUGIN_ROOT` if it is a wit root (has `skills/` +
`.claude-plugin/`), (2) walk-up from cwd to those tells, (3) host plugin cache.
Cwd-as-wit-root beats marketplace cache so a source checkout dogfoods itself.

## Cite

Host behavior follows **the capability table**: read the stamped cells in this feature's
`progress.md`; do not branch on product names. Point of use names the cell (`keep_alive`,
`tokens`, `ask`, ...), not the host.
