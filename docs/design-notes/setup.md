---
type: Design Notes
title: "setup: design rationale (maintainer notes)"
description: The "why" behind setup/SKILL.md's rules; the runtime never reads this file; each entry is anchored to the section it explains.
timestamp: 2026-08-27
tags: [setup, design-notes, context-budget]
---

# setup: design rationale (maintainer notes)

`skills/setup/SKILL.md` is loaded wholesale at first-run, and two of its outputs (`constitution.md`,
`repo-map.md`) then sit in the orchestrator's context for entire later runs, so the skill carries
rules only. The rationale lives here, anchored by section. When editing the skill, keep this file
in sync: a rule whose "why" is deleted instead of relocated loses its guard against future
"simplification".

## Intro

- **Mission.** setup does the one-time groundwork so `/wit:dev` and `/wit:rpa` can run smoothly later;
  every later phase reads what setup wrote instead of re-deriving it. The output files are the
  contract; the procedure is just how they get filled. Scan is the cheap refresh, not this job.
- **Why missing `repo-map.md` is the empty-project path:** add-issues may already have created
  `.wit/issues/` (and thus a `.wit/` directory) without a map. A directory-only tell would skip
  first-run after a prior issue filing. The observable is **repo-map absent**.
- **Why `--auto` writes simple plus `ledger | on`:** hands-off new projects (dev/rpa forwarding
  `--auto`) must not stall on the models or ledger questions; simple is the non-interactive default
  and skip is never silent (keeping the ledger is the fail-closed path).

## setup:2 (existing repos; the greenfield guided setup)

- **Why config/lock files, not source wholesale:** the stack signal lives in manifests and lockfiles;
  wholesale source reading burns the orchestrator's context (workflow.md's context budget). The same
  budget is why a large repo is documented by a dispatched subagent that returns the filled-in
  templates instead of pulling the tree into the orchestrator.
- **Why the guided setup exists (instead of marking a greenfield repo UNKNOWN):** the point is to give
  later phases real ground truth. dev's handoff preflight arms the keep-alive condition from
  `repo-map.md`'s commands: `UNKNOWN - ask` blocks it, while a genuinely-absent tool recorded as
  `n/a - not configured` passes with that clause dropped (keep-alive.md's fill rule). An invented
  command would poison every later gate, which is why "don't invent it" is absolute.
- **Why one folded question round:** the greenfield questions merge into setup:4's constitution-confirm
  so the user answers once, not twice. Models and ledger are extra rounds after that; do not fold
  them into the constitution confirm.
- **Why the greenfield `.gitignore` names `.wit/features/*/.logs/` and `.wit/issues/`:** the former is
  wit's redirected command output (workflow.md's output house rule); the latter is add-issues'
  transient draft staging. Seeding both at first-run keeps the first build / first issue-filing from
  leaking caches, build artifacts, command logs, and drafts into `git status`.

## setup:5 (plugin bootstrap)

- **Why offer, don't force:** canonical in `plugin-bootstrap.md` (never install without asking; never
  block if the user declines). The plugins are an enhancement, not a requirement: wit's phase skills
  re-detect availability at run time and fall back gracefully, so a "skip now" is never fatal.

## setup:6 (models preset)

- **Why cite `models.md` "First-run setup" instead of copying preset tables:** the tables are
  canonical in that reference; restating them in the skill drifted twice historically (rpa design
  notes). Setup writes the project file; it does not seed `## Model routing (resolved)` because
  there is no feature `progress.md` yet.

## setup:7 (token ledger)

- **Why `## Token ledger` with key `ledger` in `.wit/models.md`:** project policy belongs next to
  the models preset, not in a new always-loaded PLUGIN_ROOT file and not in YAML next to `preset`
  (two stores). Spoken form is `ledger: on` / `ledger: skip`; the table cell `--auto` writes is
  `ledger | on`. Fail-closed: anything but exact `skip` is `on`, so old repos keep today's ledger.
- **Why no mid-run toggle:** a skip after `--init` would leave a PENDING `tokens.md` that ship still
  has to reason about; setup writes once.

## setup:8 (commit)

- **Why setup commits its own outputs:** wit-directory.md's project-level rule (committed where
  written). One `chore(wit): setup` covers docs plus models so later worktrees inherit both. The
  `.wi` rename stays its own commit when it happens.

## setup:9 (report; the lean-file warning)

- **Why the ~150-line ceiling is worth a warning line:** `constitution.md` and `repo-map.md` are held
  in the orchestrator's context for entire runs (workflow.md's context budget), so overweight there
  is paid on every turn. The ceiling itself is wit-directory.md's lean-file rule; setup only
  surfaces breaches.

## Templates & the mermaid section

- **Why the `n/a - not configured` reminder sits inside the template block:** the token is
  machine-read (dev's handoff preflight and keep-alive.md's fill rule grep for that exact string),
  and the reminder riding the template is what stops a first-run from paraphrasing it.
- **Why the reserved-word list stays in the skill:** those IDs are real parse failures; the list is
  short and operative, so it stays loaded.
- **Why "tight and skimmable" closes the skill:** these files are read at the top of every later
  phase, so bloat there is paid many times over; the canonical ceiling is wit-directory.md's
  lean-file rule.
