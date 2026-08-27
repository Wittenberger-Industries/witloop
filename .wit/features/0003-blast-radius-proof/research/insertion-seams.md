---
type: Research Note
title: Safety-fact insertion seams
description: Where safety-fact and honest-gap rows land in ship, PR.md, checker result mode, and the RPA gate.
feature: 0003-blast-radius-proof
timestamp: 2026-08-27
valid_until: 2026-09-26
---

# Safety-fact insertion seams

## Responsibility Map

Plugin markdown + one agent charter. No frontend/backend split. Ship writes the durable row into `PR.md`; the checker judges it in result mode; RPA reuses that same charter and the same `PR.md` template.

## Decision (one insertion plan)

Add an **unconditional** `### Safety fact` block to the ship:5 `PR.md` template (between `### Testing` and `### Verification`). Add **always-on result-mode coverage-matrix rows** to `wit-code-checker` (same additive-table pattern as the bug-fix extra rows, but **not** work-type-gated and **not** in plan mode). Fold the checker's matrix row into that heading at ship:5, then prune `verification.md` as today. Point the RPA verification gate at those same rows; do not duplicate the table and do not add a second gate, a sixth run step, a new artifact, or a fourth severity.

Honest `unproven` is **INFO**. Missing row or writeup-only is **BLOCKER**. Valid docs-only `n/a` is **INFO**. `n/a` on a behavior diff is **BLOCKER**.

## Why this seam (not a new file)

[VERIFIED: skills/ship/SKILL.md:49-97, 202-248] Result-mode already writes ephemeral `verification.md`; ship:5 already distills it into `PR.md` `### Verification`; ship:6 already prunes it. [VERIFIED: agents/wit-code-checker.md:100-112, docs/design-notes/wit-code-checker.md:98-110] Bug-fix extra matrix rows already teach "omission is a BLOCKER in the named pass" without a new severity or a second agent. [VERIFIED: brief.md Scope] No `verify-report.md`. [VERIFIED: .wit/glossary.md:25-29] The terms Safety fact and Unproven already exist.

A dedicated `### Safety fact` heading (brief preference) is the durable user-visible copy. It is **not** folded into `### Verification` prose, because that is how a writeup swallows the row. Verification stays the checker verdict (+ bug-fix matrix when Work type is bug-fix). Safety fact stays the one proof row plus any named extras that were not run.

## PR.md heading (exact)

Unconditional. Not work-type-gated. Not omitted on docs-only (`n/a` still needs the heading). Insert in the fenced template in `skills/ship/SKILL.md` after `### Testing` and before `### Verification`:

```markdown
### Safety fact
- **Claim:** <one sentence: the change is safe because of this>
- **Proof:** `<command run this session>` | unproven (<why>) | n/a (<docs-only reason>)
- **Not run:** <named extra check>: unproven
```

Rules for that block:

- **Claim** is one fact, not a restatement of the whole suite. A green `python -m unittest discover -s tests` does not replace it. The proving command may already appear under `### Testing`; Safety fact **points at** it. [VERIFIED: brief.md example]
- **Proof** is exactly one of: a this-session command (would fail if the claim is false), the word `unproven` plus why, or `n/a` plus a docs-only reason. Any other body is writeup-only.
- **Not run** lists extra **named** checks that are not repo-map / RPA-gate commands and were not run this session, each `unproven`. Omit the bullet when nothing extra was named. Do **not** invent unnamed visual/perf rows so every PR looks instrumented (that is roadmap row 2, out of scope).
- Do not add a sibling `### Honest gaps` heading. YAGNI; the Not-run bullets are the honest-gap rows.

