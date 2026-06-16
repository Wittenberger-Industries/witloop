---
type: Design Spec
title: "wi:rpa — auto-publish a verified build to a connected tenant"
description: A gate-approved publish decision (none/feed/deploy) that, on an already-green build, packs and publishes the package(s) to the connected Orchestrator tenant at ship — best-effort, prod-guarded, hands-off-safe.
status: accepted
timestamp: 2026-06-16
tags: [rpa, publish, orchestrator, tenant, ship, design-gate]
---

# wi:rpa — auto-publish to a connected tenant

## Problem

`wi:rpa` builds a verified REFramework solution and stops at an **open PR**. Even when the operator is
logged into an Orchestrator tenant (`uip` authenticated, the org/tenant link already captured in
`orchestrator.md`), wi never pushes the built package anywhere — getting it into Orchestrator is a manual
follow-up. We want the loop to **also publish** the verified build to the connected tenant, without
weakening the "verified, reviewed, prod-safe" guarantees.

## Goals

- When the operator chose to at the **design gate** and `uip` is connected to a tenant, ship **also**
  publishes the built package(s) to that tenant — *in addition to* the PR, never instead of it.
- The decision (and how far it goes) is made **once, at the existing design gate** — so a hands-off
  `--auto` run carries it through with no extra prompt.
- Publishing is **prod-safe** (the constitution's "no production Orchestrator changes without approval"
  holds) and **best-effort** (a publish failure never fails an otherwise-shipped run).

## Non-goals

- **Feature B (Maestro paradigm)** — its own cycle (already on the README roadmap).
- **Provisioning queues/assets/triggers as part of publish** — that stays the existing "Orchestrator
  wire-up if in scope" via `uipath-platform`; publish here means the package, optionally deployed as a
  process.
- **Owning the `uip` publish/deploy mechanics** — those are delegated to `uipath-solution`; wi owns the
  decision, the guards, and the recording.
- **Auto-publishing on a red build or before review** — publish only ever runs on an already-green
  verification gate with the PR open.

## Design

### 1 · The gate decision (one new approval)

The rpa design gate — which already approves the build paradigm + Orchestrator provisioning — gains a
**publish decision**, recorded in `progress.md` beside `Build paradigm:` as `Publish:`:

- **`none`** (default) — build to PR only; no tenant push.
- **`feed`** — pack + publish the built package(s) to the connected tenant's package feed. The package is
  available in Orchestrator, but nothing runs.
- **`deploy`** — `feed`, **and** deploy + activate as a runnable **Process** in a named folder.

For `deploy`, the gate also captures the **target folder** (from `orchestrator.md`). **Hard guard:** a
**prod** folder must be explicitly approved at the gate — never the default, never auto-selected.

### 2 · Ship-time execution (new, after the green gate + PR)

At ship close-out — *after* the verification gate is green and the PR is open, so only a verified, reviewed
build is ever pushed — if `Publish: ≠ none`:

1. **Connection check first.** Confirm `uip` is authenticated to the tenant in `orchestrator.md`. If not
   connected → **skip**; record `publish approved but no tenant connection — run \`uip cloud login\`` in
   `progress.md`; surface it in the final report. This is **not** a run failure (the PR already shipped).
2. **Delegate to `uipath-solution`** for the actual `uip` calls: `pack` → `publish`; and for `deploy`,
   `deploy` → `activate` to the gate-approved folder. wi owns the decision + orchestration; the UiPath
   skill owns the CLI.
3. **Prod guard at execution too.** If the resolved target is a prod folder and the gate did not explicitly
   approve prod → skip + flag (defense in depth behind the gate guard).
4. **Best-effort.** A publish/deploy error is recorded with the **exact recovery `uip` command** in
   `progress.md` and reported — the verified PR remains the durable deliverable; the run is not failed.
5. **Record the outcome.** Published package name + version (+ folder for `deploy`) fold into
   `orchestrator.md` / the runtime-state-inventory (which already tracks "published package
   name/version" and "published-process names"), and the final run report gains a publish line.

### 3 · Constitution default & `--auto`

- `rpa-constitution-template.md` carries a `Publish:` **default (default `none`)** plus the prod-approval
  rule, so a project can opt in once instead of per run.
- **`--auto`** auto-approves the gate to the **constitution default** — so a hands-off run never silently
  pushes to a tenant unless the constitution explicitly opted in.

### 4 · Where it touches

- `skills/rpa/SKILL.md` — the design-gate step (add publish to the approve list) and the verify-&-ship step
  (the new post-PR publish action).
- `skills/rpa/references/rpa-constitution-template.md` — the `Publish:` default + prod-approval rule.
- `skills/rpa/references/rpa-directory.md` — add the `Publish:` field to the `progress.md` template
  (beside `Build paradigm:`).
- `skills/rpa/references/verification-gate.md` — note publish is a **post-gate** ship action, not part of
  the green gate.
- Delegation target: `uipath-solution` (`pack`/`publish`/`deploy`/`activate`).

## Acceptance criteria

1. The rpa design gate presents a **publish decision** (`none` | `feed` | `deploy`) and, for `deploy`, a
   target folder; the choice is recorded in `progress.md` as `Publish:`.
2. A **prod** folder for `deploy` requires explicit gate approval — it is never auto-selected and never the
   `--auto` default.
3. At ship, **after** the green verification gate and the open PR, when `Publish ≠ none`: wi checks the
   `uip` tenant connection and, if connected, delegates `pack` + `publish` (plus `deploy` + `activate` for
   `deploy`) to `uipath-solution`, targeting the approved feed/folder.
4. If publish was approved but `uip` is **not** connected → publish is skipped, a `uip cloud login`
   recovery hint is recorded in `progress.md` and surfaced in the report, and the run is **not** failed.
5. A publish/deploy **failure** is best-effort: the error + the exact recovery `uip` command are recorded
   in `progress.md` and reported; the run is not failed (the PR is the deliverable).
6. The publish outcome (package name + version, + folder for `deploy`) is recorded in
   `orchestrator.md` / the runtime-state-inventory and in the final run report.
7. `rpa-constitution-template.md` has a `Publish:` default (default `none`) + the prod-approval rule;
   `--auto` auto-approves to that default (so hands-off never pushes unless opted in).
8. The `progress.md` template (`rpa-directory.md`) has the `Publish:` field; `verification-gate.md` states
   publish is a post-gate ship action, not part of the green gate.
9. `python scripts/validate.py` passes; the plugin version is bumped across the three manifests and a
   README Roadmap bullet is added.

## Verification

This is prose + delegation wiring (like the numbered-goal-dirs feature) — **no new scripts or unit tests**.
Verify with `python scripts/validate.py` (manifests, frontmatter, `${CLAUDE_PLUGIN_ROOT}` resolution,
fence/newline balance) plus a read-back confirming the gate step, ship step, constitution, progress
template, and verification-gate doc all agree. A real tenant publish can't be unit-tested here; the design
relies on **gated + connection-checked + prod-guarded + best-effort + recorded** for safety.

## Rollout

Single PR. Bump the plugin version across the three manifests (e.g. `0.11.0` — a notable new capability;
maintainer's call) + a README Roadmap "shipped" bullet. Run `validate.py` and the file-tail check before
commit. No migration: existing rpa goals default to `Publish: none`, so behavior is unchanged until a
project opts in or the gate selects otherwise.
