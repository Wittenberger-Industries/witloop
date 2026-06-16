---
type: Design Spec
title: "wi:rpa — Maestro flow as a first-class build framework"
description: Add a Framework choice (reframework | maestro) above the build paradigm, decided at brainstorm and confirmed at the gate, that makes the architecture, SDD, build, and verification framework-aware — REFramework unchanged, Maestro built/validated via uipath-maestro-flow.
status: accepted
timestamp: 2026-06-16
tags: [rpa, maestro, framework, paradigm, architecture, sdd, verification, "1.0.0"]
---

# wi:rpa — Maestro flow as a first-class framework

## Problem

`wi:rpa` builds REFramework solutions only. The build paradigm (`xaml-only | coded`) is a flat choice made
at the design gate — and that works because **both paradigms are REFramework variants**: same Dispatcher/
Performer architecture, same queue-based SDD, same Workflow-Analyzer gate; the paradigm only changes *how*
each workflow is authored. We want to also target **UiPath Maestro flows** (`.flow`), which are a different
*framework* entirely — orchestration flows of nodes (connector / approval / script / subflow / agent / ixp),
built, validated, and eval'd by the `uipath-maestro-flow` skill (`uip maestro flow`), with no state machine,
no queues, no `Config.xlsx`. Bolting "maestro" on as a third paradigm value would hand a Dispatcher/Performer/
queue-shaped SDD to a flow build — a poor fit. Maestro has to be **first-class**.

## Goals

- A first-class **Maestro flow** target alongside REFramework, selected per run.
- The **architecture, SDD, build delegation, and verification gate all become framework-aware**: REFramework
  is unchanged; the Maestro path is flow-shaped end to end.
- The framework is decided **early** (brainstorm proposes from the process shape; the gate confirms) because
  it reshapes the plan-phase artifacts — not at the post-plan gate like the paradigm.
- Reuse, don't reinvent: the Maestro build/validate/eval is delegated to `uipath-maestro-flow`, exactly as
  REFramework delegates to `uipath-rpa-workflows`.

## Non-goals

- **Maestro BPMN / Case** (other Maestro project types) — this is Maestro **flow** (`.flow`) only.
- **Authoring eval sets** — the Maestro gate *runs* eval sets when they exist; authoring them is
  `uipath-maestro-flow`'s job, not wi's.
- **Changing the REFramework path** — it stays exactly as today (its references, gate, and paradigm).
- **Owning `uip maestro flow` mechanics** — delegated to `uipath-maestro-flow`.

## Design

### 1 · A `Framework` choice above the paradigm, decided early

A new field, distinct from `Build paradigm:`:

- **`Framework: reframework | maestro`** — recorded in `progress.md`.
- **`Build paradigm: xaml-only | coded`** — applies **only** when `Framework = reframework` (n/a for maestro).

Because the framework reshapes the plan-phase architecture + SDD, it is **proposed during brainstorm** (from
the PDD's process shape) and **confirmed at the design gate** — earlier than the paradigm. The
`rpa-constitution` carries the default (`reframework`); `--auto` uses it. The brainstorm applies a selection
heuristic and states a one-line rationale the user confirms or overrides:

- **Maestro fits** orchestration-shaped work: human approvals / HITL, Integration Service connectors,
  calling UiPath Agents, long-running / wait-heavy steps, document understanding (ixp), branching across
  systems.
- **REFramework fits** high-volume queue-based batch transactions and unattended dispatcher/performer work.

### 2 · Framework-aware planning (architecture + SDD)

- **REFramework path — unchanged:** `refr-architecture.md` (Dispatcher/Performers/queues) + the current SDD
  ToC.
- **Maestro path:**
  - A new `skills/rpa/references/maestro-architecture.md` — the architecture is a **flow diagram** (trigger
    → nodes: connector / approval / script / subflow / agent / ixp → end), mermaid, validated with
    `check_mermaid.py` exactly like the REFramework runtime diagram.
  - A **framework-conditional ToC** in `sdd-template.md`: on the Maestro path, §2 becomes the flow diagram;
    §3.1 the Maestro project/flow layout; §7.1.x the flow's nodes (each node's type, inputs/outputs, the
    connector/agent/approval it uses); §7.2–7.6 become Maestro resources (connections, triggers, agent
    registrations) — queues and `Config.xlsx` drop out. The Maestro SDD guidance lives inline in the
    conditional ToC (no separate file).

### 3 · Framework-aware build

- **REFramework — unchanged:** `build-uipath.md` → `uipath-rpa-workflows`.
- **Maestro:** a new `skills/rpa/references/build-maestro.md` — build the `.flow` (nodes + connections) by
  delegating to **`uipath-maestro-flow`**; the build DAG is shared components → the flow + its subflows →
  wire-up (connections / triggers / agent registrations via `uipath-platform`). No dispatcher/performer, no
  `Config.xlsx`.

