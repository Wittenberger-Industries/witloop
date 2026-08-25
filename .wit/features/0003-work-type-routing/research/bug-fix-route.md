---
type: Research Note
title: "Bug-fix route: reuse phases, justified bypass, same-surface proof"
description: How a reproduce-first bug-fix flow overlays Witloop phases without a parallel playbook.
feature: 0003-work-type-routing
timestamp: 2026-08-25
valid_until: 2026-09-24
---

# Bug-fix route: reuse phases, justified bypass, same-surface proof

## Responsibility Map

Not a frontend/backend app. Every capability is **plugin workflow** (skills, on-demand references,
progress stamps, checker matrix, unit tests). No product application layer. Sibling charters own
classification (`classification-seam`) and the read-only investigation exit (`investigation-route`).
This note owns only the `bug-fix` execution path after Work type is already stamped.

## Question

How can a reproduce-first bug-fix flow reuse Witloop's existing phases, record a justified narrow-fix
design-gate bypass, and enforce failing-then-passing same-surface proof?

Mode: `[repo-question]`. Outward survey limited to the local pstack playbook named by the brief and
the already-installed Superpowers `systematic-debugging` skill. No new dependencies.

## Recommendation

**Phase overlay, one on-demand route file.** After Work type is `bug-fix`, `/wit:dev` still runs
brainstorm → research → plan → plan-mode checker → (design gate **or** recorded narrow-fix bypass) →
build → ship. Specialize brainstorm questions, add a systematic-debugging evidence step inside
research, keep plan + `wit-code-checker` plan mode mandatory, skip only the **human design-gate ask**
when a fail-closed predicate holds, and reuse TDD / worktree / result-mode checker / ship unchanged
except for same-surface stamps and PR evidence.

Put the procedure in `skills/dev/references/bug-fix-route.md`, loaded only when `progress.md` reads
`Work type: bug-fix`. Always-loaded skills get one-line dispatch points so each file still decides
correctly if loaded alone (constitution rule-text rule). Feature path with missing Work type stays
today's loop.

This is a **hard-to-reverse** public-contract change (phase machine, load-bearing stamps, checker
matrix). It needs an ADR.

## Why this wins

1. The brief requires a repro-focused brainstorm, a recorded narrow-fix skip, same-surface
   fail-then-pass, and unchanged feature behavior. A parallel playbook duplicates build/ship and
   fights "reuse existing phases." [VERIFIED: `.wit/features/0003-work-type-routing/brief.md`]
2. Build already refuses to start without `tasks.md` plus a recorded gate outcome.
   [VERIFIED: `skills/build/SKILL.md`] Skipping plan or the plan-mode checker would either break that
   precondition or weaken the gate the brief wants kept for non-narrow fixes.
3. RPA and `feature-folder-cases.md` already prove the overlay pattern: keep the skill thin, load a
   reference only when the classifier lands on the case. [VERIFIED: `skills/rpa/SKILL.md`;
   `references/feature-folder-cases.md`]
4. Timing parsers treat `design gate opened` and `design gate approved` / `design gate auto-approved`
   as span boundaries. A bypass that omits those phrases makes wall-clock `unavailable`.
   [VERIFIED: `skills/ship/scripts/_ledger.py`; `tests/test_timing_report.py`]

## Don't-Hand-Roll

| Problem | Don't build | Use instead | Why |
|---|---|---|---|
| Root-cause hunt | New named debug/review agent | `superpowers:systematic-debugging` at a new research delegation point; existing `debug (any phase)` fallback | integrations.md already maps debug; brief forbids a new review agent. [VERIFIED: `skills/research/references/integrations.md`; brief Constraints] |
| Scientific method | Copy pstack's 22-playbook router | One on-demand route reference | Roadmap: borrow reproduce-first, do not copy the sticky router. [VERIFIED: `.wit/roadmap.md`] |
| Fail-then-pass proof | New first-class `evidence.md` dossier file | Ephemeral `research/repro.md` + `.logs/repro-*.txt`; durable stamps in `progress.md`, ACs in `spec.md`, excerpts in `PR.md` | Seven-file dossier is the ship close-out contract. [VERIFIED: `skills/research/references/wit-directory.md`] |
| Two-commit red/green history | Separate failing-test task / commit | One-task TDD (red and green inside the same task) | plan:4 forbids a standalone failing-test task; parallel waves race it. [VERIFIED: `skills/plan/SKILL.md`] |
| Narrow skip vs `--auto` | Reuse `design gate auto-approved (--auto)` | Distinct `design gate bypassed (narrow-fix)` stamp plus a `## Gate bypass` block | `--auto` is user-chosen hands-off, not a narrowness proof. [VERIFIED: `skills/research/SKILL.md` research:3] |
| Same-surface enforcement | Trust PR prose | Identical `repro failed on <surface>` / `repro passed on <surface>` stamps; result-mode BLOCKER if missing or mismatched | Ship already maps every AC to a run check. [VERIFIED: `skills/ship/references/verification-gate.md`] |

