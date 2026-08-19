---
type: PR Description
title: First-class Cursor host via a capability table
description: Capability table plus Cursor row
feature: 0001-cursor-capability-table
timestamp: 2026-08-19
---

## feat: First-class Cursor host via a capability table

Closes https://github.com/Wittenberger-Industries/witloop/issues/89

### Summary
Cursor is now a documented Witloop host. Host behavior lives in `references/capabilities.md`; skills stamp those cells once into `progress.md` and later phases read the stamp instead of guessing the product. Cursor is the first fully filled column (`keep_alive=none`, tokens unavailable, `AskQuestion`, named-or-inline `Task`) with adapter `references/cursor-tools.md`. ship:6 is only `finalize_tokens.py --write`. Plugin version **1.14.0**.

### Acceptance criteria
- [x] Host probe stamps `Host:`, plugin root, and `## Capabilities (resolved)` (wit-directory + rpa-directory templates; `skills/{dev,scan,rpa}/SKILL.md`; this run `progress.md` has `Host: cursor`)
- [x] `cursor-tools.md` + `capabilities.md` listed from AGENTS, README, `validate.py` (`tests/test_validate_portability.py`)
- [x] `finalize_tokens.py --write` on Cursor writes `Orchestrator: unavailable for this run`, does not import `token_report.py`, fills Duration (`tests/test_finalize_tokens.py`)
- [x] Cursor keep-alive is `none`; print block has no `/goal` and no Autopilot (`tests/test_keep_alive.py`)
- [x] Ask maps to Cursor `AskQuestion` via `cursor-tools.md`; SKILL bodies cite the `ask` cell
- [x] Skill presence searches `~/.cursor/plugins/cache/**/skills` before `(skill absent)` (`tests/test_discover_skills.py`)
- [x] Named `Task` types when listed, else inline `agents/*.md`; missing types are not fatal
- [x] Always-loaded SKILL bodies cite **the capability table**; grep `if cursor` empty in `skills/{dev,research,plan,build,ship}/SKILL.md`
- [x] `models.md` `cursor` column; dispatch reads the stamped concrete id (`tests/test_models_config.py`)
- [x] `ensure_logdir.py` + `strip_frontmatter.py` named from workflow.md / ship PR-body (`tests/test_posix_helpers.py`)

### Changes
- New `references/capabilities.md` matrix and `references/cursor-tools.md` adapter
- Host probe fields on `progress.md` templates (dev + rpa); workflow named rule **the capability table**
- `keep-alive.md` keyed by `predicate_goal` / `model_judged_goal` / `relaunch` / `none`
- `finalize_tokens.py` dispatcher; `_ledger.py` TEMPLATE names it as ship:6
- POSIX helpers `ensure_logdir.py` and `strip_frontmatter.py` (UTF-8 file write, no shell `>`)
- `discover_skills.py` union includes the Cursor plugin cache; plugin-bootstrap does not offer Claude `/plugin` on Cursor
- `models.md` `cursor` column; fable/opus → `cursor-grok-4.6-xhigh`, sonnet/haiku → `composer-2.5-fast`
- Manifests 1.13.4 → **1.14.0** (all three)

### Testing
- `python scripts/validate.py` → `[OK]`
- `python -m unittest discover -s tests` → 146 tests OK (144 at first ship gate; +2 contract tests for RPA probe fields and `finalize_tokens.py` as the ledger CLI)
- Lint / format / typecheck: `n/a - not configured` (repo-map)
- `python skills/scan/scripts/check_mermaid.py .wit/architecture.md` → mermaid OK

### Verification
Result-mode `wit-code-checker` + superpowers `requesting-code-review` (inline): **CHECK PASSED** on round 2 (`master...HEAD`). Round 1 WARNINGs (leftover `token_report.py` / `/goal` prose in `workflow.md` and `wit-directory.md`; missing RPA probe fields) were fixed in `52f03e0` and re-checked closed. No remaining BLOCKER or WARNING. INFO items from round 1 (brainstorm spelling `AskQuestion`; duplicated `parse_progress_spans`; armed-loop `/goal` close-out in ship:8; Codex adapter without a finalize one-liner) were not re-raised.

### Risk & rollout
Minor bump 1.13.4 → 1.14.0. Revert the PR; no data migration. A Claude run that forgets to stamp `Host: claude` gets unavailable orchestrator tokens until it stamps. Cursor Autopilot is not wit keep-alive.

### Decisions
[ADR-0001](.wit/adr/ADR-0001-capability-table.md): capability table; Cursor first filled row; `finalize_tokens.py` only ship:6 token CLI; keep-alive keyed by capability (`none` on Cursor).

### Rules inventory
Rule-text files this PR moves or rewords. Each still decides correctly if loaded alone.

| File | Before | After |
|------|--------|-------|
| `AGENTS.md` | Four hosts; persistence as `/goal` / Autopilot | Cursor adapter listed; persistence from stamped `keep_alive` |
| `README.md` | Four-platform table | Cursor install, column, `capabilities.md` pointer |
| `references/workflow.md` | `/goal` paste is the go; `token_report.py` finalizes | **the capability table**; keep-alive from stamped cell; `finalize_tokens.py` |
| `references/keep-alive.md` | Host-named templates | `## predicate_goal` / `model_judged_goal` / `relaunch` / `none` |
| `references/models.md` | Four host columns | `cursor` column; detection from stamped `Host:` |
| `references/copilot-tools.md`, `grok-tools.md` | Named `token_report.py` at ship | Point at `finalize_tokens.py` |
| `references/capabilities.md` | absent | Matrix + host-probe recipe |
| `references/cursor-tools.md` | absent | Cursor adapter (ask, Task, probe, none keep-alive) |
| `skills/research/references/wit-directory.md` | No probe fields; PENDING ran `token_report.py --write` | Probe fields; PENDING runs `finalize_tokens.py --write` |
| `skills/rpa/references/rpa-directory.md` | No probe fields | Same three probe fields as wit-directory |
| `skills/research/references/integrations.md` | Claude registry + `.agents/skills` | Union includes Cursor cache; `verify absence` after the union |
| `skills/scan/references/plugin-bootstrap.md` | Claude `/plugin marketplace add` | `## Host: cursor` offers marketplace/cache, not `/plugin` |
| `skills/build/references/worktrees-and-subagents.md` | Named types assumed | Named `Task` when listed, else inline; missing types not fatal |
| `skills/{dev,scan,rpa,research,brainstorm,ship,add-issues}/SKILL.md` | Host names / `token_report.py` in the always-loaded path | Cite the table / stamped cells; ship:6 is `finalize_tokens.py` |
| `scripts/validate.py` | Required `autopilot`/`grok` strings in SKILL bodies | Requires `cursor-tools.md` + `capabilities.md`; bodies must cite the table |
| `docs/roadmap.md` | #89 in the live queue | #89 shipped as v1.14.0 |

Agent charters (`agents/*.md`) are untouched.
