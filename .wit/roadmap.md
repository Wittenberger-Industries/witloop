---
type: Roadmap
title: Feature candidates from pstack and D3
description: Combined ranked backlog of pstack and D3 methods that fit Witloop, the overlaps between those sources, and the pieces Witloop should not copy.
timestamp: 2026-08-27
tags: [pstack, d3, roadmap, feature-candidates]
---

# Roadmap: feature candidates

This backlog compares pstack 0.14.3 and the D3 pack in `docs/skill-ideas/` with current Witloop.
It keeps only methods that close a real gap. Earlier D3 harvests already in the loop (causal
learnings, the verification iron law, Reflection lines, glossary, `process:` close-out) are not
re-listed as candidates.

Standing fit rules: preserve brainstorm and the design gate; keep the four advertised commands unless
the owner chooses otherwise; keep host mechanics in adapters and state in committed `.wit/`; require no
MCP; keep one feature per PR; keep `wit-code-checker` as the single review-agent contract.

Horizons are recommendations, not approval to build. `docs/roadmap.md` remains the published GitHub
issue queue. Picking a row makes it `planned`; `/wit:dev` uses its slug and assigns the next ordinal.

## Overlaps

Hard merge (one row in the table below):

| Theme | pstack | D3 | Combined as |
|-------|--------|-----|-------------|
| Ship verification honesty | `blast-radius-proof`: one safety fact, command or `unproven` | `verify-verdict-bands`: every named check is PASS, unproven, or waived | `blast-radius-proof` (row 4). Same iron-law extension; D3 is the wider form. |

Related, not merged (separate rows, named so they do not get built twice):

| Theme | pstack | D3 | How they relate |
|-------|--------|-----|-----------------|
| How a subsystem works | `understand`: on-demand traced walkthrough | `subsystems-map`: durable per-directory conventions in scan | Same question, different lifetime. Row 3 owns the walkthrough. Scan-side notes stay in Later steal-this until a repo's FRs keep contradicting folder rules. |
| Detect-only, do not require every source | `why-detect-only`: how the system got this way | `prose-slop-detect`: AI writing tells in brief/spec/`PR.md` | Same constraint, different object. Two Later rows. |
| Work types after routing | `runtime-forensics` | `codeclean` | Both are new work types on top of row 1 (already done). Cleanup also borders investigation: read-first, mutate only after confirm. |
| Run honesty | `decision-trail`: forks and evidence in `progress.md` | `correct-course` (the event), `learnings-applied` (the plan), `process-audit` (independent replay) | Complementary. Correct-course produces a mid-build event; the trail records it; learnings-applied proves lessons changed tasks; the audit re-derives process from git, not chat. |

Do-not-copy collisions (same reject, both sources):

- Extra review fan-out: pstack arena/swarm vs D3 four-agent critique loops.
- Autonomous merge: Graphite / autopilot playbooks vs D3 weekly-notes auto-merge.
- Host-sticky routers: `/poteto-mode` vs twelve Done/Next/Confirm phases and `openai.yaml`.
- Always-loaded method dumps: 21 principle skills vs `SYNTHESIS.md` and the STE linter.

Not an overlap of candidates: pstack PR babysitting vs D3 "never poll CI". Keep babysitting (check once). D3's no-poll / no-auto-merge stays in Do not copy.

| # | Candidate | Slug | Source | Proposed form | Horizon | Status | Depends on |
|---|-----------|------|--------|---------------|---------|--------|------------|
| 1 | Work-type routing: bug fix and investigation | `work-type-routing` | pstack | workflow + references | Now | done | - |
| 2 | Project-local verification map | `verification-map` | pstack | generated skill + project memory | Now | candidate | - |
| 3 | On-demand subsystem walkthrough | `understand` | pstack | delegated skill capability | Now | candidate | 1 |
| 4 | Unproven-never-PASS (safety fact + waived) | `blast-radius-proof` | both | ship evidence step | Now | in-progress | - |
| 5 | Halt-and-diff when the plan is wrong | `correct-course` | D3 | build + design-gate procedure | Now | candidate | - |
| 6 | Hindsight lens in plan-mode checker | `hindsight-lens` | D3 | checker plan-mode question | Next | candidate | 5 |
| 7 | GitHub-native PR babysitting | `github-pr-babysit` | pstack | hidden workflow | Next | candidate | - |
| 8 | Evidence-linked decision trail | `decision-trail` | pstack | feature memory | Next | candidate | 5 |
| 9 | Learnings Applied in the plan | `learnings-applied` | D3 | plan section + checker row | Next | candidate | - |
| 10 | Thin named-principle index | `principle-index` | pstack | reference | Next | candidate | - |
| 11 | Self-contained task packets | `task-dev-notes` | D3 | `tasks.md` fields | Next | candidate | - |
| 12 | Safe dependency updates | `deps-update` | D3 | hidden workflow | Next | candidate | - |
| 13 | Verification-map maintenance | `verification-map-maintenance` | pstack | maintenance skill | Later | candidate | 2 |
| 14 | Performance and runtime forensics | `runtime-forensics` | pstack | work-type references | Later | candidate | 1 |
| 15 | Detect-only `why` archaeology | `why-detect-only` | pstack | delegated skill capability | Later | candidate | 3 |
| 16 | Metrics-driven cleanup work type | `codeclean` | D3 | work-type references | Later | candidate | 1 |
| 17 | Detect-only prose check | `prose-slop-detect` | D3 | optional ship/plan pass | Later | candidate | - |
| 18 | Independent process audit | `process-audit` | D3 | ship close-out dispatch | Later | candidate | 5, 8 |

