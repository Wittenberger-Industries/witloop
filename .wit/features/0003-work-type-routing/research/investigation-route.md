---
type: Research Note
title: "Investigation route: read-only cited exit"
description: How /wit:dev should run a read-only investigation with optional how/why delegation, citations, and no .wit/ state or PR.
feature: 0003-work-type-routing
timestamp: 2026-08-25
valid_until: 2026-09-24
tags: [investigation, routing, integrations, how, read-only]
---

# Investigation route

Repo-question: how a read-only investigation should invoke installed understanding skills or a portable fallback, produce citations, and exit without `.wit/` state or a PR.

Mode: `[repo-question]`. Outward survey limited to pstack sources already named by the brief/roadmap. Checked against this tree on 2026-08-25.

## Responsibility Map

This repo is a plugin, not a split frontend/backend app. [VERIFIED: `.wit/repo-map.md`]

| Capability | Layer | Owner |
|---|---|---|
| Work-type early exit after classification | `/wit:dev` orchestrator | thin hook in `skills/dev/SKILL.md` |
| Investigation procedure (detect, delegate, fallback, cite, exit) | on-demand reference | `skills/dev/references/investigation.md` (new) |
| Skill detection union | existing helper | `skills/research/scripts/discover_skills.py` |
| Capability -> skill registry | integrations | `skills/research/references/integrations.md` (new `understand` row, not a phase row) |
| Cited answer | chat reply (the product) | orchestrator or delegated `how` |
| Feature dossier / gate / PR | none | forbidden on this route |

Classifier implementation is sibling `classification-seam`. Bug-fix flow is sibling `bug-fix-route`. This note assumes those siblings place `work type = investigation` on the orchestrator **before** feature-folder classification. [ASSUMED: sibling charter; load-bearing]

## What the solution must do

From the brief, progress decisions, and constitution:

- Investigation is a **read-only exit**: cited explanation or recommendation; no feature dossier, brainstorm, design gate, build, or PR. [VERIFIED: `brief.md`; `.wit/features/0003-work-type-routing/progress.md` Decision 2026-08-25T18:08:26]
- Entry stays `/wit:dev` (plus `--kind investigation`). No fifth advertised command, no dedicated `/wit:how`. [VERIFIED: `brief.md` Scope; `README.md` "Only these four entry points"; `.wit/roadmap.md` standing fit rules]
- Optional installed skills may be delegated; none are required; no required MCP. [VERIFIED: `brief.md` Constraints]
- Keep `wit-code-checker` as the single review-agent contract; add no named agent. [VERIFIED: `brief.md`; constitution Architecture]
- Classifier and route entry stay thin; route-specific procedure lives in on-demand references. [VERIFIED: `brief.md` Approach preferences]
- Citations use `name:N` locators, never the section sign. [VERIFIED: constitution Language]
- Work on all five hosts via the capability table. [VERIFIED: `references/capabilities.md`]
- New behavior ships with tests. [VERIFIED: constitution Testing]

## Prior art (inward)

### `/wit:dev` always opens a feature folder

`skills/dev/SKILL.md` step 2 classifies **new / resume / in-flight-overlap / done-collision / roadmap-row**, then creates `.wit/features/<slug>/` and seeds `progress.md`. Rare branches load `references/feature-folder-cases.md`. There is no work-type branch today. [VERIFIED: `skills/dev/SKILL.md` Procedure step 2; `references/feature-folder-cases.md`]

dev:1 also writes host/capability stamps into `progress.md`, may run scan, and may create `.wit/models.md`. Those writes are **incompatible** with a no-`.wit/`-state investigation unless the investigation branch skips them. [VERIFIED: `skills/dev/SKILL.md` steps 1-2; `skills/research/references/wit-directory.md` progress template]

The existing on-demand-reference pattern for a rare `dev` branch is `feature-folder-cases.md`: keep the skill thin, load the file only when the tell fires. [VERIFIED: `docs/design-notes/dev.md` "dev:2"]

### Integrations: detect, delegate, capture, log

`skills/research/references/integrations.md` is the canonical capability -> skill registry. Detection is a union implemented by `discover_skills.py` (session paths, Claude registry, Cursor cache, Copilot install dir, `~/.agents/skills/`). Delegation is mandatory when the skill is present. Fallback only after the union misses. Every delegating **phase** logs `<phase> via <skill>` or `<phase> via wit fallback (<skill> absent)` to `progress.md`. [VERIFIED: `integrations.md`; `tests/test_discover_skills.py`]

