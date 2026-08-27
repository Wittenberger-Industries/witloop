---
type: Bootstrap
title: "Witloop: cross-platform bootstrap"
description: Entry point for non-Claude harnesses; how to read and run Witloop's skills on Codex CLI, Copilot CLI, Grok Build, and Cursor.
timestamp: 2026-06-09
tags: [witloop, bootstrap, cross-platform, codex, copilot, grok, cursor]
---

# Witloop: cross-platform bootstrap

This repository **is** Witloop (plugin id `wit`, formerly `wi`): an opinionated, low-token, spec-driven dev loop. Its capabilities
are delivered as skills under `skills/` (`scan`, `dev`, `research`, `plan`, `build`, `ship`, `brainstorm`,
`rpa`) plus three subagent prompt templates under `agents/` (`wit-code-checker`, `wit-researcher`,
`wit-task-runner`). The `wit-` prefix is a deliberate cross-platform tag (PR #15); on Claude these render
as `wit:wit-<name>`; the stutter is accepted, and the checker stays `wit-code-checker` (skills call it
*the checker*).

## Plugin root

`${PLUGIN_ROOT}` is the wit plugin root on every host, including Claude: the directory holding
`skills/`, `agents/`, and `.claude-plugin/`. Resolve it once per `references/capabilities.md`
"Plugin root" (env aliases, walk-up from cwd, then host cache). Stamp the absolute path and reuse
it. Never pass an unexpanded `${PLUGIN_ROOT}` into the shell. Do not treat Claude as a special case
that keeps the env while other hosts rewrite the placeholder.

## Tool names

wit's skills use Claude Code tool names. Before following a skill, read the mapping for this host
and apply it as you go:

- **Claude Code:** native names
- **Codex CLI:** `references/codex-tools.md`
- **GitHub Copilot CLI:** `references/copilot-tools.md`
- **Grok Build:** `references/grok-tools.md`
- **Cursor:** `references/cursor-tools.md`

## Invoking wit
- Start a feature, bug-fix, or investigation: the `dev` skill (`/wit:dev` on Claude; `/wit-dev` on Copilot / `$wit-dev` on Codex once
  scan's bootstrap has installed the flat aliases into `~/.agents/skills/`; the raw plugin forms
  `/wit dev` and `$dev` always work; or describe the request and let it auto-trigger).
  `--kind feature|bug-fix|investigation` overrides the deduced work type. An investigation is a
  read-only cited answer (no dossier, design gate, keep-alive, or PR). A bug-fix is repro-first;
  a fail-closed narrow-fix may stamp `design gate bypassed (narrow-fix)`, distinct from `--auto`
  (design-gate auto-approve). Details: `README.md`.
- File a GitHub issue ("file a bug"): the `add-issues` skill (`/wit:add-issues` on Claude; `/wit-add-issues` on
  Copilot / Grok; `$wit-add-issues` on Codex once aliases are installed).
- Bootstrap a repo first with the `scan` skill.
- Only scan/dev/rpa/add-issues are user-facing commands. The phase skills (brainstorm, research, plan,
  build, ship) carry `user-invocable: false`; hidden from slash pickers, still invoked by the
  orchestrating skill and by natural language ("ship it").
- Persistence: wit hands off to a keep-alive loop at the end of brainstorm. Print the block for the
  stamped `keep_alive` capability from `references/keep-alive.md` (Claude/Codex: `/goal`; Grok and
  Cursor: model-judged `/goal`; Copilot: Autopilot). Cursor Autopilot is not wit
  keep-alive; optional `/loop` is not either. See the host tool map. wit runs without a keep-alive too,
  just less robustly.
- Superpowers precedence (integrations.md "Who initiates", `skills/research/references/integrations.md`):
  delegation points only, never self-triggered mid-phase; wit's artifact formats always win.

These skills auto-trigger from their `description` fields. When a user's request matches one, use it.
