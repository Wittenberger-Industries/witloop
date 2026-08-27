---
type: Research Note
title: "ledger: on | skip in .wit/models.md"
description: Shape, default, and honor points so skip means no tokens.md init, finalize, report table, or ship:8 check_tokens gate.
feature: 0004-setup
timestamp: 2026-08-27
valid_until: 2026-09-26
---

# ledger: on | skip in project `.wit/models.md`

Mode: `[repo-question]`. No new PLUGIN_ROOT always-loaded file. Host probe stays in `progress.md`.

## Responsibility Map

Plugin skill/reference layer only (this repo is Witloop). Setup writes the key into the **target project's** `.wit/models.md`. Dev and RPA honor it. No frontend/backend split.

## Decision

**Heading `## Token ledger`. Key `ledger`. Values `on` | `skip`. Canonical store is a Key/Value table under that heading, same idiom as `## Mixture of Agents`.** [VERIFIED: `.wit/models.md` MoA table; `references/models.md` template]

Spoken form in skills and `--auto` prose is `ledger: on` / `ledger: skip` (same dialect as MoA `points: none`). Do not also put `ledger:` in YAML frontmatter: that is a second store. `preset:` stays the only setup scalar in frontmatter. [VERIFIED: `references/models.md` frontmatter; `cross_review.parse_models_config` reads only `preset` from YAML]

**Absent heading, absent row, empty cell, or any value other than the exact token `skip` → `on`.** Old repos with today's `.wit/models.md` keep today's ledger. Typos fail closed to `on` (keeping the gate is safer than silently dropping it). [ASSUMED: fail-closed-to-on is the intended safety; load-bearing]

**`--auto` on setup writes the simple preset and this section with `ledger | on`.** Never skip on `--auto`. [VERIFIED: brief; `references/models.md` First-run `--auto` already writes simple]

**Do not teach `check_tokens.py` / `_ledger.py` about skip.** Skip means the skill does not invoke `--init`, `--write`, or verify. The script stays the on-path format gate. [VERIFIED: `check_tokens.py` docstring; `_ledger.verify` returns `"tokens.md missing"`]

**Stamp `ledger: on|skip` onto the existing `## Model routing (resolved)` first bullet in `progress.md` at resolve-once.** Honor points read that stamp (already in the context budget). They do not re-open `.wit/models.md`. Missing `ledger:` on an old progress block → `on`. No `.wit/models.md` at all (`preset: none - all inherit`) → `on`. [VERIFIED: wit-directory progress template; models.md "Dispatch reads the block"]

## Shape (bytes)

Add to the `references/models.md` template and to every file setup/`--auto` writes, after Roles (or after MoA; order is not load-bearing as long as the heading is exact):

```markdown
## Token ledger
| Key | Value |
|------|-------|
| ledger | on |
```

Interactive setup asks keep-or-skip and writes `on` or `skip` in that Value cell. `--auto` always writes `on`.

Resolved progress.md first bullet becomes:

```
- resolved <ISO-8601 stamp> from .wit/models.md (preset: <smart | simple | custom | none - all inherit> · ledger: <on | skip>)
```

[VERIFIED: current bullet is `preset:` only, wit-directory.md:175 and rpa-directory.md:193]

Do not put ledger on `## Capabilities (resolved)` `tokens=`. That cell is host measureability (Claude measures, Cursor/Copilot/Codex write `unavailable`). Project skip is orthogonal: Cursor + `ledger: on` is today's honest-unavailable ledger; Cursor + `ledger: skip` is no file. [VERIFIED: brief "Keep means today's ledger, including honest unavailable"; capabilities vs ledger]

## Why this heading and key (not YAML, not a new file)

| Option | Rejected because |
|--------|------------------|
| YAML `ledger:` next to `preset:` | Matches the brief's colon syntax, but there is then no body heading, or a heading that duplicates the YAML (two stores). `preset` is routing; ledger is project policy. |
| Row on `## Mixture of Agents` or Cross-provider | Wrong concern. MoA `points: none` must not be confused with ledger skip. |
| `.wit/setup.md` / PLUGIN_ROOT `ledger.md` | Brief + 0003-work-type-routing: no new always-loaded PLUGIN_ROOT target; project state stays in `.wit/models.md`. [VERIFIED: brief Constraints; `.wit/learnings/0003-work-type-routing.md`] |
| Capabilities `tokens=` | Host probe, not project choice. Brief: host probe stays per session in `progress.md`. |
| `## Token ledger` Key/Value (`ledger` / `on\|skip`) | **Wins.** Heading the dispatch asked for. Same table idiom as MoA (prose-read, ignored by `cross_review.py`). [VERIFIED: `test_models_config.ParseConfigTest.test_moa_section_is_ignored`] |

