---
type: Research Note
title: "Classification seam: work type before feature-folder classify"
description: Where /wit:dev infers or overrides feature, bug-fix, and investigation without changing the existing feature path.
feature: 0003-work-type-routing
timestamp: 2026-08-25
valid_until: 2026-09-24
---

# Classification seam: work type before feature-folder classify

## Responsibility Map

- **Orchestrator / plugin (not an app):** `/wit:dev` (`skills/dev/SKILL.md`) owns flag parse, work-type classify, announce, and the branch. Host adapters and flat aliases only forward arguments. [VERIFIED: skills/dev/SKILL.md:47-52, references/skill-aliases/wit-dev/SKILL.md:19-20, .wit/repo-map.md:13]
- **On-demand references:** route-specific procedure (investigation exit, bug-fix flow) stays out of the always-loaded skill. Feature-folder edge cases stay in `references/feature-folder-cases.md`. [VERIFIED: references/feature-folder-cases.md:11-17, docs/design-notes/dev.md:42-47]
- **Stdlib script + unit tests:** flag parse, `--kind` validation, exclusive tell table, and ambiguous-default live in one small Python helper so the constitution's test rule can pin them. [VERIFIED: .wit/constitution.md:32-34, tests/test_check_draft.py:1-11]
- **Not this charter:** investigation execution, bug-fix phases/gates/evidence, product-code edits, new dependencies.

## Question

Where can Witloop infer or override `feature`, `bug-fix`, and `investigation` before feature-folder classification while leaving the existing feature path unchanged?

## Current entry points [VERIFIED]

`/wit:dev` is the only advertised design-and-build command. There is no work-type flag and no intent class today. The skill classifies **feature-folder state**, not kind of work. [VERIFIED: skills/dev/SKILL.md:47-52, .wit/roadmap.md:38]

| Host | How the user enters | What happens to flags |
|---|---|---|
| Claude | `/wit:dev <idea> [--auto]` | skill body is the procedure |
| Copilot / Grok (flat alias) | `/wit-dev` | `references/skill-aliases/wit-dev/SKILL.md` locates the plugin root, reads `AGENTS.md`, follows `skills/dev/SKILL.md`, **passing `--auto` through if given** [VERIFIED: references/skill-aliases/wit-dev/SKILL.md:19-20] |
| Codex | `$wit-dev` (same alias file) | same forwarder [VERIFIED: skills/scan/references/plugin-bootstrap.md:64-70] |
| Cursor | plugin skill + natural-language auto-trigger from `description` | no alias copy required [VERIFIED: references/cursor-tools.md:44-45] |
| All five | raw plugin forms `/wit dev` / `$dev` | always work [VERIFIED: AGENTS.md:34-36] |

Natural-language auto-trigger is the `description` field. Today's phrases are feature-shaped only: `/wit:dev <idea>`, "build me", "I want a feature", "add \<capability\>", "design-and-build", plus `--auto`. [VERIFIED: skills/dev/SKILL.md:4-9]

`add-issues` competes on bug-shaped language ("file a bug", pasted stack traces). That skill **files** an issue; it does not fix. [VERIFIED: skills/add-issues/SKILL.md:4-12, .wit/roadmap.md:39]

RPA and add-issues are out of scope as new commands. They already parse `--auto` in their own skills; they do not grow `--kind`. [VERIFIED: brief.md:45-46, references/skill-aliases/wit-rpa/SKILL.md:20, references/skill-aliases/wit-add-issues/SKILL.md:20]

## Current parse and classify order [VERIFIED]

`skills/dev/SKILL.md` procedure, numbered:

1. **Host probe, scan precondition, model routing.** May write `.wit/` (rename `.wi`, scan, `.wit/models.md`). [VERIFIED: skills/dev/SKILL.md:27-46]
2. **Open the feature folder, or route the edge case first.**
   - First sentence: `Parse flags: --auto sets Gate mode: auto-approve in progress.md; tell the user the design gate will be auto-approved and recorded, not asked.` [VERIFIED: skills/dev/SKILL.md:47-49]
   - Then: **classify the idea before creating anything** as `new / resume / in-flight-overlap / done-collision / roadmap-row`. Anything but a plain new feature loads `references/feature-folder-cases.md`. Common path: kebab + next ordinal, create `.wit/features/<slug>/`, seed `progress.md`. [VERIFIED: skills/dev/SKILL.md:49-61]
