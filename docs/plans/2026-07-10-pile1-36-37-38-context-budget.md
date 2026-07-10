---
type: Implementation Plan
title: "Pile 1 — #36 trim tool output · #37 read discipline · #38 resolve routing once (v1.7.0)"
description: "Task-by-task plan for the Pile 1 context-budget issues, landing as one PR (B in the sweep): redirect-and-tail output house rule, hard context budget with per-skill citations, and resolve-once model routing cached in progress.md."
timestamp: 2026-07-10
tags: [context-budget, performance, tokens, plan]
---

# Pile 1 — #36 trim tool output · #37 read discipline · #38 resolve routing once (v1.7.0)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** land the three Pile 1 issues from the sweep triage (docs/plans/2026-07-10-issue-triage-35-42.md) as one PR: the orchestrator stops retaining verbose tool output (#36), holds only the budgeted artifact set and delegates big reads (#37), and resolves model routing once per run into a compact `progress.md` block that every dispatch reads (#38). Version v1.7.0 (PR B of the sweep).

**Architecture:** all three are instruction edits to skills/references — no scripts change and no agent charter (`agents/*.md`) is touched. `workflow.md`'s §Token budget becomes the single anchor holding two named hard rules (the **context budget** and the **output house rule**) that phase skills cite; `.wi/features/<slug>/.logs/` is a new self-gitignored ephemeral dir in the user project (never this repo); `references/models.md`'s Dispatch rule flips from "resolve at every dispatch" to "resolve once at entry, record a `## Model routing (resolved)` block in progress.md, dispatches read the block". Routing behavior is unchanged by construction — same override → role → `inherit` resolution, computed once.

**Tech stack:** markdown skill/reference edits only; `python scripts/validate.py` + `python -m unittest discover -s tests -q` as the gate (the suite is unittest-based — pytest is not installed on this machine; 47 tests green at plan time); grep sweeps for self-consistency.

## Global constraints