`cross_review.py` must not parse this section. Clone the MoA ignore test with a Token ledger fixture so a future parser change cannot couple review to skip. [VERIFIED: `parse_models_config` returns preset/roles/cross_provider/overrides/platform_map only]

## Honor points (skip means all four)

Skip is complete only when every path below is gated on the progress.md stamp `ledger: skip` (else `on`).

### 1. No `tokens.md` init

| Site | Today's action [VERIFIED] | Skip |
|------|---------------------------|------|
| `skills/research/SKILL.md` research:0 | `check_tokens.py --init .wit/features/<slug>/tokens.md` | do not run `--init` |
| `skills/build/SKILL.md` as-each-report-returns | `--init` if file absent, then append | neither |
| `skills/rpa/SKILL.md` rpa:5 pre-gate | `--init` then checker row | neither |
| `skills/rpa/SKILL.md` rpa:6 REFramework | `--init` if absent, then per-unit append | neither |
| `skills/rpa/references/build-uipath.md` §4 | `--init` if absent; **"tokens.md is mandatory"** | do not init; carve out "mandatory" |
| `skills/rpa/references/build-maestro.md` §4 | same mandatory + `--init` | same carve-out |

Agents (`wit-researcher`, `wit-task-runner`, `wit-code-checker`) do not mention `tokens.md`. Orchestrator skills own append. [VERIFIED: grep `agents/` no `tokens.md`]

### 2. No finalize

| Site | Today's action [VERIFIED] | Skip |
|------|---------------------------|------|
| `skills/ship/SKILL.md` ship:6 item 3 | `finalize_tokens.py --write .wit/features/<slug>/tokens.md` | do not run |
| `references/{grok,copilot,cursor}-tools.md` | host one-liners for that same CLI | unused if ship skips; no skip prose required |
| `references/moa.md` Token ledger | every proposer/aggregator appends a row | research/ship skip covers it if those skills own append; one clause in moa.md is recommended so a loaded-alone MoA read does not append |

### 3. No token table in the final report

| Site | Today's action [VERIFIED] | Skip |
|------|---------------------------|------|
| `skills/ship/SKILL.md` after close-out | print the token table from finalized `tokens.md`; timing table includes tokens.md wall-clock and Σ-compute | omit the **token table**. Omit the two tokens.md-sourced timing lines (`autonomous total`, `Σ subagent compute`). The two `progress.md` span lines may stay (they do not need `tokens.md`). |
| `skills/dev/SKILL.md` step 6 | "final report including the token table" | qualify: including the token table only when `ledger: on` |
| `skills/rpa/SKILL.md` rpa:7 | "token report (`tokens.md`, finalized ..., mandatory)" | not mandatory; do not print |

### 4. `check_tokens.py` is not a ship:8 gate

| Site | Today's action [VERIFIED] | Skip |
|------|---------------------------|------|
| `skills/ship/SKILL.md` ship:8 checkbox | run `check_tokens.py <tokens.md>`; non-zero blocks `Phase = done` | omit the checkbox (or mark n/a). Do not call the script. Keep-alive must not wait on this exit. |
| `skills/rpa/SKILL.md` rpa:7 | "Both → `tokens.md` passes `check_tokens.py`" | not a gate |
| `skills/rpa/references/verification-gate.md` What green means | "token ledger `tokens.md` passes `check_tokens.py`" | carve-out: when `ledger: skip`, this bullet does not apply |

`tests/test_tokens_guardrail.py` keeps `verify(missing) == "tokens.md missing"`. That pins the **on-path** script, not skip. Skip is "do not call verify". Do not add a `--skip` flag to the CLI. [VERIFIED: `test_tokens_guardrail.py:124`]