## Now

### 1. Work-type routing: bug fix and investigation

- **Source:** pstack `skills/poteto-mode/playbooks/bug-fix.md` and `investigation.md`.
- **Status:** done (Witloop 1.15.0).
- **Why it stays on the list:** rows 3, 14, and 16 depend on it.

### 2. Project-local verification map

- **Source:** pstack `skills/create-verification-skill/SKILL.md`.
- **Witloop gap:** `repo-map.md` records test and run commands, and ship runs them, but neither records
  how an agent launches, drives, observes, and cleans up the real user path.
- **Adopt:** define a host-neutral format, extend `wit-directory.md`, then generate a project
  verification skill and 3-5 item user-feature map as project-level `.wit/` memory. Reuse pstack's
  interview and proof method. Its Cursor generator may sit behind the Cursor adapter, never as the
  cross-host source of truth.
- **Risks:** never publish an unexecuted cookbook, disturb a shared app instance, or assume
  Cursor-only `control-ui` / `control-cli`.
- **Acceptance signal:** the generated instructions launch the app, pass a doctor check, drive one
  mapped feature, retain evidence after cleanup, and can be called from ship.

### 3. On-demand subsystem walkthrough

- **Source:** pstack `skills/how/SKILL.md`. Related D3 piece: `subsystems.md` (durable per-directory
  conventions). Not merged; see Overlaps.
- **Witloop gap:** scan gives a coarse project map; researchers recommend an implementation approach.
  Neither produces a traced senior-onboarding explanation of an existing subsystem.
- **Adopt:** add an `understand` capability row to `integrations.md`. Prefer pstack `how` when present;
  otherwise use a small read-only explorer and explainer flow. Call it from investigations and
  repo-questions during research. Persist only a note needed by the active feature. If that note is a
  folder convention that would change an FR, ship can fold it into `repo-map.md` or `overview.md`
  rather than inventing `.wit/subsystems.md` on day one.
- **Risks:** keep critique panels opt-in, add no new named agent, and do not turn every repo-question
  into a four-agent fan-out.
- **Acceptance signal:** a subsystem question traces its real entry point and flow, names the files
  and gotchas, and makes no product edit.

### 4. Unproven-never-PASS (safety fact + waived)

- **Status:** in-progress as `0003-blast-radius-proof` (1.16.x).
- **Source:** pstack `skills/blast-radius/SKILL.md` plus D3 `d3-dev/phase-09-verify.md` Gate Verdict.
  Hard merge; see Overlaps.
- **Witloop gap:** the checker proves acceptance criteria and reviews the diff. It does not require
  the one fact that makes a change safe to be exercised against real code. An unmeasured target (no
  perf budget, no visual check, no safety fact) can still look green because it was never a row.
  User-accepted red is informal (`remote checks: red - accepted by user`).