3. Brainstorm (never skipped; `--auto` does not collapse it). [VERIFIED: skills/dev/SKILL.md:62-67]
4. Handoff preflight; branch on Gate mode. [VERIFIED: skills/dev/SKILL.md:68-99]
5. Design (`wit:research`). [VERIFIED: skills/dev/SKILL.md:100-101]
6. Build + ship. [VERIFIED: skills/dev/SKILL.md:102-105]

There is **no Python flag parser** for `--auto`. The orchestrating model follows the prose. The same pattern is what `--kind` should join, plus a testable helper for the mechanical parts (see Recommendation).

`--auto` is **Gate mode only**. It is orthogonal to work type. [VERIFIED: skills/dev/SKILL.md:47-48, skills/research/references/wit-directory.md:156]

Feature-folder classification always creates or resumes a dossier. An investigation must never reach it. [VERIFIED: brief.md:21-22, .wit/features/0003-work-type-routing/progress.md:53, .wit/glossary.md:22]

## Recommended seam

**Insert work-type resolve as the first half of existing `dev:2`, after flag parse and before the five-class folder classifier. Do not add a fifth advertised command. Do not renumber the later steps.**

Exact order inside step 2:

1. **Parse flags from the invocation; strip them from the idea text.** Tokens: `--auto` (bare); `--kind <value>`. Values: `feature` | `bug-fix` | `investigation` only. Unknown `--kind` **stops** with the three valid values; it does not infer. `--auto` and `--kind` are independent. [VERIFIED: brief.md:31-32; `--auto` already parsed here: skills/dev/SKILL.md:47-49]
2. **Resolve work type.** Precedence below. Record source: `kind` | `inferred` | `ambiguous-default`.
3. **Announce one line** (never silent, never a question): `Work type: <type> (<source>). Override: --kind feature|bug-fix|investigation`. [VERIFIED: brief.md:17-18, 32]
4. **Branch:**
   - `investigation` → load the investigation reference (sibling `investigation-route`); **do not** folder-classify, seed a dossier, brainstorm, gate, build, or PR. [VERIFIED: brief.md:21-22]
   - `feature` or `bug-fix` → **existing folder classifier unchanged** (new / resume / overlap / done-collision / roadmap-row). Feature then continues steps 3-6 as today. Bug-fix loads its on-demand reference after the folder exists (sibling `bug-fix-route`). [VERIFIED: brief.md:38; folder classes: skills/dev/SKILL.md:50-52]

Why this is the thinnest seam that leaves the feature path unchanged:

- `--auto` already lives in this sentence. `--kind` is a sibling flag, not a new lifecycle. [VERIFIED: skills/dev/SKILL.md:47-49]
- The rare-branch pattern already exists: list the classes in the skill, load a reference only when the common path does not apply. Feature is the common path and never loads work-type procedure. [VERIFIED: references/feature-folder-cases.md:11-16, docs/design-notes/dev.md:94-99]
- Investigation is the only type that skips folder classify. Bug-fix still needs resume / overlap / roadmap / ordinal. Putting work type *instead of* folder classify for bug-fix would break resume. [VERIFIED: references/feature-folder-cases.md:19-27; bug-fix reuses dossier: .wit/roadmap.md:44]
- `dev` stays a sequencer. Tells and route procedure stay out of the always-loaded body (token cost: the skill is re-read ~75x). [VERIFIED: docs/design-notes/dev.md:11-12, 94-99]

### Step 1 stays shared

Host probe and the scan precondition stay in step 1 for every `/wit:dev` invocation, including investigation. Scan writes project `.wit/` (repo-map, constitution), not product files. Whether investigation later skips a stale-map `--refresh` write is **sibling `investigation-route`**. Moving classify before step 1 would change the feature path's first numbered step. [VERIFIED: skills/dev/SKILL.md:27-46; product-file ban: brief.md:33-34]

### Stamp so resume does not re-infer

Seed `**Work type:** feature | bug-fix` on the `progress.md` header next to `Gate mode` / `Flow` (investigation never seeds a folder). Resume reads the stamp and does not re-classify unless this invocation carries `--kind`. A missing line on a pre-change dossier means `feature`. [VERIFIED: template fields: skills/research/references/wit-directory.md:156-157; resume tell: references/feature-folder-cases.md:21-27]

`--kind` on a resume wins over the stamp (same override rule as first classify). [VERIFIED: brief.md:31]

### Host aliases and descriptions

