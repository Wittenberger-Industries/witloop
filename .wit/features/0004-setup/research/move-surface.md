---
type: Research Note
title: "Move surface: setup owns first-run; scan is refresh-only"
description: Section split from scan/dev/rpa/models.md into skills/setup/SKILL.md; bare /wit-scan is silent --refresh; missing repo-map invokes setup.
feature: 0004-setup
timestamp: 2026-08-27
valid_until: 2026-09-26
---

# Move surface: first-run into setup

## Responsibility Map

First-run write of `.wit/` project docs + models config = **setup**. Drift-check of an existing map = **scan**. Feature-loop apply/resolve of models = **dev/rpa** (one-liners only). Issue filing = **add-issues** (never setup).

## Decision

**One split.** Move scan's full first-run procedure (steps 1-7, output contract, three templates, greenfield guided setup, plugin offer, `.wi` rename, first-run commit/report) plus models.md's first-run *write* into `skills/setup/SKILL.md`. Leave scan as the `--refresh` skill (A drift, B memory hygiene, C report) plus host probe. Bare `/wit-scan` with no flags on a scanned repo **is silent `--refresh`**. Missing `.wit/repo-map.md` at scan / dev / rpa **invokes setup** (does not keep a first-run body in scan). add-issues does not.

## Why this split

Today scan is two jobs in one skill: document-and-bootstrap, then a named `--refresh` mode. [VERIFIED: skills/scan/SKILL.md intro "Two jobs" + `## --refresh`]. The brief forbids folding setup back into scan and says to move first-run *text*, not wrap the old body. [VERIFIED: brief.md Approach preferences + Scope]. Models first-run is already a citation, not a duplicated procedure: dev:1 and rpa:2 point at `models.md "First-run setup"`. [VERIFIED: skills/dev/SKILL.md:56-60; skills/rpa/SKILL.md:43-46; references/models.md:151-163]. That write trigger moves to setup; resolve-once into `progress.md` stays at the feature entries because setup has no feature folder.

## Bare `/wit-scan` with no flags: silent `--refresh`

Options considered:

| Option | Behavior on an already-scanned repo | Rejected / kept |
|--------|-------------------------------------|-----------------|
| **A. Silent `--refresh` (chosen)** | Bare `/wit-scan` runs refresh A/B/C. `--refresh` remains a synonym for auto-stale callers. | Kept |
| B. Flag required | Bare `/wit-scan` errors: pass `--refresh` or run setup. | Rejected |
| C. Bare scan still first-runs | Re-documents. | Rejected: brief says scan is refresh-only |

Why A wins:

1. After the move, scan has **one** job. A mandatory flag for the only remaining job is ceremony. [ASSUMED] (product judgment; load-bearing: yes)
2. Brief example is `Later /wit-scan only drift-checks` with no flag. [VERIFIED: brief.md:36]
3. Natural-language triggers (`refresh the scan`, `update the repo map`, `is the scan stale?`) do not include `--refresh`. [VERIFIED: skills/scan/SKILL.md description]
4. Today, bare `/wit:scan` on a scanned repo still runs the **full procedure**; `--refresh` is opt-in guidance, not a gate at step 0. [VERIFIED: skills/scan/SKILL.md:19 vs Procedure 1-7; constitution leave-if-exists is the only skip]. Silent refresh turns that footgun into the cheap correct default.
5. `dev` already calls the scan skill's `--refresh` drift pass by name. [VERIFIED: skills/dev/SKILL.md:53-55]. Keep accepting the flag as an explicit synonym so those callers do not change.

`--refresh` does not disappear from docs or from auto-stale. It stops being required for the user-typed command to do work.

## Missing-map dispatcher (replace "this IS a first scan")

Current refresh precondition: `.wit/repo-map.md` exists, otherwise "this IS a first scan: run the full procedure". [VERIFIED: skills/scan/SKILL.md:92-94]. After the move that fallback is forbidden (scan must not keep first-run text).

**Tell:** `.wit/repo-map.md` is missing. Do **not** key off "is `.wit/` a directory". add-issues already creates `.wit/issues/` (and thus `.wit/`) without a map. [VERIFIED: skills/add-issues/SKILL.md:36-40]. A directory-only tell would skip setup after a prior `add-issues` run. Brief "missing `.wit/`" is shorthand for "project not set up"; the observable is **repo-map absent**. Same tell as today's dev:1 scan-first line. [VERIFIED: skills/dev/SKILL.md:52-53]

**Scan entry:**

