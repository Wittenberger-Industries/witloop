---
type: Reference
title: "Brainstorm — refine the TO-BE (the one conversation)"
description: "This is the interactive phase and the value of `wi:rpa`: a PDD is usually AS-IS-heavy and gap-ridden, so turn it into a buildable TO-BE."
timestamp: 2026-06-09
tags: [rpa, reference]
---

# Brainstorm — refine the TO-BE (the one conversation)

This is the interactive phase and the value of `wi:rpa`: a PDD is usually AS-IS-heavy and gap-ridden, so turn
it into a buildable TO-BE. **Refine the PDD's own ToBe — but do NOT trust it** (see §0). Assume gaps *and
errors* exist even when the PDD looks complete.

**This is a real conversation with the USER — not a monologue.** In interactive mode (no `--auto`) you **put
the open questions to the user and WAIT for their answers** before writing the decision artifacts. Asking
yourself a question and answering it (`… → my answer`) and logging it as an assumption is the **`--auto`
behaviour, NOT interactive** — doing that and then asking for one bulk "approve" at the gate **defeats the
brainstorm**. Batch related questions so it's a handful of exchanges, not dozens, but the answers come from the
user.

**Step 0 — delegation check (mandatory).** If `superpowers:brainstorming` is installed, drive the dialogue with
it; else run this protocol directly. **Either engine, the dialogue is with the USER** — if the brainstorming
skill starts self-answering, stop and put the questions to the user yourself. **Stamp the mode in `progress.md`**
(`brainstorm via superpowers:brainstorming` | `via wi fallback`).

**Must-ask before the design gate (interactive mode never skips these — `--auto` self-resolves each as a logged
assumption, and says so):**
1. **Scope** — confirm in/out (§1).
2. **Framework** — **REFramework or Maestro flow?** Propose from the process shape: **Maestro** for
   orchestration-shaped work (approvals/HITL, Integration Service connectors, UiPath Agent calls,
   long-running/wait-heavy, ixp, branching across systems); **REFramework** for high-volume queue-based
   batch transactions (dispatcher/performer). State a one-line rationale; record in `progress.md`
   (`Framework:`). `--auto` takes the constitution default (`reframework`).
3. **ToBe correctness** — the PDD's ToBe + diagram are a *draft*; confirm what's wrong or missing (§0, §2).
4. **Dispatcher/Performer split + the queue handoff** (§5).
5. **Naming conventions** and **Orchestrator env / variables** (§6).
6. **Email / notification approach — never defaulted.** *Only when the process sends email or
   notifications:* if the PDD/inputs name the method, use exactly that; otherwise put the options to the
   user — **IMAP/SMTP, desktop Outlook activities, Microsoft 365, Exchange, or an Integration Service
   connector** — and record the confirmed choice (an assumption row + the SDD). Unresolved at the gate = an
   **open dependency `D`** (blocking, §7). `--auto` does **not** pick an email framework — this is the one
   must-ask it never self-resolves: it **mocks the send** (§2 mock boundary) and records the open dep.
7. **Every open dependency `D`** — resolve it now, or have the user *explicitly* defer it (§7 + the gate).
8. **Rename / rebrand / migration only** — run the **Runtime State Inventory** (§6a): the old name almost
   always lives on in Orchestrator resources and in-flight queue items a repo grep can't see.

## 0. Baseline — and challenge it

Read `pdd.md`, `.wi/inputs.md`, `.wi/components.md`, `.wi/rpa-constitution.md` (+ any recovered diagram
descriptions in `pdd-images.md`). **Extract the PDD's existing ToBe section as the *starting* `tobe.md`** (only
*derive* one from the AS-IS when the PDD has none) — **but the PDD's ToBe and its To-Be diagram are a draft,
often wrong or incomplete, NOT ground truth.** Actively challenge them with the user: does every step match
reality? what's **missing** (a whole step or process — e.g. a master-data generation/refresh the diagram
omits)? is the diagram **self-consistent**, and consistent with the written steps + the Enrichment Matrix?
Surface every contradiction and gap to the user — don't silently adopt or "fix" it. "Refine, don't trust":
refining *means* correcting, which means questioning first.