`references/skill-aliases/wit-dev/SKILL.md` must pass `--kind` through the same sentence that already passes `--auto`. [VERIFIED: references/skill-aliases/wit-dev/SKILL.md:19-20]

Expand `skills/dev/SKILL.md` `description` (and the alias description) with conservative trigger phrases so "fix this bug" / "how does X work" auto-trigger **dev**, not a fifth command. Stay under the 1024-char cap (`DESC_CAP` in `scripts/validate.py`). Current `dev` description is ~474 characters. [VERIFIED: scripts/validate.py:316-321; measured this session]

Keep add-issues verbs distinct: "file a bug" / "open an issue" stay add-issues; "fix" / "it's broken" / a repro to **repair** enter dev as bug-fix. [VERIFIED: skills/add-issues/SKILL.md:5-8 vs skills/dev/SKILL.md:4-8]

Do not add a dedicated `/wit:how`. If pstack `how` is installed, investigation **delegates** (sibling). Classification still enters through `/wit:dev`. [VERIFIED: brief.md:45-46; integrations.md:37-41]

## Intent tells and precedence

Goal: minimize false `bug-fix` and `investigation` classifications. A missed bug that runs as a feature is recoverable (`--kind` is announced). A false investigation that never opens a folder is not. [VERIFIED: brief.md:17-18, 32; open question: brief.md:55]

**Precedence (strict, first match wins):**

1. Valid `--kind` → that type. Source `kind`. Tells are ignored.
2. Invalid `--kind` → stop. Do not infer.
3. Exclusive investigation tells fire, and no bug-fix symptom tell, and no feature-construction verb → `investigation`. Source `inferred`.
4. Exclusive bug-fix symptom tells fire, and no feature-construction verb → `bug-fix`. Source `inferred`.
5. Everything else, including mixed tells → `feature`. Source `ambiguous-default` when no positive feature verb, else `inferred`.

**Feature-construction verbs** (block steps 3-4): add, build, implement, support, allow, "I want a feature", "capability", "new behavior". These match today's auto-trigger language. [VERIFIED: skills/dev/SKILL.md:4-8]

**Bug-fix exclusive tells** (symptom + repair, borrowed from add-issues classify, narrowed so they do not steal "file a bug"): broken, bug, fails / failure, regression, crash, exception, stack trace, "doesn't work" / "does not work", repro, "fix this". [VERIFIED: skills/add-issues/SKILL.md:47-50]

**Investigation exclusive tells** (read-only question, no change request): "how does X work", "why does/is", "walk me through", "explain how", "where does X live" / "which package owns". [CITED: pstack how description, local cache `skills/how/SKILL.md`; pstack investigation one-liner, local cache `skills/poteto-mode/SKILL.md:118`]

**Do not copy** pstack's "should we do X or Y" or "are we sure about Z" as investigation tells. In Witloop those are brainstorm / design-gate questions on the feature path. Copying them would steal features. [VERIFIED: brief.md:59; skills/dev/SKILL.md:12-16; pstack list: poteto-mode/SKILL.md:118]

**Mixed tells → feature.** Examples: "why is login broken and add a retry"; "how does billing work, then implement the new tier". Announce `ambiguous-default` and the override.

`--auto` is never a work-type tell. `--auto` plus investigation: still announce investigation; Gate mode is unused because there is no design gate (sibling records that). [ASSUMED: load-bearing for investigation + `--auto`; sibling `investigation-route`]

pstack's 22-playbook sticky router is **not** the model. The brief forbids copying it. Witloop keeps three types and a default-to-feature. [VERIFIED: brief.md:59, .wit/roadmap.md:45]

## Announcement behavior

Always announce after resolve, including a plain inferred `feature`. One line, then continue. Do not ask "is this a bug or a feature?". Do not route silently. [VERIFIED: brief.md:17-18, 32]

This is the only intentional addition on the happy feature path: a single status line before the existing folder classifier. Brainstorm, gates, build, and ship stay as written. [VERIFIED: brief.md:38]

`--auto` keep its existing announcement ("design gate will be auto-approved"). Work-type announcement is separate and earlier. [VERIFIED: skills/dev/SKILL.md:47-49]

## Validation and tests

Constitution: new behavior ships with tests in `tests/test_*.py`; TDD default; `python scripts/validate.py` plus the unit suite. [VERIFIED: .wit/constitution.md:32-34, .wit/repo-map.md:18-23]

