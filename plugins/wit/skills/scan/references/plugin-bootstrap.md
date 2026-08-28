---
type: Reference
title: "Plugin bootstrap: the skills wit works best with"
description: "wit runs standalone, but it's deliberately thin and gets much stronger when it can delegate to a few existing skills."
timestamp: 2026-06-07
tags: [scan, reference]
---

# Plugin bootstrap: the skills wit works best with

wit runs standalone, but it's deliberately thin and gets much stronger when it can delegate to a few
existing skills. On first setup, check what's installed and **offer** to add the rest. Never install
without asking; never block if the user declines.

## How to check availability

A skill/plugin is available if `discover_skills.py` (integrations.md search order) finds it: session
list, Claude registry, Cursor plugin cache, Copilot install dir, `~/.agents/skills/`. If unsure, treat
it as missing and offer it. (That lenient default is for this install offer only. Run-time delegation
checks are stricter: integrations.md "How to detect an available skill" - absence must be verified
against that full union before any fallback stamp.)

Read the stamped `Host:` from `progress.md` when it exists. Scan has no feature folder yet: use the
in-session host probe (`claude` | `codex` | `copilot` | `grok` | `cursor`) the same way.

## Recommended set

| Plugin / skills | Why wit wants it | Install (official source) |
|-----------------|-----------------|---------------------------|
| **obra/superpowers** | brainstorming, writing-plans, subagent-driven-development, using-git-worktrees, TDD, code-review, verification, finishing-a-branch; wit delegates the heavy loop to these | Cursor marketplace / installed cache, or Claude `/plugin` (host sections below) |
| **anthropics/skills:frontend-design** | building/refining UI for `[frontend]` tasks | `npx skills add anthropics/skills` (via skills.sh) |
| **vercel-labs/skills:find-skills** (optional) | lets wit pull a missing skill mid-run | `npx skills add vercel-labs/skills` |

If you can't verify an exact marketplace slug, don't fabricate one: give the user the command shape and
ask them to confirm the source, or point them at https://skills.sh to find it.

## Host: cursor

When Host is cursor, do not offer Claude `/plugin` marketplace or `/plugin install` commands. Point at
the Cursor plugin marketplace and the already-installed cache under `~/.cursor/plugins/cache/`.
Superpowers and wit often already live there; offer only what the union actually missed. `npx skills add`
remains valid for skills.sh entries. Skip the `~/.agents/skills/` alias copy on Cursor (plugin skills
plus natural-language auto-trigger are enough).

## Other hosts (Claude `/plugin`, Grok Claude-compat, Copilot)

On Grok Build, superpowers is available on xAI's plugin marketplace as well as via Claude-plugin
compatibility.

Claude `/plugin` install (not used when Host is cursor):

`/plugin marketplace add obra/superpowers-marketplace` then `/plugin install superpowers@superpowers-marketplace`

## Entry-command aliases (Copilot / Codex / Grok)

On Claude Code the plugin namespace already gives `/wit:setup`, `/wit:scan`, `/wit:dev`, `/wit:rpa`,
`/wit:add-issues`; skip this section.
On Cursor, skip this section: plugin skills plus natural-language auto-trigger are enough; do not copy
aliases into `~/.agents/skills/`.
On Copilot CLI the plugin prefix renders the entry points as `/wit setup`, `/wit scan`, `/wit dev`,
`/wit rpa`, `/wit add-issues`, and on Codex they invoke as `$setup`, `$scan`, `$dev`, `$rpa`,
`$add-issues`; on Grok Build they invoke as bare `/setup`, `/scan`, `/dev`, `/rpa`, `/add-issues`
(Grok qualifies clashes by **scope**, `/user:scan`, not `/wit:scan`, and a built-in of the same name
wins; prefer branded `/wit-setup` if bare `/setup` clashes).
wit ships flat **forwarding aliases** that read as one token: `/wit-setup`, `/wit-scan`, `/wit-dev`,
`/wit-rpa`, `/wit-add-issues` (Copilot / Grok) and `$wit-setup`, `$wit-scan`, `$wit-dev`, `$wit-rpa`,
`$wit-add-issues` (Codex), which are also the collision-free branded form on Grok.

As part of the same offer below, ask once whether to install them: copy each directory under
`${PLUGIN_ROOT}/references/skill-aliases/` (i.e. `wit-setup/`, `wit-scan/`, `wit-dev/`, `wit-rpa/`,
`wit-add-issues/`) into `~/.agents/skills/`, the shared flat-skills directory these harnesses read
(Copilot, Codex, and Grok Build all scan it; never a harness's own managed dir like `~/.grok/skills/`;
create it if absent; overwriting an existing `wit-*` alias there is fine, they are wit's own
forwarders). The aliases are version-independent (they forward to whatever wit plugin is installed), so
this is a one-time copy per machine, not a per-update chore. Declining costs nothing: the plugin forms
keep working.

## The offer

After detecting what's missing, ask once with AskUserQuestion, e.g.:

- Host: cursor: "superpowers isn't installed; it powers wit's brainstorm/build/ship. Install it now?"
  → on yes, point at the Cursor marketplace / installed cache (Host: cursor section). Do not output
  Claude `/plugin` commands.
- Other hosts: "superpowers isn't installed; it powers wit's brainstorm/build/ship. Install it now?"
  → on yes, output (or run, if the environment allows) the two `/plugin` commands in Other hosts and
  confirm they registered.
- Group the offer: list everything missing and let the user pick which to add (multi-select).

Record the outcome in your scan report ("installed: superpowers; skipped: find-skills"). wit's phase skills
each detect availability again at run time and fall back gracefully, so a "skip now" is never fatal; the
user can re-run `/wit:scan` or install later.
