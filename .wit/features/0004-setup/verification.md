---
type: Verification
title: Verification - /wit-setup first-run (plan mode)
description: Round 2. Scan-invoke BLOCKER closed. Remaining WARNINGs on ceilings, RPA gate skip, and stamp templates.
feature: 0004-setup
status: issues-found
timestamp: 2026-08-27
---

# Verification: /wit-setup first-run (plan mode)

Work type: feature. Bug-fix matrix skipped. Safety fact result-mode rows skipped.
Mode: plan, round 2 of 2. Applicable learnings: 0003-work-type-routing; 0003-blast-radius-proof (honor, no covering task required).

Round 1 BLOCKER (Task 2 tell-only vs ADR-0004 run-setup) is closed: Task 2 Do now **runs setup** (no mere tell, no chained refresh). Spec AC2 matches (`spec.md:38-40`). ADR-0004 scan/dev/rpa invoke is mapped.

## Coverage matrix

| Item | Covering task / honor | Result |
|------|----------------------|--------|
| AC1 setup SKILL user-invocable, owns first-run (docs, models, ledger), `--auto` simple + `ledger \| on` | Task 1 | covered |
| AC2 scan refresh-only; bare invoke silent `--refresh`; missing repo-map **runs setup**; no re-doc in scan; no chained refresh | Task 2 | covered |
| AC3 dev:1 / rpa:2 invoke setup on missing repo-map; forward `--auto`; no models.md write; resolve-once stays; investigation skip; add-issues skip; absent models.md + map present runs models+ledger slice | Task 4 | covered |
| AC4 `## Token ledger` / `ledger` `on` \| `skip`; absent or not-exact-`skip` is `on`; skip: no `--init`, no finalize, no token table, no ship:8 `check_tokens.py` | Task 4 (shape + default + stamp Do); Task 5 (honor sites listed) | covered at named Files; see WARNING for RPA verification-gate leftover |
| AC5 five advertised commands; README setup-first; USER_COMMANDS alpha including setup; alias `wit-setup/`; manifests + RELEASE 1.16.2; catalog 0.2.0; architecture entry subgraph includes setup; plugin-root tell stays `skills/scan/SKILL.md` | Task 1 (lockstep, tell, 1.16.2, catalog, subgraph); Task 3 (alias + host maps) | covered |
| ADR-0004 fifth command owns first-run; scan user-facing refresh; bare scan silent refresh; missing `repo-map.md` at scan / dev / rpa **runs setup first**; add-issues does not; investigation skips; fail-closed `on`; `--auto` simple + `ledger \| on`; plugin-root tell stays scan; no new PLUGIN_ROOT file | Task 1, 2, 3, 4, 5 | covered (scan invoke is Task 2) |
| Glossary **Setup** (scan / dev / rpa run setup first) | Task 2 (scan); Task 4 (dev/rpa) | covered (locked tell is missing `repo-map.md`, not missing `.wit/`) |
| Glossary **Scan** (refresh only; does not create from scratch) | Task 2 | covered |
| Pitfall glob vs four-command tests | Task 1 | covered |
| Pitfall directory tell vs add-issues (tell is missing `repo-map.md`) | Task 2, Task 4 | covered |
| Pitfall scan tell-only | Task 2 (run setup; no chained refresh) | covered |
| Pitfall refresh A.3 dangling "rules above" | Task 2 | covered |
| Pitfall inherit-all upgrade hole | Task 4 | covered |
| Pitfall investigation calls setup | Task 4 | covered |
| Pitfall skip still inits tokens.md / dossier mandatory | Task 5 | covered at listed files; see WARNING for RPA verification-gate |
| Pitfall plugin-root tell swapped to setup | Task 1 | covered |
| Pitfall new PLUGIN_ROOT always-loaded file | ledger in `.wit/models.md`; no new PLUGIN_ROOT target in Files | covered |
| Pitfall mid-run ledger toggle | Task 5 | covered |
| Pitfall Grok `/setup` clash | Task 3 (`references/grok-tools.md` branded `/wit-setup`); Task 1 advertised set | covered |
| Pitfall architecture `(1.16.0)` PLUGIN_ROOT caption | Task 1 | covered |
| Learning 0003-work-type-routing (serial wiring after new files exist) | honored: Task 1 creates `skills/setup/SKILL.md`; Task 2 and Task 4 add pointers after. Task 5 Depends on 4 for `skills/dev/SKILL.md` + `skills/rpa/SKILL.md` overlap. No parallel create+point wave. | honored |
| Learning 0003-blast-radius-proof (second checker table before bug-fix matrix) | N/A: plan does not edit `agents/wit-code-checker.md` or add a checker coverage table | honored (N/A) |
| Constitution: public skill contract needs ADR | ADR-0004 present | covered |
| Constitution: no em dashes in shipped text | every task `assertNotIn` em dash on files it edits | covered |
| Constitution: TDD / tests in `tests/` | Task 1 failing asserts first; `tests/test_setup.py` | covered |
| Constitution: hotspot files serial | Waves 4 then 5; Task 5 Depends on 4 | covered |
| Constitution: three-manifest lockstep | Task 1 RELEASE 1.16.2 | covered |
| Constitution: behavior bumps minor | spec locks patch 1.16.2 (owner directed) | see INFO |
| Locked: tell predicate is missing `repo-map.md` not missing `.wit/` | Task 2, Task 4 | covered |
| Locked: bare scan is silent `--refresh` | Task 2 | covered |
| Locked: setup does not seed `## Model routing (resolved)` | Task 4 resolve-once stays | covered |
| Locked: fail-closed ledger default `on` | Task 4, Task 5 | covered |
| Locked: no mid-run ledger toggle | Task 5 | covered |
| Spec Design: stamp `· ledger: <on\|skip>` on resolved-routing first bullet | Task 4 Do names the stamp; templates live in Task 5 Files | see WARNING |