1. Host probe (unchanged pattern; scan still has no `progress.md`). [VERIFIED: skills/scan/SKILL.md:35-39]
2. `.wi/` and no `.wit/` → invoke setup (rename lives in setup, was scan:1). [VERIFIED: skills/scan/SKILL.md:44-45]
3. No `.wit/repo-map.md` → invoke setup, then **stop**. Do not chain refresh A/B/C. A fresh setup commit plus an immediate `chore(wit): scan refresh` re-stamp is empty work and a second commit. Brief "then continue" for scan means setup satisfied the request, not "run refresh on a map you just wrote". [ASSUMED] (interpretation of brief:18-19; load-bearing: yes)
4. Map present → refresh A/B/C, flag or not.

**Dev (feature / bug-fix only):** after the work-type prelude, if repo-map missing → run setup (forward `--auto` if present), then continue. Stale map → scan `--refresh` (unchanged). Investigation still exits before any of this. [VERIFIED: skills/dev/SKILL.md:38-39; docs/design-notes/dev.md:106-112]

**Rpa:** today does **not** check for a scan. [VERIFIED: skills/rpa/SKILL.md procedure; no repo-map tell]. New one-liner after host probe, before rpa:1: if repo-map missing → run setup (forward `--auto`), then continue. rpa still owns UiPath bootstrap, ingest, rpa-constitution; those are not scan first-run.

**add-issues:** no setup, no scan. Preflight uses `ensure_logdir.py` on `.wit/issues/` and says not to rely on a greenfield `.gitignore`. [VERIFIED: skills/add-issues/SKILL.md:36-40]. Keep that. Filing an issue against a repo with no wit state stays valid.

## What moves into `skills/setup/SKILL.md`

Copy the first-run body (do not leave scan as an orchestrator that still runs steps 1-7).

| Source | Content | Setup role |
|--------|---------|------------|
| scan SKILL intro "Two jobs" + outputs list | Understand + bootstrap; four files under `.wit/` | Setup's mission and output contract |
| scan Procedure **Host probe** | Detect host; resolve plugin root; no feature `progress.md` | Same, as an advertised entry |
| scan **1** | Root census, greenfield vs existing, `.wi` → `.wit` rename | Setup:1 |
| scan **2** | Existing: stack-detection cookbook → three files; greenfield guided setup + `.gitignore` | Setup:2 |
| scan **3** | Frontend / backend classify | Setup:3 |
| scan **4** | Constitution bootstrap from template; leave if exists | Setup:4 |
| scan **5** | Plugin bootstrap offer | Setup:5; follow the plugin-bootstrap reference |
| scan **6** | Commit scan outputs | End-of-setup commit (see below) |
| scan **7** | 4-8 line report + lean-file warning | Setup report |
| scan templates (repo-map, overview, architecture) + mermaid write rules + `check_mermaid.py` invocation | First write of those files | Inline in setup, same as today in scan |
| models.md **First-run setup** *write* | Absent `.wit/models.md` → ask smart/simple/custom; `--auto` → simple; commit | Setup step after docs, before the commit. Cite `models.md "First-run setup"`; do not duplicate the preset tables |
| dev:1 `.wi` rename | Duplicate of scan:1 | Drop from dev; setup:1 is enough |

Greenfield constitution-confirm stays one folded question round (scan:2 into scan:4). [VERIFIED: docs/design-notes/scan.md:37-38]. Models (and ledger, out of scope here) are extra rounds after that; do not fold models into the constitution confirm.

**Commit:** one setup commit at the end covering docs + models (`chore(wit): setup`), after the current two-commit sequence (`chore(wit): scan - repo docs` then `chore(wit): models config`). [VERIFIED: skills/scan/SKILL.md:81-84; references/models.md:157]. Rename of `.wi` stays its own commit when it happens. Refresh keep `chore(wit): scan refresh`. [VERIFIED: skills/scan/SKILL.md:149]