## Dossier exact-count (silent fifth honor point)

Skip without this carve-out still fails ship:8: "dossier = exactly the flow's manifest" and wit-directory "seven-file dossier: ... tokens, PR". [VERIFIED: wit-directory.md:81; ship/SKILL.md:314-317, 421-424; rpa-directory.md:60-62]

- **dev + `ledger: on`:** seven files (today).
- **dev + `ledger: skip`:** six files (drop `tokens.md`). Tree comment in wit-directory: tokens.md is present when `ledger: on`.
- **rpa + skip:** run dossier omits `tokens.md`.

Do not delete a leftover `tokens.md` on skip except as a tidy stray if the skip manifest does not list it. Mid-run hand-edit of `ledger` from `on` to `skip` is a pitfall (scaffold may exist, still PENDING). Do not toggle mid-feature. [ASSUMED: no auto-delete; load-bearing for tidy]

## Constitution carve-out

**No.** Scan's `constitution-template.md` and this repo's `.wit/constitution.md` do not say `tokens.md` is mandatory. [VERIFIED: both files, grep]

Do not add a constitution rule. The phrase **"tokens.md is mandatory"** lives in RPA build refs (`build-uipath.md:78`, `build-maestro.md:33`), not in constitution. Those two sentences plus wit-directory / rpa-directory dossier lists are the carve-outs.

## `--auto`