Ship:5 prose (above the fence, beside today's bug-fix sentences at SKILL.md:210-211): always copy the result-mode Safety fact matrix row into this heading; do not replace Proof with narrative. Bug-fix evidence stays where it is (Summary / Testing / Verification). Rules inventory stays conditional.

## Checker: result-mode only, always-on

Prior art: the work-type-gated table at `agents/wit-code-checker.md:100-109`, plus the result-only frontend WARNING at `:131-135`.

**Plan mode: skip.** A safety fact is a this-session ship proof. Plan-mode cannot see gate logs. Do not require a covering task. Carve glossary terms **Safety fact** and **Unproven** out of the plan-mode "glossary term that must be honored" mapping (`wit-code-checker.md:87-90`) so every feature plan does not pick up an unmapped-term BLOCKER. Cover them with the result-mode rows below. [VERIFIED: glossary.md:25-29 honor point is "At ship"]

**Result mode: every shipping work type** (feature, bug-fix, RPA). Investigation never ships. Do not skip when Work type is missing or `feature` (the opposite of the bug-fix table). Bug-fix still carries its own five rows **and** this table; the same-surface command may also be the Safety fact Proof.

Add a second small table immediately after the bug-fix one (do not merge; keep the work-type gate on bug-fix rows intact per ADR-0002):

| Item | Plan mode | Result mode | Severity |
| Safety fact (one claim + Proof) | skip | If `PR.md` exists: heading `### Safety fact` whose Proof is a this-session command, `unproven`, or `n/a` plus docs-only reason. If `PR.md` is absent (first ship:2, before ship:5): the checker still **writes this row** into `verification.md` from this-session evidence (`.logs/gate-*.txt` or RPA analyzer/validate logs). Writeup-only = prose with none of those three tokens. | omitted matrix row, missing heading when `PR.md` exists, or writeup-only: **BLOCKER**. Honest `unproven`: **INFO**. Valid `n/a`: **INFO**. `n/a` on a runtime-behavior diff: **BLOCKER**. |
| Named extra non-gate checks | skip | Each extra check named in spec.md (RPA: sdd.md), pitfalls.md (RPA: assumptions.md), or Testing that is not a repo-map / RPA-gate command and has no this-session log: listed `unproven` under Not run. | named but omitted: **BLOCKER**. Listed `unproven`: **INFO**. |

Do not change report caps, `## CHECK PASSED` / `## ISSUES FOUND`, tools, or the 2-round loop. [VERIFIED: constitution.md Architecture; ADR-0002 decision 6; design-notes/wit-code-checker.md:107-110]

### Sequencing (ship:2 before ship:5)

[VERIFIED: skills/ship/SKILL.md:29-65 vs :202] Checker result-mode runs at ship:2; `PR.md` is first written at ship:5. Do **not** reorder. Do **not** pre-write `PR.md` at ship:1 (wit-directory "one writer per phase"; ship:5 owns `PR.md`). Do **not** add a second checker dispatch after ship:5.

Absent-`PR.md` is therefore **not** a missing Safety fact. The checker fills the matrix row in `verification.md`. Ship:5 copies that row under `### Safety fact`. When `PR.md` already exists (keep-alive re-entry, a second review round after the file was written), missing heading or writeup-only is BLOCKER. That is the bug-fix "PR names it" idea with the first-pass hole closed.

Happy-path copy hole (green checker, then ship:5 drops the heading): close with (1) the template heading always present, (2) ship:5 "copy the row verbatim" prose, (3) one ship:8 close-out box: `PR.md` contains `### Safety fact` whose Proof is a this-session command, `unproven`, or `n/a`. That box is not a second gate; it is the same class as today's "PR.md exists" checkbox at SKILL.md:401-402.

### Why INFO, not WARNING, for honest unproven

[VERIFIED: skills/ship/SKILL.md:96-97] A WARNING carried into `PR.md` needs a roadmap line or GitHub issue. Mapping unproven to WARNING (roadmap row 4 Adopt text) would turn every honest gap into a waiver ceremony, which is the D3 WAIVED band under another name. [VERIFIED: brief.md constraints; progress.md Decisions] No WAIVED band. Brief prefers INFO. INFO never loops (`wit-code-checker.md:147-150`). Only BLOCKER returns to build / blocks the PR (`ship/SKILL.md:85-94`).

Known wrinkle, do not "fix": an INFO-only report in practice returns `## ISSUES FOUND` [VERIFIED: docs/design-notes/wit-code-checker.md:79-80]. Ship already keys the loop on BLOCKER presence, not on that marker. Leave the markers unchanged.

Roadmap Adopt also said every AC is PASS / unproven / waived. **Do not implement that.** Existing "What green means" already requires each acceptance criterion to map to a check that passed (`verification-gate.md:57-58`). Unproven is not a way to skip an AC or a configured repo-map command. Honor the brief over the harvest paragraph.

## Docs-only tell (no fourth work type)

[VERIFIED: ADR-0002] Work types stay `feature` | `bug-fix` | `investigation`. Do not add docs-only as a type.

`n/a` is valid **only** when Proof is `n/a` plus a one-line reason **and** `git diff --stat` does not touch runtime-loaded plugin surfaces. Runtime-loaded for this repo:

- `skills/`
- `agents/`
- `scripts/`
- `tests/`
- `references/`
- `.claude-plugin/`
- `.codex-plugin/`
- `AGENTS.md`

Examples that may use `n/a`: `docs/`, README-only, `.wit/roadmap.md` only. A SKILL.md / agent charter / `validate.py` / unittest change is behavior: Proof must be a command or `unproven`, never `n/a`. Checker: `n/a` plus a touched runtime path = BLOCKER (false docs-only). Docs-only with a real command is allowed (over-proving). Missing heading is still BLOCKER.

Repo-map `n/a - not configured` for lint/format/typecheck stays under `### Testing`. Do not collide those tokens with Safety fact `n/a`.

## Iron law (unchanged)

Do **not** add a sixth item to `verification-gate.md` "Run, in this order". Safety fact is PR honesty, not a new command.

Add one paragraph after the Testing capture sentence (`verification-gate.md:39`) and a "do not skip" clause under the iron law (`:14-27`):

- Testing still lists every repo-map gate command actually run.
- `### Safety fact` names one claim and points at one this-session command, or says `unproven` / `n/a`.
- `unproven` never skips a configured repo-map command (`python scripts/validate.py`, `python -m unittest discover -s tests` here). Those stay red-gate on failure, as today.
- Iron-law red flags ("should pass", "looks good", quoting an earlier message) are the writeup-only BLOCKER on the Safety fact row.

## RPA sameness

[VERIFIED: skills/rpa/SKILL.md:141-166] RPA runs `${PLUGIN_ROOT}/skills/rpa/references/verification-gate.md` (tooling + checker result mode), then reuses **ship** for docs-sync, `PR.md`, close-out. It does not invent a second PR template. The ship:5 heading therefore appears on RPA PRs automatically.

[VERIFIED: skills/rpa/references/verification-gate.md:75-115] The RPA gate already dispatches the same `wit-code-checker` charter, "same interface and logging as ship:2", with spec.md → sdd.md and pitfalls.md → assumptions.md. Always-on result-mode rows in the charter apply with no RPA fork.

Because each touched file must still decide correctly if loaded alone (constitution Git), add a **pointer paragraph** in the RPA "Checker (result mode)" section, not a copied table:

- Same Safety fact + named-extra rows as `agents/wit-code-checker.md`.
- Proof command = a this-session command from **this** gate's list (`uip restore` / validate / Analyzer / Maestro validate or eval), or `unproven`, or `n/a`.
- Unproven does not skip restore, validate, Analyzer error-level, or paradigm check.
- Named extras (example: Maestro `eval` when no eval sets exist) list `unproven` rather than vanishing from Testing.

Optional one-line under "What green means" (`:117-126`): result-mode matrix includes the Safety fact row. Do not rename that section's existing "verdict is PASS" (it already means checker green, not D3 PASS). Do not edit `skills/rpa/SKILL.md` (fewest files; it already points at this gate + ship:5).

## Files to change

| File | What to insert | Why |
| `skills/ship/SKILL.md` | Unconditional `### Safety fact` in the ship:5 template; copy-the-row prose; ship:8 close-out box. One sentence at ship:1 pointing at the gate paragraph, not a new run step. | Durable row. Sole `PR.md` writer. |
| `skills/ship/references/verification-gate.md` | Honesty paragraph + iron-law "unproven does not skip" clause. No step 6. | Gate file still decides if loaded alone. |
| `agents/wit-code-checker.md` | Glossary carve-out for plan mode; always-on result-mode table (Safety fact + named extras). | BLOCKER without a fourth severity. Single review agent. |
| `skills/rpa/references/verification-gate.md` | Pointer in checker result-mode section; optional green-means bullet. | RPA gate loaded-alone; same rows. |
| `docs/design-notes/wit-code-checker.md` | Additive subsection, sibling to "Additive bug-fix matrix rows". | Charter edits keep rationale in sync (file's own rule). |
| `docs/design-notes/ship.md` | ship:5 bullet: why Safety fact is a sibling heading, why INFO, why no second gate. | Skill edits keep rationale in sync. |

Do not add `verify-report.md`. Do not edit `skills/rpa/SKILL.md`, `wit-directory.md`, `workflow.md`, or ADR-0001/0002/0003. Glossary already defines the terms.

## Don't-hand-roll

| Problem | Do not build | Use instead | Why |
| Blast-radius writeup as a new dossier type | `verify-report.md` | `PR.md` `### Safety fact` + ephemeral matrix row in `verification.md` | Ship already folds checker output into `PR.md`. |
| D3 PASS / CONCERNS / FAIL / WAIVED | Fourth public vocabulary | BLOCKER / WARNING / INFO | Brief + checker contract. |
| Unproven as WARNING | Waiver pointer per unproven row | INFO | WARNING requires issue/roadmap pointer (`ship/SKILL.md:96-97`). |
| Docs-only work type | Fourth `--kind` | `n/a` + diff tell | ADR-0002 standing. |
| Sixth gate command | New item in "Run, in this order" | Honesty row pointing at a command already in Testing | Iron law unchanged. |
| `### Honest gaps` heading | Extra PR section | Not-run bullets under `### Safety fact` | One heading, brief preference. |
| Plan-mode covering task | Fake "run the proof" task | Result-mode only | This-session evidence does not exist at the design gate. |
| Second checker after ship:5 | Extra dispatch | Absent-`PR.md` fallback + ship:5 copy + ship:8 box | One result-mode dispatch. |

## Alternatives rejected

1. **Put the row only inside `### Verification`.** Rejected: Verification is distilled narrative; a writeup can hide the fact. Brief asked for `### Safety fact`.
2. **Reorder checker after ship:5.** Rejected: Verification is distilled *from* the checker, so `PR.md` cannot be complete first; ship:2 review-before-package stays.
3. **Pre-write `PR.md` at ship:1.** Rejected: two writers on one dossier file; ship:5 already owns it.
4. **Work-type-gate the rows like bug-fix.** Rejected: every behavior PR needs the fact, including features.
5. **Plan-mode row that tasks must name the proof command.** Rejected: out of brief scope; cannot prove this-session.
6. **INFO-less matrix tick with no finding.** Rejected: brief wants unproven **visible**. INFO is the visible non-fail.

## Tests (production files a contract test would Read)

Sibling owns unittest shape and the 1.16.x bump. A string/charter test in the existing style (`tests/test_keep_alive.py`, `tests/test_validate_portability.py`: `Path.read_text`, assert heading / token / table strings) would Read:

- `skills/ship/SKILL.md` (heading `### Safety fact`, Proof tokens `unproven` and `n/a`, placement between Testing and Verification, close-out box)
- `skills/ship/references/verification-gate.md` (no sixth Run step; unproven-does-not-skip clause)
- `agents/wit-code-checker.md` (result-mode table: missing/writeup-only BLOCKER; honest unproven INFO; plan-mode skip / glossary carve-out)
- `skills/rpa/references/verification-gate.md` (pointer to the same rows; no duplicated D3 names)

Do not live-dispatch a checker. Do not add a Python parser for `PR.md` bodies beyond reading those skill/charter strings unless the sibling's contract-test note says otherwise.

## Assumptions Log

| Claim | Why assumed | Load-bearing? |
| RPA skips ship:1/ship:2 and reuses ship from docs-sync / PR onward | Stated at `skills/rpa/SKILL.md:141-147` [VERIFIED] | Yes: RPA gate must carry the pointer so the checker still runs the rows |
| INFO-only unproven yields `## ISSUES FOUND` in practice but does not loop or block the PR | Design notes wrinkle + ship:2 BLOCKER rule [VERIFIED] | Yes: spec must say INFO does not return to build |
| Roadmap Adopt (unproven → WARNING; every AC is PASS/unproven/waived) is superseded by this brief | Brief + progress.md Decisions vs `.wit/roadmap.md:117-122` [VERIFIED] | Yes: plan must not implement the harvest paragraph |
| Docs-only path list is complete for this plugin | No existing classifier in repo; list derived from layout [ASSUMED completeness] | Yes: false `n/a` vs missed `n/a` → spec Open question if plan wants a different path set |
| `tests/test_bug_fix_checker.py` / `tests/test_work_type_release.py` are absent on this worktree | Glob of `tests/` [VERIFIED] | No (sibling charter) |

## Risks / unknowns

- First-pass result-mode has no `PR.md`. If the charter forgets the absent-file fallback, every ship:2 is a BLOCKER. Plan must state the fallback in the table.
- Ship:5 must copy the row; template + close-out are the backstop, not a live checker re-read.
- INFO-only `## ISSUES FOUND` may confuse a human reading the console; do not change markers; say so in pitfalls.
- Do not let `unproven` leak onto configured repo-map / RPA-gate commands.
- Do not collide Testing's repo-map `n/a - not configured` with Safety fact `n/a`.
- Charter is a sensitive surface: additive table only; no marker/tool/cap edits (constitution).
- Docs-only path list may need a spec Open question if README vs `AGENTS.md` classification is disputed.

## Dependency Legitimacy

None added.

## Hard-to-reverse?

No. Additive heading, additive matrix rows, same taxonomy. Reversible by deleting those insertions. Public `PR.md` shape changes slightly but does not fork the dossier manifest or the review-agent contract. No new ADR required beyond following standing ADR-0001/0002/0003 (do not add a work type, do not add a review agent, do not special-case plugin root).
