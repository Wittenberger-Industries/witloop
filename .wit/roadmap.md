---
type: Roadmap
title: pstack-derived feature candidates
description: Ranked backlog of pstack methods that fit Witloop, plus the pieces Witloop should not copy.
timestamp: 2026-08-25
tags: [pstack, roadmap, feature-candidates]
---

# Roadmap: pstack-derived feature candidates

This backlog compares pstack 0.14.3 with current Witloop and keeps only methods that close a real gap.

Standing fit rules: preserve brainstorm and the design gate; keep the four advertised commands unless
the owner chooses otherwise; keep host mechanics in adapters and state in committed `.wit/`; require no
MCP; keep one feature per PR; keep `wit-code-checker` as the single review-agent contract.

Horizons are recommendations, not approval to build. `docs/roadmap.md` remains the published GitHub
issue queue. Picking a row makes it `planned`; `/wit:dev` uses its slug and assigns the next ordinal.

| # | Candidate | Slug | Proposed form | Horizon | Status | Depends on |
|---|-----------|------|---------------|---------|--------|------------|
| 1 | Work-type routing: bug fix and investigation | `work-type-routing` | workflow + references | Now | candidate | - |
| 2 | Project-local verification map | `verification-map` | generated skill + project memory | Now | candidate | - |
| 3 | On-demand subsystem walkthrough | `understand` | delegated skill capability | Now | candidate | 1 |
| 4 | Blast-radius safety-fact proof | `blast-radius-proof` | ship evidence step | Now | candidate | - |
| 5 | GitHub-native PR babysitting | `github-pr-babysit` | hidden workflow | Next | candidate | - |
| 6 | Evidence-linked decision trail | `decision-trail` | feature memory | Next | candidate | - |
| 7 | Thin named-principle index | `principle-index` | reference | Next | candidate | - |
| 8 | Verification-map maintenance | `verification-map-maintenance` | maintenance skill | Later | candidate | 2 |
| 9 | Performance and runtime forensics | `runtime-forensics` | work-type references | Later | candidate | 1 |
| 10 | Detect-only `why` archaeology | `why-detect-only` | delegated skill capability | Later | candidate | 3 |

## Now

### 1. Work-type routing: bug fix and investigation

- **pstack source:** `skills/poteto-mode/playbooks/bug-fix.md` and `investigation.md`.
- **Witloop gap:** `skills/dev/SKILL.md` classifies feature-folder state, not the kind of work.
  `add-issues` files bugs but does not fix them. Debug delegation begins only after a phase fails.
- **Adopt:** route `feature | bug-fix | investigation` before the normal feature flow. A bug starts
  from a reproduced symptom, uses runtime hypotheses, and ships the smallest proven fix. A read-only
  investigation returns a cited walkthrough and stops without a PR. Keep the design gate for
  non-trivial behavior changes; any bypass needs an explicit product decision.
- **Why it fits:** bug fixes reuse the dossier, task-runner, checker, and ship machinery.
  Investigations add one explicit read-only exit instead of copying pstack's 22-playbook router.
- **Acceptance signal:** a bug request records failing-then-passing evidence on the same surface; a
  "how does X work?" request leaves product files and git state unchanged.

### 2. Project-local verification map

- **pstack source:** `skills/create-verification-skill/SKILL.md`.
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

- **pstack source:** `skills/how/SKILL.md`.
- **Witloop gap:** scan gives a coarse project map; researchers recommend an implementation approach.
  Neither produces a traced senior-onboarding explanation of an existing subsystem.
- **Adopt:** add an `understand` capability row to `integrations.md`. Prefer pstack `how` when present;
  otherwise use a small read-only explorer and explainer flow. Call it from investigations and
  repo-questions during research. Persist only a note needed by the active feature.
- **Risks:** keep critique panels opt-in, add no new named agent, and do not turn every repo-question
  into a four-agent fan-out.
- **Acceptance signal:** a subsystem question traces its real entry point and flow, names the files
  and gotchas, and makes no product edit.

### 4. Blast-radius safety-fact proof

- **pstack source:** `skills/blast-radius/SKILL.md`.
- **Witloop gap:** the checker proves acceptance criteria and reviews the diff. It does not require
  the one fact that makes a change safe to be exercised against real code.
- **Adopt:** during ship, state one safety fact and run one cheap proof. Record the command and result
  in `PR.md`, or mark the fact `unproven`. Docs-only changes may record `n/a` with a reason.
