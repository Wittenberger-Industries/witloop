---
type: Task List
title: "Tasks: First-class Cursor host via a capability table"
description: Small ordered tasks (each with files + verify) and the build waves for this feature.
feature: 0001-cursor-capability-table
timestamp: 2026-08-19
---

# Tasks: First-class Cursor host via a capability table

> Ordered. Each task is small enough for one focused sitting and ends green.
> I'm using the writing-plans skill to create the implementation plan (captured here, not under docs/superpowers/plans/).

## Task 1: Capability table, probe template, workflow pointer   [infra]
- **Files:** `references/capabilities.md`, `references/workflow.md`, `skills/research/references/wit-directory.md`, `tests/test_capabilities.py`
- **Do:** Add `references/capabilities.md` (capability x host matrix for claude/codex/copilot/grok/cursor; Cursor cells per ADR-0001). Add named rule **the capability table** to `workflow.md` (pointer only; do not embed the matrix). Extend the `progress.md` template with `Host:`, `Plugin root (resolved):`, and `## Capabilities (resolved)`. TDD: tests parse the matrix and assert Cursor `keep_alive=none`, `tokens=unavailable`, `ask=AskQuestion`.
- **Verify:** `python -m unittest tests.test_capabilities`
- **Depends on:** -

## Task 2: cursor-tools.md + bootstrap listings   [docs]
- **Files:** `references/cursor-tools.md`, `AGENTS.md`, `README.md`, `scripts/validate.py`, `tests/test_validate_portability.py`
- **Do:** Write `cursor-tools.md` (Shell/StrReplace/AskQuestion/Task map; keep-alive none; tokens unavailable; marketplace vs plugin cache; named-vs-inline; plugin-root order from ADR-0001). List it from `AGENTS.md` and README. Extend `validate.py` portability file list with `references/cursor-tools.md` and `references/capabilities.md`. TDD: unittest that `validate.py` fails if `cursor-tools.md` is missing (temp rename or the list is asserted).
- **Verify:** `python -m unittest tests.test_validate_portability`; `python scripts/validate.py`
- **Depends on:** 1

## Task 3: POSIX helpers   [backend]
- **Files:** `skills/ship/scripts/ensure_logdir.py`, `skills/ship/scripts/strip_frontmatter.py`, `tests/test_posix_helpers.py`, `references/workflow.md`, `skills/add-issues/SKILL.md`
- **Do:** TDD then implement stdlib CLIs beside `now.py`. `ensure_logdir.py <dir>` creates the dir + `*\n` gitignore as UTF-8 (feature `.logs/` or `.wit/issues`). `strip_frontmatter.py <in.md> <out.md>` writes the body without YAML frontmatter as UTF-8 to `<out.md>` (never stdout + `>`; PowerShell `>` is UTF-16). Exit 1 on unclosed frontmatter. Point workflow.md's log-dir recipe and add-issues' issues-dir + publish awk at these scripts. Lead `now.py` over `date -Iseconds` in the same recipe block if it still leads with POSIX. Do not edit `skills/ship/SKILL.md` here (task 5 owns every ship recipe).
- **Verify:** `python -m unittest tests.test_posix_helpers`; grep `ensure_logdir.py` in `references/workflow.md` and `skills/add-issues/SKILL.md`; grep `strip_frontmatter.py` in `skills/add-issues/SKILL.md`
- **Depends on:** 1

## Task 4: Keep-alive keyed by capability   [backend]
- **Files:** `references/keep-alive.md`, `tests/test_keep_alive.py`
- **Do:** Rekey `keep-alive.md` by `keep_alive` cell: `predicate_goal` (Claude/Codex), `model_judged_goal` (Grok), `relaunch` (Copilot Autopilot + warning), `none` (Cursor: chat persists; optional `/loop` documented; no `/goal`; no Autopilot). TDD: select Cursor → `none` block contains neither `/goal` as the print command nor `autopilot`. Preserve Grok `update_goal` text so existing validate.py keep-alive check still passes until task 8 retargets it.
- **Verify:** `python -m unittest tests.test_keep_alive`
- **Depends on:** 1

## Task 5: Token dispatcher   [backend]
- **Files:** `skills/ship/scripts/finalize_tokens.py`, `skills/ship/scripts/_ledger.py`, `skills/ship/SKILL.md`, `references/grok-tools.md`, `references/copilot-tools.md`, `references/cursor-tools.md`, `tests/test_finalize_tokens.py`
- **Do:** TDD then add `finalize_tokens.py --write <tokens.md>` that reads `Host:` from `progress.md`. Route by `tokens` cell / Host slug: `claude` → `token_report.py`; `grok` → `grok_token_report.py` (unchanged SystemExit on missing session); `cursor`, `copilot`, `codex`, missing Host, and any unknown slug → write `Orchestrator: unavailable for this run`, fill Duration from progress spans, never import/run `token_report.py` (assert by planting `HOME/.claude` and checking it is not opened). ship:6 names only this CLI. ship:7 PR-body uses `strip_frontmatter.py <in> <out>` (no `>`). ship:8 log-dir recreate uses `ensure_logdir.py`, not `mkdir -p`. Update `_ledger` PENDING prose. Point grok/copilot/cursor tool maps' ship:6 one-liners at `finalize_tokens.py`. Preserve Task 5's ship:6/7/8 lines if later tasks touch this file (task 7 must not). All-unavailable ledger must still pass `check_tokens.py`.
- **Verify:** `python -m unittest tests.test_finalize_tokens tests.test_tokens_guardrail tests.test_grok_token_report tests.test_timing_report`; grep `finalize_tokens.py` in `skills/ship/SKILL.md` `references/grok-tools.md` `references/copilot-tools.md` `references/cursor-tools.md`; grep `ensure_logdir.py` in `skills/ship/SKILL.md`
- **Depends on:** 1, 2, 3