## Findings

### BLOCKER

None. Round 1 scan tell-only BLOCKER is closed.

### WARNING

1. **Task 1 exceeds the task-unit ceiling.** Files list 13 paths (`tasks.md:15-18`) and two concerns (first-run body moved from scan 1-7 plus models/ledger, and five-command lockstep). Rough ceiling is ~5-8 files. Pre-mortem: a fresh runner is likely to ship an incomplete first-run body or a green glob with a thin setup SKILL.

2. **Task 5 exceeds the task-unit ceiling and includes a research don't-touch file.** Files list 12 paths (`tasks.md:76-81`). Research `ledger-skip.md:153-158` says do **not** mention skip in `skills/scan/references/constitution-template.md` (that template has no tokens.md wording). Listing it inflates an already oversized unit and invites a constitution skip rule the research note forbids.

3. **RPA local green still requires `tokens.md`.** Research honor point 4 and minimum file 8 is `skills/rpa/references/verification-gate.md` (`ledger-skip.md:102-107`, `:143`): "token ledger `tokens.md` passes `check_tokens.py`" (`verification-gate.md:125-126`). Task 5 Files omit it. `skills/rpa/SKILL.md:141-143` still sets Gate = that file. Built exactly as written, skip plus rpa:7 following the unedited gate still demands a ledger skip forbids creating. `rpa/SKILL.md` is in Task 5; the loaded-alone gate is not.

4. **Resolve-once `· ledger:` stamp is split across tasks.** Spec Design (`spec.md:60`) and research (`ledger-skip.md:30`, `:45-49`) stamp `· ledger: <on|skip>` on the progress.md resolved-routing first bullet. Honor points read that stamp; missing `ledger:` fail-closes to `on` (`ledger-skip.md:30`). Task 4 Do names the stamp (`tasks.md:68-70`) but Files omit the templates (`wit-directory.md:175`, `rpa-directory.md:193`). Task 5 lists those templates (`tasks.md:78-79`) but Do is skip carve-out only (`tasks.md:82-87`). Seed today copies the template (`skills/dev/SKILL.md:72`).

