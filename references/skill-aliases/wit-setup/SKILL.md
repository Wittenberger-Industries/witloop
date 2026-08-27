---
type: Skill
name: wit-setup
description: >
  Alias of wit's setup skill for flat-skill installs (Copilot CLI /wit-setup, Codex CLI $wit-setup, Grok Build
  /wit-setup); forwards to the wit plugin's setup entry point: first-run document the project and bootstrap
  wit in it. Supports "--auto" to write the simple models preset plus ledger on.
---

# /wit-setup: alias of wit's `setup` skill

A forwarding alias, installed flat (`~/.agents/skills/`) so the command reads `/wit-setup` on Copilot CLI
and Grok Build, and `$wit-setup` on Codex CLI, without the plugin-namespace prefix. The real skill ships
inside the wit plugin; this file contains no setup logic of its own.

1. Locate the **wit plugin root**: the installed plugin directory (or clone) holding `skills/`,
   `agents/`, and `.claude-plugin/` (Copilot: under `~/.copilot/installed-plugins/…`; Grok: the active
   wit entry's installPath in `~/.claude/plugins/installed_plugins.json`).
2. Read `AGENTS.md` at that root (the cross-platform bootstrap), then follow `skills/setup/SKILL.md` with
   the user's arguments, passing `--auto` through if given.

If no wit plugin root exists, say so and point the user at
`https://github.com/Wittenberger-Industries/witloop`; do not improvise the setup from this alias.
