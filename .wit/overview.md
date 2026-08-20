---
type: Overview
title: Witloop - overview
description: A human-facing tour of what this project is and how it is organized.
timestamp: 2026-08-19
---

# Witloop - overview  (documented 2026-08-19 by /wit:scan)

## What it is
Witloop (`wit`, formerly `wi`) is an opinionated, low-token spec-driven engineering loop shipped as a plugin. One source tree targets Claude Code, Codex CLI, Copilot CLI, Grok Build, and Cursor. You scan a project once, then `/wit:dev` brainstorms, designs, and ships a feature to an open PR.

## Stack
Markdown skills and agent charters, plus stdlib Python for validation, token ledgers, mermaid checks, and GitHub-issue drafts. No application runtime, no package lockfile. Version `1.14.1` in the three plugin manifests.

## How it is organized
- `skills/` - user-facing `scan`, `dev`, `rpa`, `add-issues`; hidden phase skills `brainstorm`, `research`, `plan`, `build`, `ship`
- `agents/` - `wit-researcher`, `wit-task-runner`, `wit-code-checker` charters
- `references/` - host tool maps (`codex`, `copilot`, `grok`, `cursor`), `capabilities.md`, `workflow.md`, `keep-alive.md`, `models.md`, skill aliases
- `scripts/validate.py` - plugin-structure gate (portability files, YAML, version parity)
- `docs/` - maintainer plans/specs/design-notes and the live `docs/roadmap.md` queue
- `.claude-plugin/` and `.codex-plugin/` - marketplace/plugin manifests

On-repo wit state for this source repo lives in `.wit/` (dogfood). Consumer projects get their own `.wit/` when they run scan.

## Run it
Install via the host marketplace (see README). Develop by editing skills/references/scripts; gate with `python scripts/validate.py` and `python -m unittest discover -s tests` (or `pytest tests/`). Exact commands: `repo-map.md`.

## Data & external services
None at runtime. Token parsers read local transcripts (Claude) or Grok session files. Shipping uses `gh` against GitHub.

## Conventions & gotchas
- Host-specific procedure lives in `references/*-tools.md`, not in the five always-loaded SKILL bodies
- `.gitignore` is a whitelist; new top-level paths need `!/path`
- Agent charters are the most sensitive surface (caps, markers, tool lists)
- Hotspots (`dev`/`build`/`ship` SKILL.md, `wit-directory.md`, `workflow.md`) are strictly serial across branches
- Ledger rule: exact token numbers or `unavailable`, never a guessed scrape

## Open questions
- None from this scan. Cursor is a documented host as of v1.14.0 (`references/cursor-tools.md`, ADR-0001). Postponed owner work remains #34 (cross-vendor MoA).