## Task 6: Skill discovery + plugin-bootstrap + models cursor column   [backend]
- **Files:** `skills/research/scripts/discover_skills.py`, `skills/research/references/integrations.md`, `skills/scan/references/plugin-bootstrap.md`, `references/models.md`, `tests/test_discover_skills.py`, `tests/test_models_config.py`
- **Do:** TDD a stdlib helper that unions session-list paths (argv or stdin) + `~/.claude/plugins/installed_plugins.json` installPaths + `~/.cursor/plugins/cache/**/skills` + Copilot install dir + `~/.agents/skills/`. Integrations.md documents that order and forbids `(skill absent)` before it. plugin-bootstrap: when Host is cursor, do not offer Claude `/plugin marketplace add`; point at Cursor marketplace / installed cache. Add `cursor` column to `references/models.md` platform map (`fable`/`opus` → `cursor-grok-4.6-xhigh`; `sonnet`/`haiku` → `composer-2.5-fast`). Retarget host detection: resolve-once reads stamped `Host:` from `progress.md` (not "follows grok-tools.md else claude"). Extend `PlatformMapTest` for `host="cursor"` and for stamp-driven detection.
- **Verify:** `python -m unittest tests.test_discover_skills tests.test_models_config`; grep -n "plugin marketplace add" `skills/scan/references/plugin-bootstrap.md` must be inside a non-Cursor branch; grep `Host:` in `references/models.md` host-detection paragraph
- **Depends on:** 1

## Task 7: SKILL body pointers + validate.py retarget   [infra]
- **Files:** `skills/dev/SKILL.md`, `skills/research/SKILL.md`, `skills/scan/SKILL.md`, `skills/rpa/SKILL.md`, `skills/brainstorm/SKILL.md`, `skills/build/references/worktrees-and-subagents.md`, `scripts/validate.py`
- **Do:** Replace host-name keep-alive/token lists in always-loaded bodies with one pointer to **the capability table** and keep-alive.md. Do not edit `skills/ship/SKILL.md` (task 5 owns ship:6/7/8). Host probe at scan/dev/rpa entry: detect slug from the running harness (tool surface / which adapter applies: `claude` | `codex` | `copilot` | `grok` | `cursor`), resolve plugin root (env if a wit root → walk-up from cwd → host cache; cwd-as-wit-root beats marketplace cache), copy that host's cells from `capabilities.md` into `## Capabilities (resolved)`. Every host including `claude` is stamped; never copy this feature's `Host: cursor` block as a universal pattern. Replace "Pasting the `/goal` line is the go" with a go-signal keyed by stamped `keep_alive` (`predicate_goal`/`model_judged_goal` paste `/goal`; `relaunch` paste Autopilot command; `none` = user confirmation / chat continues, never `/goal`). worktrees-and-subagents: named `wit-*` when in session list, else inline; missing types are not a hard failure. Retarget `validate.py` so `dev`/`research` must cite `capabilities.md` (or "capability table") rather than contain the strings `autopilot` and `grok`; keep Task 2's portability tuple. Keep Grok text in `keep-alive.md` / `grok-tools.md`. Map AskUserQuestion → ask capability (Cursor: AskQuestion) in brainstorm/scan/research via the tool map, not a new if-tree.
- **Verify:** `python scripts/validate.py`; `python -m unittest discover -s tests`; grep `if cursor` in `skills/{dev,research,plan,build,ship}/SKILL.md` is empty; grep `Pasting the /goal` in `skills/dev/SKILL.md` `skills/research/SKILL.md` is empty; grep `Host: claude` detection/stamp recipe in `skills/dev/SKILL.md`
- **Depends on:** 2, 4, 5, 6

## Task 8: Manifest bump and host copy   [docs]
- **Files:** `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, `docs/roadmap.md`
- **Do:** Bump plugin version **1.13.4 → 1.14.0** in all three manifests (parity). Mention Cursor in plugin/marketplace descriptions (keep-alive none, capability table) without claiming Autopilot. Note #89 in `docs/roadmap.md` shipped list. Rules inventory in the later PR body; this task only bumps copy + version.
- **Verify:** `python scripts/validate.py` (manifest parity)
- **Depends on:** 7

## Waves  (derived from Depends on + Files: what build runs concurrently)
- Wave 1: task 1
- Wave 2: tasks 2, 3, 4, 6 (disjoint files; 3 and 2 both touch workflow.md? Task 2 does not. Task 3 does. Task 1 already created workflow.md pointer. Task 3 edits workflow.md log-dir: serialize 3 after 1, parallel with 2/4/6)
- Wave 3: task 5 (owns all of `skills/ship/SKILL.md`: finalize_tokens, strip_frontmatter, ensure_logdir, adapter one-liners)
- Wave 4: task 7 (hotspot SKILL bodies except ship + validate.py retarget; must not touch ship/SKILL.md)
- Wave 5: task 8