## 1. Decompose into processes (1..N)

A PDD may describe several processes. Identify each distinct end-to-end **business process** — its own
trigger, its own business outcome — and list them as the **process inventory**. Each becomes a process unit
with its own `tobe.md` + an SDD §7 block.

**Don't over-decompose — separate three things that look alike:**
- A **business process** (own trigger + outcome) → its own inventory row.
- A **deployable unit** of one process — REFramework **Dispatcher + Performer** are two packages implementing
  *one* process, not two processes. List them as units *under* the process, not as separate rows.
- An **out-of-scope or mocked** step (e.g. a "daily SAP→CSV refresh" the build won't really do) → record it as
  out-of-scope with its PDD citation, not as a process to build.

Fix **scope** here too: list what's **in** vs **out**, each with the PDD section that says so (e.g. one invoice
type in, another out). Note dependencies between in-scope processes (B consumes A's output) — that ordering
feeds the build DAG.

## 2. Refine each process's TO-BE — the findings pass

Walk the steps and surface, proposing a resolution for each (confirm with the user, or under `--auto`
record as an assumption):

- **PDD contradictions / wrong diagram** — where the written steps, the To-Be diagram, the Enrichment Matrix,
  and the data inputs **disagree**, flag it; the PDD's own ToBe is the *most likely* thing to be wrong. Don't
  reconcile it silently — ask the user.
- **Missing steps** — data used but never sourced; "send report" with no "generate"; no "mark
  complete"/audit step; an "if approved" with no else.
- **Redundant / collapsible** — AS-IS UI navigation that disappears under an API ("open app → find screen
  → search" → one `GetRecord`). Collapse them.
- **Decisions & branches** — make each condition explicit; give every branch a defined outcome.
- **Triggers & I/O** — what starts it (file/email/schedule/queue), the inputs per unit, the outputs and
  destination.
- **Exceptions** — per step: business (expected reject → no retry, route/notify) vs system (timeout/app
  down → retry per Config). PDDs rarely cover this; always probe.
- **Mock boundary** — which systems/steps are **real** vs **mocked/stubbed** for this build? Unknown
  integrations (a not-yet-specified SAP query), out-of-scope transfers, or test-only endpoints get mocked
  (a folder drop, a stub) — establish this explicitly so the build knows what to wire vs fake.

## 3. Clarify implementation per step — inline, no bias

For each step whose implementation is genuinely open, ask once: **"UI activity, API, or connector?"** and
record the answer **inline on that step** in `tobe.md`. The curated `references/connectors.md` only
*informs* the question neutrally ("an Outlook connector exists if you'd prefer it over UI") — **UI is a
perfectly valid answer** when there's no API or the interaction is inherently UI. Do not frame UI as wrong
and do not produce a separate "everything-must-be-API" table.

## 4. Reuse before build

For each capability a step needs (notify, login to SystemX, read a queue…), check `.wi/components.md`
first. If a component exists, the step **reuses** it (note the component). Only genuinely new capabilities
become new sub-workflows.

## 5. Per process: transaction + shape (REFramework)

- **Interrogate the Dispatcher/Performer split WITH the user — don't inherit the PDD's step order as the unit
  boundary.** Walk each step and decide *together* whether it's **collection** (Dispatcher: query / read /
  download / enqueue) or **processing** (Performer: per-transaction work), then nail the **handoff contract** =
  exactly what crosses the queue (the item schema below). The PDD lists steps linearly; that is *not*
  automatically the Dispatcher↔Performer line. Confirm: what does each unit own, and what's in the queue item?
- **What is one transaction?** the unit of work + the minimal data to process it without re-querying, its
  unique reference, and its status. This defines the queue-item schema.
- **Shape:** batch of independent items → queue-based; single linear run → one-shot performer.
- **Dispatcher or not?** items must be *collected first* (query/read/scrape) → Dispatcher (collect→enqueue)
  + Performer; items arrive already-queued/triggered → Performer only. Ask: *"where do work items come
  from, and how many per run?"*
- **Queue items carry references + keys, not resolved data or files.** A transaction holds the document
  **reference** (Storage Bucket / shared-folder path), its **unique id**, and the **lookup keys** the consumer
  will need — *not* the file bytes, and *not* master-data fields the consumer can fetch itself. Keep the
  collector (Dispatcher) lean: it *collects and references*; the **consumer (Performer) resolves every
  master-data lookup** (CSV/DB/dictionary) right before it writes them out. Cleaner responsibilities, smaller
  items, and no stale data frozen at enqueue time. Ask per field: "does the performer already have this, or a
  key to fetch it? then don't put the resolved value in the item."
- **Enrichment timing = where the KEY is known, not where the lookup runs.** Note when each lookup key becomes
  available — in the Dispatcher (from source metadata) or only in the Performer (post-extraction). The
  Dispatcher passes the **key**; the Performer does the **lookup**. (Vendor keyed on an extracted field →
  fully performer-side; a store keyed on a source field → Dispatcher passes the store key, Performer looks up
  the record.)
- **Derive what's computable; never invent a source for a generated value.** A field determined by the
  *content* (e.g. credit-note vs invoice from the sign of the amount) is **derived** in the Performer, not
  carried as a source field; a value the process itself **generates** (e.g. a new unique IDoc id) is created,
  not looked up. Only attribute a field to a source you've actually confirmed holds it (don't assume the
  queue/DocuWare/Agent carries it).

