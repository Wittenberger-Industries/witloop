---
type: Research Note
title: Capability table home and SKILL cite pattern
description: Where the host capability matrix lives, how always-loaded SKILL bodies cite it, and how the host probe stamps cells for later phases.
feature: 0001-cursor-capability-table
timestamp: 2026-08-19
valid_until: 2026-09-18
---

# Capability table home and SKILL cite pattern

**Question:** Where does the capability table live, and how do always-loaded SKILL bodies cite capabilities instead of host if-trees?

**Mode:** repo-question. Evidence is this repo. No web survey.

## Responsibility Map

Neither frontend nor backend: this is plugin Markdown + `scripts/validate.py`. Layers:

| Capability | Layer |
|---|---|
| Matrix (capability x host) + cite rule + host-probe contract | `references/capabilities.md` (new sibling of `workflow.md`) |
| Phase contracts (unchanged job) | `references/workflow.md` (one named-rule pointer) |
| Keep-alive *templates* keyed by `keep_alive` cell | `references/keep-alive.md` (cursor-adapter rekeys; this charter only cites it) |
| Per-host procedure that *fills* a column | `references/{claude-default,codex,copilot,grok,cursor}-tools.md` |
| Stamp `Host:` + `Plugin root (resolved):` + capability cells | `skills/{dev,rpa}/SKILL.md` at feature seed; scan resolves in-session only |
| Read stamped cells, one pointer, no product-name forks | always-loaded SKILL bodies: `skills/{dev,research,plan,build,ship}/SKILL.md` |
| Template fields for the stamp | `skills/research/references/wit-directory.md` `progress.md` template |
| Portability gate | `scripts/validate.py` (file list + retarget body-string checks) |

Token parsers, Cursor adapter cells, POSIX helpers: out of scope (siblings).

## Recommendation (one approach)

