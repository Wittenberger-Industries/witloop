---
type: Reference
title: "Codex CLI: tool & capability mapping for wit"
description: Claude Code → Codex CLI tool-name and capability equivalents used when running wit on Codex.
timestamp: 2026-06-09
tags: [codex, tools, portability, reference]
---

# Codex CLI: tool & capability mapping for wit

wit's skills are written with Claude Code names. On Codex CLI, use these equivalents.

## ${PLUGIN_ROOT}

Follow `references/capabilities.md` **Plugin root**. Same order on every host. Never pass an
unexpanded `${PLUGIN_ROOT}` into the shell. Codex often sets `PLUGIN_ROOT` (and sometimes
`CLAUDE_PLUGIN_ROOT`); those are step-1 aliases, not a reason to skip the stamp.

## Tools
| wit/skill says | Codex equivalent |
|---|---|
| Read / Write / Edit a file | native file tools / `apply_patch` |
| Bash / run a command | `shell` |
| Grep / Glob | native search (`shell` with `rg`/`grep`/`find`) |
| dispatch a subagent / task-runner | `spawn_agent` (parallel: multiple `spawn_agent`, or `spawn_agents_on_csv`) |
| parallel waves | `spawn_agent` bounded by `[agents] max_threads` (default 6); inline the task-runner/researcher prompt; do not rely on named-role dispatch |
| TodoWrite | `update_plan` |
| WebFetch / WebSearch | `web_search` |
| invoke a wit skill | skills load natively: `$skill-name` or `/skills` (entry points also as `$wit-setup`/`$wit-scan`/`$wit-dev`/`$wit-rpa`/`$wit-add-issues` once setup's bootstrap installs the flat aliases to `~/.agents/skills/`); just follow its instructions |
| resolve a skill's `SKILL.md` path (dispatch pointer for pinned runners) | it is under the skill's native install dir (`~/.agents/skills/<skill>/SKILL.md`, or the plugin/clone dir wit was installed from); the orchestrator resolves it once and passes it in the `[frontend]`-style dispatch |

## /goal keep-alive
Codex has a native `/goal`. Use the same condition line wit prints. For non-interactive runs, `codex exec`
with `--ask-for-approval never --sandbox workspace-write`.

## Worktrees
If the sandbox blocks branch/push (detached HEAD / externally managed worktree), do **not** fail: commit
all work in place and hand the user a suggested branch name, commit message, and PR body to apply via the
app's native controls. Detect with read-only `git rev-parse --git-dir`/`--git-common-dir` and
`git branch --show-current` before creating a worktree.

## Subagent caveat
Repo-local custom-agent *roles* are not reliably selectable by name across Codex builds. wit's build/research
fan-out passes the agent prompt inline to a generic worker, so this caveat does not block wit.