### 4 · Framework-aware verification gate

`verification-gate.md` branches on `Framework`:

- **REFramework — unchanged:** approved-paradigm check + `uip` restore/validate + Workflow Analyzer
  (zero error-level).
- **Maestro:** `uip maestro flow validate` (mandatory) + `uip maestro flow eval` **when eval sets exist**
  (run-if-present, reported); **no** Workflow-Analyzer / paradigm check (they're REFramework-specific).
- The goal-level **checker (result mode)** over `sdd.md` §13 runs on **both** paths, unchanged.

### 5 · Constitution, progress, threading, and Feature A

- `rpa-constitution-template.md`: a `Framework:` default (`reframework`) + a short Maestro sub-section
  (connectors-over-script, approval/HITL patterns, eval expectations).
- `progress.md` template (`rpa-directory.md`): add the `Framework:` field; annotate `Build paradigm:` as
  "REFramework only." Register the two new reference files in the rpa layout doc.
- `rpa/SKILL.md`: thread `Framework` through **brainstorm** (propose + rationale) → **plan** (route to the
  framework's architecture/SDD shape) → **gate** (confirm framework; paradigm only when REFramework) →
  **build** (route to `build-uipath.md`/`uipath-rpa-workflows` or `build-maestro.md`/`uipath-maestro-flow`)
  → **verify** (the framework's gate branch).
- `brainstorm-protocol.md`: add the framework-selection step (shape heuristic + rationale).
- **Feature A (publish) is framework-agnostic:** `uipath-solution` packs/publishes either a REFramework or a
  Maestro project, so the `Publish:` flow needs no rework — noted, not changed.

## Acceptance criteria

1. `progress.md` carries a `Framework: reframework | maestro` field (template in `rpa-directory.md`), with
   `Build paradigm:` annotated as REFramework-only.
2. `brainstorm-protocol.md` adds a framework-selection step: propose `reframework` or `maestro` from the
   process shape (the heuristic above), with a one-line rationale, recorded in `progress.md`.
3. `rpa/SKILL.md` threads `Framework` through brainstorm → plan → gate → build → verify; the design gate
   confirms the framework and asks for the build paradigm **only when** `Framework = reframework`.
4. `rpa-constitution-template.md` has a `Framework:` default (`reframework`) + a Maestro sub-section;
   `--auto` uses the constitution default.
5. A new `skills/rpa/references/maestro-architecture.md` defines the Maestro **flow** architecture (node
   types, a mermaid flow-diagram example, `check_mermaid.py` validation).
6. `sdd-template.md` has a **framework-conditional ToC**: the Maestro path reshapes §2 (flow diagram), §3.1
   (Maestro layout), §7.1.x (flow nodes), and §7.2–7.6 (Maestro resources; no queues/`Config.xlsx`); the
   REFramework ToC is unchanged.
7. A new `skills/rpa/references/build-maestro.md` defines the Maestro build (delegate to
   `uipath-maestro-flow`; flow + subflows + wire-up DAG; no dispatcher/performer/`Config.xlsx`).
8. `verification-gate.md` branches on `Framework`: REFramework path unchanged; Maestro path uses
   `uip maestro flow validate` (mandatory) + `eval` when eval sets exist, with no Analyzer/paradigm check;
   the checker (result mode) runs on both.
9. `build-uipath.md` and `refr-architecture.md` are marked as the **REFramework** path (a one-line scope
   note), so the split between the two frameworks is explicit.
10. The `${CLAUDE_PLUGIN_ROOT}` references to the two new files resolve; `python scripts/validate.py`
    passes; the version is bumped to `1.0.0` across the three manifests with a README Roadmap bullet.

## Verification

Prose + two new reference docs + delegation wiring — **no new scripts or unit tests** (like the prior rpa
features). Verify with `python scripts/validate.py` (manifests, frontmatter, **`${CLAUDE_PLUGIN_ROOT}`
resolution** — which catches a mistyped new-file path — fence/newline balance, OKF) plus a read-back
confirming every phase (brainstorm/plan/gate/build/verify), the constitution, and the progress template
agree on the `Framework` model and that the REFramework path is untouched. The real Maestro build/validate/
eval is delegated to `uipath-maestro-flow` and isn't wi's to unit-test.

## Rollout

Single PR. Bump the plugin version to **`1.0.0`** across the three manifests + a README Roadmap "shipped"
bullet (wi:rpa now covers both UiPath frameworks). Run `validate.py` and the file-tail check before commit.
No migration: existing rpa runs default to `Framework: reframework`, so behavior is unchanged until a run
selects Maestro.
