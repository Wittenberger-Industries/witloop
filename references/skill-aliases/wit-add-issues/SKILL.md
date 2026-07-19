---
type: Skill
name: wit-add-issues
description: >
  Alias of wit's add-issues skill for flat-skill installs (Copilot CLI /wit-add-issues, Codex CLI
  $wit-add-issues, Grok Build /wit-add-issues); forwards to the wit plugin's add-issues entry point:
  file a well-formed GitHub issue (Bug, Feature, or Task) with typed body, labels, and relationships.
---

# /wit-add-issues: alias of wit's `add-issues` skill

A forwarding alias, installed flat (`~/.agents/skills/`) so the command reads `/wit-add-issues` on
Copilot CLI and Grok Build, and `$wit-add-issues` on Codex CLI, without the plugin-namespace prefix.
The real skill ships inside the wit plugin; this file contains no filing logic of its own.

1. Locate the **wit plugin root**: the installed plugin directory (or clone) holding `skills/`,
   `agents/`, and `.claude-plugin/` (Copilot: under `~/.copilot/installed-plugins/…`; Grok: the active
   wit entry's installPath in `~/.claude/plugins/installed_plugins.json`).
2. Read `AGENTS.md` at that root (the cross-platform bootstrap), then follow
   `skills/add-issues/SKILL.md` with the user's arguments, passing `--auto` through if given.

If no wit plugin root exists, say so and point the user at
`https://github.com/Wittenberger-Industries/witloop`; do not improvise issue filing from this alias.