Today **no test parses `--auto`**. Gate-mode is prose. The closest prior art is `skills/add-issues/scripts/check_draft.py` + `tests/test_check_draft.py`: a stdlib helper with pinned fixtures. [VERIFIED: tests/ tree this session; tests/test_check_draft.py:1-11]

**Pin in a new helper** `skills/dev/scripts/classify_work_type.py` (stdlib, no new dep):

- argv-like string → `{auto: bool, kind: str|None, idea: str, work_type, source}`
- `--kind` validation
- exclusive tell table
- mixed / empty idea → `feature` + `ambiguous-default`

The skill invokes it (`python <plugin-root>/skills/dev/scripts/classify_work_type.py -- ...`, workflow.md "Script invocation") and **does not override** a script `work_type` of `kind` or `inferred`. The orchestrator does not get a third, untested vote. [VERIFIED: references/workflow.md "Script invocation"; constitution simplicity: .wit/constitution.md:25-28]

**Also pin in `scripts/validate.py`** (same style as the headless-only clause): `skills/dev/SKILL.md` still contains `--kind`, the announce/override sentence, and "before" + folder-class list so a compression pass cannot drop the seam. [VERIFIED: scripts/validate.py:180-187]

**Fixture cases the unit file must name:**

| Invocation | Expected type | Source |
|---|---|---|
| `add search command` | feature | inferred |
| `add search --auto` | feature | inferred; `auto` true |
| `--kind investigation how does auth work` | investigation | kind |
| `how does auth work` | investigation | inferred |
| `login is broken` / `fix this crash` | bug-fix | inferred |
| `why is login broken and add a retry` | feature | ambiguous-default |
| `--kind feature login is broken` | feature | kind |
| `--kind nope …` | error, no infer | n/a |
| empty idea / resume-shaped slug only | feature | ambiguous-default |

`--auto` + `--kind` together: both applied; idea text has neither token.

No new dependency. [VERIFIED: .wit/constitution.md:37-39]

## Compared shapes

| | A. All tells inline in `dev/SKILL.md` | B. Recommended: step-2 parse + script + on-demand refs | C. Classify in a new step 1.5 / before scan |
|---|---|---|---|
| Feature path | Pays for unused tell prose every turn (~75x) | Fall-through after one announce + script call | Renumbers the hotspot; scan/host probe move |
| Investigation skip | Possible but easy to miss amid folder text | Hard skip: never reach folder classify | Can skip scan writes; sibling-owned |
| Testability | validate.py string anchors only | Unit fixtures on the helper | Same helper, more skill churn |
| Reversibility | Hotspot edit | Small skill delta + new reference/script | Larger procedure rewrite |
| Fit | Fights "keep dev thin" | Matches `--auto` + `feature-folder-cases.md` | Over-fits investigation purity |

**Rejected A:** always-loaded hotspot; constitution + design-notes forbid concentrating logic here. [VERIFIED: docs/design-notes/dev.md:94-99, .wit/constitution.md:42]

**Rejected C:** changing step 1 sequencing is a feature-path change. Investigation scan-write policy belongs to sibling `investigation-route`. [VERIFIED: skills/dev/SKILL.md:27-46]

**Rejected (out of scope):** a fifth command or `/wit:how`. [VERIFIED: brief.md:45-46]

## Decision

Use **shape B**. Work type is resolved at the start of `dev:2` by a stdlib helper (`--kind` > exclusive tells > announced `feature`), announced in one line, then:

- investigation exits via an on-demand reference and never folder-classifies;
- feature and bug-fix enter the existing five-class folder classifier unchanged;
- feature continues today's brainstorm → research → gate → build → ship.

Host aliases pass `--kind` next to `--auto`. `description` fields gain conservative NL tells under the 1024-char cap. `progress.md` stamps `Work type` so resume does not re-infer.

This is a **public skill contract** (`--kind`, description auto-trigger, new `progress.md` field). Constitution requires an ADR. [VERIFIED: .wit/constitution.md:40]

## Don't-Hand-Roll