Two load-bearing clashes with investigation:

1. **"wit still owns the artifacts: capture the external skill's result into the matching `.wit/` file"** would force a dossier. Investigation must be an explicit exception: the chat reply is the artifact. [VERIFIED: `integrations.md` "When you delegate"]
2. **Phase logging to `progress.md`** has nowhere to go if no folder is created. Mode must be announced in the reply instead. [VERIFIED: same file; brief no-dossier]

"Who initiates: wit does" already applies during an active `dev` run: optional skills fire only at matrix points, never by description match. [VERIFIED: `integrations.md` "Who initiates"] The phrase "research investigation" in that paragraph means researcher subagents, not this work type; rename it when editing so the two do not collide.

Frontend work is the closest optional-skill pattern: registry row + pointer protocol (resolve `SKILL.md` path, hand it to a dispatch that has no Skill tool, log `via`). Investigation can reuse detection and the pointer, but **must not** write `## Skill paths (resolved)` because that block lives in `progress.md`. [VERIFIED: `integrations.md` Frontend work; `wit-directory.md` Skill paths]

Research / `wit-researcher` is the wrong engine: it writes `.wit/features/<slug>/research/`, feeds an ADR and the design gate, and its charter is a sensitive surface. [VERIFIED: `skills/research/SKILL.md`; `agents/wit-researcher.md`; constitution "Agent charters"]

Debug delegation (`systematic-debugging`) starts only after a phase fails. [VERIFIED: `.wit/roadmap.md` candidate 1 gap; `integrations.md` debug row]

### Four advertised commands

User-invocable skills today: `scan`, `dev`, `rpa`, `add-issues` (no `user-invocable: false`). Hidden phase skills: `brainstorm`, `research`, `plan`, `build`, `ship`. Flat aliases exist only for the four. [VERIFIED: each `skills/*/SKILL.md` frontmatter; `references/skill-aliases/`; `README.md`; `AGENTS.md`]

Adding `skills/investigate/SKILL.md` even with `user-invocable: false` expands the skill surface the way phase skills do, and a `description` that matches "how does X work" would compete with `/wit:dev` and with pstack `how`. The brief forbids a dedicated `/wit:how`. [VERIFIED: `brief.md` Scope]

### Tests that already police this area

- `tests/test_discover_skills.py` `IntegrationsDocTest` locks union order and the verify-absence-before-fallback rule.
- `tests/test_capabilities.py` locks the host matrix.
- `scripts/validate.py` requires integrations.md to contain "verify absence"; SKILL descriptions stay under 1024 chars; no section sign.
- No test currently asserts the four user-invocable names. [VERIFIED: `tests/` glob; `scripts/validate.py`]

## Prior art (pstack, named by the brief)

pstack 0.14.3 investigation playbook (`skills/poteto-mode/playbooks/investigation.md`):

1. Route through **how** (Explain for narrow questions, Critique for "are we sure?"). Motivation questions also route through **why**.
2. Throughput checkpoint: `n/a, read-only investigation`.
3. Output is how-shaped (Overview / Key Concepts / How It Works / Where Things Live / Gotchas) or a recommendation with a tradeoffs table.
4. Apply **unslop**. No PR. If the investigation precedes a code change, hand back and re-route. [CITED: that playbook, read 2026-08-25]

pstack `how` (`skills/how/SKILL.md`):

- Simple: one read-only explainer Task. Complex: 2-4 read-only explorer Tasks, then one explainer.
- `readonly: true` on every subagent.
- Critique mode spawns a multi-model critic panel after explain. [CITED: pstack `how/SKILL.md`, read 2026-08-25]
- Explorer findings cite file paths, symbols, and line numbers. [CITED: `how/references/explorer-prompt.md`]

pstack `why` (`skills/why/SKILL.md`): seven evidence categories, MCP discovery, parallel investigators. Source control is the only guaranteed source. [CITED: pstack `why/SKILL.md`] Witloop's own roadmap parks full `why` as **Later** candidate 10 (detect-only; most categories need optional MCPs) and lists "Full seven-category `why` as a core dependency" under Do not copy. [VERIFIED: `.wit/roadmap.md`]

Roadmap candidate 3 (`understand`) wants an integrations row preferring `how`, a small explorer/explainer fallback, called from investigations **and** from research repo-questions, persisting a note only when a feature is active. It **depends on** this feature. Critique panels stay opt-in; no new named agent; do not fan out every question into four agents. [VERIFIED: `.wit/roadmap.md` candidate 3]