- **One PR, stacked-sweep conventions:** branch `pile1-context-budget` off current `main`, squash-merge at the end, **no AI attribution** in commits or the PR (repo convention).
- **No agent-charter edits.** `agents/*.md` are out of scope for this pile (triage: only #40/#42 may touch them).
- **No rule removed, no gate weakened.** #36 changes where output *lives*, never what is checked; #37 removes redundant reads, never inputs to a decision; #38 caches a deterministic resolution, never changes it. The unavailable→`inherit` fallback and the never-re-ask rule stay verbatim.
- **Routing defaults stay opus/sonnet; never bake the live session model into the resolved block** — the block records **configured** tiers only (triage guardrail 6; memory: no top-tier models by default).
- **Staleness rule (settled at pick-up per guardrail 6):** re-resolve routing when the block is **absent** or `.wi/models.md` **changed after the block's stamp**; a dispatch-time unavailable→`inherit` fallback does NOT rewrite the block.
- **`.logs/` is a user-project path** (`.wi/features/<slug>/.logs/`), self-gitignored via its own `.gitignore` containing `*`, listed in wi-directory's ephemera and pruned at ship's tidy. It is NOT added to this repo's `.gitignore` (guardrail 5).
- **progress.md block lines must not open with a bare ISO stamp** — `token_report.py`'s `STAMP_RE` matches stamps at line start; the block's stamp stays mid-line (`- resolved <stamp> …`), verified safe against `skills/ship/scripts/token_report.py:62`.
- **Version bump to 1.7.0 in all THREE manifests** — `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (the `plugins[0].version`, ~line 15; leave the top-level `0.1.0`), and `.codex-plugin/plugin.json` — `validate.py` asserts the three agree.
- After every markdown edit: `python scripts/validate.py` green, and check the file **tail** (this repo has shipped mid-sentence truncated files; validate only guards trailing newline + fence balance).
- Two deliberate off-list additions, each flagged in the PR body: `skills/ship/references/verification-gate.md` (its iron law says "full output read" — it must not contradict the new house rule) and `skills/rpa/references/{rpa-directory,verification-gate}.md` (the rpa progress template + one MoA gating line read `.wi/models.md` at dispatch time — #38's AC2 is incomplete without them).

---

### Task 1: `workflow.md` §Token budget — the shared anchor (#36 + #37)

Both issues hang off this section; the triage mandates one coherent section edit.

**Files:**
- Modify: `skills/research/references/workflow.md` (§Token budget, lines 80–93)

**Interfaces:**
- Produces: two **named** rules later tasks cite verbatim — "**the context budget**" and "**the output house rule**" — plus the log-dir path convention `.wi/features/<slug>/.logs/` and the redirect idiom. Every citation in Tasks 3–6 must use these two names.

- [ ] **Step 1: Replace the section opening.** The current section opens with:

    `research` and the post-gate loop should hold at most: `constitution.md`, `repo-map.md`, the feature's `progress.md`, and the one
    artifact for the active phase. Research and build tasks run in subagents that return summaries; their
    transcripts never enter the orchestrator's context. That is what makes a hands-off, multi-file feature affordable.

  Replace those three lines (and only them — everything from "The cost is also *measured*…" to the section's end is #35 text and stays verbatim) with:

    Every token the orchestrator retains is re-read on every later turn (~75× measured on a real run), so
    standing weight compounds for the whole run. Two hard rules keep a hands-off run affordable — phase
    skills cite them as **the context budget** and **the output house rule**:

    1. **The context budget — hold at most:** `constitution.md`, `repo-map.md`, the feature's
       `progress.md`, and the one artifact for the active phase. `progress.md` is the state of record:
       phase re-entry reads it (plus the active artifact) and **never re-Reads prior-phase artifacts**
       already summarized there. To confirm one criterion or rule, read that section, not the whole
       file. Reading beyond the budget is delegated: researchers (research) and task-runners (build)
       read sources and return summaries — an ad-hoc "let me check file X" on a large file is a
       subagent dispatch, not an orchestrator Read.
    2. **The output house rule — never pipe unbounded command output into context.** Redirect to the
       feature's log dir and read the verdict, not the stream. Once per feature:
       `mkdir -p .wi/features/<slug>/.logs && printf '*\n' > .wi/features/<slug>/.logs/.gitignore`
       (self-gitignored — the dir never enters `git status` or a dossier commit). Then per command:
       `<cmd> > .wi/features/<slug>/.logs/<name>.txt 2>&1; echo $?; tail -n 30 .wi/features/<slug>/.logs/<name>.txt`.
       On red, pull the failing lines (`grep -n -B1 -A3 -iE 'fail|error' <log>`), never the whole log —
       the file stays on disk for deeper dives and is pruned at ship's dossier tidy (wi-directory.md's
       ephemera list). Diffs enter by summary, then hunk: `git diff --stat` first, open only the hunks a
       finding needs; never read a whole diff into context.

    Research and build tasks run in subagents that return summaries; their transcripts never enter the
    orchestrator's context. That is what makes a hands-off, multi-file feature affordable.

- [ ] **Step 2: Verify** — `python scripts/validate.py` exits 0; the #35 measurement text ("The cost is also *measured*…" through "…never estimated.") is byte-identical to before (check with `git diff` — the hunk must not touch those lines); file tail intact.
- [ ] **Step 3: Commit** — `git checkout -b pile1-context-budget` then `git commit -m "feat: workflow.md token budget — context budget + output house rule (#36, #37)"`

### Task 2: `wi-directory.md` — `.logs/` ephemera + state-of-record note (#36 + #37)

**Files:**
- Modify: `skills/research/references/wi-directory.md` (tree ~line 38, ephemera bullet ~line 68, paragraph after the progress.md template ~line 154)

**Interfaces:**
- Produces: the ephemera list ship §6.2 prunes by name now includes `.logs/`; the tree shows it. (The `## Model routing (resolved)` template addition is Task 7, not here — keep the commits by concern.)

- [ ] **Step 1: Tree entry.** After the `cross-review.md` tree line, insert (matching the existing indentation and comment column):

    ├── .logs/          # redirected command output (gates, CI pulls — workflow.md's output house rule) — self-gitignored, EPHEMERAL

- [ ] **Step 2: Ephemera bullet.** Change the bullet opening `**\`research/\`, \`verification.md\`, and \`cross-review.md\` are ephemeral.**` to `**\`research/\`, \`verification.md\`, \`cross-review.md\`, and \`.logs/\` are ephemeral.**`, change its "…prunes all three before the PR" to "…prunes all four before the PR", and append to the bullet:

    `.logs/` holds redirected command output (workflow.md's output house rule); its own `.gitignore`
    (containing `*`) keeps it out of `git status` and every dossier commit, so it is never tracked — the
    tidy plain-deletes the directory.

  The "After `done`, a feature folder holds exactly the seven-file dossier" sentence stands unchanged.
- [ ] **Step 3: State of record (#37).** In the paragraph after the progress.md template ("Update the **Phase** field and append to **Log** at every transition…"), append one sentence:

    `progress.md` is the run's state of record — phase re-entry reads it (plus the active phase
    artifact) and never re-Reads prior-phase artifacts already summarized here (workflow.md's context
    budget).

- [ ] **Step 4: Verify** — `python scripts/validate.py` exits 0; file tail intact.
- [ ] **Step 5: Commit** — `git commit -m "feat: wi-directory — .logs/ ephemera (#36); progress.md state-of-record note (#37)"`

### Task 3: `build/SKILL.md` — wave-gate redirect + budget citation (#36 + #37)

**Files:**
- Modify: `skills/build/SKILL.md` (intro Inputs line ~22, §2.2 dispatch content ~52, wave-end gate refinement (a) ~88)

(The §2.2 **Model per dispatch** sentence is rewritten in Task 8, not here.)

- [ ] **Step 1: Budget citation (#37).** After `Inputs: \`tasks.md\`, \`spec.md\`, \`constitution.md\`, \`repo-map.md\`.` append:

    That list is also the ceiling — workflow.md's **context budget**: hold `tasks.md` (the active
    artifact) plus `progress.md` and the two project files; consult `spec.md` **by section** when a task
    needs a criterion verbatim. Runners read everything else — never pre-read a runner's source files
    "to prepare" a dispatch. On re-entry, `progress.md`'s ticks + Log are the build's state; don't
    re-Read prior-phase artifacts to reconstruct it.

- [ ] **Step 2: Dispatch content note (#37).** In §2.2, after "Each gets exactly what it needs and nothing more: its task block, the relevant constitution rules, and the repo commands." append: "Pointers and rules, not pasted file bodies: the runner reads its own files (workflow.md's context budget)."
- [ ] **Step 3: Wave-end gate redirect (#36).** In refinement (a), after "run the full lint + test commands once, serially, before dispatching the next wave" insert:

    — output redirected per workflow.md's output house rule
    (`… > .wi/features/<slug>/.logs/w<N>-tests.txt 2>&1`), verdict read from the exit code +
    `tail -n 30`, failures pulled by grep, never the whole log —

  and change the same sentence's "when `.wi/models.md` sets `check_points: per-wave`" to "when the resolved-routing block's cross-provider row says `per-wave` (progress.md; #38's resolve-once rule)".
- [ ] **Step 4: Verify** — `python scripts/validate.py` exits 0; file tail intact.
- [ ] **Step 5: Commit** — `git commit -m "feat: build — wave-gate output redirect (#36), context-budget citation (#37)"`

### Task 4: `ship/SKILL.md` + `verification-gate.md` — gate/CI/diff discipline (#36 + #37)

**Files:**
- Modify: `skills/ship/SKILL.md` (Inputs ~17, §1 ~28, §2 ~37, §6.2 ~249, §8 ~321/331)
- Modify: `skills/ship/references/verification-gate.md` (iron law list, lines 17–19) — **off-list reconciliation, flag in PR body**

- [ ] **Step 1: Budget citation (#37).** After ship's `Inputs: …\`repo-map.md\`.` line append:

    Hold exactly that (workflow.md's **context budget** — `spec.md` + `pitfalls.md` are this phase's
    artifacts, read by section where possible): the diff enters as `--stat` + hunks (§2), command output
    as exit code + tail (§1/§8), and the checker — not you — re-reads the repo.

- [ ] **Step 2: §1 gate redirect (#36).** After "…and any CI-equivalent command from `repo-map.md`." insert:

    Run every gate command per workflow.md's **output house rule** — redirected to
    `.wi/features/<slug>/.logs/gate-<step>.txt`, verdict from the exit code + `tail -n 30`, failures
    pulled by grep. The log file is the evidence and stays on disk; the transcript keeps only the
    verdict.

- [ ] **Step 3: §2 diff discipline (#36).** Change "Self-review the diff with fresh eyes, specifically against:" to "Self-review the diff with fresh eyes — overview via `git diff --stat`, then open only the hunks a criterion or finding needs (workflow.md's output house rule: never a whole-diff read) — specifically against:".
- [ ] **Step 4: §6.2 prune note (#36).** In the §6.2 sentence about untracked ephemera (after "…is untracked — plain-delete it, `git rm` has no pathspec to match"), extend the parenthetical: "; `.logs/` is likewise never tracked (self-gitignored) — plain-delete the directory".
- [ ] **Step 5: §8 CI logs (#36).** Change "then watch them to completion: `gh pr checks <pr-url-or-number> --watch --fail-fast`, bounded by a sane timeout" to append "— redirected to `.wi/features/<slug>/.logs/pr-checks.txt`; the final table (its tail) is the evidence you log to `progress.md`". Change "Pull the failing logs (`gh run view <run-id> --log-failed`; an external check via its details URL) and diagnose." to:

    Pull the failing logs to a file, not into context
    (`gh run view <run-id> --log-failed > .wi/features/<slug>/.logs/ci-<run-id>.txt 2>&1`; an external
    check via its details URL), read the failing lines by grep/tail, and diagnose.

- [ ] **Step 6: Iron law reconciliation (#36).** In `verification-gate.md`, the iron law's numbered list reads "…2. run it now; 3. read the whole output + exit code; 4. confirm it matches the claim." Replace items 2–4 with:

    2. run it now, output redirected per workflow.md's output house rule; 3. read the exit code + the
    log's tail (the full output stays on disk — grep it on red); 4. confirm it matches the claim.

  Nothing else in the file changes — the red-flags list and "What green means" already key on commands run + exit codes, not retained streams.
- [ ] **Step 7: Verify** — `python scripts/validate.py` exits 0; both file tails intact.
- [ ] **Step 8: Commit** — `git commit -m "feat: ship — gate/CI/diff output discipline (#36), context-budget citation (#37)"`

### Task 5: `scan/SKILL.md` — gitignore guidance + lean-file warning (#36 + #37)

**Files:**
- Modify: `skills/scan/SKILL.md` (step 2 greenfield ~58, step 7 report ~78, `--refresh` §A ~106, §C report ~132)

- [ ] **Step 1: Greenfield gitignore (#36, guardrail 5).** Change "Also drop a stack-appropriate `.gitignore` (caches, build artifacts) so the first build doesn't leak them." to "Also drop a stack-appropriate `.gitignore` (caches, build artifacts, `.wi/features/*/.logs/` — wi's redirected command output) so the first build doesn't leak them."
- [ ] **Step 2: First-scan lean warning (#37).** In step 7's report line, change "and anything left `UNKNOWN`." to "anything left `UNKNOWN`, and a **lean-file warning** when `constitution.md` or `repo-map.md` exceeds the ~150-line ceiling (wi-directory.md) — both are held in the orchestrator's context for entire runs, so overweight there is paid every turn."
- [ ] **Step 3: Refresh lean check (#37).** In `--refresh` §A after item 5, add:

    6. **Lean check:** `constitution.md` / `repo-map.md` grown past ~150 lines → flag it in the report
       with a suggested split or trim (the constitution is user-owned — suggest, never rewrite).

- [ ] **Step 4: Verify** — `python scripts/validate.py` exits 0; file tail intact.
- [ ] **Step 5: Commit** — `git commit -m "feat: scan — .logs/ gitignore guidance (#36), lean-file warnings (#37)"`

### Task 6: `dev/SKILL.md` + `research/SKILL.md` — budget citations (#37)

**Files:**
- Modify: `skills/dev/SKILL.md` (## Boundaries, ~line 116)
- Modify: `skills/research/SKILL.md` (## Operating principles, ~line 20)

- [ ] **Step 1: dev boundary bullet.** Add to ## Boundaries (after the first bullet):

    - **Context budget (workflow.md):** dev holds `repo-map.md`, `constitution.md`, and the feature's
      `progress.md`; resume detection reads each in-flight feature's `progress.md` — nothing else; the
      handoff preflight checks `brief.md` once. Bigger reads are delegated — the phase skills' subagents
      do the reading.

- [ ] **Step 2: research operating principle.** Insert a principle after "**State on disk.**…":

    - **Hold the budget.** workflow.md's **context budget** is a hard rule: `constitution.md`,
      `repo-map.md`, `progress.md`, plus the one active artifact (`brief.md` while researching;
      `spec.md`/`tasks.md` while planning). Researchers read sources and return short reports — never
      pull their material into this context. Re-entry (§0) reads `progress.md` + the active artifact,
      not prior-phase files.

- [ ] **Step 3: Verify** — `python scripts/validate.py` exits 0; both tails intact.
- [ ] **Step 4: Commit** — `git commit -m "feat: dev+research cite the context budget (#37)"`

### Task 7: `models.md` resolve-once rule + progress templates (#38 core)

**Files:**
- Modify: `references/models.md` (config-file intro ~30, first-run setup §, ## Dispatch rule §)
- Modify: `skills/research/references/wi-directory.md` (progress.md template, between the `- **Branch:**` bullet and `## Log`)
- Modify: `skills/rpa/references/rpa-directory.md` (run-level progress.md template, between `- **SDD ToC source:**`/`- **Worktree:**` bullets and `## Processes`) — **off-list, flag in PR body**

**Interfaces:**
- Produces: the block format below. Cell names are load-bearing — Task 8's dispatch points read `checker`, `researcher`, `task-runner`, `rpa-build`, the `cross-provider` row's `(at-finish | per-wave)` token, and the `MoA` row's `points`. Use these exact names everywhere.

- [ ] **Step 1: wi-directory progress.md template.** Insert into the template, after the `- **Branch:** <branch or "-">` line, before `## Log`:

    ## Model routing (resolved)
    <!-- written when progress.md is seeded (dev step 1-2 / rpa step 2) from .wi/models.md; dispatches
         read THIS block, not models.md. Rewrite only when absent or .wi/models.md changed after the
         stamp (models.md's resolve-once rule). Keep the stamp mid-line — Log-span parsing keys on
         stamps that OPEN a line. -->
    - resolved <ISO-8601 stamp> from .wi/models.md (preset: <smart | simple | custom | none — all inherit>)
    - orchestrator=<tier> (informational) · checker=<tier> · researcher=<tier> · task-runner=<tier> · rpa-build=<tier>
    - cross-provider=<none | provider model (at-finish | per-wave)> · MoA=<none | points=<…>; proposers=<…>; layers=<n>; aggregator=<tier>>

- [ ] **Step 2: rpa-directory run-level template.** Insert the same three `- ` lines (with the same one-line comment pointing at models.md's resolve-once rule) as a `## Model routing (resolved)` section after the header bullets, before `## Processes`.
- [ ] **Step 3: models.md config-file intro.** Change "Project-level, persisted, read at every dispatch point." to "Project-level, persisted, resolved **once per run** at the entry skills (the resolve-once rule below); dispatches read the resolved block in `progress.md`, not this file."
- [ ] **Step 4: models.md first-run setup.** At the end of the "## First-run setup" section, append: "Setup ends by resolving the routing once and recording it as the `## Model routing (resolved)` block when the feature's `progress.md` is seeded (dev step 2 / rpa's run seed) — the resolve-once rule below."
- [ ] **Step 5: models.md Dispatch rule rewrite.** Retitle the section "## Dispatch rule (build, research, ship, rpa) — resolve once, dispatch many" and replace its body with:

    **Resolve at entry.** At dev step 1 / rpa step 2 — or at the first dispatch that finds no block
    (legacy features, pre-1.7 runs) — resolve every dispatch kind **once**: per-agent override → the
    agent's own role → `inherit` (`wi-code-checker` reads the `wi-code-checker` role, `wi-researcher`
    reads `wi-researcher`, `wi-task-runner` reads `wi-task-runner`; RPA build delegations resolve
    `rpa-build` override → `wi-task-runner` role → `inherit` — `rpa-build` is a **role label** for those
    delegations, not a registered agent; there is no `agents/rpa-build.md`). Record the result as the
    `## Model routing (resolved)` block in the feature's `progress.md` (template: wi-directory.md),
    stamped, with the cross-provider and MoA rows carried compactly. The block caches the **configured**
    tiers, never the live session model (the no-auto-escalation rule above); resolving once changes
    cost, never behavior — same `.wi/models.md`, same assignments.

    **Dispatch reads the block.** At every wi Agent dispatch, read the tier from the resolved block and
    pass it as the dispatch's model parameter — do **not** re-open this reference or `.wi/models.md`.
    Re-resolve (rewrite the block) only when the block is **absent** or `.wi/models.md` **changed after
    the block's stamp** (its last commit — `git log -1 --format=%cI -- .wi/models.md` — or mtime, newer
    than the stamp). No `.wi/models.md` at all → everything inherits; record
    `preset: none — all inherit` so later dispatches don't re-check. **Exception — MoA dispatches:** a
    dispatch carrying an `MoA role:` marker resolves from the block's MoA row — each proposer at its
    listed `proposers` tier, the aggregator at the `aggregator` tier
    (`${CLAUDE_PLUGIN_ROOT}/references/moa.md`). **Fallback (unchanged):** a configured model that
    errors as unavailable at dispatch time → re-dispatch with `inherit` and note it in `progress.md` —
    the block itself stands; the config didn't change. Never stall a run on a model assignment.

- [ ] **Step 6: Verify** — `python scripts/validate.py` exits 0 (checks the template blocks still open with frontmatter `type`); `python -m unittest discover -s tests -q` green (`test_models_config.py`, `test_timing_report.py` must not regress); all three tails intact.
- [ ] **Step 7: Commit** — `git commit -m "feat: resolve model routing once per run — models.md rule + progress.md block (#38)"`

### Task 8: dispatch points read the block (#38)

**Files:**
- Modify: `skills/dev/SKILL.md` (step 1, ~line 35)
- Modify: `skills/research/SKILL.md` (§1c ~62, §1 MoA gating ~71 and its closing "No section…" line ~82)
- Modify: `skills/build/SKILL.md` (§2.2 Model per dispatch, ~54)
- Modify: `skills/ship/SKILL.md` (§2 checker ~56, §2 MoA gating ~59, §2 cross-provider gating ~76)
- Modify: `skills/rpa/SKILL.md` (step 2, ~44)
- Modify: `skills/rpa/references/verification-gate.md` (MoA gating ~92) — **off-list, flag in PR body**

**Interfaces:**
- Consumes: the block cells from Task 7 (`checker`, `researcher`, `task-runner`, `rpa-build`, cross-provider `(at-finish | per-wave)`, MoA `points`) and the phrase "resolve-once rule".

- [ ] **Step 1: dev step 1.** After "…Never re-ask an existing config." append:

    Finish by resolving the routing once (override → role → `inherit` per dispatch kind — models.md's
    **resolve-once rule**); step 2 records it as the `## Model routing (resolved)` block when
    `progress.md` is seeded, and a resumed feature missing the block gets it written on re-entry. Every
    later dispatch reads the block, not `.wi/models.md`.

- [ ] **Step 2: research §1c.** Replace "When `.wi/models.md` exists, dispatch each researcher on its routed model (override → `wi-researcher` role → inherit; `${CLAUDE_PLUGIN_ROOT}/references/models.md`)." with "Dispatch each researcher on the `researcher` tier from `progress.md`'s resolved-routing block (absent, or `.wi/models.md` changed after its stamp → resolve once and rewrite the block; `${CLAUDE_PLUGIN_ROOT}/references/models.md`'s resolve-once rule)."
- [ ] **Step 3: research §1 MoA gating.** Change "When `.wi/models.md` has `## Mixture of Agents` with `points` including `research`:" to "When the resolved-routing block's MoA row includes `research` in its `points` (mirroring `.wi/models.md`'s `## Mixture of Agents` section):" and the branch's closing "No section, or `research` not in `points` → skip this branch entirely" to "MoA row `none`, or `research` not in its `points` → skip this branch entirely".
- [ ] **Step 4: build §2.2.** Replace the **Model per dispatch** sentence ("when `.wi/models.md` exists, resolve each runner's model as per-agent override → `wi-task-runner` role → `inherit` (…) and pass it on the dispatch; a model that errors as unavailable → re-dispatch on `inherit` and note it in `progress.md`. No config → inherit, as always.") with:

    **Model per dispatch (tiered model routing):** pass each runner the `task-runner` tier from
    `progress.md`'s `## Model routing (resolved)` block; block absent, or `.wi/models.md` changed after
    its stamp → resolve once now and rewrite the block
    (`${CLAUDE_PLUGIN_ROOT}/references/models.md`'s resolve-once rule). A model that errors as
    unavailable → re-dispatch on `inherit` and note it in `progress.md` (the block stands — the config
    didn't change). No config → inherit, as always.

- [ ] **Step 5: ship §2 ×3.** (a) Change "(on the `wi-code-checker` role's model when `.wi/models.md` exists, else inherit)" to "(on the `checker` tier from `progress.md`'s resolved-routing block — models.md's resolve-once rule — else inherit)". (b) Change "If `.wi/models.md` has a `## Mixture of Agents` section with `points` including `review` (see …moa.md)" to "If the resolved-routing block's MoA row includes `review` in its `points` (see …moa.md; the block mirrors `.wi/models.md`'s `## Mixture of Agents` section)". (c) Change "If `.wi/models.md`'s `## Cross-provider config` names a provider (≠ `none`) and its API key is present" to "If the resolved-routing block's cross-provider row names a provider (≠ `none`) and its API key is present" — the script invocation keeps `--config .wi/models.md` (the script parses the file itself; that costs no orchestrator context).
- [ ] **Step 6: rpa step 2.** Change "The config's `wi-task-runner` tier then rides every build delegation (override key `rpa-build` — a routing role label for those delegations, not a registered agent; there is no `agents/rpa-build.md`), and at ship…" to:

    Resolve the routing once now (models.md's **resolve-once rule**) and record it as the
    `## Model routing (resolved)` block when the run's `progress.md` is seeded (rpa-directory.md's
    template); every build delegation then reads the block's `rpa-build` cell (`rpa-build` resolves
    override → `wi-task-runner` role → `inherit` — a routing role label, not a registered agent; there
    is no `agents/rpa-build.md`), and at ship…

  (the rest of the sentence unchanged).
- [ ] **Step 7: rpa verification-gate MoA gating.** Change "when `.wi/models.md` has a `## Mixture of Agents` section whose `points` include `review`" to "when `progress.md`'s resolved-routing block's MoA row includes `review` in its `points` (mirroring `.wi/models.md`'s `## Mixture of Agents` section)".
- [ ] **Step 8: Verify** — `python scripts/validate.py` exits 0; all six tails intact; then the leftovers sweep:
  - `grep -rn "at every wi Agent dispatch" skills/ references/` → only models.md's rewritten "Dispatch reads the block" paragraph.
  - `grep -rni "when \`\.wi/models\.md\` exists" skills/` → zero dispatch-point hits (first-run-setup/legacy mentions elsewhere are fine).
  - `grep -rn "resolved-routing block\|Model routing (resolved)" skills/ references/` → dev, research (×2), build (×2 — §2.2 + per-wave from Task 3), ship (×3), rpa SKILL, rpa verification-gate, wi-directory, rpa-directory, models.md — nothing else.
- [ ] **Step 9: Commit** — `git commit -m "feat: dispatch points read the resolved-routing block (#38)"`

### Task 9: version bump + full gate

**Files:**
- Modify: `.claude-plugin/plugin.json` (`"version": "1.6.0"` → `"1.7.0"`)
- Modify: `.claude-plugin/marketplace.json` (`plugins[0].version` `"1.6.0"` → `"1.7.0"`; top-level `metadata.version` `0.1.0` untouched)
- Modify: `.codex-plugin/plugin.json` (`"version": "1.6.0"` → `"1.7.0"`)

- [ ] **Step 1:** Make the three edits.
- [ ] **Step 2: Full gate** — `python scripts/validate.py` exits 0 (includes the three-manifests-agree check) and `python -m unittest discover -s tests -q` all green (47 at plan time).
- [ ] **Step 3: Standalone-correctness read.** Re-read each touched file **alone**, asking the triage's test: does it still make correct decisions if loaded by itself? Specifically: build/ship/research/dev each name their reads and cite the two workflow.md rules by name; models.md alone fully defines resolve-once + staleness + fallback; wi-directory alone defines `.logs/` lifecycle end-to-end (create → self-gitignore → prune).
- [ ] **Step 4: Tail sweep** — `for f in $(git diff --name-only main); do tail -c 120 "$f"; done` (Git Bash) reading each tail as a complete sentence/line; no mid-sentence cuts.
- [ ] **Step 5: Commit** — `git commit -m "chore: bump to v1.7.0 (pile 1 — #36 #37 #38)"`

### Task 10: Checkpoint A dry-run + PR

- [ ] **Step 1: Dry-run (guardrail 3 / the issues' AC).** In a fresh session on a scratch repo (same harness as docs/plans/2026-07-03-dry-run-dev-rpa.md), run a small `/wi:dev --auto` feature end-to-end against the branch build and assert:
  - **#38:** with a fixed `.wi/models.md` (simple preset), every dispatch's model equals the pre-change resolution (checker=opus, researcher=sonnet, task-runner=sonnet) — read the block in `progress.md` + the dispatch log lines; the block was written once at seed, models.md not re-opened at dispatch points (no re-reads visible in the transcript).
  - **#36:** wave-gate + ship-gate outputs landed in `.wi/features/<slug>/.logs/`, `git status` never showed the dir (self-gitignore works), the dir is gone after ship's tidy, and every gate still fired (checker, validate-equivalents, tests) with verdicts logged.
  - **#37:** the transcript shows no re-Read of `spec.md`/`brief.md`/prior-phase artifacts on phase re-entry, and no orchestrator whole-file Read of project source (delegated instead); no "missing context" stall — the checker passes had their inputs.
  - **Measurement:** run `python skills/ship/scripts/token_report.py` on the dry-run session and compare orchestrator cache-write/read per turn against the pre-sweep baseline numbers recorded in the triage (evidence base: ~396K/turn on 0009-guardian-invite) and, more comparably, against a same-scratch-feature run on `main` if one is affordable — expect a lower per-turn context; record the numbers in the PR body.
- [ ] **Step 2: PR.** Push `pile1-context-budget`; open the PR titled `Pile 1: trim tool output, read discipline, resolve-once routing (#36 #37 #38) (v1.7.0)`. Body: the three issues' acceptance-criteria checklists ticked with evidence, the dry-run numbers, the two flagged off-list touches (verification-gate.md iron-law wording; rpa-directory template + rpa verification-gate MoA line) with one-line rationales, and `Closes #36`, `Closes #37`, `Closes #38`. **No AI attribution.** Squash-merge after review (repo convention).

## Self-review checklist (run after writing, before the PR)

- Every #36 AC maps: house rule → Task 1; build §2 + ship §1/§8 → Tasks 3–4; diff `--stat`+hunk → Tasks 1, 4; `.logs/` gitignored + pruned → Tasks 2, 5; dry-run delta → Task 10.
- Every #37 AC maps: each phase skill cites + names reads → Tasks 3 (build), 4 (ship), 6 (dev, research); re-entry rule → Tasks 1, 2, 6; delegated reads at dispatch points → Tasks 1, 3; scan warn → Task 5; dry-run → Task 10.
- Every #38 AC maps: resolved once at entry + recorded → Tasks 7, 8 (dev/rpa); dispatch points read the block → Task 8; fallback/no-re-ask unchanged + identical assignments → Tasks 7, 10; Dispatch rule section updated → Task 7.
- Cell-name consistency: `checker` / `researcher` / `task-runner` / `rpa-build` / `cross-provider …(at-finish | per-wave)` / `MoA … points=` — identical strings in wi-directory, rpa-directory, models.md, and all Task 8 call sites.
- No agent charter, no `.gitignore` of this repo, no script, no test file touched; `docs/plans/` addition is whitelisted.
