---
type: Implementation Plan
title: "PR D2 — #48 drop legacy/backward-compat support (v1.9.0)"
description: Delete the seven backward-compat families (pre-rename .wi/goals migration, old-filename models-config rename, untracked-dossier move fallbacks, unnumbered-features clauses, old review-file prune, pre-1.7 routing-backfill labels, 4-column ledger acceptance); dev classifier drops to five classes, feature-folder-cases to four cases, validate.py bans .wi/goals unconditionally, the ledger gate accepts only the Duration format. The issue's stays-list is binding.
timestamp: 2026-07-11
tags: [context-budget, consistency, safe-refactor, plan]
---

# PR D2 — #48 (v1.9.0)

> **For agentic workers:** this plan is mostly deletion surgery over shipped markdown plus one
> behavior flip in the ledger gate. "Tests" are `scripts/validate.py`, `pytest tests/`, the AC grep
> assertions, load-alone scenario Q&A on the changed files, and file-tail checks after every edit.

**Goal:** land GitHub issue #48 — drop every shim that exists to support artifacts written by older
wi versions. An old-format repo/dossier is simply **not recognized**: it gets the fresh-state path,
never a migration. Baseline: `main@4a53b08` (v1.8.0).

**Why minor:** removes supported behavior (the migrations, the rename, the dossier-move fallbacks)
and changes the ledger gate's accepted format → **1.9.0** in all three manifests.

**Binding stays-list (from the issue — the one real risk is over-deleting):**

- "legacy" describing the *user's* code/systems stays: `agents/wi-researcher.md` ("legacy/unmaintained",
  the rename-inventory "old name" prose), `skills/research/SKILL.md` tech-choice line,
  `skills/rpa/references/connectors.md` ("Legacy desktop / Citrix"), brainstorm-protocol's
  rename/migration guidance (all about the user's process, not wi versions).
- Self-repair keeps its mechanism, loses the version framing: missing resolved-routing block →
  resolve once now (relabel: guards hand-edited/incomplete progress.md); build-uipath's dossier
  check keeps its out-of-order-resume trigger; a missing `Flow:` line still defaults to `dev`
  (already unframed — untouched).
- Graceful `unavailable` on a date-only Log stamp stays (honesty rule, not version compat) — only
  the test's `legacy` variable name is relabeled.
- `docs/` archives keep their historical text (out of lint scope by design).
- README's Codex "compat" lines are cross-*platform* compatibility, not version compat — stay.

## Disposition table (rules inventory — rides in the PR body)

| # | Family | Site | Disposition |
|---|---|---|---|
| 1 | `.wi/goals` migration | `references/feature-folder-cases.md` description + intro (legacy-repo class, rpa routing note, compose example) + "Legacy migration" section | **Deleted** → four case sections |
| 1 | | `skills/dev/SKILL.md` step 2 classifier (`legacy-repo` class + tell) | **Deleted** → five classes |
| 1 | | `skills/rpa/SKILL.md` step 2 legacy-repo pointer | **Deleted** |
| 1 | | `skills/research/references/wi-directory.md` Slugs-bullet xref list ("legacy migration") | **Deleted** from the list |
| 1 | | `scripts/validate.py` 7c `MIGRATION_CMD` + sanctioned-line exemption + docstring | **Deleted** — `.wi/goals` banned unconditionally |
| 2 | models-config rename | `references/models.md` First-run setup (rename path + old-filename tell) | **Deleted** — absent → fresh setup; an old-named config is simply absent |
| 2 | | `skills/dev/SKILL.md` step 1 "a pre-1.3 legacy config → rename" | **Deleted** |
| 2 | | `skills/rpa/SKILL.md` step 2 same clause | **Deleted** |
| 3 | untracked-dossier move fallback | `skills/build/SKILL.md` dossier paragraph | **Deleted** |
| 3 | | `skills/build/references/worktrees-and-subagents.md` fallback sentence | **Deleted** ("Resume-safe" sentence stays, reworded) |
| 3 | | `skills/rpa/SKILL.md` step 6 fallback sentence | **Deleted** |
| 3 | | `skills/rpa/references/build-uipath.md` dossier check | **Relabeled** — keeps the out-of-order-resume trigger, loses "a pre-1.3 run" |
| 4 | unnumbered features | `wi-directory.md` Slugs bullet legacy sentence | **Deleted** — one neutral clause: non-numeric names contribute nothing to the max |
| 4 | | `skills/rpa/references/ingest.md` Slugs xref clause | **Deleted** |
| 4 | | `feature-folder-cases.md` migrated-dossiers numbering note | **Deleted** (with the section) |
| 5 | old review-file prune | `skills/ship/SKILL.md` ship:6.2 parenthetical | **Deleted** (`.logs/` clause stays) |
| 6 | routing-backfill labels | `references/models.md` dispatch rule "(legacy features, pre-1.7 runs)" | **Relabeled** → "(a hand-edited or incomplete progress.md)" |
| 6 | | dev step 1 resumed-feature block clause | **Stays as-is** (already version-unframed self-repair) |
| 7 | 4-column ledger acceptance | `skills/ship/scripts/_ledger.py` verify() conditional + `_data_rows` docstring | **Deleted** — Duration column + cells + totals required unconditionally; missing column = new failure reason |
| 7 | | `skills/ship/scripts/check_tokens.py` docstring | **Updated** to the single accepted format |
| 7 | | `tests/test_tokens_guardrail.py` legacy-acceptance test | **Replaced** by a rejection test; `_v2` suffix dropped from the duration-gate test name |
| 7 | | `tests/test_timing_report.py` `legacy` variable | **Relabeled** `date_only` (behavior test stays — graceful `unavailable`) |

## Global constraints (roadmap guardrails)

- validate.py + pytest green after each commit (never piped through `tail`); file tails checked
  after every markdown edit.
- No new files outside whitelisted dirs (this PR adds only this plan doc under `docs/`).
- Citations stay `name:N` / quoted headings; no section signs.
- No AI attribution in commits/PRs.
- Version → **1.9.0** in `.claude-plugin/plugin.json`, the wi entry in
  `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json` (validate.py parity check).
- Retires the #35 legacy-ledger guardrail (the 4-column acceptance was its last consumer).

## Tasks

- [ ] Commit 1: this plan doc.
- [ ] Commit 2 (code, test-first): rejection test replaces the legacy-acceptance test → flip
  `_ledger.verify()` to require the Duration format; `check_tokens.py` docstring; validate.py 7c
  unconditional `.wi/goals` ban + docstring; timing-test variable relabel.
- [ ] Commit 3 (prose): families 1–6 across the nine markdown files per the disposition table.
- [ ] Commit 4: version bump 1.9.0 (three manifests).
- [ ] Push, PR `Fixes #48` with the disposition table + AC grep results + scenario Q&A results.

## Verification (the issue's AC)

- [ ] `grep -rinE "pre-1\.|pre-rename|old-named|old filename" skills agents references scripts tests` → no hits.
- [ ] `legacy` survives only in: `agents/wi-researcher.md`, `skills/research/SKILL.md`,
  `skills/rpa/references/connectors.md`.
- [ ] validate.py rejects any `.wi/goals` mention with no exemption; docstring matches.
- [ ] dev step 2 = five classes; feature-folder-cases.md = four case sections; wi-directory xref consistent.
- [ ] `check_tokens.py` fails a 4-column ledger (new test); remaining tests green.
- [ ] Scenario Q&A (load-alone subagents on the changed files): old-named models config → fresh
  setup, no rename; a `.wi/goals` repo → plain new-feature path, no migration offered;
  current-format flows → behavior unchanged.