5. **Task 3 Verify is only the new class after appending a shared test module.** Task 3 Depends on 2 and appends `SetupAliasTests` to `tests/test_setup.py` (`tasks.md:49-57`). Verify: `python -m unittest tests.test_setup.SetupAliasTests` only. A bad append can break Task 1/2 classes without failing this Verify.

6. **Leftover first-run citations outside Task 2's retarget list.** Task 2 one-line retargets `workflow.md`, `capabilities.md`, `integrations.md`, `add-issues/SKILL.md` (`tasks.md:42-45`). Still loaded after a refresh-only scan:
   - `skills/research/references/wit-directory.md:19` "Written once by scan"; `:28` models.md "written+committed at first dev/rpa run". Task 5 lists the file; Do is skip only.
   - `references/skill-aliases/wit-scan/SKILL.md:5-6` still "bootstrap wit". No task Files list.

### INFO

7. **Pre-mortem file overlap is serialized, not hidden.** Task 4 and Task 5 both list `skills/dev/SKILL.md` and `skills/rpa/SKILL.md`; Task 5 Depends on 4 (`tasks.md:89`). Task 2 and Task 3 both append `tests/test_setup.py`; Task 3 Depends on 2 (`tasks.md:58`). Task 2 and Task 4 share `tests/test_setup.py` with no Depends-on edge (both Depend on 1); Waves list 2 then 4.

8. **Constitution versioning vs owner patch.** Constitution says behavior/artifact changes bump minor. Spec locks 1.16.2 because the owner directed 1.16.x (`spec.md:87-88`). Recorded override, not a missing task.

9. **Recommended pins not in the plan (not required by ACs):** `tests/test_models_config.py` Token-ledger-ignored clone; `references/moa.md` skip clause (`ledger-skip.md:148-151`). Spec test plan is `tests/test_setup.py` string pins (`spec.md:79-81`). Host tool-map finalize one-liners need no skip prose (`ledger-skip.md:89`).

10. **Brief origin vs locked spec.** Brief still says no repo-map → tell / send the user to setup (`brief.md:22-23`, `:44`). Spec AC2, ADR-0004, and Task 2 **run** setup. Origin text, not a task miss.

11. **Keep the `## tokens.md template` heading** in wit-directory even when skip exists (`ledger-skip.md:206`; `test_capabilities.py` slices on it). Task 5 Do does not name that pin.

## Silent down-scope

None remaining. Scan missing-map dispatcher now runs setup (finding 1 from round 1 closed). No v1/stub/TODO in tasks. Models first-run move, ledger skip, five-command lockstep, and text-move (not wrap scan) are not stubbed. `--auto` forward is in Task 4 Do (`tasks.md:65`). Setup description triggers ("set up wit here", "bootstrap wit") are in Task 1 Do (`tasks.md:23-24`).

## Over-build

No new dependency, no `.wit/setup.md`, no `validate.py` command registry, no `check_tokens.py --skip`. Simplicity ladder held. Finding 2 is the extra-file note (`constitution-template.md` against research don't-touch).

## Pre-mortem

- Task 1 (13 files, two concerns) is the stall line if the runner greens lockstep tests with a thin setup body.
- Task 5 (12 files) is the stall line if skip is applied to SKILL.md `--init` sites and not to `verification-gate.md` / dossier sentences, or if constitution-template gets a skip rule.
- Task 4/5 `skills/dev/SKILL.md` + `skills/rpa/SKILL.md` overlap: serialized by Depends on 4.
- Task 2/3 `tests/test_setup.py` overlap: serialized by Depends on 2; Task 3 Verify class-only (finding 5).
- Task 2/4 `tests/test_setup.py` overlap: Waves 2 then 4; file-overlap DAG.
- Round 2 of 2: remaining WARNINGs escalate to the human design gate. No further checker loop.

## Verdict

Plan mode round 2. Round 1 BLOCKER closed (Task 2 runs setup; AC2 matches ADR-0004). No new BLOCKER. WARNINGs remain on ceilings, RPA verification-gate skip, stamp-template split, Task 3 class-only Verify, and leftover first-run citations. Learnings honored. Escalate remaining findings to the design gate.

## ISSUES FOUND
