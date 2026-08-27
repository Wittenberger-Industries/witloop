---
type: Skill
name: scan
description: >
  Refresh an already-scanned project's .wit/ facts. Use this skill when the user types "/wit:scan",
  "/wit:scan --refresh", or says "refresh the scan", "update the repo map", "is the scan stale?", or
  "scan the repo" on a project that already has a repo-map. Bare invoke (no flags) is silent
  --refresh. Missing repo-map.md runs setup. Python-first, stack-agnostic.
---

# /wit:scan (refresh: drift-check + memory hygiene)

One job: re-verify `.wit/` facts **without re-documenting**.

Bare `/wit:scan` (no flags) is silent `--refresh`. `--refresh` remains a synonym for auto-stale
callers (`dev`).

Missing `.wit/repo-map.md` → **run setup** (follow `${PLUGIN_ROOT}/skills/setup/SKILL.md`). Do not merely tell the user to run it. Do not re-document from this skill. Do not chain a refresh after
setup writes the map; stop. `.wi/` with no `.wit/` is the same tell (setup owns the rename).

Map present? A/B/C below.

Design rationale for this skill lives in the wit repo's `docs/design-notes/scan.md` (maintainer doc,
never loaded at runtime).

**Host probe (once at entry).** Detect `claude` | `codex` | `copilot` | `grok` | `cursor` per **the
capability table** (`${PLUGIN_ROOT}/references/capabilities.md` Host probe; same tells as
`wit:dev`). Plugin root per capabilities.md **Plugin root** (never pass unexpanded `${PLUGIN_ROOT}`).
Scan has no feature `progress.md`: keep the slug in-session. A later `dev` / `rpa` stamps `Host:` +
`Plugin root (resolved):` + `## Capabilities (resolved)`.

## `--refresh`: drift check + memory hygiene

`--refresh` keeps the `.wit/` facts honest **without re-documenting**: verify what a later phase would
actually trust, touch only what drifted. `dev` runs this automatically at feature start when the scan
looks stale.

### A · Drift check (facts, not prose)

Anchor on the repo-map's `scanned <YYYY-MM-DD>` stamp and diff reality against the recorded facts:

1. **Config & commands:** `git log --since=<scan date> --name-only -- <config/lock files>` (the
   stack-detection cookbook at `${PLUGIN_ROOT}/skills/scan/references/stack-detection.md` lists them).
   If any changed, re-verify the affected `Commands` rows the cheap way (read the scripts/tool
   sections; run a `--version`/`--help` probe only when reading is inconclusive) and update
   `repo-map.md`. Unchanged config ⇒ commands stand; don't re-run the suite to "check".
2. **Stack & classification:** new language/framework in the lockfiles? frontend appeared in a
   backend-only repo? Update the facts and the frontend/backend line.
3. **Structure vs `architecture.md`:** `git diff --stat $(git rev-list -1 --before="<scan date>" HEAD)..HEAD`
   at directory level (or `git log --stat --since="<scan date>"`): modules/dirs added or removed that the
   diagram doesn't show? Update the mermaid when the change is structural; leave it alone for churn
   inside existing nodes.

   Mermaid has two syntax traps; both **must** be avoided or the whole diagram fails to render:
   1. **Quote every node label** containing `:` `/` `->` `+` `(` `)` as `id["..."]`; a bare special char
      breaks the parser.
   2. **Node IDs are identifiers, not display names.** Keep them short and safe (`[a-z][a-z0-9_]*`) and
      **never use a mermaid reserved word as an ID**: `graph`, `end`, `subgraph`, `class`, `classDef`,
      `style`, `linkStyle`, `click`, `state`, `direction`, `flowchart`, `default`. Put the module's real
      name in the quoted label, not the ID: `gbuild["graph: builder / nodes"]`, **not** `graph["..."]`.
      When a module's name is a keyword, suffix the ID (`graph_mod`, `end_node`).

   **Validate the diagram for real** before committing; don't eyeball it:

   ```
   python ${PLUGIN_ROOT}/skills/scan/scripts/check_mermaid.py .wit/architecture.md
   ```

   (python fallback: `references/workflow.md` "Script invocation".)

   Fix every error the checker prints; never save a diagram that doesn't pass.
4. **`overview.md`:** update only sections made wrong (organization, run steps, external services).
5. **`constitution.md` is user-owned; never rewrite it.** If reality now contradicts a rule (e.g. the
   lint tool changed), surface the contradiction in the report and let the user amend.
6. **Lean check:** `constitution.md` / `repo-map.md` grown past ~150 lines → flag it in the report with
   a suggested split or trim (suggest, never rewrite).

Re-stamp `repo-map.md` (`scanned <today>, refreshed`). If the **Kind or core stack fundamentally changed**
(greenfield grew real code, repo swapped language), say so in the report; do not re-document from this
skill.

### B · Memory hygiene (learnings consolidation)

If `.wit/learnings.md` exists (dev or rpa projects alike), give the compounding memory a maintenance pass:

1. **Dedupe:** index lines (or detail files) describing the same gotcha → merge into one, keep the
   clearest hook, fix the links. Match on **WHEN-context** (the situation the lesson fires in), not
   on surface wording alone.
2. **Promote:** use the index counter as promotion evidence - promote at `seen >= 3` (`>= 2` for
   rule-shaped lessons). Fold the rule into its source of truth (`constitution.md`, user-owned:
   confirm with the user; `repo-map.md`; or `glossary.md`), then shrink the index line to a
   tombstone: `- <hook> → promoted to constitution (<date>)`. Delete the detail file once promoted.
3. **Prune / retire:** (a) the code/tool the learning warns about is gone (verify against the repo,
   not memory) → delete the detail file and its index line; or (b) the lesson is now structurally
   enforced - verify the named test, CI check, or constitution rule actually exists in the repo,
   then tombstone the line as `- <hook> → enforced by <check> (<date>)` and delete the detail file.
4. **Target:** keep the index readable at a glance (roughly ≤30 lines). If it's bigger after
   consolidation, the bar for "worth a line" in ship:4 was too low; note that in the report.
5. **Process-drift trend:** scan index lines' `process:` clauses. The same friction appearing in
   ~3 features (or more) → surface it in the refresh report with a concrete proposed amendment
   (example: "checker round budget too small for this repo - raise to 3 in constitution?" /
   "remote checks flaky - add the CI wait note to repo-map?"). Propose, never self-apply;
   constitution stays user-owned. Fewer than 3 shared frictions → stay silent on process drift.

Glossary gets the same light pass: merge duplicate/aliased terms, drop ones the codebase no longer uses.
ADRs are **immutable history, never pruned** (supersede with a new ADR instead).

### C · Report (refresh)

Commit what drifted (`chore(wit): scan refresh`). Then report, 3-6 lines: what drifted and was fixed
(commands, diagram, facts), contradictions flagged for the user, learnings merged/promoted/pruned
(counts), process-drift trends surfaced (if any), or "no drift - scan is current."