## State of the Art (in this repo)

| Old way | Current / recommended way | When it changed / what is deprecated |
|---|---|---|
| Every `/wit:dev` is a feature | Work type selects feature / bug-fix / investigation before feature-folder classification | This feature. Missing Work type remains `feature`. [VERIFIED: `.wit/glossary.md`; brief] |
| Design gate "May skip when: never" | Never for `feature`. For `bug-fix` only after the conjunctive predicate and the audit stamp | workflow.md contract change; ADR. [VERIFIED: `references/workflow.md` Contracts table] |
| Debug only after a phase fails (build:3) | Bug-fix also delegates systematic-debugging **before** the fix, as research evidence | New initiator row; build:3 stays for task failures. [VERIFIED: `skills/research/references/integrations.md`; `skills/build/SKILL.md`] |
| Checker plan mode always feeds a human (or `--auto`) gate | Plan mode still always runs; human ask may be skipped only for a recorded narrow-fix | Checker still feeds the gate; it does not replace it. [VERIFIED: `agents/wit-code-checker.md`] |
| pstack ships failing-repro commit then fix commit | Witloop keeps red+green in one task; proof is logs + PR, not split history | Wit TDD/wave contract wins over pstack step 5. [VERIFIED: `skills/plan/SKILL.md`; CITED: local pstack `bug-fix.md` step 5] |

Checked local Superpowers `systematic-debugging@plugin-cache` and pstack `bug-fix.md` on 2026-08-25.
No registry package is added.

## Prior art (inward)

### Existing phase machine

`/wit:dev` is brainstorm (interactive, never skipped) → research (autonomous approach) → plan
(`spec.md` / `tasks.md` / `pitfalls.md`) → `wit-code-checker` plan mode → design gate → build
(worktree + `wit-task-runner` TDD) → ship (verification gate + checker result mode + PR).
[VERIFIED: `skills/dev/SKILL.md`; `references/workflow.md`]

Build precondition: a plan exists **and** the design gate passed (interactive approve or
`--auto`). [VERIFIED: `skills/build/SKILL.md`]

`progress.md` is the state machine. Phase values today: `brainstorm | research | plan | design-gate |
build | ship | done`. Template has `Gate mode`, `Flow`, Host cells; no Work type field yet.
[VERIFIED: `skills/research/references/wit-directory.md` progress.md template]

### Design-gate stamps are load-bearing

research:2 stamps `- <ts> **Update** design gate opened`. research:3 stamps
`design gate approved, phase = build` or `design gate auto-approved (--auto), phase = build`.
[VERIFIED: `skills/research/SKILL.md`]

`_ledger.parse_progress_spans` (mirrored in `token_report.py` and `grok_token_report.py`):

- span1 = first `design gate opened` − first `phase = research`
- span2 = last `PR opened` (else `phase = done`) − last `design gate approved` / `design gate auto-approved`
- missing boundary → `None`, never a guess

[VERIFIED: `skills/ship/scripts/_ledger.py`; `tests/test_timing_report.py`]

A bypass that skips `design gate opened` breaks span1. A bypass that skips both approval phrases
breaks span2. `test_auto_approved_variant_counts_as_gate_approval` shows the second phrase is an
allow-list, not a prefix match on "approved" alone. [VERIFIED: `tests/test_timing_report.py`]

### Overlay prior art

- RPA keeps `/wit:rpa` on the same two conversations, but brainstorm is a loaded
  `brainstorm-protocol.md` with extra must-asks. [VERIFIED: `skills/rpa/references/brainstorm-protocol.md`]
- `feature-folder-cases.md` is loaded only when classification is not "plain new feature."
  [VERIFIED: `references/feature-folder-cases.md`]
