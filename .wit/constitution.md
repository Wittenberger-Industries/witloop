---
type: Constitution
title: "Constitution: Witloop"
description: The project's ground rules, read by every wit phase.
timestamp: 2026-08-19
---

# Constitution: Witloop

> The rules wit follows for this repo. Edit freely; this overrides wit's defaults.

## Language & tooling
- **Primary language:** Markdown skills plus Python 3.x stdlib scripts
- **Package manager / runner:** none; CPython on PATH, optional PyYAML for validate.py
- **Canonical commands:** see .wit/repo-map.md (do not duplicate here)

## Code style
- No project formatter or linter is configured. `python plugins/wit/scripts/validate.py` is the structure gate and must pass before ship.
- Type checking: not configured; new Python stays stdlib-typed by convention, no mypy gate.
- Prefer small, pure functions; isolate side effects; no dead code or commented-out blocks.
- Naming follows existing files; match the surrounding module, don't import a new style.
- No em-dashes in shipped text, scripts, manifests, PR bodies, or commits. Citations use `name:N` locators, never the section sign.

## Simplicity  (build the least that works)
- Before building, ask whether it needs to exist at all. Speculative need = skip it, say so in one line. (YAGNI)
- Reach in order: stdlib → native platform feature → already-installed dep → a few lines → and only then new code or a new dependency.
- Deletion over addition. No abstraction until a second caller exists (no interface-of-one, no config for a value that never changes). Fewest files, shortest working diff.
- Lazy, not negligent: never simplify away input validation at trust boundaries, error handling that prevents data loss, security, or accessibility.
- Mark a deliberate shortcut with a comment naming its ceiling and the upgrade path.
- Host-specific procedure lives in `references/` adapters, not in the always-loaded SKILL bodies.

## Testing  (this is enforced, not optional)
- New behavior ships with tests. Default to TDD: write the failing test first.
- Tests live in `tests/`, named `test_*.py`. A change isn't done until `python plugins/wit/scripts/validate.py` and the unit suite pass.
- Don't weaken or delete a test to make the suite green: fix the code or change the test deliberately with a noted reason.

## Architecture & dependencies
- Respect existing module boundaries and layering; don't reach across them for convenience.
- Adding a dependency is a decision: clear the Simplicity ladder first, then justify it in the feature's spec.
- Any hard-to-reverse decision (public skill contract, host capability table, token ledger rule, agent charter) requires an ADR.
- Agent charters (`agents/*.md`) are the most sensitive surface: minimal additive diffs only; never alter report caps, output markers, verification-gate contracts, or tool lists unless the spec names that change.
- Hotspots (`skills/dev/SKILL.md`, `skills/build/SKILL.md`, `skills/ship/SKILL.md`, `wit-directory.md`, `workflow.md`) stay serial: one in-flight branch at a time.

## Git & shipping
- One feature → one branch/worktree → one focused PR. Small, reviewable commits.
- Conventional-ish commit subjects (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore(wit):`).
- The ship gate (`validate.py` + unit tests) must pass before opening a PR.
- Behavior/artifact changes bump **minor**; pure relocation/compression bumps **patch**. All three plugin manifests stay in version lockstep.
- New top-level paths need a `.gitignore` `!/` whitelist line.
- No AI attribution in commits or PRs.
- Rule-text PRs attach a before/after rules inventory; each touched file must still decide correctly if loaded alone.

## Safety
- Never commit secrets. Read config from the environment.
- Don't run destructive commands (force-push, db drops, mass deletes) without explicit user confirmation.

## Out of scope by default
- Scraping vendor usage dashboards into the token ledger
- New application runtimes or package lockfiles
- Gemini / OpenCode / Factory Droid hosts until a capability-table row exists for them
- Treating Cursor Autopilot as wit keep-alive
- Rewriting agent charter contracts