Setup `--auto` = simple Roles/Cross-provider/MoA (today's simple preset) **plus** `## Token ledger` with `ledger | on`. [VERIFIED: brief; models.md First-run `--auto` → simple]

Interactive setup asks the keep-or-skip question once, never re-asks (edit `.wit/models.md`). Same persistence rule as preset. [VERIFIED: models.md "never re-asked"]

## Minimum file list that must mention skip

These files, loaded alone, would still init, finalize, gate, print the table, or fail dossier-exact if they keep today's unconditional wording:

1. `references/models.md` (template, default-absent=`on`, `--auto` writes `on`, resolve-once stamp)
2. `skills/research/SKILL.md` (research:0 `--init`; append / checker rows)
3. `skills/build/SKILL.md` (`--init` if absent + append)
4. `skills/ship/SKILL.md` (finalize; ship:8 checkbox; token table; dossier manifest)
5. `skills/rpa/SKILL.md` (rpa:5/6 init+append; rpa:7 check_tokens + mandatory token report)
6. `skills/research/references/wit-directory.md` (tree; seven-file dossier; progress.md resolved bullet; tokens.md template intro: scaffold is research:0 **when ledger is on**)
7. `skills/rpa/references/rpa-directory.md` (tree; run dossier; progress.md resolved bullet)
8. `skills/rpa/references/verification-gate.md` (green includes check_tokens)
9. `skills/rpa/references/build-uipath.md` ("mandatory" + `--init`)
10. `skills/rpa/references/build-maestro.md` (same)
11. `skills/dev/SKILL.md` (step 6 "including the token table")

Recommended, not required for the four skip meanings:

- `references/moa.md` Token ledger section (loaded-alone append)
- `tests/test_models_config.py` (Token ledger section ignored, clone of MoA test)

Do **not** mention skip in (keep on-path only):

- `skills/ship/scripts/check_tokens.py`, `_ledger.py`, `finalize_tokens.py`
- `references/workflow.md` ledger-rule paragraph
- `references/{grok,copilot,cursor}-tools.md` finalize one-liners
- `skills/scan/references/constitution-template.md` / `.wit/constitution.md`
- host `tokens=` capability cell

Setup's `SKILL.md` (new) will write the section; that file is in-scope for the sibling setup-move charter, not duplicated here beyond: whatever writes `.wit/models.md` must emit `## Token ledger` / `ledger` / `on|skip`.

## Cheapest string pins (no live ship run)

1. `references/models.md` contains the exact heading `## Token ledger` and a table row whose first cell is `ledger` and whose value cells document `on` and `skip`.
2. First-run `--auto` sentence contains `ledger` and `on` (not `skip`).
3. Each of research, build, ship, rpa `SKILL.md` contains `ledger: skip` (or `ledger=skip`) adjacent to their `--init` / finalize / `check_tokens.py` / token-table wording.
4. wit-directory seven-file sentence names the skip six-file carve-out.
5. `test_models_config.py`: `FULL_CONFIG + TOKEN_LEDGER_SECTION` parses equal to `FULL_CONFIG` (section ignored).
6. Guardrail tests unchanged: missing `tokens.md` still fails `verify` (on-path).

## Don't-Hand-Roll

| Problem | Do not build | Use instead | Why |
|---------|--------------|-------------|-----|
| Project ledger toggle | New `.wit/setup.md` or PLUGIN_ROOT file | `## Token ledger` in `.wit/models.md` | Brief + 0003 |
| Skip as a `check_tokens.py` flag | `--skip` / read models.md from the script | Skill does not invoke | Script owns format; skills own policy |
| Skip via Capabilities `tokens=` | Overload host probe | Separate `ledger` key | Orthogonal (unavailable vs omitted) |
| Re-read `.wit/models.md` at every append | Extra Read per wave | Resolve-once stamp on progress.md | Existing resolve-once rule |

## State of the art (this repo)

| Old way | Current way (today, 1.16.x) | Skip way |
|---------|------------------------------|----------|
| Soft checkbox, ledger easy to omit | Deterministic `--init` + finalize + `check_tokens.py` blocks done [VERIFIED: docs/specs/2026-06-15-tokens-md-guardrails-design.md] | Project opt-out in `.wit/models.md`; scripts unchanged |
| No models.md → inherit routing, ledger still on | Same | Still on (absent key) |
| Host cannot measure → `unavailable` still gates | Same | `skip` omits the file; `on` keeps unavailable |

checked `cross_review.py` parse (no version pin; stdlib script in repo), docs read 2026-08-27.

## Assumptions Log

| Claim | Why assumed | Load-bearing? |
|-------|-------------|---------------|
| Values other than exact `skip` honor as `on` | Safety; brief only names `on` and `skip` | yes |
| Dual store (YAML + table) is forbidden | One key, one heading | yes |
| Mid-run toggle is unsupported; leftover tokens.md is a stray vs six-file manifest | No brief guidance | yes |
| Timing span lines from progress.md may remain when the token table is omitted | Brief names the token table, not the whole Timing block | no |
| ADR-0004 (new public command) can record this key; no extra ADR | Key is backward compatible via default `on` | no |

## Risks / unknowns

- Ship:8 dossier-exact will fail skip unless wit-directory / rpa-directory manifests drop `tokens.md`. Plan must have a covering task.
- RPA build refs say "tokens.md is mandatory" and will `--init` even if rpa/SKILL.md skips, unless both are edited.
- In-flight features with an old progress.md stamp (no `ledger:`) must stay `on`. Re-resolve when models.md changes after the stamp already exists; a hand-edit to `skip` mid-run needs a re-resolve (or a pitfalls line: do not toggle mid-feature).
- `test_capabilities.py` slices wit-directory on `## \`tokens.md\` template`; keep that heading even when skip exists.
- Keep-alive loops that wait on `check_tokens.py` exit: skip must not leave that wait unsatisfiable. Ship:8 wording is the keep-alive condition. [VERIFIED: ship/SKILL.md:415-418]

## Dependency Legitimacy

none added.

## Citations

- `.wit/models.md` current shape (frontmatter `preset`; body tables Roles / Cross-provider / MoA / Platform map)
- `references/models.md` template + First-run `--auto` + resolve-once
- `skills/research/references/wit-directory.md` tokens.md template, seven-file dossier, progress.md resolved block
- `skills/ship/SKILL.md` ship:6 finalize, ship:8 check_tokens, final token table
- `skills/build/SKILL.md` append + `--init`
- `skills/research/SKILL.md` research:0 `--init` + ledger rule
- `skills/rpa/SKILL.md` rpa:5/6/7
- `skills/rpa/references/verification-gate.md`, `build-uipath.md`, `build-maestro.md`, `rpa-directory.md`
- `skills/ship/scripts/check_tokens.py`, `_ledger.py`
- `tests/test_tokens_guardrail.py`, `tests/test_capabilities.py`, `tests/test_models_config.py`
- `.wit/learnings/0003-work-type-routing.md`
- `.wit/features/0004-setup/brief.md`