## 6. Orchestrator provisioning & naming

The SDD's infrastructure (§1.3) and Orchestrator sections (§7.2–7.6) need **concrete resource names + values**,
and the back-half build provisions from them. **Ask the user for the real values** — anything they don't know
becomes an **open dependency `D`** (surfaced at the gate), not a silent `(confirm)` placeholder you build past.
Capture answers into `.wi/orchestrator.md`:

- **Naming conventions** — the org's standard for workflow / argument / asset / queue / process names
  (prefixes, casing, the `<Project>_<Unit>` pattern). Ask; don't invent one silently.
- **Orchestrator link** — org / tenant / **folder** (+ the dev/test/prod folder split).
- **Published process / package names** — one per process (e.g. `Acme_Dispatcher`, `Acme_Performer`).
- **Queues** — name(s) + dev/test/prod split.
- **Assets** — config assets + **credential names** (names ONLY, never values — they're Orchestrator credentials).
- **Storage Buckets** — name + purpose (the document/file transport from §5).
- **Config / environment variables** — the `Config.xlsx` Settings/Constants the run needs **and their values
  per environment** (dev/test/prod): URLs, folder/UNC paths, poll interval, queue concurrency/retries,
  target-system constants, feature toggles. Names *and* values — ask, don't default silently.
- **UiPath Agent(s)** — if a step calls a UiPath Agent (e.g. a document-extraction agent), its **name** +
  input/output contract (point at the sample output registered in `.wi/inputs.md`).
- **Triggers** — time or queue, schedule, concurrency.

Under `--auto` (or when the user doesn't have them yet) **propose convention-based names**
(`<Solution>_<Process>_<Queue|Asset|Bucket>`) and log them as assumptions to confirm — a named default beats a
blank §7. Secrets stay names-only (constitution rule).

```markdown
---
type: Orchestrator Manifest
title: Orchestrator manifest — <solution>
description: Concrete Orchestrator resources (folder, processes, queues, assets, buckets, agents, triggers) — names only.
resource: <Orchestrator folder URL>
timestamp: <YYYY-MM-DD>
---

# Orchestrator manifest — <solution>

## Link
- Org / tenant: <org> / <tenant>
- Folders: dev=<>  test=<>  prod=<>   (URL: <orchestrator url>)

## Processes (published packages)
| Process | Package name | Type | Trigger |
|---------|--------------|------|---------|
| <Dispatcher> | <Solution_Dispatcher> | dispatcher | time/queue |
| <Performer>  | <Solution_Performer>  | performer  | queue |

## Queues / Assets / Storage Buckets
| Kind | Name | Purpose | Notes |
|------|------|---------|-------|
| Queue      | <Solution_Performer_Queue> | transactions   | SLA/retry |
| Asset      | <Solution_Config>          | config         | — |
| Credential | <Solution_DocuWareCred>    | API auth       | NAME only; value lives in Orchestrator |
| Bucket     | <Solution_Documents>       | file transport | — |

## Agents
| Name | Runs on | Input | Output | Invoked by |
|------|---------|-------|--------|------------|
| <DocExtractionAgent> | Orchestrator/Agent | docText | <sample in inputs.md> | Performer |

> `?` / `<...>` = unknown or proposed (convention default) — confirm at the design gate.
```

## 6a. Runtime State Inventory — rename / rebrand / migration runs only

Skip this for a greenfield automation. **When the run renames, rebrands, or migrates an existing automation,**
the source/code changes are the easy part — the old identity also lives in **runtime state no repo grep can
see**, and the build will look green while production still references the old name. Sweep five categories and
record each into `orchestrator.md` (a rename map) + `assumptions.md`, with a **separate migration task** in
`tasks.md` (renaming how *new* items are written never fixes the *existing* ones). "None — verified by X" is
a valid answer; a **blank is not**.

1. **In-flight / stored data** — queue items already enqueued under the old queue, transaction references and
   status keyed on the old string, Storage-Bucket paths, records in a target system.
2. **Live Orchestrator config** — queue / asset / storage-bucket / **published-process** names, folder names,
   triggers, alerts/dashboards named after the thing (none of it in the repo).
3. **OS / platform-registered** — robot/machine names, the **published package** name in the feed, Library
   feed entries, scheduled triggers registered in Orchestrator.
4. **Credential & asset *names*** — the Orchestrator credential/asset **keys** (names only) referencing the
   old name; renaming the key and the workflow that reads it must move in lockstep.
5. **Build artifacts** — the published `.nupkg` package name/version, generated process names, anything a
   downstream consumer binds to by name.

Every load-bearing row becomes an assumption + a migration task; the checker (plan mode) then verifies each
has a covering task.

## 7. Log assumptions & open dependencies

Every gap you filled, every default you applied, every "we assumed X because the PDD didn't say" → a row in
the process's `assumptions.md`. In RPA the business sign-off is on these assumptions, so they are first-class.

Keep a second register in the same file: **open dependencies `D1..Dn`** — referenced-but-missing inputs (a
mapping xlsx, a dropped diagram) and genuine ambiguities the PDD can't settle. Each `Dn` names the gap, its
impact, and who/what resolves it. **Open deps are blocking by default:** at the design gate, present each `Dn`
to the user as a question and either **resolve it** (→ a confirmed assumption, e.g. "D4 store-key → A14") or get
the user's **explicit decision to defer** (build the stub/mock, accept the risk). Do **not** silently proceed
into the build with a `Dn` quietly marked "needs input later / before production" — **deferral is the user's
call, not a default.** (`--auto` records each for after-the-fact review and says so.)

## `tobe.md` format (per process)

```markdown
---
type: TO-BE
title: TO-BE — <process name>
description: <the refined target process, one line>
feature: <run-slug>
timestamp: <YYYY-MM-DD>
---

# TO-BE — <process name>  (refined from PDD ToBe; <date>)

## Trigger
<what starts it; inputs per unit>

## Steps
1. <step> — **impl: connector(Outlook) / API / UI activity** — <notes; reuses Component X?>
2. <decision: if <cond>> → <branch A> ; else → <branch B>
3. ...

## Exceptions
- <business exception> → no retry, route to <exception queue/notify>
- <system exception> → retry per Config

## Outputs
<what is produced and where it goes>
```

Include a small **mermaid flowchart** of the TO-BE (validate with
`${CLAUDE_PLUGIN_ROOT}/skills/scan/scripts/check_mermaid.py`). Keep `tobe.md` faithful to the refined
process — the SDD turns it into the technical design.