| Problem | Do not build | Use instead | Why |
|---|---|---|---|
| 22-way sticky playbook router | pstack poteto-mode playbook list | Three work types + default `feature` | Brief + roadmap: borrow methods, do not copy the router [VERIFIED: brief.md:59, .wit/roadmap.md:45] |
| Fifth slash command | `/wit:investigate`, `/wit:how` | `/wit:dev` + `--kind` + NL tells | Four advertised commands stay [VERIFIED: brief.md:45-46, AGENTS.md:40-41] |
| LLM-only classify | Unpinned "does this feel like a bug?" | Stdlib helper + exclusive tells | Tests required; false investigation is expensive [VERIFIED: .wit/constitution.md:32-34] |
| Duplicate folder-case logic | New resume/overlap rules per work type | Existing `feature-folder-cases.md` after feature/bug-fix resolve | Already factored; bug-fix still needs a folder [VERIFIED: references/feature-folder-cases.md:11-17] |

## State of the Art (in this repo)

| Old way | Current way | When it changed |
|---|---|---|
| Six inline folder branches in `dev:2` | Five classes in the skill; rare cases in `feature-folder-cases.md` | #39 / #48 [VERIFIED: docs/plans/2026-07-11-prc-39-40-relocate-dedup.md, docs/plans/2026-07-11-prd2-48-drop-legacy.md] |
| `--auto` parsed in prose only | Keep prose for Gate mode; add a helper for `--kind` + tells | This feature; `--auto` parse site stays [VERIFIED: skills/dev/SKILL.md:47-49] |
| add-issues type infer asks when ambiguous | Work-type never asks; ambiguous → announced `feature` | Deliberate; work-type is not issue-type [VERIFIED: skills/add-issues/SKILL.md:47-50 vs brief.md:32] |

## Dependency Legitimacy

None added. Helper is stdlib, same class as `check_draft.py`. [VERIFIED: .wit/constitution.md:16-17, 37-39]

## Assumptions Log

| Claim | Why assumed | Load-bearing? |
|---|---|---|
| Bug-fix always folder-classifies (resume/overlap/roadmap apply) | Roadmap says bug-fix reuses the dossier; sibling owns the flow | **Yes** |
| `--auto` on investigation is ignored for Gate mode (no gate exists) | Brief: investigation has no design gate | **Yes** (sibling `investigation-route`) |
| Step 1 scan writes are allowed before an investigation exit | Product-file ban does not name `.wit/` scan artifacts | **Yes** (sibling may tighten) |
| Expanding `dev` description will not steal "file a bug" from add-issues if verbs stay distinct | Host auto-trigger matching is not specified beyond description text | **Yes** |
| Resume uses stamped `Work type` and does not re-infer without `--kind` | Needed so an in-flight feature is not reclassified as investigation | **Yes** |
| pstack `how` / `why` remaining in the session will not self-trigger mid-`/wit:dev` if description expands | integrations.md "Who initiates" covers superpowers during an active run, not pstack `how` at session start | **Yes** (sibling + integrations row) |

## Risks / unknowns

- Host auto-trigger collision: "how does X work" may fire pstack `how` instead of `/wit:dev` on Cursor. Plan must keep investigation reachable from `/wit:dev` even when `how` is present; do not depend on winning the description race. [CITED: pstack `skills/how/SKILL.md` description]
- Invalid `--kind` stop vs infer: recommend stop. If plan chooses infer, tests and the announce line must change together.
- Helper invocation on PowerShell: use `python` + plugin-root path, never `python3` in the invocation (validate.py bans it). [VERIFIED: scripts/validate.py:41-42]
- `progress.md` `Work type` line: ship / token timing parse keys on Log stamps that **open** a line, not header fields. Adding a header bullet is safe if it is not a Log line. [VERIFIED: skills/research/references/wit-directory.md:172-173]
- Description cap: keep the expanded `dev` + alias descriptions under 1024 characters. [VERIFIED: scripts/validate.py:316-321]
- Rule-text PR needs a before/after rules inventory; `dev/SKILL.md` is a hotspot (serial, one in-flight branch). [VERIFIED: .wit/constitution.md:42, 51]
- Manifest versions bump together on this behavior change (minor). [VERIFIED: .wit/constitution.md:48]

## Citations

1. `skills/dev/SKILL.md` (procedure steps 1-2, `--auto`, description)
2. `references/feature-folder-cases.md` (folder classes; load-only-when-needed)
3. `references/skill-aliases/wit-dev/SKILL.md` (flag pass-through)
4. `skills/add-issues/SKILL.md:47-50` (existing classify tells)
5. `scripts/validate.py` (description cap, contract anchors)
6. `.wit/constitution.md` (tests, simplicity, ADR-on-public-contract)
7. Local pstack cache: `skills/poteto-mode/SKILL.md:118-119`, `skills/how/SKILL.md` (tells to borrow / not copy)
