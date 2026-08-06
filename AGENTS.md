---
type: Bootstrap
title: "Witloop: cross-platform bootstrap"
description: Entry point for non-Claude harnesses; how to read and run Witloop's skills on Codex CLI, Copilot CLI, and Grok Build.
timestamp: 2026-06-09
tags: [witloop, bootstrap, cross-platform, codex, copilot, grok]
---

# Witloop: cross-platform bootstrap

This repository **is** Witloop (plugin id `wit`, formerly `wi`): an opinionated, low-token, spec-driven dev loop. Its capabilities
are delivered as skills under `skills/` (`scan`, `dev`, `research`, `plan`, `build`, `ship`, `brainstorm`,
`rpa`) plus three subagent prompt templates under `agents/` (`wit-code-checker`, `wit-researcher`,
`wit-task-runner`). The `wit-` prefix is a deliberate cross-platform tag (PR #15); on Claude these render
as `wit:wit-<name>`; the stutter is accepted, and the checker stays `wit-code-checker` (skills call it
*the checker*).

## If you are not Claude Code
wit's skills use Claude Code tool names and the `${CLAUDE_PLUGIN_ROOT}` variable. Before following a skill,
read the mapping for your platform and apply it as you go:

- **Codex CLI:** `references/codex-tools.md`
- **GitHub Copilot CLI:** `references/copilot-tools.md`
- **Grok Build:** `references/grok-tools.md`

Key rule: **`${CLAUDE_PLUGIN_ROOT}` is the wit plugin root** (the directory holding `skills/`, `agents/`,
`.claude-plugin/`) whether that's an installed plugin dir (e.g. Copilot's
`~/.copilot/installed-plugins/…`) or a clone of this repo. Resolve every `${CLAUDE_PLUGIN_ROOT}` path
against it.

## Invoking wit
- Start a feature: the `dev` skill (`/wit:dev` on Claude; `/wit-dev` on Copilot / `$wit-dev` on Codex once
  scan's bootstrap has installed the flat aliases into `~/.agents/skills/`; the raw plugin forms
  `/wit dev` and `$dev` always work; or describe the feature and let it auto-trigger).
- File a GitHub issue: the `add-issues` skill (`/wit:add-issues` on Claude; `/wit-add-issues` on
  Copilot / Grok; `$wit-add-issues` on Codex once aliases are installed).
- Bootstrap a repo first with the `scan` skill.
- Only scan/dev/rpa/add-issues are user-facing commands. The phase skills (brainstorm, research, plan,
  build, ship) carry `user-invocable: false`; hidden from slash pickers, still invoked by the
  orchestrating skill and by natural language ("ship it").
- Persistence: wit hands off to a keep-alive loop at the end of brainstorm: Claude/Codex use built-in
  `/goal`; Grok Build uses its native (model-judged) `/goal`; Copilot uses Autopilot flags (see the tool
  map). wit runs without it too, just less robustly.
- Superpowers precedence (integrations.md "Who initiates", `skills/research/references/integrations.md`):
  delegation points only, never self-triggered mid-phase; wit's artifact formats always win.

These skills auto-trigger from their `description` fields. When a user's request matches one, use it.

## Cursor Cloud specific instructions

This repo is the Witloop plugin itself: markdown skills/agents/references plus a few stdlib-only Python
helper scripts. There is **no server, web app, or CLI binary to launch** — "running" the project means
running its CI gate (structural validation + unit tests) and, optionally, exercising a bundled skill
script directly. The full command set lives in `.github/workflows/validate.yml`.

- **Interpreter:** on the cloud VM only `python3` (and `pip`/`pip3`) are on PATH — bare `python` is not,
  even though `validate.py`'s docstring and CI (via `actions/setup-python`) say `python`. Use `python3`
  locally: `python3 scripts/validate.py` and `python3 -m unittest discover -s tests`.
- **Dependencies:** the only external dep is PyYAML, and only `scripts/validate.py` uses it (it degrades
  gracefully and skips the full YAML parse when absent; the unit tests never need it). The update script
  installs it for CI parity.
- **Known pre-existing test failure:** `test_encode_drops_drive_colon_and_separators`
  (`tests/test_tokens_guardrail.py`) asserts Windows drive-letter path semantics (`D:/...` → `D-...`) that
  do not hold on Linux/POSIX. It fails identically on GitHub CI (also Ubuntu), so a red result here is the
  repo's own state, not a broken environment. Expect 84 pass / 1 fail until the repo fixes it upstream.
- **validate.py is the guardrail:** it enforces trailing newlines, balanced code fences, OKF `type`
  frontmatter, manifest version parity across the three `plugin.json`/`marketplace.json` manifests, and
  several banned-string lints. Run it after editing any `skills/`, `agents/`, `references/`, `docs/`,
  `AGENTS.md`, or `README.md` file, or a manifest.