- Brief preference: "Keep the classifier and route entry points thin; put route-specific procedure
  in on-demand references." [VERIFIED: brief Approach preferences]

### Debug delegation already exists, but too late for a bug-fix route

integrations.md row `debug (any phase)` → `superpowers:systematic-debugging`, initiator "the failing
phase (e.g. build:3)", artifact `progress.md` log entry, fallback inline hypothesis-and-test.
Delegation is mandatory when the skill is present. [VERIFIED: `skills/research/references/integrations.md`]

Roadmap gap statement: "Debug delegation begins only after a phase fails."
[VERIFIED: `.wit/roadmap.md` candidate 1]

`systematic-debugging` iron law: no fixes without root-cause investigation first; reproduce
consistently before proposing a fix. [VERIFIED: Superpowers `systematic-debugging/SKILL.md` in Cursor
plugin cache, fetched 2026-08-25]

### TDD / checker / ship already match most of pstack's later steps

- Constitution: failing test first; tests in `tests/test_*.py`; `validate.py` + unit suite before ship.
  [VERIFIED: `.wit/constitution.md`]
- Task-runner: write the failing test, confirm it fails for the right reason, implement the minimum,
  run the exact Verify. [VERIFIED: `agents/wit-task-runner.md`]
- plan:4: red and green live inside one task; never a separate failing-test task.
  [VERIFIED: `skills/plan/SKILL.md`]
- Checker is the single review-agent contract; plan mode before the gate, result mode at ship; no
  second agent type. [VERIFIED: `agents/wit-code-checker.md`; brief Constraints]
- Ship PR.md already has Testing + Verification sections. [VERIFIED: `skills/ship/SKILL.md` ship:5]
- Verification iron law: no PASS without a command run this session, redirected per the output house
  rule. [VERIFIED: `skills/ship/references/verification-gate.md`]

### pstack bug-fix playbook (local, named by the brief)

pstack: orchestrator owns the task; reproduce on the matching surface; binary-search with runtime
evidence; smallest change the evidence justifies; verify on the same surface; failing-then-passing
output verbatim; TDD when the test is cheap; then open a PR. [CITED:
`/home/ubuntu/.cursor/plugins/cache/cursor-public/9717366/bdf7aa355337897f167153e05069aca505dae17c/skills/poteto-mode/playbooks/bug-fix.md`]

Map onto Witloop, do not copy the rest:

| pstack step | Witloop reuse |
|---|---|
| 1 Reproduce yourself | Repro-focused brainstorm + research evidence step; orchestrator drives the surface |
| 2 Binary-search cause | `systematic-debugging` (or inline fallback); optional `how`/`why` only if already installed; no new agents |
| 3 Plan the smallest fix | Existing plan skill; thin spec/tasks for a narrow fix |
| 4 Same-surface verify | Named surface in brief/spec; after-log; ship AC mapping |
| 5 Failing test then fix | Wit one-task TDD, not pstack's two-commit history |
| 6 Opening a PR | Existing ship |

pstack's `architect` fan-out and `/loop` are host-specific and out of scope. [CITED: same playbook
steps 2-3; VERIFIED: brief Out of scope]

## Compared shapes

### A. Phase overlay (recommended)

Same state machine. On-demand `bug-fix-route.md`. Brainstorm questions specialized. Research adds an
evidence step and a bypass predicate. Plan + plan-mode checker always run. Human gate skipped only
when the predicate holds. Build/ship reused.

- Complexity: low-medium (pointers + one reference + stamp/parser tests)
- Blast radius: workflow.md, research gate step, build precondition, progress template, checker
  matrix rows, timing parser allow-list
- Reversibility: low (stamps and "never skip" are public). ADR required
- Maintenance: one file owns the route; feature SKILL bodies stay thin
- Fit: matches brief, constitution Simplicity, overlay prior art, no new agent or dependency

### B. Parallel playbook (rejected)

A new `skills/bug-fix/` (or a pstack-shaped playbook) that reproduce → hypothesize → patch → PR
outside the phase machine.

- Rejected because build/ship/checker/TDD already exist; a fifth advertised path is out of scope;
  dossier and resume (`Phase` field) would fork; feature behavior is harder to keep unchanged.
  [VERIFIED: brief Scope & non-goals; `references/workflow.md`]

### C. Skip-to-build after brainstorm (rejected)

Write a one-pager and enter build for every bug-fix, skipping research fan-out, plan-mode checker,
and the gate.

