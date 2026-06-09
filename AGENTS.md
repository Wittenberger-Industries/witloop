# wi — cross-platform bootstrap

This repository **is** the wi plugin: an opinionated, low-token, spec-driven dev loop. Its capabilities
are delivered as skills under `skills/` (`scan`, `dev`, `research`, `plan`, `build`, `ship`, `brainstorm`,
`rpa`) plus two subagent prompt templates under `agents/`.

## If you are not Claude Code
wi's skills use Claude Code tool names and the `${CLAUDE_PLUGIN_ROOT}` variable. Before following a skill,
read the mapping for your platform and apply it as you go:

- **Codex CLI:** `references/codex-tools.md`
- **GitHub Copilot CLI:** `references/copilot-tools.md`

Key rule: **`${CLAUDE_PLUGIN_ROOT}` is this repo's root** (the directory holding `skills/`, `agents/`,
`.claude-plugin/`). Resolve every `${CLAUDE_PLUGIN_ROOT}` path against it.

## Invoking wi
- Start a feature: the `dev` skill (`/wi:dev` on Claude, `/dev` or `$dev` elsewhere, or describe the
  feature and let it auto-trigger).
- Bootstrap a repo first with the `scan` skill.
- Persistence: wi hands off to a keep-alive loop at the end of brainstorm — Claude/Codex use built-in
  `/goal`; Copilot uses Autopilot flags (see the tool map). wi runs without it too, just less robustly.

These skills auto-trigger from their `description` fields. When a user's request matches one, use it.