Do not copy: sticky `/poteto-mode` and the 22-playbook router. [VERIFIED: `.wit/roadmap.md` Do not copy]

## Options compared

### A. Hidden skill `skills/investigate/` (`user-invocable: false`)

A sixth skill directory, description-triggered, procedure in its `SKILL.md`.

- **Fits** a "phase skill" habit, but investigation is an **exit**, not a loop phase.
- **Breaks** the four-command story as soon as the description matches "how does X work" (picker / auto-trigger competition with `dev` and pstack `how`). The brief already forbids `/wit:how`.
- New skill descriptions count against the 1024-char cap and validate.py SKILL glob; more always-discoverable surface.
- **Rejected.**

### B. On-demand `skills/dev/references/investigation.md` plus an `understand` integrations row (recommended)

`/wit:dev` classifies work type (sibling), then if `investigation`: announce type + `--kind` override, Read the reference, follow it, **stop**. No feature folder.

- Matches the existing `feature-folder-cases.md` pattern and "keep dev thin". [VERIFIED: `docs/design-notes/dev.md`]
- Keeps the four advertised commands. Hidden procedure cannot appear as `/wit:how`.
- Reuses `discover_skills.py` without a new helper.
- Needs a documented exception to the `.wit/` capture and `progress.md` log rules.
- **Winner.**

### C. Reuse `wit-researcher` / the research skill

Point the route at the existing researcher charter or at `skills/research/SKILL.md`.

- Researcher **must** write `research/` notes under a feature slug; research owns ADR + design gate. [VERIFIED: `agents/wit-researcher.md`; `skills/research/SKILL.md`]
- Would require charter edits (report caps, write path). Constitution: agent charters are the most sensitive surface. [VERIFIED: constitution Architecture]
- Conflates "how should we implement this feature" with "how does this subsystem work".
- **Rejected.**

Inline-only with no `how` delegation is not a real third option: it would violate "Delegation is mandatory when the skill is present." [VERIFIED: `integrations.md`]

## Decision

**Use option B.** After work type is `investigation`, `/wit:dev` loads `skills/dev/references/investigation.md` and exits in-session. Prefer installed pstack `how` (and `why` only when present **and** the question is motivational). Otherwise run a portable, read-only explorer/explainer fallback. The user-visible reply is the only artifact.

This is the smallest shape that satisfies the brief, the four-command constraint, integrations.md, and "no new named agent". Candidate 3 can later reuse the same `understand` row for research repo-questions and optionally persist a note **when a feature dossier already exists**; that persist path stays out of this feature.

Close call? Placement is not close (A and C fail hard constraints). Fallback depth (inline vs 2 explorers) is a close call; pick the cheaper default below and allow a cap of 2 explorers when the question is cross-cutting. That is reversible.

Hard-to-reverse? **Yes** as part of the public `/wit:dev` contract (early exit that never opens a dossier). The parent feature should record an ADR covering work-type routing; this route is one section of that ADR, not a second plugin.

## Recommended shape (prescriptive)

### 1. Route ownership

In `skills/dev/SKILL.md`, after work-type classification and **before** feature-folder classification (dev:2 today):

1. Announce `Work type: investigation` and the `--kind` override in one line. Do not ask. [VERIFIED: brief Acceptance]
2. Read `${CLAUDE_PLUGIN_ROOT}/skills/dev/references/investigation.md`.
3. Follow it to completion in this turn.
4. Stop. Do not brainstorm, seed `progress.md`, arm keep-alive, dispatch research/build/ship, or open a PR.

`--auto` is a no-op on this route (there is no gate). `--kind investigation` wins over intent; this route does not re-classify. [ASSUMED: classification-seam owns precedence; load-bearing for hook order]

Host/plugin-root resolve may run **in memory** so `discover_skills.py` can be invoked. It must not stamp `progress.md`. Skip: scan writes, `.wit/models.md` first-run create, `.wi/` rename, keep-alive print, token ledger init.

If `.wit/repo-map.md` / `constitution.md` / `.wit/adr/` already exist, **read** them as evidence. If they do not, explore the live tree; do not run scan to create them. [VERIFIED: roadmap acceptance "leaves product files and git state unchanged"]

### 2. Optional skill detection and delegation