- **Adopt:** during ship, every acceptance criterion and every named gate check is PASS, unproven, or
  waived. At minimum, state one safety fact and run one cheap proof (pstack's form). Unproven is
  never silent PASS. A waived FAIL needs a written reason, the user's approval, and a copy in
  `PR.md`. Docs-only changes may record `n/a` with a reason. Keep checker severity as BLOCKER /
  WARNING / INFO; map unproven to WARNING and waived-fail to a recorded INFO with the reason. Do not
  invent a fourth public verdict vocabulary, and do not ship this as two gates.
- **Why it fits:** this is a narrow extension of Witloop's "fresh command, or no PASS" rule, not a
  second review agent.
- **Acceptance signal:** each behavior PR names a safety fact and a reproducing command or an honest
  `unproven`; a conscious skip is named in `PR.md` with a reason; a convincing writeup alone cannot
  pass.

### 5. Halt-and-diff when the plan is wrong

- **Source:** D3 `d3-dev/phase-08-implement.md` Correct-Course sub-procedure.
- **Witloop gap:** `skills/build/SKILL.md` already appends a missed in-scope task, routes out-of-scope
  work to the roadmap, and reopens the design gate for architecture or public-contract changes. A
  false plan assumption can still become "one more task" with no impact analysis and no proposed
  artifact diffs. That is silent deviation with extra checkboxes.
- **Adopt:** when a runner or the orchestrator finds the plan wrong, halt. Write one-line impact on
  each affected FR, spec section, and remaining task, plus exact "from / to" diffs for
  `spec.md` / `tasks.md` / `pitfalls.md`. If acceptance criteria or a locked decision change, reopen
  the existing design gate. If the change is in-scope plumbing, apply the diffs, stamp a Reflection,
  and resume. Do not require a GitHub issue comment.
- **Why it fits:** this is the missing shape for the routing Witloop already has. Rows 6, 8, and 18
  read the event it leaves behind.
- **Acceptance signal:** a plan-wrong moment leaves a recorded impact list and artifact diffs; the
  run does not keep coding on the old `tasks.md`.

## Next

### 6. Hindsight lens in plan-mode checker

- **Source:** D3 `d3-dev/phase-06-critique.md` Hindsight technique.
- **Witloop gap:** plan-mode checker already traces coverage, wiring, silent down-scope, and
  applicable learnings. It does not ask which gap in today's artifacts would force a mid-build
  correct-course.
- **Adopt:** one extra plan-mode question in `agents/wit-code-checker.md`: assume this spec caused a
  correct-course; name the most plausible failure and the artifact gap behind it, or state none.
  Same agent, same BLOCKER / WARNING / INFO taxonomy. Do not copy four parallel critique agents or
  a three-to-five-pass loop.
- **Depends on:** row 5, so the named event exists.
- **Acceptance signal:** a plan with a hidden "this task cannot be done as written" hole fails the
  gate before code; a clean plan can answer "none" in one line.

### 7. GitHub-native PR babysitting

- **Source:** pstack `skills/poteto-mode/playbooks/babysit.md`.
- **Witloop gap:** ship watches the PR it creates, but there is no workflow for "check PR N", review
  threads, or flake-versus-stale-base triage on an existing PR.
- **Adopt:** a `gh`-based hidden workflow with `check`, `threads-only`, `background`, and `drive`
  modes. Order work as conflicts, threads, then CI. Check once; do not poll in a loop. Never merge
  without an explicit request.
- **Acceptance signal:** "check PR N" reports GitHub's mergeability and blockers once, with no
  mutation; `threads-only` touches comments and nothing else.

### 8. Evidence-linked decision trail

- **Source:** pstack `skills/show-me-your-work/SKILL.md`.
- **Witloop gap:** `progress.md` records phase state and decisions, but unattended forks and reversals
  may lack evidence pointers. Correct-course (row 5) produces the richest of those events.
- **Adopt:** strengthen `progress.md` Decisions for `--auto` and keep-alive runs before adding a TSV.
  Record only forks, pivots, reverts, gates, correct-course diffs, and their evidence. Do not copy
  transcript scraping or pstack's mandatory second-model trail review.
- **Acceptance signal:** a reviewer can reconstruct an unattended run's meaningful choices without
  reading the chat transcript.

### 9. Learnings Applied in the plan

- **Source:** D3 `d3-dev/phase-04-plan.md` Step 0 and required `## Learnings Applied`.
- **Witloop gap:** research stamps `applicable learnings:`; the checker only warns when a plan hits a
  lesson's context and ignores it. `tasks.md` never has to show *how* a lesson changed a task. Easy
  to stamp and then plan as if the index were empty.
- **Adopt:** plan writes a short Learnings Applied section (quote each applicable hook and the task
  or pitfall that honors it, or `none`). Checker plan mode treats a missing section as BLOCKER when
  the stamp is not `none`. Keep recall via `.wit/learnings.md` hooks. Do not add a SYNTHESIS.md that
  every phase must load; scan `--refresh` already promotes and retires.
- **Acceptance signal:** a feature with a relevant index hook names the task that avoids the old
  failure; a feature with `none` still has the section.

### 10. Thin named-principle index

- **Source:** pstack `skills/principle-*/SKILL.md` and the Principles index in
  `skills/poteto-mode/SKILL.md`.
- **Witloop gap:** the constitution has the rules, but not a short vocabulary for methods such as
  "prove it works", "fix root causes", and "encode lessons in structure".
- **Adopt:** one on-demand `references/principles.md` with 6-8 names, triggers, and one rule each.
  Cite a principle only when it changed a decision. Do not create 21 always-loaded skills.
- **Acceptance signal:** a phase can point to one named method and the concrete choice it changed,
  while a default `/wit:dev` run does not load the index.

### 11. Self-contained task packets

- **Source:** D3 `d3-dev/phase-05-tasks.md` Dev Notes ("copy, don't reference").
- **Witloop gap:** plan already aims at a runner that can execute one task without rereading the
  world, but the template is Files / Do / Verify. Data shapes, constraints, and "no guidance found"
  holes live in spec or research notes the runner is not holding.
- **Adopt:** each task may carry a short Facts block: the 3-5 pasted details the runner needs, each
  with a `[Source: spec.md#…]` citation, or `No guidance found - resolved as: …`. Do not paste the
  whole spec. Do not require 2-5 minute task sizing.
- **Acceptance signal:** a task-runner given only `tasks.md` plus the named files can finish without
  opening `brief.md`.

### 12. Safe dependency updates

- **Source:** D3 `d3-deps/SKILL.md`.
- **Witloop gap:** no workflow for updating dependencies without a supply-chain surprise. Scan
  records the package manager; nothing uses it for a categorized, approvable update.
- **Adopt:** a hidden workflow (not a fifth advertised command). Read the manager from
  `repo-map.md`. Pins live in `.wit/deps-pins.md` (reason, unblock condition, pinned-since). Bucket
  candidates as SKIPPED / FIXES / FLAGGED / SAFE. HARD STOP on untracked high or critical
  advisories. Apply only approved buckets at exact versions; roll back the lockfile on install
  failure; run repo-map test/lint/build as the gate. Show major bumps as info only.
- **Risks:** do not hardcode npm. Dependabot is optional when `gh` works; the ecosystem audit command
  is enough to start. Never auto-merge.
- **Acceptance signal:** "update deps" presents buckets, applies only what was approved, and leaves
  the tree unchanged if tests fail.

## Later

| Candidate | Source | Steal this, not the wrapper | Why later |
|-----------|--------|-----------------------------|-----------|
| Verification-map maintenance | pstack | `skills/maintain-verification-skill/SKILL.md`: source scan plus one live pass | Needs row 2 to prove useful first. |
| Performance and runtime forensics | pstack | `perf-issue.md`, `hillclimb.md`, `runtime-forensics.md`, `trace-forensics.md` | Add as a work type after row 1 (done) has more than one extra type in use. |
| Detect-only `why` archaeology | pstack | `skills/why/SKILL.md`: evidence-category search | Delegate when sources exist; never require every category. Same detect-only rule as row 17, different object. |
| Metrics-driven cleanup work type | D3 | `d3-codeclean`: review-first; same-session leftover vs long-standing drift; coverage theater vs coverage-by-complexity; spec-ready briefs for behavior-changing items; running report on disk | Inference is cheap now that row 1 exists. Still needs a scoped, confirm-then-mutate path that does not turn every investigation into a rewrite. |
| Detect-only prose check | D3 | `d3-ai-check` plus `ai-patterns.md` Section 0: a match is a candidate, never a verdict; report candidates / confirmed failures / legitimate keeps; hollow-but-clean; contrast-based negation | Witloop already bans em dashes. A thin optional pass on brief/spec/`PR.md` is enough. Do not take the 11-dimension rubric, channel scores, or a rewrite skill. |
| Independent process audit | D3 | `d3-dev/phase-12-audit.md`: a fresh subagent re-derives PASS/FAIL from `git` / `gh` and the files on disk, not from the conversation | Ship close-out is still self-attested. `process:` clauses plus scan trending already catch repeated friction. Worth it after rows 5 and 8 exist so the audit has a mid-build event and a trail to look for. |
| Per-directory subsystem notes | D3 | `d3-dev` `subsystems.md`: conventions that change what an FR may assume | Cousin of row 3. `repo-map.md` Layout plus `overview.md` How it's organized already cover the tour. Add a scan section only after a repo shows FRs that contradicted a folder's real rules. |

## Do not copy

| Piece | Source | Why it does not fit Witloop |
|-------|--------|-----------------------------|
| Sticky `/poteto-mode` and all 22 playbooks | pstack | Replaces the four-command, two-gate state machine with a Cursor-sticky router. |
| `/architect` as the plan | pstack | Conflicts with `spec.md`, `tasks.md`, and the design gate. |
| Default arena, interrogate, or swarm panels | pstack | Duplicates optional MoA and build waves at a large token cost. Same reject as D3's four-agent critique. |
| Twenty-one standalone principle skills | pstack | Reverses Witloop's always-loaded compression work; row 10 keeps the useful part. |
| Full seven-category `why` as a core dependency | pstack | Most categories need optional MCPs; row 15 is detect-only. |
| Graphite shipping, `watch-pr`, and autopilot playbooks | pstack | Vendor-specific and incompatible with one feature per PR and no autonomous merge. |
| Transcript recall | pstack | Cursor-path-specific; `progress.md` is Witloop's portable resume record. |
| `poteto-agent`, Comment Sicko, and TypeScript rules in core | pstack | Extra agent contracts or stack-specific policy; existing agents and target constitutions own these jobs. |
| Benny Slack automations | pstack | Useful but host-, tracker-, and Slack-specific; keep outside Witloop core. |
| Twelve never-skippable phases and Done/Next/Confirm at every phase | D3 | Replaces brainstorm + design gate + hands-off with twelve user stops. Contradicts `--auto` and keep-alive. |
| `.specify/` memory and spec folders | D3 | `.wit/` is the committed store. |
| GitHub issue as a hard gate before implementation | D3 | `/wit:add-issues` is a separate command. One feature, one PR. If an issue already exists, `Closes #N` in `PR.md` is enough. |
| Three to five critique passes with four parallel subagents, severity trends, and `critique.md` | D3 | Token-heavy second review loop. Row 6 keeps the useful question inside `wit-code-checker`. |
| Zero autonomous phase advancement | D3 | Directly contradicts keep-alive and `--auto`. |
| Copilot review hard-stop and "never poll CI" | D3 | Ship already reports the PR and verifies remote checks once they conclude. Row 7 checks an existing PR once; it does not poll. |
| ASD-STE100 plus `scripts/ste_lint.py` as a mandatory artifact gate | D3 | Bans contractions, Latin abbreviations, and phrasal verbs; high false-positive cost. Compact reasoning and the em-dash rule already cover the useful part. |
| `SYNTHESIS.md` as an always-loaded working set | D3 | Learnings recall is the index plus hooks; scan `--refresh` promotes and retires. Row 9 wires enforcement without a second corpus. |
| `agents/openai.yaml` Copilot agent wrapper | D3 | Host-specific. Adapters own host mechanics. |
| `d3-releasenotes` weekly `/updates`, ISO-week auto-merge, D3-Dashboard paths | D3 | Vendor and product specific. No autonomous merge. Steal only: PR vs direct-commit de-dupe, and an ISO-week helper if a project later wants changelogs. |
| npm-only audit commands, Astro/PHP tool tables, `Store.php` locking notes | D3 | Stack samples from the origin repo. `repo-map.md` names the real tools. |
| `d3-content` rewrite, LinkedIn/Email/Slack channel scores | D3 | Marketing workflow. Row 17 is detect-only on engineering artifacts. |
| Compound as post-merge-only writes to `main` | D3 | Witloop harvests learnings before the PR so they ride the feature branch. |

## Citations

1. pstack 0.14.3: `README.md`, `skills/poteto-mode/SKILL.md`, the named candidate sources, and `agents/`.
2. D3 pack (2026-08 update): `docs/skill-ideas/d3-dev/` (skill, phases 1-12, `engineering-writing-style.md`,
   `scripts/ste_lint.py`, `agents/openai.yaml`), `docs/skill-ideas/d3-ai-check/` (`SKILL.md`,
   `references/ai-patterns.md`, `references/research.md`), `docs/skill-ideas/d3-deps/SKILL.md`,
   `docs/skill-ideas/d3-codeclean/SKILL.md`, `docs/skill-ideas/d3-releasenotes/` (`SKILL.md`,
   `scripts/week-window.mjs`).
3. Witloop: `skills/dev/SKILL.md`, `skills/build/SKILL.md`, `skills/plan/SKILL.md`,
   `skills/scan/SKILL.md`, `skills/ship/SKILL.md`, `skills/ship/references/verification-gate.md`,
   `skills/research/references/integrations.md`, `skills/research/references/wit-directory.md`,
   `agents/wit-code-checker.md`, `references/moa.md`, `.wit/learnings.md`, and `docs/roadmap.md`.