Put the matrix in a **new sibling** `references/capabilities.md`. Keep `workflow.md` as phase contracts. Always-loaded SKILL bodies get **one named-rule pointer** and then read **stamped cells** in `progress.md`. Adapters fill columns. Do not add `if cursor` / `if grok` forks to those SKILL bodies. Do not put the matrix inside `workflow.md` (lean-file and concern split). Do not put it in `keep-alive.md` (one capability's templates). Do not put it in `AGENTS.md` (bootstrap, Claude-absent only).

Hard-to-reverse: **yes**. Constitution already names "host capability table" as an ADR trigger. Record an ADR.

## How hosts are named today

Canonical product labels in bootstrap and adapters `[VERIFIED: AGENTS.md:4-24, README.md:85-98, references/{codex,copilot,grok}-tools.md]`:

| Stamp slug (to use) | Product label used in prose | Adapter file | In AGENTS.md / README table? |
|---|---|---|---|
| `claude` | Claude Code | (skills written in Claude names; no `claude-tools.md`) | yes |
| `codex` | Codex CLI | `references/codex-tools.md` | yes |
| `copilot` | GitHub Copilot CLI | `references/copilot-tools.md` | yes |
| `grok` | Grok Build | `references/grok-tools.md` | yes |
| `cursor` | Cursor | **missing** (`cursor-tools.md` does not exist) | **no** |

Slug `cursor` is already used as a progress stamp on this feature `[VERIFIED: .wit/features/0001-cursor-capability-table/progress.md:19]` and as a dry-run label `[VERIFIED: docs/plans/2026-07-19-learnings-lifecycle-dryrun.md:18]`. It is not a documented host `[VERIFIED: .wit/repo-map.md Unknowns, AGENTS.md:21-24]`.

`validate.py` portability list is exactly `references/{codex,copilot,grok}-tools.md` plus `AGENTS.md`. No `cursor-tools.md`, no capabilities file `[VERIFIED: scripts/validate.py:152-165]`.

`${CLAUDE_PLUGIN_ROOT}` is the wit plugin root on every host `[VERIFIED: AGENTS.md:26-29]`. Grok is the only adapter that makes **resolve-once into `progress.md`** a hard protocol `[VERIFIED: references/grok-tools.md:16-41]`.

## Count: host-name forks (always-loaded SKILL bodies vs references)

Always-loaded bodies = `skills/{dev,research,plan,build,ship}/SKILL.md` `[VERIFIED: brief "five always-loaded SKILL bodies"]`.

| File | Product-name forks in the body | What they do |
|---|---|---|
| `dev/SKILL.md` (120 lines) | **2 clusters** | Intro (dev:18) lists Claude/Codex `/goal`, Grok model-judged `/goal`, Copilot Autopilot. Step 4 (dev:75-79) repeats that list and points at three adapter files. `[VERIFIED: skills/dev/SKILL.md:17-18,57,75-79]` |
| `research/SKILL.md` (179 lines) | **2 clusters + 1 Claude tool name** | Intro `/goal` or Autopilot (research:16). Copilot per-skill install omit-version (research:44). Design gate `AskUserQuestion` (research:153). Step 4 reprints the same three-host keep-alive list (research:167-171). `[VERIFIED: skills/research/SKILL.md]` |
| `plan/SKILL.md` (136 lines) | **0** | No host names. `[VERIFIED: grep on skills/plan/SKILL.md]` |
| `build/SKILL.md` (115 lines) | **0 in the body** | Dispatch if-tree lives in the lazy reference. `[VERIFIED: skills/build/SKILL.md; skills/build/references/worktrees-and-subagents.md:78-87]` |
| `ship/SKILL.md` (438 lines) | **2 clusters** | ship:6 names `token_report.py` as Claude and `grok_token_report.py` as Grok, "non-Claude host runs the one its platform tool map names" `[VERIFIED: skills/ship/SKILL.md:277-282]`. ship:8 names Claude/Codex `/goal` or Copilot Autopilot `[VERIFIED: skills/ship/SKILL.md:430]`. Line 52 globs `~/.claude/plugins/**` as the superpowers reviewer path (Claude-default, not an if-tree). |

**Body total: four files carry host names; plan and build bodies are already cite-clean.** The keep-alive list is copy-pasted in **dev and research** (validate.py *requires* that: both files must contain `autopilot` and `grok`) `[VERIFIED: scripts/validate.py:160-165]`. That gate is why SKILL bodies still enumerate hosts instead of citing a table.

Host forks that belong in adapters / lazy refs (not this charter to rewrite, except as the table's consumers):

- `references/keep-alive.md` (70 lines): three host-named template branches `[VERIFIED: references/keep-alive.md:26-66]`.
- `references/{codex,copilot,grok}-tools.md`: entire files.
- `skills/scan/references/plugin-bootstrap.md`: Copilot/Codex/Grok alias section `[VERIFIED: plugin-bootstrap.md:34-49]`.
- `skills/build/references/worktrees-and-subagents.md:78-87`: Claude vs Copilot vs Codex vs Grok dispatch.
- `skills/research/references/wit-directory.md:236-258` and `skills/ship/scripts/_ledger.py:56`: Claude vs non-Claude finalizer (token-dispatcher sibling).
- `references/models.md:79-108`: `grok` column; "host is grok when the run follows grok-tools.md; otherwise claude" `[VERIFIED: references/models.md:98-100]`.
- `AGENTS.md` / README platform table: four hosts, no Cursor.

scan / brainstorm / rpa SKILL bodies: `AskUserQuestion` as the Claude tool name (scan:48,70; brainstorm:107). rpa body has **no** Grok/Copilot/keep-alive strings `[VERIFIED: grep]`. Those files are not the five always-loaded bodies; do not add Cursor prose there either: they should pick up the same pointer when they need `ask` / `keep_alive`.

No `if grok` / `if cursor` *code* exists. Forks are prose enumerations at point of use.

## Lean-file math: why not `workflow.md`

Lean-file rule: past ~150 lines a file is doing too much `[VERIFIED: skills/research/references/wit-directory.md:68-69]`. scan warns when `constitution.md` / `repo-map.md` exceed that ceiling because those two are *held* every turn `[VERIFIED: skills/scan/SKILL.md:79-80,107]`. `workflow.md` is a constitution hotspot `[VERIFIED: .wit/constitution.md:42]` and is cited by phase skills, so the same ceiling is the right budget even though it is cite-not-hold.

| File | Lines now | Headroom to 150 |
|---|---|---|
| `references/workflow.md` | **124** `[VERIFIED: wc]` | ~26 |
| `references/keep-alive.md` | 70 | ~80 |
| `AGENTS.md` | 47 | large, but wrong job |

A 7-capability x 5-host matrix + host-probe protocol + cite rule is ~40-80 lines (compact table ~18, probe ~20, legend ~15). Folding that into `workflow.md` lands ~165-200 lines and mixes **phase contracts** with **host matrix**. Each future host (constitution: Gemini / OpenCode / Factory Droid wait on a table *row*) adds a column; that growth must not live in the phase-machine hotspot.

`keep-alive.md` is the template source for **one** capability. Stuffing the whole matrix there would make every keep-alive print load plugin_root / tokens / ask. Wrong.

`AGENTS.md` is "If you are not Claude Code" bootstrap `[VERIFIED: AGENTS.md:18-24]`. The matrix includes Claude. Wrong home.

## Home: `references/capabilities.md`

New file, OKF `type: Reference`, listed in `validate.py`'s portability tuple next to the `*-tools.md` adapters (brief also requires `cursor-tools.md` on that list; adapter sibling owns creating it).

`workflow.md` gains a **named rule**, same shape as existing ones `[VERIFIED: references/workflow.md:92,118,124]`:

> Host behavior is **the capability table** (`${CLAUDE_PLUGIN_ROOT}/references/capabilities.md`). Entry skills stamp cells into `progress.md`; later phases read those cells and never re-guess the product. Adapters fill columns; skills do not.

That is ~3 lines. `workflow.md` stays under 150.

### Table shape (one matrix; adapters fill cells)

Columns: host slugs `claude | codex | copilot | grok | cursor`. Rows: glossary capabilities `[VERIFIED: .wit/glossary.md:10]`. Cells are **capability values**, not procedures. Procedure stays in the adapter. Cursor column is complete in this PR (adapter sibling); other columns are the existing hosts collapsed from today's forks.

| capability | claude | codex | copilot | grok | cursor |
|---|---|---|---|---|---|
| `plugin_root` | native `${CLAUDE_PLUGIN_ROOT}` `[VERIFIED: README.md:94]` | compat var `[VERIFIED: codex-tools.md:13-18]` | resolve install/clone `[VERIFIED: copilot-tools.md:13-27]` | resolve-once protocol `[VERIFIED: grok-tools.md:16-41]` | resolve even when env empty (cache or walk-up) `[VERIFIED: brief]`; procedure in `cursor-tools.md` |
| `subagent` | named Agent/Task `[VERIFIED: worktrees-and-subagents.md:84-85]` | inline `spawn_agent` `[VERIFIED: codex-tools.md:26-27,43-45]` | `task` / `/fleet` `[VERIFIED: copilot-tools.md:37-38]` | inline `spawn_subagent` `[VERIFIED: grok-tools.md:93-106]` | named `Task` `wit-*` when present, else inline `agents/*.md` `[VERIFIED: brief]` |
| `keep_alive` | `predicate_goal` `[VERIFIED: keep-alive.md:26-34]` | `predicate_goal` `[VERIFIED: keep-alive.md:26-34]` | `relaunch` `[VERIFIED: keep-alive.md:37-48]` | `model_judged_goal` `[VERIFIED: keep-alive.md:50-66]` | `none` `[VERIFIED: brief; .wit/glossary.md:16]` |
| `tokens` | `token_report.py` `[VERIFIED: ship/SKILL.md:277-278]` | unavailable (no per-task usage) `[VERIFIED: wit-directory.md:257-258]` | unavailable + optional `/usage` paste `[VERIFIED: copilot-tools.md:61-77]` | `grok_token_report.py` `[VERIFIED: grok-tools.md:148-150]` | `unavailable` orchestrator; Duration from `progress.md`; never `token_report.py` `[VERIFIED: brief]` |
| `ask` | `AskUserQuestion` `[VERIFIED: research/SKILL.md:153]` | (not in codex-tools table) `[ASSUMED]` | (not in copilot-tools table) `[ASSUMED]` | `ask_user_question` `[VERIFIED: grok-tools.md:87]` | Cursor `AskQuestion` `[VERIFIED: brief]` |
| `shell` | Bash + **python fallback** `[VERIFIED: workflow.md:120-124]` | `shell` `[VERIFIED: codex-tools.md:24]` | `bash` `[VERIFIED: copilot-tools.md:35]` | `run_terminal_command` `[VERIFIED: grok-tools.md:82]` | Python scripts; tiny helpers for POSIX side effects `[VERIFIED: brief]`; posix-helpers sibling |
| `skill_invoke` | session list + `~/.claude/plugins/installed_plugins.json` + `~/.agents/skills/` `[VERIFIED: integrations.md:19-26]` | native `$skill` / aliases `[VERIFIED: codex-tools.md:30]` | `/wit <skill>` + aliases `[VERIFIED: copilot-tools.md:41]` | session list **and** Claude registry before `(skill absent)` `[VERIFIED: grok-tools.md:47-53]` | search Cursor plugin cache before `(skill absent)` `[VERIFIED: brief]`; procedure in adapter |

`keep_alive` value set is already named in the brief: `predicate_goal | model_judged_goal | relaunch | none`. Other value enums (`named_or_inline`, parser ids) are locked in the spec; adapters must use the table's vocabulary, not invent synonyms.

### Don't-Hand-Roll

| Problem | Do not build | Use instead | Why |
|---|---|---|---|
| Fifth-host fork in SKILL.md | `if cursor` / `if grok` in always-loaded bodies | stamped cell + **the capability table** | Constitution: host procedure in adapters `[VERIFIED: .wit/constitution.md:30]`; brief: no Cursor prose in those bodies |
| Skills re-detect the harness each phase | sniff CLI / tool list mid-ship | `progress.md` `Host:` + capability block | Same resolve-once pattern as Model routing `[VERIFIED: skills/dev/SKILL.md:31-35]` |
| Keep-alive templates copied into skills | host lists in dev:4 / research:4 | `keep-alive.md` keyed by stamped `keep_alive` | Already "single source of the exact templates" `[VERIFIED: references/keep-alive.md:16-17]` |
| validate.py forcing host names into SKILL bodies | keep `if "grok" not in body` on `dev`/`research` | assert the table + `keep-alive.md` capability keys (and `cursor-tools.md` exists) | Today's gate *creates* the if-tree `[VERIFIED: scripts/validate.py:160-165]` |

### State of the Art (this repo)

| Old way (through v1.12 Grok) | Current way (this feature) | When it changed |
|---|---|---|
| Thin `*-tools.md` adapter + **product-name branches at point of use** (keep-alive.md three branches; ship:6 names Grok's parser; validate.py requires `grok`/`autopilot` in SKILL bodies) `[VERIFIED: docs/roadmap.md:125-129, scripts/validate.py:160-165]` | One capability x host matrix; adapters fill cells; skills read **stamped** cells | This PR. Grok #43 is the last "add a host = add a fork" ship. |

## Exact cite pattern (SKILL bodies)

Follow the named-rule pattern already used for context budget, ledger rule, and python fallback `[VERIFIED: references/workflow.md:92,118,124]`.

**The pointer (use this sentence, once per SKILL that needs a host behavior):**

```
Host behavior follows **the capability table** (`${CLAUDE_PLUGIN_ROOT}/references/capabilities.md`):
read the stamped cells in this feature's `progress.md`; do not branch on product names.
```

**At a point of use, name the cell, not the host:**

| Today's SKILL prose | Replace with |
|---|---|
| "print the keep-alive handoff for the current platform verbatim from keep-alive.md (`/goal` on Claude Code & Codex, Grok Build's model-judged `/goal`, Autopilot on Copilot)" `[VERIFIED: skills/dev/SKILL.md:75-79]` | "print the keep-alive handoff **verbatim from `${CLAUDE_PLUGIN_ROOT}/references/keep-alive.md`**, the template keyed by the stamped `keep_alive` cell (**the capability table**)." |
| "That is the Claude Code finalizer; a non-Claude host runs the one its platform tool map names (Grok Build: `grok_token_report.py`)" `[VERIFIED: skills/ship/SKILL.md:280-282]` | "Finalize tokens per the stamped `tokens` cell (**the capability table**)." Concrete dispatcher is the token-dispatcher sibling. |
| "ask with AskUserQuestion" `[VERIFIED: skills/research/SKILL.md:153]` | "ask with the stamped `ask` tool (**the capability table**)." |
| Intro lines that list Claude/Codex/Grok/Copilot keep-alive | Drop the product list. One clause: "kept alive by the stamped `keep_alive` capability (the **capability table**), if armed." |

Rules:

1. **One pointer per file**, plus cell names at the step that uses them. No second path to `cursor-tools.md` from always-loaded bodies.
2. **No Cursor-specific procedure** in those five files (no plugin-cache walk, no `AskQuestion` spelling, no `/loop`, no `token_report.py` skip). That is all adapter or stamped-cell meaning.
3. **No new `if cursor` / `if grok`.** Removing the existing host lists is in scope for the SKILL edits this feature must make so the pointer is the only host story. plan/build bodies already comply; touch them only if they gain a cell cite (build's dispatch stays in the lazy reference; that reference may read the stamped `subagent` cell, cursor-adapter).
4. **validate.py must stop requiring `grok` and `autopilot` inside `dev`/`research` SKILL.md.** Retarget: `references/capabilities.md` has a `cursor` column and a `keep_alive` row; `keep-alive.md` still has the Grok `update_goal` template *or* (after adapter rekey) a `model_judged_goal` template. Leaving the old body-string checks in place would fail the brief the moment host names leave the SKILL bodies `[VERIFIED: scripts/validate.py:160-165]`.

`${CLAUDE_PLUGIN_ROOT}` in the pointer stays. After the probe, the orchestrator substitutes the stamped absolute root the same way Grok already does `[VERIFIED: grok-tools.md:39-41]`.

## Host probe: who writes `Host:` and `Plugin root (resolved):`, who reads them

### Written today

| Field | Who writes it today | Template |
|---|---|---|
| `Plugin root (resolved): <abs>` | Grok protocol only: "start of any wit entry skill (scan / dev / rpa)", persist in `progress.md` because Grok shells do not keep `export` `[VERIFIED: references/grok-tools.md:23-27]` | **Not** in the `progress.md` template `[VERIFIED: wit-directory.md:137-185]` |
| `Host:` | **Nobody in skills.** This feature's `progress.md` already has `- **Host:** cursor` and `- **Plugin root (resolved):** D:\ClaudeCowork\wi-plugin\wi-plugin` `[VERIFIED: progress.md:19-20]`, which is the target shape, not the shipped template. |
| Model routing | `dev:1-2` / `rpa:2` seed `## Model routing (resolved)`; later dispatches read that block, not `.wit/models.md` `[VERIFIED: skills/dev/SKILL.md:31-35; wit-directory.md:161-168]` | In the template |
| Host detection for models | "host is `grok` when the run follows `grok-tools.md`; otherwise `claude`" `[VERIFIED: references/models.md:98-100]` | Re-guess; no `Host:` stamp |

Later phases **do not read** a Host block. They re-enumerate products at keep-alive print and token finalize `[VERIFIED: skills/dev/SKILL.md:75-79; skills/ship/SKILL.md:277-282]`.

### Write contract (this feature)

**When:** feature seed, same moment as Model routing: `dev:2` and `rpa:2`. That is when `progress.md` first exists.

**Who:** the entry skill (dev / rpa). Scan **resolves** plugin root in-session for its own `${CLAUDE_PLUGIN_ROOT}` script calls (check_mermaid, etc.) but **does not** invent a feature folder to persist `Host:`. A following `/wit:dev` re-runs the probe and stamps. Duplicate resolve is cheap; the stamp is canonical.

**Where in the file:** header bullets after `Flow:`, matching this feature's progress.md `[VERIFIED: progress.md:17-20]`. Plus a resolve-once block modeled on Model routing, so skills read **cells** without opening `capabilities.md` (context budget holds `progress.md`, not extra references `[VERIFIED: references/workflow.md:94-100]`).

Template addition for `wit-directory.md`:

```markdown
- **Host:** <claude | codex | copilot | grok | cursor>
- **Plugin root (resolved):** <abs>

## Capabilities (resolved)
<!-- written at seed from references/capabilities.md for Host:; later phases
     read THIS block, not the table and not the product name. -->
- resolved <ISO-8601 stamp> from references/capabilities.md (host: <slug>)
- plugin_root=<abs> · subagent=<cell> · keep_alive=<cell> · tokens=<cell> · ask=<cell> · shell=<cell> · skill_invoke=<cell>
```

`plugin_root` in the block is the same absolute path as the header bullet (header stays greppable; block is what skills branch on).

**Probe procedure** (lives in `capabilities.md`, not in SKILL bodies): detect the running harness once (session tools / env / AGENTS path; Cursor when `CLAUDE_PLUGIN_ROOT` is empty and Cursor cache or walk-up wins: adapter fills that detection). Look up the row. Stamp Host + root + cells. Never re-sniff in research/plan/build/ship.

**Read contract:** any later phase that needs a host behavior reads `progress.md`'s `## Capabilities (resolved)` (or the header `Host:` / `Plugin root (resolved):` if the block is missing: treat missing as a probe bug, re-run probe once, do not guess `claude`). Same staleness rule as Model routing: rewrite only when absent.

Scan/dev/rpa are the three names grok-tools already uses for "entry" `[VERIFIED: grok-tools.md:23]`. Keep that set.

## Alternatives considered

| Option | Verdict |
|---|---|
| **A. Matrix inside `workflow.md`** | Rejected. 124 + ~50 lines breaks ~150; hotspot merge contention; future host columns bloat the phase machine. Brief allowed a sibling *if* size would break lean-file: it would. |
| **B. Matrix inside `keep-alive.md`** | Rejected. That file is the template source for `keep_alive` only `[VERIFIED: keep-alive.md:7-17]`. |
| **C. Matrix inside `AGENTS.md`** | Rejected. Bootstrap for non-Claude; Claude is a column; always-loaded skills do not load AGENTS mid-phase. |
| **D. No matrix file; skills look up `*-tools.md` by stamped `Host:`** | Rejected. That is still a host if-tree (`if host == grok read grok-tools`). Brief: skills read **capabilities**, not product names. |
| **E. Stamp only `Host:`; skills keep the table in context** | Rejected. Context budget forbids holding `capabilities.md` `[VERIFIED: workflow.md:94-100]`. Resolve-once stamp matches models + plugin root. |
| **F. Sibling `references/capabilities.md` + workflow named rule + stamped cells** | **Winner.** Lean-file, fewest *loaded* bytes, adapters stay the procedure layer, SKILL bodies stay one pointer. |

Close call vs A if someone insists on fewest files: a 15-line *stub* table in `workflow.md` still fails the "complete Cursor row + four other hosts + probe protocol" size test, and the next host PR would split it anyway. Split now.

## Runtime State Inventory

Not a rename of a datastore key; it **adds** persisted keys. Sweep still required so plan grows covering tasks.

1. **Stored data:** feature `progress.md` header + new `## Capabilities (resolved)` block. Existing in-flight features (including this one) already have `Host:` / `Plugin root (resolved):` without the capability block `[VERIFIED: this feature progress.md:19-20]`. Migration: on re-entry, if `Host:` exists and the block is missing, fill the block from the table (one task). No DB, queues, or cache keys. `tokens.md` `_PENDING` prose names `token_report.py` / Grok (token-dispatcher sibling).
2. **Live service config outside git:** none verified (no CI env-var *names* keyed on host product). GitHub issue #89 is the product request, not runtime config.
3. **OS / platform-registered state:** installed plugin id remains `wit`; flat aliases `wit-*` under `~/.agents/skills/` `[VERIFIED: AGENTS.md:32-36]`. Not keyed on `Host:`. None to migrate.
4. **Secrets & env-var names:** `CLAUDE_PLUGIN_ROOT`, Grok `GROK_PLUGIN_ROOT` / `PLUGIN_ROOT` `[VERIFIED: grok-tools.md:28-31]`. Cursor may have no env var `[VERIFIED: brief]`. Do not rename these keys; the probe *reads* them. No secret-name change.
5. **Build / installed artifacts:** `scripts/validate.py` portability tuple and SKILL-body string checks `[VERIFIED: validate.py:152-165]`; README / AGENTS host lists; three plugin manifests (version bump, not a host key). Published marketplace package name stays `wit`.

## Assumptions Log

| Claim | Why assumed | Load-bearing? |
|---|---|---|
| Codex and Copilot `ask` cells equal some mapped tool (not listed in those adapters' tool tables) | `AskUserQuestion` is absent from `codex-tools.md` / `copilot-tools.md` tool grids this session | **Yes.** Spec must either mark those cells `unknown` until adapters document them, or record the mapped name after a spike. Do not invent. |
| Scan-without-progress.md must not create a feature folder just to stamp `Host:` | Brief's stamp example is a `/wit:dev` run; grok-tools names scan as an entry that resolves plugin root | **Yes.** Spec Open question if scan should write a project-level stamp. Recommendation: no. |
| Capability *value* enums beyond `keep_alive` (e.g. `named_or_inline` vs `named`/`inline`) | Brief names capabilities, not every enum | **Yes.** Spec locks the vocabulary so adapters and SKILL cites share strings. |
| Cursor detection tells (`AskQuestion` in the tool list, empty `CLAUDE_PLUGIN_ROOT`, Cursor cache path) | Brief states outcomes, not the sniff order | No for this charter (cursor-adapter). Probe contract only requires: detect once, stamp, never re-guess. |

## Risks / unknowns (plan must consume)

1. **validate.py SKILL-body `grok`/`autopilot` checks** will fail as soon as host lists leave `dev`/`research`. Retarget in the same PR or the gate stays red. Resolve: change the checks; pitfalls: "removed if-trees, left the validator requiring them."
2. **Codex/Copilot `ask` cells unverified.** Do not fill with guessed tool names. Spike or leave `unknown` in the table for those two hosts; Cursor row still ships complete.
3. **In-flight `progress.md` files** with `Host:` but no capability block (this feature). Re-entry must backfill, or ship:6 has nothing to read but `Host:` and will grow a host if-tree again.
4. **`workflow.md` named-rule pointer** must use a `${CLAUDE_PLUGIN_ROOT}/references/capabilities.md` path so validate.py's broken-ref check guards the new file `[VERIFIED: scripts/validate.py:137-150]`.
5. **keep-alive.md rekey** (predicate_goal / none / ...) is cursor-adapter scope; this charter only requires SKILL cites to key off the **stamped cell**. If keep-alive.md still uses host headings in this PR, the print step is "pick the section that matches the cell" (adapter documents the map). Pitfall: SKILL grows `if keep_alive == none` *and* `if cursor`.
6. **ship SKILL is already 438 lines** (far over lean-file). Cite edit must be a substitution, not a new section.
7. **models.md still says host is grok-or-claude** `[VERIFIED: references/models.md:98-100]`. Cursor column is cursor-adapter; table placement only requires the probe stamp be the source of host identity so models stop re-guessing. Coordinate so both do not invent parallel sniffers.

## Dependency Legitimacy

None added. Markdown reference plus validate.py path check. Verdict: n/a.

## Citations (repo)

1. `.wit/constitution.md:30,40,42` (adapters, ADR trigger, workflow hotspot)
2. `references/workflow.md:92,118,124` (named-rule cite pattern) and lean-file via `wit-directory.md:68-69`
3. `scripts/validate.py:152-165` (portability list + SKILL-body host-name gate)
4. `references/grok-tools.md:16-27` (resolve-once plugin root into `progress.md` at scan/dev/rpa)
5. `skills/dev/SKILL.md:75-79` and `skills/ship/SKILL.md:277-282` (the if-trees to replace)
6. `.wit/glossary.md:10-14` (capability table + host probe terms)