- **Why it fits:** this is a narrow extension of Witloop's "fresh command, or no PASS" rule, not a
  second review agent.
- **Acceptance signal:** each behavior PR names a safety fact and a reproducing command or an honest
  `unproven`; a convincing writeup alone cannot pass.

## Next

### 5. GitHub-native PR babysitting

- **pstack source:** `skills/poteto-mode/playbooks/babysit.md`.
- **Witloop gap:** ship watches the PR it creates, but there is no workflow for "check PR N", review
  threads, or flake-versus-stale-base triage on an existing PR.
- **Adopt:** a `gh`-based hidden workflow with `check`, `threads-only`, `background`, and `drive`
  modes. Order work as conflicts, threads, then CI. Never merge without an explicit request.
- **Acceptance signal:** "check PR N" reports GitHub's mergeability and blockers once, with no
  mutation; `threads-only` touches comments and nothing else.

### 6. Evidence-linked decision trail

- **pstack source:** `skills/show-me-your-work/SKILL.md`.
- **Witloop gap:** `progress.md` records phase state and decisions, but unattended forks and reversals
  may lack evidence pointers.
- **Adopt:** strengthen `progress.md` Decisions for `--auto` and keep-alive runs before adding a TSV.
  Record only forks, pivots, reverts, gates, and their evidence. Do not copy transcript scraping or
  pstack's mandatory second-model trail review.
- **Acceptance signal:** a reviewer can reconstruct an unattended run's meaningful choices without
  reading the chat transcript.

### 7. Thin named-principle index

- **pstack source:** `skills/principle-*/SKILL.md` and the Principles index in
  `skills/poteto-mode/SKILL.md`.
- **Witloop gap:** the constitution has the rules, but not a short vocabulary for methods such as
  "prove it works", "fix root causes", and "encode lessons in structure".
- **Adopt:** one on-demand `references/principles.md` with 6-8 names, triggers, and one rule each.
  Cite a principle only when it changed a decision. Do not create 21 always-loaded skills.
- **Acceptance signal:** a phase can point to one named method and the concrete choice it changed,
  while a default `/wit:dev` run does not load the index.

## Later

| Candidate | Steal this, not the wrapper | Why later |
|-----------|-----------------------------|-----------|
| Verification-map maintenance | `skills/maintain-verification-skill/SKILL.md`: source scan plus one live pass | Needs candidate 2 to prove useful first. |
| Performance and runtime forensics | `perf-issue.md`, `hillclimb.md`, `runtime-forensics.md`, `trace-forensics.md` | Add as work types only after candidate 1 settles routing. |
| Detect-only `why` archaeology | `skills/why/SKILL.md`: evidence-category search | Delegate when sources exist; never require every category. |

## Do not copy

| pstack piece | Why it does not fit Witloop |
|--------------|-----------------------------|
| Sticky `/poteto-mode` and all 22 playbooks | Replaces the four-command, two-gate state machine with a Cursor-sticky router. |
| `/architect` as the plan | Conflicts with `spec.md`, `tasks.md`, and the design gate. |
| Default arena, interrogate, or swarm panels | Duplicates optional MoA and build waves at a large token cost. |
| Twenty-one standalone principle skills | Reverses Witloop's always-loaded compression work; candidate 7 keeps the useful part. |
| Full seven-category `why` as a core dependency | Most categories need optional MCPs; candidate 10 is detect-only. |
| Graphite shipping, `watch-pr`, and autopilot playbooks | Vendor-specific and incompatible with one feature per PR and no autonomous merge. |
| Transcript recall | Cursor-path-specific; `progress.md` is Witloop's portable resume record. |
| `poteto-agent`, Comment Sicko, and TypeScript rules in core | Extra agent contracts or stack-specific policy; existing agents and target constitutions own these jobs. |
| Benny Slack automations | Useful but host-, tracker-, and Slack-specific; keep outside Witloop core. |

## Citations

1. pstack 0.14.3: `README.md`, `skills/poteto-mode/SKILL.md`, the named candidate sources, and `agents/`.
2. Witloop: `skills/dev/SKILL.md`, `skills/scan/SKILL.md`, `skills/ship/SKILL.md`,
   `skills/research/references/integrations.md`, `skills/research/references/wit-directory.md`,
   `agents/wit-code-checker.md`, `references/moa.md`, and `docs/roadmap.md`.