- Rejected because build requires `tasks.md` and a gate outcome [VERIFIED: `skills/build/SKILL.md`];
  the brief keeps the gate for non-narrow fixes; skipping the checker replaces the human gate with
  nothing; root cause would be guessed in brainstorm, which brainstorm forbids ("Don't do the
  technical research or choose the approach here"). [VERIFIED: `skills/brainstorm/SKILL.md`]

`--auto` is not a substitute for shape A: it still runs research, plan, checker, and records a
full gate summary; it does not prove narrowness. [VERIFIED: `skills/research/SKILL.md` research:3]

## Prescribed overlay

### 1. Brainstorm specialization

Keep `brief.md` and the four must-asks. When Work type is `bug-fix`, the on-demand route **reinterprets**
them (RPA-style), it does not add a second conversation:

1. **Scope** : the symptom, the named surface, and explicit non-goals (no drive-by refactor, no
   extra work type).
2. **Behavior** : expected vs actual, with a concrete trigger. This is the WHAT of the bug, not the
   root cause.
3. **Acceptance** : "the original repro fails, then passes, on the same named surface"; name the
   root cause and the smallest justified fix in the eventual result (acceptance of the run, not a
   guessed HOW).
4. **Hard constraints** : compatibility, public-behavior freeze when the user wants a narrow fix,
   must-reuse.

Persist a `## Repro contract` section inside `brief.md` (not a new dossier type):

- **Surface:** exact command, test node, or UI path (the same string later phases reuse)
- **Trigger:** steps
- **Observed / expected**
- **Force strategy** if intermittent

Still delegate dialogue method to `superpowers:brainstorming` when present; wit still writes
`brief.md`. Stamp stays `brainstorm via superpowers:brainstorming | via wit fallback`, plus
`, dialogue` / `, self-answered (headless)`. [VERIFIED: `skills/brainstorm/SKILL.md` Step 0]

`--auto` still does not skip brainstorm. [VERIFIED: `skills/dev/SKILL.md`; `skills/brainstorm/SKILL.md`]

Feature brainstorm must-asks and `question-patterns.md` stay untouched when Work type is missing or
`feature`.

### 2. Systematic-debugging delegation (research evidence step)

Add a matrix initiator, not a new agent:

| wit phase | skill | initiator | artifact | fallback |
|---|---|---|---|---|
| debug (bug-fix evidence) | `superpowers:systematic-debugging` | research, after brief, before approach fan-out | `research/repro.md` + `.logs/repro-before.txt` + progress stamps | inline hypothesis-and-test (already documented) |

Keep the existing `debug (any phase)` row for build:3 task failures.

Rules:

- Orchestrator stays in the lead (pstack "You own this task"). [CITED: pstack `bug-fix.md` lead-in]
- Delegation is mandatory when the skill is present; stamp
  `debug via superpowers:systematic-debugging` or
  `debug via wit fallback (systematic-debugging absent)`. [VERIFIED: integrations.md]
- Reproduce on the **brief's Surface** before any fix. Force the trigger if needed. A bug that will
  not reproduce does not enter build; record a blocker. [CITED: pstack step 1]
- Binary-search with runtime evidence; the surviving mechanism is written to `research/repro.md`
  before plan. [CITED: pstack step 2; VERIFIED: Superpowers systematic-debugging Phase 1]
- Optional installed `how` / `why` skills may be used if present. Do not require them (roadmap
  candidates 3 and 10; this feature's non-goals). [VERIFIED: `.wit/roadmap.md`; brief Out]
- No `wit-debugger` agent. Checker remains the only review-agent contract.

Research fan-out after evidence: usually one `[repo-question]` leftover at most ("what is the
smallest justified fix given this mechanism"). Most narrow bugs need no tech-choice researcher.

### 3. Runtime evidence state and artifacts

Working (ephemeral; pruned at ship:6):

- `research/repro.md` : `type: Research Note`: hypotheses ruled out, surviving mechanism, commands
- `.logs/repro-before.txt` / `.logs/repro-after.txt` : redirected per the output house rule
  [VERIFIED: `references/workflow.md` output house rule; wit-directory.md ephemera list]

Durable (must exist after prune):

- `progress.md` Log, exact phrases, same `<surface>` string:

  `- <ts> **Update** repro failed on <surface>`
  `- <ts> **Update** repro passed on <surface>`

- `spec.md` acceptance criteria that name the surface, the fail-then-pass requirement, the root
  cause, and the smallest fix
- `PR.md` Testing: verbatim fail then pass excerpts (pstack reply contract, folded into the existing
  section). [CITED: pstack **Reply**; VERIFIED: `skills/ship/SKILL.md` PR template]

Do not add an eighth dossier file. After `done`, the folder remains the seven-file manifest.
[VERIFIED: wit-directory.md "After `done`"]

`.logs/` is already self-gitignored. That is correct: the **stamps and PR excerpts** are the
committed proof; the raw logs are the session working set. [VERIFIED: wit-directory.md ephemera]

### 4. Narrow-fix predicate (fail-closed)

Bypass the **human ask and gate-summary render** only. Still write spec/tasks/pitfalls, still run
plan-mode checker, still commit the dossier on main
(`docs(<slug>): feature dossier (design gate)`), still emit `design gate opened` so span1 closes.
[VERIFIED: research:2 stamp wording; wit-directory.md design-gate commit]

All of the following must be true. Any false → existing interactive or `--auto` gate. Missing field
→ false.

1. `Work type` is exactly `bug-fix` (never `feature`, never missing; missing means feature).
2. Root cause is recorded from runtime evidence: `repro failed on <surface>` exists and
   `research/repro.md` names the surviving mechanism.
3. **Public behavior unchanged:** no advertised command, skill contract, CLI flag, user-visible
   default, or published API/schema change.
4. **Architecture unchanged:** no new module, dependency, layer, or external service; nothing
   ADR-worthy. [VERIFIED: constitution "hard-to-reverse"; plan ADR rule]
5. Blast radius is the files `tasks.md` names; no silent extra surface.
6. Plan-mode checker has **no BLOCKER**. WARNINGs are allowed and must be copied into the bypass
   block. [VERIFIED: checker severity; research:2 leftover findings go to the gate]
7. The planned change is the smallest fix the evidence justifies (checker's existing over-build
   WARNING; a belt-and-suspenders extra is not a narrow fix). [CITED: pstack lead-in; VERIFIED:
   `agents/wit-code-checker.md` hunt over-build]

`--auto` is orthogonal. If the predicate holds, use the bypass stamp (justified skip), not
`design gate auto-approved (--auto)`. If it fails under `--auto`, keep today's auto-approve path.

If build later discovers an architectural need, revoke the bypass and re-open the design gate
(existing mid-run amend). [VERIFIED: `skills/dev/SKILL.md` Boundaries; `skills/build/SKILL.md` §3]

### 5. Audit stamp and progress block

After plan-mode checker, always:

`- <ts> **Update** design gate opened`

Then, if the predicate holds, **do not ask**. Write the structured block and:

`- <ts> **Update** design gate bypassed (narrow-fix): <one-line reason>, phase = build`

Extend `_ledger.parse_progress_spans` (and the copies in `token_report.py` /
`grok_token_report.py`) so span2's start allow-list is:

`design gate approved` | `design gate auto-approved` | `design gate bypassed`

Do not reuse `design gate auto-approved`. A substring of `approved` is not enough; tests pin the
allow-list. [VERIFIED: `_ledger.py`; `tests/test_timing_report.py`]

Structured block (progress.md, durable):

```markdown
## Gate bypass
- **Status:** narrow-fix
- **Public behavior unchanged:** yes
- **Architecture unchanged:** yes
- **Root cause:** <mechanism>
- **Why skip:** <one line>
- **Checker (plan mode):** PASS | N WARNINGs (<list>)
- **Surface:** <exact surface string>
```

Build precondition becomes: interactive/auto-approve stamp **or** (`Work type: bug-fix` **and**
`## Gate bypass` Status `narrow-fix` **and** a `design gate bypassed (narrow-fix)` log line).
Refuse otherwise; route back to research. Feature path never consults this block.

workflow.md Contracts table: design-gate "May skip when" changes from `never` to
`never for feature; bug-fix only when the narrow-fix predicate and audit stamp are recorded`.
Rule 2 ("Two gates, both deliberate") stays for feature; bug-fix names brainstorm as the scope
gate and either the design gate or the recorded bypass as the second control.

research:4 keep-alive re-print: treat bypass like `--auto` (no second paste). Persistence was
armed at the brainstorm handoff. [VERIFIED: `docs/design-notes/research.md` research:4]

### 6. TDD, build, ship, checker reuse

**Plan.** Always produce `spec.md` / `tasks.md` / `pitfalls.md`. Narrow plans are small (typically
1-3 tasks). First behavioral task's **Verify** is the brief's Surface (or a cheap automated stand-in
that **is** that surface). Red and green stay inside that task. [VERIFIED: `skills/plan/SKILL.md`]

**Build.** Worktree, waves, `wit-task-runner`, wave-end suite, build:3 debug delegation: unchanged.
The runner already confirms the test fails for the right reason before the fix.
[VERIFIED: `agents/wit-task-runner.md`] After the fix task, the orchestrator writes
`repro passed on <surface>` from a fresh run of the **same** command, redirected to
`.logs/repro-after.txt`. Wrong-surface or inconclusive is not a pass. [CITED: pstack step 4]

When a cheap local test exists, that test **is** the surface (constitution TDD). When a test would
be expensive, integration-heavy, or unclear, keep the original surface and add an automated
regression test when practical; if not practical, spec.md must say why. [VERIFIED: brief Acceptance;
CITED: pstack step 5]

Do not adopt pstack's "failing repro commit then fix commit." It contradicts plan:4 and the
sole-committer / wave-end model. [VERIFIED: `skills/plan/SKILL.md`; `skills/build/SKILL.md`]

**Ship.** Existing verification gate + result-mode `wit-code-checker` + PR.md + tidy. No new review
agent. [VERIFIED: brief Constraints]

**Checker (additive matrix rows, spec must name this charter tweak).** Constitution: do not change
report caps, output markers, or tool lists. Add coverage-matrix inputs when Work type is `bug-fix`:

| Item | Plan mode | Result mode | Severity if missing |
|---|---|---|---|
| Repro contract / named surface | task Verify names it | diff + logs use it | BLOCKER |
| Root cause recorded | spec / repro note | PR names it | BLOCKER |
| Same-surface fail-then-pass | tasks include the verify | both stamps + matching surface; after-run exists | BLOCKER |
| Regression test or "impractical" rationale | a task or an explicit out | test present or rationale still in spec/PR | BLOCKER if neither |
| Over-build / extra "might help" | existing over-build hunt | existing | WARNING |

`## CHECK PASSED` / `## ISSUES FOUND` unchanged. [VERIFIED: `agents/wit-code-checker.md` Output]

**PR evidence.** `PR.md` Summary names root cause + smallest fix. Testing pastes fail then pass
(same surface). Verification carries the result-mode matrix. [VERIFIED: ship:5 template; brief
Acceptance]

### 7. Backwards compatibility

- Missing `Work type` = `feature`. Feature must-asks, gate "never skip", `--auto`, RPA, add-issues
  unchanged.
- Seven-file dossier, agent report markers, keep-alive cells, host adapters unchanged.
- New optional `Work type:` and `## Gate bypass` in the progress template; existing features without
  them remain valid.
- Behavior change → minor bump, three manifests in lockstep. [VERIFIED: constitution Git & shipping]
- Rule-text PR: inventory every touched skill/reference; each file loaded alone still chooses
  feature-default unless Work type is `bug-fix`. [VERIFIED: constitution Git & shipping]
- `wit-code-checker` stays the only review agent; MoA still means multiple instances, not new types.
  [VERIFIED: `agents/wit-code-checker.md`; `references/moa.md`]

### 8. Tests (this repo's style)

No new runtime. Prefer stdlib unittests next to the existing stamp tests.

1. **`parse_progress_spans`:** a fixture with `design gate opened` + `design gate bypassed (narrow-fix)`
   yields the same span math as approve; missing `design gate opened` still yields `None` for span1;
   `--auto` fixture still passes. Extend `tests/test_timing_report.py` and the grok/finalize fixtures
   if they assert the allow-list. [VERIFIED: `tests/test_timing_report.py`]
2. **Predicate fail-closed:** a small helper (recommended) or a contract test that the route
   reference names all seven conjuncts and that a missing Work type / BLOCKER / public-behavior
   change forbids the bypass phrase. Helper validates the **audit record**, it does not classify
   the user's intent (sibling `classification-seam`).
3. **Template:** `test_capabilities.py`-style slice of the progress template asserts optional
   `Work type:` and that `Gate mode` / `Flow` still exist. [VERIFIED: `tests/test_capabilities.py`]
4. **Skill isolation:** feature-path strings in `skills/brainstorm/SKILL.md` and workflow.md still
   describe the two-gate feature loop when Work type is absent.
5. **Same-surface:** if a helper parses stamps, mismatched surface strings fail.

`python -m unittest discover -s tests` and `python scripts/validate.py` remain the ship gate.
[VERIFIED: `.wit/repo-map.md`]

A tiny `check_narrow_fix.py` (stdlib, like `check_tokens.py`) is justified if the orchestrator would
otherwise re-judge narrowness in prose. Ceiling: validate the block + stamps, exit 0/1. Upgrade path:
drop it if a later work type needs a general gate-policy module. [VERIFIED: constitution Simplicity
"mark a deliberate shortcut"]

## Files the plan should touch (this charter only)

- `skills/dev/references/bug-fix-route.md` (new, on-demand)
- Thin pointers: `skills/dev/SKILL.md`, `skills/brainstorm/SKILL.md`, `skills/research/SKILL.md`,
  `skills/build/SKILL.md`, `references/workflow.md`, `skills/research/references/wit-directory.md`,
  `skills/research/references/integrations.md`
- Stamp allow-list: `_ledger.py`, `token_report.py`, `grok_token_report.py` + timing tests
- Additive checker matrix rows in `agents/wit-code-checker.md` (spec-named; no marker/tool change)
- ADR for the gate-skip + stamp change
- Not this charter: classifier implementation, investigation exit, new agents, product app edits

## Dependency Legitimacy

None added. `systematic-debugging` and pstack `bug-fix` are optional installed skills / local
playbooks, not packages.

## Assumptions Log

| Claim | Why assumed | Load-bearing? |
|---|---|---|
| Sibling `classification-seam` stamps `Work type:` on `progress.md` before brainstorm | Required so this overlay can branch; not owned here | Yes |
| Investigation route creates no dossier, so it never hits this bypass | Sibling scope; brief | No (out of scope if false) |
| Optional `how` / `why` skills stay optional | Roadmap candidates 3 and 10; brief forbids required MCP/plugins | No |
| A stdlib bypass-record helper is wanted rather than prose-only | Testability; YAGNI if contract tests suffice | Yes (plan must pick) |
| Host adapters need no new cells for bug-fix | Capability table is host mechanics, not work type | No |

## Risks / unknowns

1. **Stamp allow-list drift.** `_ledger.py`, `token_report.py`, and `grok_token_report.py` each
   implement span parsing. A bypass phrase added in one copy and not the others makes one host's
   wall-clock `unavailable`. Plan: change all three and pin with tests.
   [VERIFIED: three parsers exist; `tests/test_timing_report.py` uses `token_report.parse_progress_spans`]
2. **Checker charter sensitivity.** Additive matrix rows are allowed only if the spec names them.
   Do not change `## CHECK PASSED`, tool lists, or modes. [VERIFIED: constitution Architecture]
3. **`--auto` vs bypass confusion.** Operators may treat `--auto` as "skip the gate because it is a
   small fix." Docs and stamps must stay distinct; tests must reject using the `--auto` phrase for a
   narrow-fix.
4. **False narrow-fix.** Predicate is self-scored by the orchestrator. Mitigation: fail-closed
   conjuncts, plan-mode BLOCKER veto, result-mode same-surface BLOCKER, mid-build reopen if the fix
   grows, optional `check_narrow_fix.py`.
5. **Surface that is not automatable.** Brief allows "when practical." Spec must record the
   impractical case; otherwise ship BLOCKER. [VERIFIED: brief Acceptance]
6. **workflow.md "never skip" readers.** Resume docs, README, and design-notes still say the gate
   never skips. Plan must update the contracts table and leave feature wording intact.
7. **Helper vs prose (assumption).** If the plan skips `check_narrow_fix.py`, contract tests on the
   reference text become the only mechanical lock.

## Citations

1. Local pstack playbook:
   `/home/ubuntu/.cursor/plugins/cache/cursor-public/9717366/bdf7aa355337897f167153e05069aca505dae17c/skills/poteto-mode/playbooks/bug-fix.md`
2. Superpowers systematic-debugging (Cursor cache, 2026-08-25):
   `/home/ubuntu/.cursor/plugins/cache/cursor-public/684/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/systematic-debugging/SKILL.md`