Add an **`understand` capability** to `integrations.md` (not a phase-matrix row). Investigation is not a wit phase.

| wit capability | preferred skill (REQUIRED when installed) | initiator | artifact | fallback |
|---|---|---|---|---|
| understand (investigation) | `how` | `/wit:dev` after work type `investigation` | chat reply only | `skills/dev/references/investigation.md` explorer/explainer |
| understand (motivation, optional extra) | `why` | same, only if the question is motivational **and** `why` is present | chat reply only | git/`gh`/in-repo docs + labeled gaps; never a seven-MCP sweep |

Detection: `python ${CLAUDE_PLUGIN_ROOT}/skills/research/scripts/discover_skills.py --name how` (and `--name why` when the question is motivational). Stamp absent only after the full union. [VERIFIED: `discover_skills.py`; `integrations.md` union order; Cursor adapter "Plugin-cache skill discovery"]

**Delegation is mandatory when `how` is present.** Resolve the `SKILL.md` path from the union (pointer protocol, in-memory, no `progress.md` Skill paths block). The orchestrator Reads that path and follows Explain (default) or Critique-as-recommendation (see below). Pinned runners are not in play: the orchestrator is inline and uses the stamped `skill_invoke` cell if the host can invoke skills; otherwise the absolute path is enough. [VERIFIED: `integrations.md` pointer protocol; `references/capabilities.md` skill_invoke]

Do **not** add `how` or `why` to scan's recommended install set in this feature. Investigation must work standalone. [VERIFIED: `plugin-bootstrap.md` current recommended set; brief "require no MCP or external plugin"]

`why`: detect-only extra, not a core dependency. Skip if absent or if the question is mechanical ("how does X work?"). Do not copy the seven-category MCP default. If `why` is present, wit initiates it; if it no-ops without MCPs, the fallback still cites git/`gh`/in-repo docs. [VERIFIED: `.wit/roadmap.md` candidate 10 and Do not copy; brief no required MCP]

unslop / critic panels / arena: do not require. Critique "are we sure?" answers use a recommendation + tradeoffs table in the same reply, without a multi-model panel. [VERIFIED: `.wit/roadmap.md` Do not copy "Default arena..."; candidate 3 "keep critique panels opt-in"]

Who initiates: this is an active `dev` run. `how`/`why` description-match is not a trigger; wit initiates at this matrix point. [VERIFIED: `integrations.md` Who initiates]

### 3. Portable fallback (when `how` is absent)

Encode the method in `investigation.md`, in Witloop's voice. Do not vendor pstack prompt files.

- **Simple** (one module, one symbol, one flow): orchestrator explores with Read / Grep / Glob / read-only git and writes the answer. No subagent. "When in doubt, lean simple." [CITED: pstack `how/SKILL.md` complexity rule]
- **Complex** (cross-cutting subsystem): at most **two** read-only explorer dispatches (generic Task / host `subagent` cell, **not** `wit-researcher` or `wit-task-runner`), then the orchestrator synthesizes. Cap 2, not pstack's 4. [VERIFIED: roadmap candidate 3 "do not turn every repo-question into a four-agent fan-out"; constitution Simplicity]
- Explorers return: components, flow, files read, non-obvious. Explainer output is the user-facing how-shape.
- No new named agent. [VERIFIED: brief Out]

