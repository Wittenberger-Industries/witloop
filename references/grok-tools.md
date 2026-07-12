---
type: Reference
title: "Grok Build: tool & capability mapping for wi"
description: "Claude Code to Grok Build (grok CLI) tool-name and capability equivalents used when running wi on Grok, plus the mandatory resolve-once plugin-root protocol and the model-judged keep-alive pointer."
timestamp: 2026-07-12
tags: [grok, tools, portability, reference]
---

# Grok Build: tool & capability mapping for wi

wi's skills are written with Claude Code names. On Grok Build (`grok` CLI), use these equivalents.

Cells marked `(SPIKE S-N)` are confirmed on a real Grok Build session before this file ships (the recon
spike in `docs/plans/2026-07-12-43-grok-build-platform.md`); everything else is final.

## ${CLAUDE_PLUGIN_ROOT}: resolve once, then use an absolute path (mandatory)

`${CLAUDE_PLUGIN_ROOT}` means the **wi plugin root**: the directory holding `skills/`, `agents/`, and
`.claude-plugin/`. Grok aliases the env var for hooks only, and it can read empty in a tool shell
(SPIKE S1), so wi must resolve it, not rely on the variable:

1. Resolve **once** at the start of any wi entry skill (scan / dev / rpa), before the first
   `${CLAUDE_PLUGIN_ROOT}` script call.
2. **Never pass an unexpanded `${CLAUDE_PLUGIN_ROOT}` into the shell.** Resolution order:
   1. `$CLAUDE_PLUGIN_ROOT` if non-empty and it contains `skills/` + `.claude-plugin/`.
   2. `$GROK_PLUGIN_ROOT` / `$PLUGIN_ROOT` if they look like the wi root.
   3. The loaded wi plugin path from `grok inspect` / plugin list.
   4. Walk up from cwd for a dir holding both `skills/scan/SKILL.md` and `.claude-plugin/plugin.json`
      (clone / `--plugin-dir`).
3. Use that **absolute path** in every `python <root>/skills/.../*.py` call for the rest of the run. If
   `export` does not survive across Grok shell tool calls (SPIKE S2), absolute-path-per-call is the only
   guarantee; if it does, a one-time `export CLAUDE_PLUGIN_ROOT=<resolved>` is a convenience, not a
   substitute for step 3.

This is the same root rule Copilot uses (`references/copilot-tools.md` "${CLAUDE_PLUGIN_ROOT}"), made a
hard protocol because Grok shells out. The script-invocation fallback is `references/workflow.md`
"Script invocation".

## Install & enable

`grok plugin install Wittenberger-Industries/wi-plugin --trust` (SPIKE S3: confirm the exact flags and
whether `--trust` / a post-install enable step are required), then enable if plugins are disabled by
default. Grok loads Claude marketplace plugins (skills, agents, hooks, `AGENTS.md`) with zero config; the
clone + `--plugin-dir` path is the fallback. Publishing to the official catalog is a separate PR to
`xai-org/plugin-marketplace`.

## Tools

Exact ids are read from `grok inspect` on the spike (SPIKE S3/S7). The `?`-flagged rows differ most across
Grok Build versions.

| wi/skill says | Grok equivalent (confirm on spike) |
|---|---|
| Read a file | `read_file` |
| Write / create a file | `write` (some builds `create_file`) ? |
| Edit a file | `search_replace` |
| Bash / run a command | `run_terminal_command` |
| Grep / Glob | `grep` / file search (`run_terminal_command` with `rg`/`grep`/`find`) |
| dispatch a subagent / task-runner | `spawn_subagent` (built-in types `general-purpose \| explore \| plan`, depth limit 1; `isolation`, `background`, `capability_mode` optional) |
| parallel waves | multiple `spawn_subagent` calls in one turn; inline the runner/researcher prompt (do not rely on named-role dispatch) |
| TodoWrite | `todo_write` |
| WebSearch | `web_search` |
| WebFetch | `web_fetch` or the build's fetch-style tool, if present; else `web_search` with a URL ? |
| invoke a wi skill | skills load natively: `/scan`, `/dev`, `/rpa` (SPIKE S4; qualified `/wi:scan` if a name collides), or natural-language auto-trigger; flat `wi-*` aliases give a one-token form once scan's bootstrap installs them |
| resolve a skill's `SKILL.md` path (dispatch pointer for pinned runners) | it is under the skill's install dir (the resolved wi root's `skills/<skill>/SKILL.md`, or `~/.agents/skills/<skill>/SKILL.md` for flat aliases); the orchestrator resolves it once and passes it in the `[frontend]`-style dispatch |

## Subagent dispatch (inline, Codex-style)

Grok's tool is `spawn_subagent`. Dispatch each wi role as `general-purpose` with the role's contract
inlined into the prompt; do **not** assume the named `wi-task-runner` agent resolves (SPIKE S7):

| wi role | Grok dispatch |
|---------|----------------|
| `wi-task-runner` | `general-purpose`, prompt = inlined `agents/wi-task-runner.md` contract + task skeleton; **shared** feature worktree (`isolation: none`) |
| `wi-researcher` | `explore` or `general-purpose` + read-only; inline researcher contract |
| `wi-code-checker` | `general-purpose`; inline checker contract |

The named `agents/*.md` files are never edited and never assumed to register as Grok agents; the prompt
content is always inline, exactly as on Codex (`skills/build/references/worktrees-and-subagents.md`).

## Worktrees (three mechanisms, one canonical)

- **wi feature worktree** (`git worktree add -b wi/<slug> ...`) is canonical; the orchestrator is the sole
  committer.
- **Grok session `-w`** is an optional outer shell; do **not** nest a wi feature worktree inside it
  (SPIKE S8). If already inside a session worktree (detached HEAD / linked worktree), follow the sandboxed
  variant in `skills/build/references/worktrees-and-subagents.md`: commit in place, hand the user a
  branch name + commit + PR text.
- **Subagent `isolation: worktree`** is the level-2 escalate only (file collision / non-parallel-safe
  tests), matching the existing escalation ladder.

## Keep-alive

Grok's `/goal` is **model-judged**, not a hard predicate: see the Grok Build branch in
`references/keep-alive.md`. Reuse the condition line as the definition of done; the unattended-run warning
applies.

## Models & usage

`grok models` lists ids (`grok-4.5` default, `grok-composer-2.5-fast` fast; SPIKE S6). Pass the model on
`spawn_subagent` / the session per `references/models.md` "Platform model resolution (non-Claude hosts)".
Usage: `/usage`; `token_report.py`'s Claude transcript parse does not apply, so per-subagent figures are
`unavailable` and durations come from wi's own stamps, the same as the Copilot ledger note.

## Permissions (unattended)

`--always-approve` / `--yolo` and headless `-p` / `--max-turns` / `--continue` run Grok unattended; the
same unattended warning as Copilot applies. `--check` (headless self-verification) is optional and is not
wi's keep-alive.
