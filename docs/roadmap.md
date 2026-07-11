---
type: Roadmap
title: "wi roadmap — the live queue of open issues"
description: Tracking surface for all open issues — order, version targets, sequencing constraints, and the standing per-PR guardrails. Supersedes the 2026-07 triage doc as the thing that gets updated; that doc is frozen as the sweep's history.
timestamp: 2026-07-11
tags: [roadmap, triage, plan]
---

# wi roadmap (live)

**This file is the tracking surface for open work — update it here, not in the triage doc.**
History and rationale of the 2026-07 sweep live in `docs/plans/2026-07-10-issue-triage-35-42.md`
(frozen; PRs A–D shipped #35–#40, #42, #47, #49 as v1.6.0 → v1.8.0, Checkpoints A and B passed —
B's record: `docs/plans/2026-07-11-checkpoint-b-42.md`). Every issue below is spec-grade (acceptance
criteria + file lists in the body); the per-issue implementation plan is written from that AC at
pick-up, into `docs/plans/`, and rides in the PR.

## Queue (in order)

| Slot | Issue | What | Version | Effort · Risk | Why this order |
|---|---|---|---|---|---|
| next | **#48** drop legacy/backward-compat support | Delete the seven compat families (pre-1.3/pre-rename shims, 4-column ledger acceptance, validate.py 7c carve-out); dev classifier → 5 classes, feature-folder-cases → 4 cases | **v1.9.0** (removes supported behavior → minor) | M · Low by decree (compat is a declared non-goal; the issue's stays-list is **binding**) | Delete before compressing — no point compressing text #41 would then re-touch |
| then | **#41** compress skill prose | One file per PR (mandated): **ship → research → build → dev**, then rpa/scan; rationale moves to `docs/wi-design-notes/<skill>.md` | v1.9.1+ (patch per pass) | L · Medium (judgment-heavy; strongest guardrails) | Last of the sweep by design — benefits from #35 (measure), #39 (template), #40 (dedup), #42 (directive present), #48 (legacy text gone) |
| then | **#53** ledger split labels | `token_report.py` split rows labeled from `agent-<id>.meta.json` `description` (+ the description==Source convention) instead of 48-char prompt prefixes | minor (artifact format) | S · Low | After #48 (shared `_ledger.py`/`check_tokens.py`/tests surface); small — may interleave between #41 passes (disjoint files) |
| then | **#52** dispatch-time skill pointer | Generalized capability-tag → registry → resolved SKILL.md path in the dispatch; frontend first; fixes the unreachable `[frontend]` delegation (charters have no Skill tool) | minor (runner behavior) | S–M · Low–Medium | After #41's build/dev passes — touches `build/SKILL.md` + a charter (hotspots, strictly serial). Owner decision 2026-07-11: pointer, **not** a Skill-bearing variant agent; Checkpoint B's baseline-b runners empirically validated the read-the-skill-file mechanism |
| parallel, gated | **#43** Grok Build platform | Fourth platform adapter (`references/grok-tools.md`, keep-alive `/goal`-family branch, AGENTS.md row, bootstrap, models.md xAI entry) | minor | M · Low–Medium | Independent of the sweep; **gated on Grok Build beta access** — every runtime claim verified on a real session. The planned **release/1.8.0 → Grok "baseline-c" comparison** doubles as its verification run (evidence method: the Checkpoint B harness) |
| ⏸ postponed | **#34** cross-vendor MoA proposers | Let the MoA council use OpenAI / DeepSeek / Grok / Gemini | — | — | Postponed (owner, 2026-07-10). Revisit after the sweep: #35 already landed (simplifies it), and #43's models.md xAI groundwork overlaps it |

## Sequencing rules (standing)

- **Strictly serial on the hotspots** — `build/SKILL.md`, `ship/SKILL.md`, `dev/SKILL.md`,
  `wi-directory.md`, `workflow.md`: never two branches editing them at once. Stacked PRs,
  squash-merge, rebase + retarget the next after each merge.
- **#48 before #41** (delete before compressing) — same logic as dedup-before-compress.
- **#41 is one file per PR**, each independently revertible, each shipping its rules inventory +
  loaded-token delta.
- **Agent charters are the most sensitive surface** (autonomous, no human in the loop): minimal
  additive diffs only; never alter report caps, output markers, verification-gate contracts, or
  tool lists. Currently only #52 may touch them.
- `release/1.8.0` is pinned (Checkpoint-B-validated bytes) for the Grok Build comparison — don't
  delete it; the local `checkpoint-b` evidence folder outside the repo is permanent.

## Standing guardrails (apply to every PR)

1. **Rules inventory** before/after for any PR that moves, rewords, or deletes rule text — attach it
   to the PR body. Test: *does each touched file still make correct decisions if loaded alone?*
2. `python scripts/validate.py` + `pytest tests/` green (never pipe validate.py through `tail` —
   exit code swallowed); after bulk markdown edits check file **tails** (the repo has shipped
   mid-sentence truncations; validate.py guards only trailing-newline + fence balance).
3. Behavior/artifact changes → **minor** bump, pure relocation/compression → patch; all **three**
   manifests together (`.claude-plugin/plugin.json`, the wi entry in `marketplace.json`,
   `.codex-plugin/plugin.json` — validate.py enforces parity).
4. New files only in `.gitignore`-whitelisted dirs (`references/`, `docs/`); any new top-level path
   needs a `!/path` line or it silently vanishes.
5. Citations use `name:N` locators (`ship:8`, `sdd:7.1.3`) or quoted headings — never the section
   sign (validate.py bans it), never spelled-out step/section words.
6. No AI attribution in commits or PRs.
7. Quality-sensitive changes validate against a **real run**, not a dry-run (a simulation shares the
   model's blind spots) — the Checkpoint B harness (frozen A/B transcripts + `analyze.py` + dossier
   snapshot-diff + independent code review) is the reusable method.

## Pick-up notes (carried from the triage doc + the issues)

- **#48** — inventory first (grep `legacy` / `pre-1.` / `pre-rename` / `old-named` / `old filename`),
  classify every hit against the issue's binding stays-list ("legacy" describing the *user's* code
  stays; self-repair behaviors keep their mechanism, lose only the pre-1.x framing; graceful
  `unavailable` stays), then delete the seven compat families; PR body carries the
  deleted-vs-relabeled disposition table. Dry-runs: old-named models config → fresh setup; a
  pre-rename work-unit folder → treated as unscanned; current-format flows unchanged. Retires the
  #35 legacy-ledger guardrail.
- **#41** — order by loaded-per-run impact (ship → research → build → dev, then rpa/scan); rationale
  to `docs/wi-design-notes/`; report the loaded-token delta per pass. The proven verification
  pattern for prose refactors: per-branch fixture dry-run subagents + load-alone Q&A subagents +
  a removed-behavior audit (the load-bearing angle).
- **#52** — log strings and the checker contract stay byte-identical; the generality proof (new
  capability = registry row + tag, zero protocol changes) is demonstrated on paper in the PR body.
- **#53** — prefer the meta.json `description` + description==Source convention over the id-join
  (no ledger byte-format change); keep the count-mismatch note; `--write` stays idempotent.
- **#43** — all runtime claims (install path, namespace, `/goal` semantics vs wi's condition
  template, model ids) verified on a real Grok Build session before merge; keep-alive lands in the
  `/goal` family branch with the headless `-p`/`--max-turns`/`--continue` fallback.
