---
type: Reference
title: "The capability table"
description: "Capability x host matrix. Skills read stamped cells in progress.md, not product-name if-trees."
timestamp: 2026-08-27
tags: [capabilities, hosts, portability, reference]
---

# The capability table

Source of host behavior. Always-loaded SKILL bodies cite **the capability table** and then
read stamped cells in `progress.md`. Adapters (`references/*-tools.md`) fill columns.
Do not add product-name if-trees in those bodies.

## Matrix

| capability | claude | codex | copilot | grok | cursor |
|---|---|---|---|---|---|
| plugin_root | resolve-once | resolve-once | resolve-once | resolve-once | resolve-once |
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

## Plugin root

`${PLUGIN_ROOT}` is the wit plugin root on every host: the directory holding `skills/`, `agents/`,
and `.claude-plugin/`. It is not Claude-specific. Do not branch "if Claude, keep the env; else
replace the placeholder." Every host including Claude follows this order, then uses the stamped
absolute path.

Resolve **once** at setup / scan / dev / rpa entry, before the first script call. Stamp
`Plugin root (resolved): <abs>` in `progress.md` (setup / scan keep it in-session). Later phases read that
stamp and never re-guess. **Never pass an unexpanded `${PLUGIN_ROOT}` into the shell.** Call scripts
as `python <abs>/skills/.../x.py`.

Order:

1. The first non-empty env that is a wit root (`skills/` + `.claude-plugin/` + `skills/scan/SKILL.md`):
   `PLUGIN_ROOT`, `WIT_PLUGIN_ROOT`, `CLAUDE_PLUGIN_ROOT`, `GROK_PLUGIN_ROOT`. Claude usually sets
   `CLAUDE_PLUGIN_ROOT`; that is one alias, not a special case.
2. Walk up from cwd (cwd first, then parents) to those same tells. A checkout of this repo wins so
   source dogfoods itself.
3. Host plugin cache. The adapter names the path: Claude `~/.claude/plugins/`; Copilot
   `~/.copilot/installed-plugins/`; Grok `~/.claude/plugins/installed_plugins.json` (Claude-compat)
   then `~/.grok/plugins/`; Cursor `~/.cursor/plugins/cache/`. Prefer plugin id `wit`.

## Host probe

At setup / scan / dev / rpa entry, detect the running harness once (`claude` | `codex` | `copilot` |
`grok` | `cursor`), resolve plugin root per **Plugin root** above, copy that host's cells into
`progress.md` as `Host:`, `Plugin root (resolved):`, and `## Capabilities (resolved)`. Later phases
read that block and never re-guess. Every host including `claude` is stamped.

## Cite

Host behavior follows **the capability table**: read the stamped cells in this feature's
`progress.md`; do not branch on product names. Point of use names the cell (`keep_alive`,
`tokens`, `ask`, ...), not the host.
