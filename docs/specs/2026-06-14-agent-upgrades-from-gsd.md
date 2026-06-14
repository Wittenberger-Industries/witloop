---
type: Design Spec
title: Agent upgrades — features to add to researcher, task-runner, and a new checker
description: Feature roster for wi's agents drawn from GSD-core's agent patterns, with each output mapped to its OKF type.
status: proposed
timestamp: 2026-06-14
tags: [agents, researcher, task-runner, checker, gsd, okf]
---

# Agent upgrades — features to add to researcher, task-runner, and a new checker

Features to add to wi's two agents (`researcher`, `task-runner`) and one new agent (`checker`),
distilled from [GSD-core](https://github.com/open-gsd/gsd-core)'s agent patterns (see the
[takeaways](/docs/specs/2026-06-14-okf-knowledge-format.md) discussion that preceded this). GSD is
the heavy opposite of wi, so this borrows *judgment patterns* (portable prose), not its 33-agent
structure.

**Everything here respects [OKF](/docs/specs/2026-06-14-okf-knowledge-format.md).** Two rules thread
through the whole spec:

1. Every artifact an agent writes opens with YAML frontmatter carrying a non-empty `type` (plus
   `title`/`description`/`timestamp`, bundle-relative `/…` links, numbered `## Citations` for external
   sources). Each feature below names the `type` of whatever it emits.
