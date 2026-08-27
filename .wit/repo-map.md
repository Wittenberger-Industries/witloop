---
type: Repo Map
title: Repo map - Witloop
description: Stack, exact verified commands, and conventions scan recorded for this repo.
timestamp: 2026-08-27
---

# Repo map  (scanned 2026-08-27, refreshed)

- **Kind:** existing
- **Languages:** Markdown (skills, agents, references) + Python 3.13 (scripts/tests; CI is Python 3.x)
- **Package manager:** none (no pyproject/lockfile). Optional: `pip install pyyaml` so `validate.py` runs its YAML-parse checks
- **Frontend / backend:** neither - Claude/Codex/Copilot/Grok/Cursor plugin, not an app
- **Layout:** plugin root. `skills/` (setup, scan, dev, brainstorm, research, plan, build, ship, rpa, add-issues), `skills/dev/references/work-types.md`, `skills/dev/references/investigation.md`, `skills/dev/references/bug-fix.md`, `agents/`, `references/` (capability table + host tool maps + workflow), `scripts/validate.py`, `tests/`, `docs/` (plans, specs, design-notes, roadmap), `.claude-plugin/`, `.codex-plugin/`
- **Architecture:** see `architecture.md` (mermaid module/dependency diagram)

## Commands  (verified runnable)
- **Install:** `n/a - not configured` (this source repo, or marketplace install; no project venv)
- **Test (all):** `python -m unittest discover -s tests` (CI) - **Test (one):** `python -m unittest tests.test_<mod>.<Class>.<name>`
  Equivalent: `pytest tests/` and `pytest tests/test_<mod>.py::TestClass::test_name` (pytest 9.x present locally; tests are unittest)
- **Lint:** `n/a - not configured`           - **Format:** `n/a - not configured`
- **Typecheck:** `n/a - not configured`      - **Run / dev:** `n/a - not configured`     - **Build:** `n/a - not configured`
- **Plugin structure gate:** `python scripts/validate.py` (CI + every PR; never pipe through `tail`)
- **Tests parallel-safe:** yes (isolated temp dirs; no shared db or fixed ports)

## CI
- **Provider/files:** `.github/workflows/validate.yml`  - **Enforces:** `pip install pyyaml`, `python scripts/validate.py`, `python -m unittest discover -s tests`

## Conventions
- **Style/lint:** no ruff/mypy. Standing guardrails in `docs/roadmap.md`: no em-dashes in shipped text; citations use `name:N` locators; rules-inventory on any rule-text PR; three-manifest version bump together
- **Tests in:** `tests/test_*.py` (unittest)
- **Imports/module style:** stdlib scripts under `skills/*/scripts/` and `scripts/validate.py`; tests add those dirs to `sys.path`
- **Gitignore:** whitelist (`*` then `!/path`). New top-level dirs need a `!/` line or they vanish. `.wit/` is whitelisted so dogfood scan/dev artifacts can commit

## Entry points
- Skills: `/wit:setup`, `/wit:scan`, `/wit:dev`, `/wit:rpa`, `/wit:add-issues` (host aliases in `references/skill-aliases/` and `AGENTS.md`). `/wit:dev` accepts `--kind feature|bug-fix|investigation`
- Manifests: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json` (version parity required; three-manifest lockstep)
- Python: `scripts/validate.py`; ship token dispatcher `finalize_tokens.py` under `skills/ship/scripts/`; POSIX helpers `ensure_logdir.py` / `strip_frontmatter.py`; skill discovery `skills/research/scripts/discover_skills.py`

## Unknowns
- None recorded. Cursor is documented (`references/cursor-tools.md`). Codex/Copilot `ask` cells stay `unknown` (no Ask row in those adapters).