**`--auto` forwarding:** when dev/rpa invoke setup, pass `--auto` so setup writes the simple models preset without asking. [VERIFIED: references/models.md:158-159 for today's `--auto` → simple]. Ledger `--auto` is question 3; do not specify it here. User-typed `/wit-scan` on a new project has no `--auto` today; setup runs interactive.

## What stays in `skills/scan/SKILL.md`

| Stay | Why |
|------|-----|
| `## --refresh` A (drift check) | The remaining user-facing job; auto-stale from dev:1 |
| `## --refresh` B (memory hygiene) | Learnings/glossary pass; not first-run |
| `## --refresh` C (report) + `chore(wit): scan refresh` | Refresh commit |
| Host probe at entry | Scan is still an advertised command |
| Mermaid trap list in A.3 | Refresh still edits `architecture.md`; "rules above" today points at the template block that will leave this file. [VERIFIED: skills/scan/SKILL.md:108-111, 275-282]. Keep the two parser traps + reserved-word IDs in A.3 so refresh never loads setup |
| `check_mermaid.py` path | Shared script; rpa also cites it. [VERIFIED: skills/rpa/SKILL.md:67] |
| Citation to `stack-detection.md` | A.1 config/lock list. [VERIFIED: skills/scan/SKILL.md:99-100] |
| Lean check in A.6 | Refresh surfaces bloat; does not rewrite constitution |

**Precondition rewrite:** "`.wit/repo-map.md` exists; else invoke setup and stop. Never run a first-document pass from this skill."

**Description (pitfall for plan, not question 1 docs lockstep):** drop first-run auto-triggers (`set up wit here`, `document this codebase`, `opens a new project`) so they can belong to setup. Keep refresh language. Leaving them on scan would steal setup's trigger. Advertised README/AGENTS/alias copy is question 1.

**Intro rewrite:** delete "Two jobs" / bootstrap. One job: re-verify. Point already-scanned users at bare `/wit-scan` (and `--refresh` as synonym). No-map → setup.

Do **not** extract new template files unless setup SKILL size forces it. Scan already inlines templates; moving that block is the smallest diff. stack-detection stays under `skills/scan/references/` (two callers: setup:2 and refresh A.1). `check_mermaid.py` stays under `skills/scan/scripts/`.

## First-run-only references: move with setup

These are never used by `--refresh`:

- `skills/scan/references/constitution-template.md` → `skills/setup/references/constitution-template.md`. Refresh A.5: constitution is user-owned, never rewrite. [VERIFIED: skills/scan/SKILL.md:115]
- `skills/scan/references/plugin-bootstrap.md` → `skills/setup/references/plugin-bootstrap.md`. Refresh does not re-offer plugins. Retarget "On first scan" and "re-run `/wit:scan`" to setup. [VERIFIED: plugin-bootstrap.md:13, 91]. Alias *list* growth is question 1; this question only retargets the offer step.

Leave `stack-detection.md` and `check_mermaid.py` in scan.

## One-liners in dev / rpa

**dev:1** (after host probe, feature/bug-fix only):

- If `.wi/` and no `.wit/`, or `.wit/repo-map.md` missing: run **setup** first (forward `--auto`). Do not proceed without a repo map and constitution.
- Stale map (`scanned` older than ~2 weeks, or config/lock/CI changed): run the scan skill's **`--refresh`** (unchanged).
- **Drop** the `.wi` rename paragraph (setup:1).
- **Drop** "Model routing first-run setup" write/ask. **Keep** apply `.wit/models.md` if present, warn-once on orchestrator mismatch, resolve-once into `## Model routing (resolved)` when `progress.md` is seeded (dev:2). Absent models.md → dispatch rule already says inherit-all. [VERIFIED: references/models.md:182-183]

**rpa** (new, after host probe, before rpa:1):

- If `.wit/repo-map.md` missing: run **setup** first (forward `--auto`), then continue.

**rpa:2** (replace, do not delete resolve):

- **Drop** "Run the model routing first-run setup here too" write/ask. [VERIFIED: skills/rpa/SKILL.md:43-46]
- **Keep** resolve-once + `## Model routing (resolved)` on the run's `progress.md`. Apply existing `.wit/models.md`. Project-level rpa outputs (`inputs.md`, `components.md`, `orchestrator.md`, first-run `rpa-constitution.md`) stay rpa's, committed where written.

Do **not** add "if models.md missing, run setup". That would re-enter full setup on a scanned repo that never ran dev. Question asked for the `.wit`/map tell only. Models-absent upgrade hole: see Risks.

## `models.md` heading rename

Today: `## First-run setup (dev / rpa entry points)`. [VERIFIED: references/models.md:151]

**Rename to:** `## First-run setup (setup)`

Keep the `First-run setup` prefix so citations `models.md "First-run setup"` still resolve. [VERIFIED: skills/dev/SKILL.md:56-57; skills/rpa/SKILL.md:43-44; docs/plans/2026-07-11-prc2-47-49-promote-workflow-drop-section-signs.md:52]

**Body rewrite (write vs resolve):**

- Trigger: when `.wit/models.md` is **absent**, **setup** asks once (smart / simple / custom), writes, commits. `--auto` → simple, logged as an assumption. File persists; never re-asked. Present → skip the write.
- Delete "at a wit entry skill (dev:1, rpa:2)".
- Last paragraph today mixes write with "Setup ends by resolving the routing once and recording it as the `## Model routing (resolved)` block when the feature's `progress.md` is seeded (dev:2 / rpa's run seed)". [VERIFIED: references/models.md:161-163]. **Split:** setup only writes the project file. Resolve-once **stays** at dev:1 / rpa:2 (and first-dispatch fallback). Setup has no `progress.md`.
- `## Dispatch rule` still "At dev:1 / rpa:2". [VERIFIED: references/models.md:167]. Do not move resolve-once into setup.

dev/rpa citations become: apply per `models.md "First-run setup"` (file already written) + resolve-once per `## Dispatch rule`. The first-run *question* is not in those skills.

## Design-notes sync (scan.md rule)

`docs/design-notes/scan.md` sync rule: a rule whose why is deleted instead of relocated loses its guard. [VERIFIED: docs/design-notes/scan.md:13-14]

Move to a new `docs/design-notes/setup.md`, anchored to setup steps: Intro mission (one-time groundwork), scan:2 / :5 / :6 / :7, templates + mermaid why, models first-run *write* why (from `docs/design-notes/dev.md` ## dev:1 routing sentence and `docs/design-notes/rpa.md` ## rpa:2 "trigger plus a citation").

Keep in `docs/design-notes/scan.md`: `--refresh` A and B; rewrite Intro so scan's mission is drift-check, not "one-time groundwork so `/wit:dev` can run". [VERIFIED: docs/design-notes/scan.md:18-23]

`docs/design-notes/dev.md` ## dev:1: "scan-first" becomes "setup-first when the map is missing; `--refresh` when stale". Keep resolve-once why. [VERIFIED: docs/design-notes/dev.md:30-40]

`docs/design-notes/rpa.md` ## rpa:2: first-run *write* citation moves; keep why rpa-build is a role label and why project-level rpa files commit where written. Add a line for the new missing-map → setup one-liner.

## Call sites that must retarget (this question, not advertised-command lockstep)

| Location | Today | After |
|----------|-------|-------|
| `skills/research/references/wit-directory.md` | constitution/repo-map "Written once by scan"; "scan its docs"; "dev/rpa `models.md`" [VERIFIED: wit-directory.md:19-28, 60-61] | setup writes those project files; scan `--refresh` updates facts; models write is setup |
| `skills/research/references/integrations.md` | "scan offers to install the recommended set on first run (see the scan skill's …)" [VERIFIED: integrations.md:14] | setup offers; point at setup's plugin-bootstrap path |
| Template stamps in overview/architecture | "documented … by /wit:scan" [VERIFIED: skills/scan/SKILL.md:210, 248] | new writes say `/wit-setup`. Existing consumer files stay historical |
| plugin-bootstrap "re-run `/wit:scan`" | plugin re-offer [VERIFIED: plugin-bootstrap.md:91] | re-run setup |
| rpa-directory comment | "written when progress.md is seeded (dev:1-2 / rpa:2) from .wit/models.md" [VERIFIED: skills/rpa/references/rpa-directory.md:189] | seed/resolve unchanged; file *create* is setup. Comment can stay if it describes resolve |

Out of this charter: README/AGENTS "four commands", skill-aliases, validate.py skill list, marketplace description (question 1). Ledger skip honor points (question 3).

## Runtime State Inventory

Writer migration (scan/dev first-run → setup), not a string rename of a datastore key.

1. **Stored data:** `.wit/repo-map.md`, `overview.md`, `architecture.md`, `constitution.md`, `models.md` keep those paths. No table/enum value keyed on "scan". Template by-lines in *new* writes change to `/wit-setup`; do not migrate existing consumer files. `.wi` rename remains a git mv + one commit, now under setup.
2. **Live service config outside git:** none keyed on scan-as-writer. Skill id `scan` stays user-facing (refresh).
3. **OS / platform-registered state:** none. Alias install is question 1.
4. **Secrets & env-var names:** none.
5. **Build / installed artifacts:** skill name `scan` remains; no published package rename. `check_mermaid.py` path stays.

Code edit is not a data migration. No backfill of old "by /wit:scan" stamps.

## Comparison (section ownership)

| Approach | Complexity | Blast radius | Rejected because |
|----------|------------|--------------|------------------|
| **Move first-run text into setup (chosen)** | One new skill body; scan shrinks to refresh | Scan/dev/rpa/models.md/design-notes + two reference moves | — |
| Setup orchestrates scan's old Procedure 1-7 | Smaller copy-paste | Scan keeps first-run forever; two skills to edit in lockstep | Brief: "not an orchestrator that still calls scan's old body" [VERIFIED: brief.md:70] |
| Delete first-run from scan; no-map only *tells* the user to type setup | Smallest scan diff | `/wit-scan` on a new project becomes a dead end; fights brief "invokes setup" and "run setup first, then continue" | Question: missing `.wit/` at scan *invokes* setup |

## Assumptions Log

| Claim | Why assumed | Load-bearing? |
|-------|-------------|---------------|
| Bare scan should not require `--refresh` | Brief example omits the flag; one remaining job | yes |
| Scan that invoked setup then **stops** (no chained refresh) | Avoid double commit / re-stamp of a fresh map | yes |
| Tell is `repo-map.md` missing, not `.wit/` directory missing | add-issues can create `.wit/` first | yes |
| Setup does not seed `## Model routing (resolved)` | No feature folder at setup time | yes |
| Already-scanned repos without `models.md` inherit-all until the user runs setup | Question forbids models first-run in dev/rpa | yes |
| One setup commit for docs+models | Brief "commit" singular; fewer commits | no |
| constitution-template and plugin-bootstrap move under `skills/setup/references/` | First-run-only files | no (could cite in place) |

## Risks / unknowns

- **Upgrade hole:** a repo that ran old scan (has repo-map, no `models.md`) will no longer get the smart/simple/custom question on first `/wit:dev` or `/wit:rpa`. Dispatch inherit-all. [VERIFIED: references/models.md:182-183]. Plan: pitfalls.md; optional user-facing "run `/wit-setup` to configure models". Do not auto-invoke setup from that tell.
- **Investigation:** "missing .wit at dev" must not fire for work type investigation. [VERIFIED: skills/dev/SKILL.md:38-39]
- **`--auto` forwarding** from dev/rpa into setup is required or the models question reappears on hands-off new projects.
- **Mermaid "rules above"** in refresh A.3 breaks when templates leave scan. A.3 must carry the trap list (or a reference). Unverified until the edit: whether inlining ~15 lines exceeds scan's lean target. [ASSUMED]
- **plugin-bootstrap path** is cited from integrations.md and historically "the scan skill". Moving the file without retargeting those citations leaves a dead path. Pair the move with those citation edits (not README four-command pins).
- **Rpa new behavior:** first `/wit:rpa` on a greenfield repo will run full setup (repo-map, constitution, plugins, models) before UiPath bootstrap. Today rpa skipped scan entirely. Required by the brief; call it out in rpa design notes so it is not "simplified" away.
- Ledger question and `ledger:` key: question 3. Setup's step list has a slot after models; do not invent the key here.

## Dependency Legitimacy

none added.

## Don't-Hand-Roll

| Problem | Don't build | Use instead | Why |
|---------|-------------|-------------|-----|
| First-run docs | New documenter in setup that calls scan's Procedure | Move steps 1-7 + templates | Brief; one writer |
| Models question | Duplicate preset tables in setup/SKILL.md | Cite `models.md "First-run setup"` | Already canonical; drifted when duplicated [VERIFIED: docs/design-notes/rpa.md:37-39] |
| Refresh vs first-run dispatcher | New flag parser script | Skill-text tell on `repo-map.md` | Matches today's scan/dev pattern; no new code |

## Verified this session

- `skills/scan/SKILL.md` Procedure 1-7 vs `## --refresh` A/B/C, including "this IS a first scan" (2026-08-27)
- `skills/dev/SKILL.md` step 1 scan-if-missing, stale `--refresh`, models first-run, investigation skip
- `skills/rpa/SKILL.md` rpa:2 models first-run; no scan-if-missing
- `references/models.md` `## First-run setup (dev / rpa entry points)` + dispatch rule
- `skills/add-issues/SKILL.md` no scan/setup; creates `.wit/issues/`
- `docs/design-notes/scan.md` sync rule; first-run vs refresh why
- `docs/design-notes/dev.md` ## dev:1; work-type prelude
- `docs/design-notes/rpa.md` ## rpa:2 trigger-plus-citation
- `skills/scan/references/plugin-bootstrap.md` first-scan offer + re-run scan
- brief.md acceptance + open question on bare scan
- No web, no spike, no new deps