Read-only sandbox is **best-effort**: set host `readonly: true` when the Task schema has it (observed on pstack's Cursor `how`). Do not add a capability-table row for it. The portable guarantee is the prompt contract plus the deny-list below. [ASSUMED: Codex/Copilot/Grok Task schemas lack a uniform readonly flag; load-bearing: tests must assert the prompt contract, not a host flag]

### 4. Output contract

Lead with the announcement, then the answer. Do not print a keep-alive block.

```
Work type: investigation (override: --kind feature|bug-fix|investigation)
investigation via how
  OR investigation via how + why
  OR investigation via wit fallback (how absent)
```

Then one of:

- **Explain:** Overview; Key Concepts; How It Works; Where Things Live; Gotchas. [CITED: pstack investigation.md / how output]
- **Decide:** recommendation plus a short tradeoffs table, then the same Sources block.

**Citations (every non-obvious claim):**

- Code: `path:N` or `path:symbol` locators (constitution `name:N` form; never the section sign). [VERIFIED: constitution Language]
- Git: commit hash and/or `gh` PR number when used.
- External: URL. Training-data claims are labeled inference, not fact.
- Close with `## Sources` (files, commits, PRs, gaps). Null searches are first-class when a why-shaped question was asked. [CITED: pstack `why` Sources Consulted, light version]

If the answer is that the user actually needs a change: say so, name `--kind feature` or `--kind bug-fix`, and **do not** start brainstorm. Hand back. [CITED: pstack investigation.md; brief "shows the override instead of asking"]

Apply compact-reasoning: the reply is the product, so the explanation keeps full depth; sequencing around it stays short. [ASSUMED: compact-reasoning carve-out analogous to design-gate; not load-bearing]

### 5. Read-only guarantees (deny-list)

The route must not:

- Create or edit `.wit/features/**`, `progress.md`, `brief.md`, `tokens.md`, ADRs, `roadmap.md`, `.wit/models.md`
- Run scan in a way that writes `repo-map.md` / constitution
- Print or arm keep-alive
- Create a branch, worktree, commit, or PR
- Edit product files
- Dispatch `wit-researcher`, `wit-task-runner`, or `wit-code-checker`
- Invoke brainstorm / research / plan / build / ship

Allowed: Read, Grep, Glob, WebSearch/WebFetch, `discover_skills.py`, read-only git (`status`, `log`, `blame`, `show`, `rev-parse`), `gh` view/list. Shell must not redirect into the repo.

Exit check: `git status --porcelain` (or host equivalent). Pre-existing dirt is ignored. New paths under `.wit/features/` or edited product files from this turn are a defect; stop and do not present the answer as successful until those writes are undone. Do not `git checkout` user files to "clean" them.

### 6. No-dossier / no-gate exit

Success is: the user has a cited answer in this turn, git state for product + `.wit/` is unchanged by this turn, and the session is not armed to continue into research. There is no `Phase = done` because there is no `progress.md`. Do not invent a shadow log.

Mid-run "how does X work?" **during** an in-flight feature is out of scope for this route (that is candidate 3 calling `understand` from research). This feature only covers `/wit:dev` classified as investigation from the start.

### 7. Tests

New `tests/test_investigation_route.py` (unittest, TDD). Mechanical contract tests, no live subagents:

1. **Four commands:** among `skills/*/SKILL.md`, names without `user-invocable: false` are exactly `{scan, dev, rpa, add-issues}`. No `skills/investigate/` and no `/wit:how` advertised in `README.md` / `AGENTS.md`.
2. **Hook order:** `skills/dev/SKILL.md` mentions investigation **and** loading `skills/dev/references/investigation.md` before feature-folder creation language ("classify the idea before creating", `progress.md` seed).
3. **Deny-list strings** in `investigation.md`: no feature dossier; no keep-alive; no PR; do not write `progress.md`.
4. **integrations.md:** `understand` capability; `how` preferred; `why` optional; capture-into-`.wit/` exception for investigation; Who initiates still says wit initiates; rename "research investigation" so it cannot mean this work type.
5. **Detection:** existing `discover_skills.py --name how` present/absent still holds; add one case that a Cursor-cache `how/SKILL.md` is `present` (mirrors `test_discover_skills.py`).
6. **Output contract:** investigation.md requires the `investigation via how` / `investigation via wit fallback (how absent)` lines and `path:N` / Sources.
7. **Fallback cap:** text forbids a new named agent and caps explorers at 2.
8. **validate.py:** keep the "verify absence" integrations check; add a cheap marker if needed (`understand` or `investigation via`) so a compression pass cannot drop the exception.

Do not weaken `IntegrationsDocTest`. Behavior change is a **minor** version bump in lockstep across the three manifests. [VERIFIED: constitution Git & shipping]

## Don't-Hand-Roll

| Problem | Don't build | Use instead | Why |
|---|---|---|---|
| Find whether `how`/`why` is installed | Host if-trees / memory | `discover_skills.py --name` | Union already tested; Cursor cache is step 3 |
| Cross-host skill invoke | New capability row | Stamped `skill_invoke` + pointer path | Capability table already exists |
| Cited walkthrough method | New named agent; copy of pstack prompts | Delegate `how`, else short fallback in investigation.md | Brief: optional skills; no new agent |
| Audit "which mode ran" | Shadow `.wit/` log | Reply line `investigation via …` | No dossier by contract |
| Motivation archaeology | Seven-MCP `why` core | Optional `why` if present; else git/`gh`/docs + gaps | Roadmap candidate 10 is Later; no required MCP |

## State of the art (this repo)

| Old way | Current way (this feature) | When it changed |
|---|---|---|
| `/wit:dev` always means "open a feature folder and loop to a PR" | `/wit:dev` may early-exit as investigation | this feature |
| Optional skills always capture into `.wit/` | Investigation is the exception: reply is the artifact | this feature; must be written into integrations.md |
| "research investigation" = researcher subagents | Keep that meaning; don't reuse the word for this work type | wording fix while editing integrations.md |
| pstack sticky router with `/how` as a playbook | Borrow how-shaped method; entry remains `/wit:dev` | brief / roadmap Do not copy |

## Dependency Legitimacy

No new package. Optional runtime skills `how` and `why` are detected, never installed as a hard dependency. Verdict: **none added**.

pstack `how` / `why` as optional delegates: already present in this session's Cursor cache under `cursor-public/9717366/…/skills/how` and `skills/why` (real plugin tree, not a registry guess). [VERIFIED: glob of that cache] Do not auto-substitute a similarly named skill.

## Assumptions Log

| Claim | Why assumed | Load-bearing? |
|---|---|---|
| Classification-seam inserts the work-type branch **before** feature-folder classification | Sibling charter; this note cannot implement the classifier | **Yes** -> spec Open question (hook order) |
| `--kind investigation` is already selected when this route runs | Sibling owns override precedence | **Yes** -> spec (do not re-classify here) |
| Codex/Copilot/Grok lack a uniform Task `readonly:` flag | Adapters document subagent spawn, not a readonly cell | **Yes** -> spec (prompt contract is the guarantee) |
| Natural-language "how does X work?" without `/wit:dev` may hit pstack `how` directly | Host skill auto-trigger is outside wit once `dev` is not loaded | No (out of this route's contract) |
| Compact-reasoning carve-out for the explanation body | Analogous to design-gate depth | No |
| Candidate 3 may later persist a research note when a dossier exists | Roadmap "Depends on 1"; brief forbids persist on this route | No (explicit non-goal) |
| `git status --porcelain` is available on all five hosts via stamped `shell` | repo-map / adapters assume git for ship | No; fallback is "do not write", not the status check |

## Risks / unknowns

1. **Hook vs classifier race:** if classification-seam puts work type after folder creation, investigation will have already seeded `progress.md`. Plan must make hook-before-create a BLOCKER acceptance criterion. (Sibling dependency.)
2. **integrations.md capture rule:** a partial edit that adds `how` but leaves "always capture into `.wit/`" unmodified will cause agents to write a dossier. The exception must be in the same file the orchestrator already loads.
3. **`how` auto-trigger vs `/wit:dev`:** on Cursor, both descriptions might match. Who-initiates covers an active wit run; if the host loads `how` *instead of* `dev`, wit never announces work type. Mitigate by keeping entry as `/wit:dev` / `--kind investigation`; widening `dev`'s description is classification-seam (watch the 1024-char cap).
4. **Readonly host flag unverified** for Codex/Copilot/Grok. Build must not document `readonly: true` as universal. Tests assert deny-list text.
5. **Exit `git status` vs pre-existing dirt:** naive "must be empty" fails on a dirty worktree. Procedure must ignore paths this turn did not create.
6. **Minor version bump + three-manifest lockstep** required (behavior change).
7. **Alias copy:** `references/skill-aliases/wit-dev/SKILL.md` still describes only the feature loop. Optionally one clause that `/wit:dev` may early-exit as a read-only investigation; not a new alias.

## Runtime State Inventory

Not a rename/migration. None of the five categories apply. None - verified by scope (workflow/reference change; no stored keys, env names, units, or published package rename).

## Citations (this note)

1. `/workspace/.wit/features/0003-work-type-routing/brief.md`
2. `/workspace/.wit/constitution.md`
3. `/workspace/.wit/repo-map.md`
4. `/workspace/skills/dev/SKILL.md`
5. `/workspace/skills/research/references/integrations.md`
6. `/workspace/skills/research/scripts/discover_skills.py`
7. `/workspace/.wit/roadmap.md` (candidates 1, 3, 10; Do not copy)
8. pstack `skills/poteto-mode/playbooks/investigation.md`
9. pstack `skills/how/SKILL.md` and `how/references/explorer-prompt.md`
10. pstack `skills/why/SKILL.md`
11. `/workspace/README.md` four advertised commands
12. `/workspace/references/capabilities.md`
