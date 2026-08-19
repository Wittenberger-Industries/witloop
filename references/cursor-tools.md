---
type: Reference
title: "Cursor: tool & capability mapping for wit"
description: "Claude Code to Cursor tool-name and capability equivalents, plus plugin-root order, marketplace vs cache, named-vs-inline Task, keep-alive none, and tokens unavailable."
timestamp: 2026-08-19
tags: [cursor, tools, portability, reference]
---

# Cursor: tool & capability mapping for wit

wit's skills are written with Claude Code names. On Cursor, use these equivalents.
Host cells live in `references/capabilities.md` (**the capability table**); this file is the
Cursor procedure. Stamp `Host: cursor` once at scan / dev / rpa entry and read that stamp later.

## ${CLAUDE_PLUGIN_ROOT}: resolve once (mandatory)

`${CLAUDE_PLUGIN_ROOT}` means the **wit plugin root**: the directory holding `skills/`, `agents/`, and
`.claude-plugin/`. Cursor does not inject that variable into the agent shell (it is empty here, same
class of gap as Grok). Resolve it yourself; never pass an unexpanded `${CLAUDE_PLUGIN_ROOT}` into
`Shell`.

Order (ADR-0001; cwd-as-wit-root beats marketplace cache so this source repo dogfoods itself):

1. `$CLAUDE_PLUGIN_ROOT` (or another non-empty plugin-root env) **if** it is a wit root: it contains
   `skills/` and `.claude-plugin/` (validate with `skills/scan/SKILL.md` present).
2. Walk up from cwd (cwd first, then parents) to a directory with those same tells.
3. Host plugin cache: under `~/.cursor/plugins/cache/`, a directory that validates as a wit root
   (observed layout `wittenberger-industries-witloop/wit/<hash>/`). Prefer plugin id `wit`.

Stamp `Plugin root (resolved): <abs>` in `progress.md` and reuse that absolute path for every
`python <root>/skills/.../*.py` call. Later phases never re-guess.

## Install: marketplace vs plugin cache

Install wit from the **Cursor plugin marketplace** (Settings / plugins). Do **not** run Claude
`/plugin marketplace add` or `/plugin install` on this host; those commands do not install Cursor
plugins and look like a failed install when wit is already in the cache.

The marketplace copy lands at `~/.cursor/plugins/cache/<publisher>/wit/<hash>/` with `skills/` +
`.claude-plugin/`. That cache is a valid wit root **only after** walk-up from cwd has failed: if the
session is opened on this repo (or any clone that is itself a wit root), step 2 wins and you run the
tree being edited, not a stale published hash.

No `~/.agents/skills/` alias copy is required on Cursor. Plugin skills plus natural-language
auto-trigger from each skill `description` are enough.

## Tools

| wit/skill says | Cursor equivalent |
|---|---|
| Read | `Read` |
| Write / create a file | `Write` |
| Edit | `StrReplace` |
| Bash / run a command | `Shell` (Python scripts; POSIX or PowerShell, see Shell below) |
| Grep / Glob | `Grep` / `Glob` |
| dispatch a subagent / task-runner | `Task` (named `wit-*` when listed, else inline; see below) |
| TodoWrite | `TodoWrite` |
| AskUserQuestion | `AskQuestion` (schema below) |
| WebSearch | `WebSearch` |
| WebFetch | `WebFetch` |
| invoke a wit skill | plugin skills + natural-language auto-trigger from `description` |
| resolve a skill's `SKILL.md` path | under the resolved wit root `skills/<skill>/SKILL.md`, or `~/.cursor/plugins/cache/**/skills/<skill>/SKILL.md`; pass the absolute path in a `[frontend]`-style dispatch |

**AskQuestion** (maps `AskUserQuestion`): fields `id`, `prompt`, `options` (list of `{id, label}`),
optional `allow_multiple`. If the tool is missing, ask the same question in prose. Do not invent
Claude `AskUserQuestion` field names on this host.

## Named vs inline subagent dispatch

`Task` is the dispatch tool. Prefer a named `subagent_type` when it appears in this session's Task
list: `wit-task-runner`, `wit-researcher`, `wit-code-checker`. If those names are absent, dispatch a
generic type and **inline** the matching `agents/*.md` charter into the prompt. Missing named types
is not a hard failure (a Cursor dry-run with no `wit-*` types still completed inline). Prompt
skeletons stay in `skills/build/references/worktrees-and-subagents.md`.

## Keep-alive: none

Capability `keep_alive` is `none`. This Cursor chat already persists until it is closed.

- Do **not** paste Claude `/goal`.
- Do **not** relaunch Copilot Autopilot flags.
- Do **not** treat **Cursor Autopilot** as wit keep-alive. That skill triages an existing PR
  (conflicts, comments, CI); it does not drive research -> build -> ship.

Print the `none` block from `references/keep-alive.md` (capability-keyed). Optional Cursor `/loop`
may re-wake a chat after `Phase` is done; it is a user opt-in, **not** wit keep-alive and not a
go-signal.

## Tokens: unavailable

Capability `tokens` is `unavailable`. ship:6 runs
`python <resolved-root>/skills/ship/scripts/finalize_tokens.py --write .wit/features/<slug>/tokens.md`
which writes `Orchestrator: unavailable for this run` and fills Duration from `progress.md`. Do **not**
run `token_report.py` (it binds Claude transcripts under `~/.claude/projects/**` and will pick a foreign
leftover session). Never scrape a Usage dashboard.

## Plugin-cache skill discovery

Before stamping `(skill absent)`, search the union that includes
`~/.cursor/plugins/cache/**/skills/<name>/SKILL.md`. Session list still wins when it names the skill.
Full order lives in `skills/research/references/integrations.md`; this glob is the Cursor-specific
insert and must run before the absent stamp.

## Shell (PowerShell)

Cursor's reviewed shell on Windows is PowerShell. POSIX one-liners (`mkdir -p`, `printf`, `date
-Iseconds`, `awk`, `mktemp`, `&&`) fail here. Invoke bundled scripts with `python` (not `python3`)
for plugin-root scripts. Never use PowerShell `>` to persist bytes: it writes UTF-16 LE with BOM.
Helpers write UTF-8 themselves (`now.py` and siblings). Script-invocation fallback is
`references/workflow.md` "Script invocation".

## Models

Live Task slugs: `cursor-grok-4.6-xhigh`, `composer-2.5-fast`, `inherit`. Do not document or pick
`cursor-grok-4.5-high`. Resolve from stamped `Host: cursor` through `references/models.md`
`## Platform model map`.