2. New outputs that are their own files are added to the `type` vocabulary in the OKF spec §5 and the
   `.wi/` directory specs. New `type` values introduced here: **`Verification`** (the checker's report)
   and **`Runtime State Inventory`** (optional standalone; otherwise a section). The new agent file
   itself carries `type: Agent`, like `researcher.md` and `task-runner.md` already do.

Priorities: **P1** = high value / low cost, do first; **P2** = valuable; **P3** = optional / heavier.

---

## 1. `researcher` — features to add

The researcher's notes are already `type: Research Note` (ephemeral, pruned at ship). These features
mostly add sections to that note and promote load-bearing rows into the typed `spec.md` / `tasks.md` /
`pitfalls.md` / ADR.

| # | Feature | What it adds | OKF output | Pri |
|---|---------|--------------|------------|-----|
| R1 | **Per-claim provenance tags** | Tag every factual claim inline `[VERIFIED: src]` / `[CITED: url]` / `[ASSUMED]`. `[ASSUMED]` = "not confirmed this session — needs user sign-off before it becomes a locked decision." | `## Assumptions Log` table in the Research Note; load-bearing assumptions promoted to the ADR `## Citations` and `spec.md` Open questions so the **design gate** surfaces them. | P1 |
| R2 | **Dependency-legitimacy (slopsquatting) flag** | Any package found via web/training is `[ASSUMED]` *even if the registry resolves it* (slopsquats resolve too). Check registry + real source repo + age/adoption; verdict OK/SUS/SLOP. | `## Dependency Legitimacy` section in the Research Note; each new dep + verdict flows into `spec.md` (Dependencies). SUS/ASSUMED → a blocking gate question. Pairs with T7 (task-runner never auto-substitutes). | P1 |
| R3 | **Runtime State Inventory** (rename/refactor/migration goals) | The five-category sweep for state a code grep can't see (detailed in §4). Triggered when the goal is a rename/rebrand/refactor/migration. | `type: Runtime State Inventory` doc (or a `## Runtime State Inventory` section in the Research Note); every load-bearing row promoted to `spec.md` (Interfaces & data changes), `tasks.md` (a *migration* task, separate from the code-edit task), and `pitfalls.md`. | P1 |
| R4 | **Prescriptive output schema** | "Use X" not "Consider X or Y." Add a **Don't-Hand-Roll** table (problem → don't build → use instead → why) and a **State of the Art** table (old → current → when it changed / deprecations). Pin every recommended lib to a verified version. | Sections in the Research Note / chosen-approach; no new type. | P2 |
| R5 | **Confidence + freshness stamp** | HIGH/MED/LOW per finding, and a `valid_until` estimate (≈30 d stable, ≈7 d fast-moving) so a later goal knows when the research is stale. | Body confidence notes + frontmatter extension `valid_until:` on the Research Note; ties into `scan --refresh` drift. | P2 |
| R6 | **Web-query hygiene** | Don't inject the year into search queries (biases toward stale dated pages); check publication dates on results instead. | Behavioral rule in the agent body; no output change. | P1 |
| R7 | **Capability → layer map** (optional, lighter than GSD's tier map) | For frontend/backend repos, map each capability to its owning layer before researching, so the planner doesn't misplace work (e.g., auth in the client). | `## Responsibility Map` section in the Research Note; the checker (C-cov) can verify task placement against it. | P3 |

wi already has: source discipline, a single `Verified:` line, bounded spike, `[repo-question]`/`[tech-choice]`
modes. R1/R5 upgrade the single line into per-claim tags + an assumptions table the gate consumes.

---

## 2. `task-runner` — features to add

The task-runner writes code + a short report and ticks `progress.md` (already `type: Goal Progress`).
Its deviations and deferred items fold into `progress.md` — no new file type needed.

| # | Feature | What it adds | OKF output | Pri |
|---|---------|--------------|------------|-----|
| T1 | **Typed deviation taxonomy** | Explicit rules with priority: **R1** auto-fix bugs · **R2** auto-add *missing critical* security/correctness functionality · **R3** auto-fix blocking issues · **R4** STOP + ask on architectural changes (new table, switch library, auth model). "When in doubt → ask." | Deviations logged to `progress.md` "Decisions / blockers" + the report. | P1 |
| T2 | **Analysis-paralysis guard** | 5+ consecutive Read/Grep/Glob with no Edit/Write/Bash → STOP, state in one line why nothing's written, then write or report blocked. | Behavioral; surfaced in the report if it trips. | P1 |
| T3 | **Fix-attempt limit** | After 3 auto-fix attempts on one task → stop, record under "Deferred Issues," do **not** re-run the build hoping it clears. | "Deferred Issues" in `progress.md` + report. | P1 |
| T4 | **Self-check before "done"** | Verify claimed files exist (`[ -f ]`) and the exact Verify command actually passed; scan own output for stubs (`=[]`, "TODO", "coming soon", data wired to nothing); refuse fake-green. | `Self-Check: PASS/FAIL` line in the report; ticks `progress.md` only on PASS. Bakes the v0.9.0 "gate on file-state, not console" lesson into the agent. | P1 |
| T5 | **Worktree git prohibitions** | Name the landmines and why: no `git stash` (the stash stack is shared across worktrees via `refs/stash` — a pop applies a sibling's WIP), no `git clean` (deletes feature-branch files it sees as untracked), no `reset --hard` / `update-ref` on protected branches. Sanctioned alternative: commit WIP to a throwaway branch you own. | Behavioral rules in the agent body. Hardens wi's parallel-worktree model. | P1 |
| T6 | **Auth-gate outcome** | Treat "401 / run X login / set ENV" as a *gate*, not a failure: stop, report the exact steps, let the keep-alive loop pause cleanly. | A distinct `Auth gate` status in the report; recorded in `progress.md`. | P2 |
| T7 | **Package-install safety** | A failed/unknown install is a **blocker**, never auto-substitute a similar name (slopsquat risk). Pairs with R2. | Blocker in the report + `progress.md`; constitution rule. | P1 |

wi already has: strict task scope, "other tasks aren't your backlog," scoped lint/typecheck, no commit
(orchestrator commits), parallel-sibling awareness, ~15-line report. T1 adds the *permission* to fix
small correctness/security gaps while still escalating structural ones.

---

## 3. `checker` — the new agent (verification)

GSD splits `gsd-plan-checker` (verifies plans *will* hit the goal, before execution) from `gsd-verifier`
(verifies code *did*, after). wi stays lean: **one** read-only agent, two modes. It complements — not
duplicates — the human **design gate** (it feeds it) and `superpowers:requesting-code-review` (which
does line-level review; the checker works at the goal/coverage level).

**Proposed frontmatter** (OKF-conformant, mirrors the other agents):

```yaml
---
type: Agent
name: checker
model: inherit          # opt-in cheaper tier later (see X3)
color: magenta
tools: ["Read", "Grep", "Glob", "Bash"]   # read-only, like GSD's plan-checker
description: |
  Goal-backward verification for wi. PLAN mode: before the design gate, verify the spec+tasks WILL
  achieve the goal (coverage, wiring, scope, no silent scope-reduction). RESULT mode: at ship, verify
  the build DID satisfy the spec's acceptance criteria + locked decisions. Read-only; returns
  BLOCKER/WARNING/INFO findings. Writes .wi/goals/<slug>/verification.md (type: Verification).
---
```

| # | Feature | What it does | Pri |
|---|---------|--------------|-----|
| C1 | **Two modes** | `plan` (pre-gate: reads brief, spec, tasks, pitfalls, constitution, glossary, ADRs) and `result` (ship: reads the diff/build + spec acceptance criteria). | P1 |
| C2 | **Goal-backward coverage** | Start from what the goal must deliver → which task delivers each truth → are artifacts *wired*, not just created? Catches "endpoint exists but auth check is missing." | P1 |
| C3 | **Coverage matrix** | Every `spec.md` acceptance criterion, constitution rule, ADR decision, glossary term, **Runtime State Inventory** row (R3), and pitfall must map to a covering task. Unmapped = finding. | P1 |
| C4 | **Scope-reduction detection** | Scan tasks for "v1 / simplified / static for now / stub / wire later" against locked decisions. Silent down-scoping of a decision = **BLOCKER** (GSD's "most insidious" failure). | P1 |
| C5 | **Mandatory severity** | Every finding carries BLOCKER / WARNING / INFO. A finding without severity is invalid output. Named soft-failure: "issuing warnings for what are really blockers." | P1 |
| C6 | **Adversarial stance** | Assume the plan/result is flawed until coverage proves otherwise; don't credit intent, only verifiable coverage. Extends wi's verification iron-law. | P2 |
| C7 | **Scope/context ceilings** | Flag task-units that won't fit a fresh context window (rough ceilings on tasks/files per unit) — wi's whole premise. | P2 |
| C8 | **Bounded revision loop** | In `plan` mode, return findings → plan revises → re-check, max N (e.g. 2), then escalate the remainder to the human design gate. Mirrors wi's existing bounded-retry. | P1 |

**Output (OKF):** `.wi/goals/<slug>/verification.md`, `type: Verification`, ephemeral like `research/` —
ship folds the verdict + any waived findings into `PR.md` and prunes `verification.md` at close-out
unless the constitution opts to keep it. **The fixed 7-file dossier rule is preserved** (verification.md
is transient, exactly like research notes).

**Where it slots in:**

```
brainstorm → research → plan → [checker: plan mode] → DESIGN GATE → build → [checker: result mode] → ship → PR
```

---

## 4. Runtime State Inventory — the detailed explanation

**The problem.** A rename, rebrand, refactor, or migration changes *source files* — but the old name or
shape usually also lives in **runtime state** that no `grep` of the repo will ever surface. You update
every file, the tests pass, and production still breaks because a queue, a scheduled job, a secret key,
or a stored record still carries the old identity. GSD's framing is exact:

> "A grep audit finds files. It does NOT find runtime state."

So the inventory is a **mandatory, explicit sweep** the researcher runs whenever the goal is a
rename/rebrand/refactor/migration. For each of five categories it must answer concretely — and "None —
verified by X" is a valid answer, but a **blank is not** (a blank can't distinguish "checked, found
nothing" from "never checked").

**The canonical question:** *After every file in the repo is updated, what runtime systems still have the
old string cached, stored, or registered?*

**The five categories** (stack-agnostic):

1. **Stored data** — datastores keyed on the old string: DB table/column/enum *values*, collection
   names, cache keys, queue names, document IDs, a `user_id` like `dev-os`. These need a **data
   migration** (update existing rows), which is a *different task* from the code edit that changes how
   new rows are written.
2. **Live service config that lives outside git** — config held in an external system's UI or DB, not in
   your repo: CI/CD env-var *names*, webhook URLs, dashboards/alerts named after the thing, feature-flag
   keys, cron jobs in a scheduler UI, cloud resource names/tags. A `git diff` shows none of this.
3. **OS / platform-registered state** — things registered at install/registration time: systemd unit
   names, Windows Task Scheduler tasks, pm2/process names, launchd plists, container image tags in a
   registry, the installed package name.
4. **Secrets & env-var names** — the *keys/names* (never the values) that reference the old name: vault
   key names, `.env` variable names, CI secret names. Distinguish "rename the key" from "code reads the
   key" — both must change in lockstep or reads break.
5. **Build / installed artifacts** — artifacts that carry the old name and won't auto-update from a
   source rename: compiled binaries, package metadata (`*.egg-info`, `dist/`), lockfile entries,
   generated code, Docker layers, the *published* package name.

**The key distinction — data migration vs code edit.** Every item found becomes one or both, and they
are **separate tasks**. "Change how new records are written" (code) does not fix "the million existing
records keyed on the old value" (data migration). The checker (C3) then verifies each inventory row has
a covering task.

**Worked example — wi:dev (rename service `recsolution` → `docflow`):** all source updated, but the
Redis cache keys `recsolution:*` (stored data → migration), the CI secret name `RECSOLUTION_API_KEY`
(secret name → rename + code read), the Grafana dashboard "RecSolution Health" (live config), the
systemd unit `recsolution.service` (OS-registered), and the published npm package `@acme/recsolution`
(build artifact) all still carry the old name. Five tasks a grep would never have produced.

**Worked example — wi:rpa (where this bites hardest):** renaming an automation touches Orchestrator
**queue / asset / process names** (live service config), the **published package name** (build
artifact), **credential *names*** (secrets — names only, per the rpa-constitution), and **queue items
in flight** (stored data) — none in the repo. This maps cleanly onto wi:rpa's existing
`orchestrator.md` (`type: Orchestrator Manifest`) and `inputs.md` registries.

**OKF placement.** The inventory is a `type: Runtime State Inventory` concept doc (or a
`## Runtime State Inventory` section inside the `type: Research Note`). Load-bearing rows are promoted
into the already-typed `spec.md` (Interfaces & data changes), `tasks.md` (one migration task per item),
and `pitfalls.md` ("renamed the code, left the queue") — so the durable record lives in the dossier's
existing OKF concepts and the inventory itself can be pruned like other research notes.

---

## 5. OKF impact summary (what implementing this touches)

- **New `type` values** → add to OKF spec §5 vocabulary + the `.wi/` directory specs:
  `Verification` (checker report), `Runtime State Inventory` (if standalone). `Agent` already exists.
- **`skills/research/references/wi-directory.md`** — add `verification.md` → `Verification` and the
  optional inventory to the type list + tree; note both are **ephemeral** (pruned at close-out, like
  `research/`), so the 7-file dossier rule holds.
- **`skills/rpa/references/rpa-directory.md`** — same additions (RSI + verification apply to RPA runs).
- **`docs/specs/2026-06-14-okf-knowledge-format.md`** — extend the `type` table.
- **`scripts/validate.py`** — no logic change (it accepts any non-empty `type`); the new
  `agents/checker.md` will be picked up by the existing OKF + name/description checks, so it must carry
  `type: Agent` + `name` + `description`.
- **Cross-cutting** — every artifact these features emit follows the wi OKF profile: frontmatter with
  `type`, bundle-relative `/…` links, numbered `## Citations`.

## 6. Cross-cutting (apply to all three agents)

- **X1 — Self-verifying writes:** any agent that writes a file confirms it exists and parses before
  returning (generalizes T4). Reinforces [[harness-artifacts-masquerade-as-results]].
- **X2 — Machine-detectable completion markers:** standardize return markers (e.g.
  `## RESEARCH COMPLETE` / `## CHECK PASSED` / `## ISSUES FOUND` / `## TASK COMPLETE|BLOCKED`) so the
  hands-off keep-alive loop and the cross-platform spawn variants can detect completion robustly.
- **X3 — Per-agent model tier (opt-in):** allow a cheaper model for cheap/parallel agents (many
  researchers, simple task-runners). `model: inherit` stays the portable cross-platform default.
- **X4 — MCP-tools gotcha:** if the researcher lists docs-MCP tools (`mcp__context7__*`, …) to enable
  docs-first research, note the Claude Code bug where a `tools:` allowlist can strip MCP tools from an
  agent — keep a WebSearch/WebFetch fallback.

## Citations

[1] [gsd-phase-researcher.md](https://github.com/open-gsd/gsd-core/blob/next/agents/gsd-phase-researcher.md) — provenance tags, package-legitimacy gate, Runtime State Inventory, prescriptive schema.
[2] [gsd-executor.md](https://github.com/open-gsd/gsd-core/blob/next/agents/gsd-executor.md) — deviation rules, analysis-paralysis guard, fix-attempt limit, self-check, worktree git prohibitions, auth gates.
[3] [gsd-plan-checker.md](https://github.com/open-gsd/gsd-core/blob/next/agents/gsd-plan-checker.md) — goal-backward verification, scope-reduction detection, mandatory severity, adversarial stance.
[4] [agent-contracts.md](https://github.com/open-gsd/gsd-core/blob/next/gsd-core/references/agent-contracts.md) — completion markers + handoff contracts.
[5] [ARCHITECTURE.md](https://github.com/open-gsd/gsd-core/blob/next/docs/ARCHITECTURE.md) — model profiles, context budget, agent taxonomy.
