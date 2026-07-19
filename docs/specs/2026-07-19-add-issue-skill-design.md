---
type: Design Spec
title: "add-issues skill - structured GitHub issue filing (/wit:add-issues)"
description: >
  Accepted design for a fourth user-invocable wit skill that turns a bug (or typed issue) into a
  well-formed GitHub issue: ephemeral OKF draft under .wit/issues/, fixed body sections including
  test-backed acceptance criteria for Bug, and GitHub Issues metadata (type, labels, milestone,
  assignees, projects, parent/sub-issues, blocked-by/blocking). Implemented as skills/add-issues/.
status: accepted
timestamp: 2026-07-19
tags: [add-issues, github, okf, skill, design]
---

# add-issues skill - structured GitHub issue filing

> **Shipped name:** `add-issues` (plural). Commands: `/wit:add-issues`, `/wit-add-issues`,
> `$wit-add-issues`. Drafts are ephemeral (deleted on publish/abort); GitHub is the source of truth.

## Summary

Add a **user-invocable** skill `add-issue` so an agent can file a high-quality GitHub issue against the
repo the session is connected to. The skill runs a short dialogue (or accepts a rich dump), writes an
OKF draft locally, confirms once with the user, then creates the issue via `gh` with the richest
metadata the repo/org supports.

Invocation forms (same pattern as scan / dev / rpa):

| Harness | Form |
|---------|------|
| Claude Code | `/wit:add-issue` (also bare `/add-issue` where the plugin namespace applies) |
| Copilot CLI / Grok Build | `/wit-add-issue` (flat alias) |
| Codex CLI | `$wit-add-issue` |
| Natural language | "file a bug", "open a GitHub issue for …", "add an issue about …" |

This is a **fourth entry skill** (today only scan / dev / rpa are user-facing). Phase skills stay
`user-invocable: false`.

## Problem and goal

**Problem:** Ad-hoc `gh issue create` (or browser filing) produces uneven issues: missing repro steps,
no acceptance criteria, no test commitment, weak labels/types, and no use of Issues 2.0 hierarchy or
dependencies. wit already demands spec-grade issues on its own roadmap; the skill should make that the
default for any connected repo.

**Goal:** From a bug report or defect description, produce one GitHub issue that is:

1. **Readable** — fixed section order, scannable by humans and agents.
2. **Actionable** — acceptance criteria include at least one **new test** that would have caught the bug.
3. **Typed and linked** — issue type, labels, and relationships filled in when the repo supports them.
4. **Reviewable before create** — local OKF draft + confirm gate (unless `--auto`).

**Non-goals (this skill):**

- Implementing the fix (`/wit:dev` owns that).
- Bulk import / migration of existing trackers.
- Replacing repo issue *templates* when the user explicitly wants a template form (skill may *prefer*
  its body, or offer to start from a template — see Open questions).
- Editing closed issues or running triage boards (future skill territory).

## Design decisions (proposed)

### D1 · User-invocable entry skill, not a phase

`add-issue` sits beside scan / dev / rpa. It does **not** enter the brainstorm → research → build →
ship loop. Optional handoff line in the final report: "Ready for `/wit:dev` with issue #<n> as the
seed."

### D2 · Draft on disk first (OKF), then `gh`

Mirror ship's `PR.md` pattern:

1. Write `.wit/issues/<slug>.md` with OKF frontmatter + body.
2. User confirms (or `--auto`).
3. Strip frontmatter → temp body file → `gh issue create --body-file …` (plus metadata flags).
4. Append the created issue URL/number back into the draft frontmatter (`github_issue: <n>`,
   `url: …`) and optionally commit the draft under the project's wit-commit rule.

Rationale: durable draft if create fails; reuse for re-file; keeps OKF as the source of truth; agents
can re-read the issue without scraping GitHub.

### D3 · Fixed body sections (bug-first template)

Required sections, in this order:

```markdown
## Summary

## Steps to reproduce

## Actual results

## Expected results

## Root cause

## Proposed fix

## Acceptance criteria
```

Rules:

- **Summary:** 2–5 sentences; problem + impact; no dump of logs here.
- **Steps to reproduce:** numbered; concrete inputs/commands; "N/A — not a repro bug" only when
  type ≠ Bug (see D5).
- **Actual / Expected:** observable behavior, not speculation.
- **Root cause:** fill when known (code pointer, hypothesis with evidence); otherwise `Unknown —
  needs investigation` (never invent).
- **Proposed fix:** optional direction; not a full design. `TBD` allowed.
- **Acceptance criteria:** checklist of observable done-states. **Hard rule for Bug (and default for
  this skill):** at least one criterion requires a **new automated test** that fails on the bug and
  passes after the fix (name the test area / suggested test id when possible). Other criteria cover
  product behavior and regressions.

Optional trailing sections (include only when they have content):

- `## Environment` (OS, versions, flags)
- `## Evidence` (logs, screenshots links, failing command output tails)
- `## Out of scope`
- `## References` (related PRs, docs, ADRs)

### D4 · Title conventions

- Prefer: `<area>: <symptom in user terms>` (e.g. `ship: PR body keeps OKF frontmatter`).
- Cap ~72 chars; no trailing period; no issue-number prefix.
- Agent proposes; user can override at the confirm gate.

### D5 · GitHub metadata — use everything `gh` exposes

Create path (GitHub CLI ≥ 2.94.0 for hierarchy/deps; degrade gracefully on older `gh` / GHES):

| Capability | Flag / mechanism | Skill behavior |
|------------|------------------|----------------|
| Title | `--title` | Required |
| Body | `--body-file` | Stripped OKF body |
| Issue type | `--type` | Default `Bug` when filing a defect; ask if ambiguous. Discover org types via API/`gh` when available; skip with a log line if unsupported |
| Labels | `--label` | Propose from repo label list (`gh label list`); prefer existing labels; never invent label names that don't exist unless user asks to create them (`gh label create`) |
| Assignees | `--assignee` | Optional; ask or leave unset |
| Milestone | `--milestone` | Optional; list open milestones |
| Projects | `--project` | Optional when Projects v2 is connected |
| Parent (sub-issue) | `--parent` | When this issue is a child of an epic/parent |
| Blocked by | `--blocked-by` | Dependencies that must land first |
| Blocking | `--blocking` | Issues this one unblocks (rare at create time) |
| Template | `--template` | See Open questions |

After create, optionally:

- `gh issue edit <n> --add-sub-issue …` if children were planned as separate drafts.
- Pin / comment with a short "Filed by wit add-issue" is **out** (no AI attribution noise; matches
  ship guardrail).

**Degradation:** if a flag fails (org has no issue types, old GHES, missing project permission), log
`skipped <capability> (<reason>)`, still create the issue with what works, and surface skips in the
confirm gate / final report.

### D6 · Dialogue shape (interactive, few rounds)

Not a monologue. Batch questions; wait for answers. Suggested rounds:

1. **Seed:** what's broken / what's wanted? (or accept pasted notes / stack traces)
2. **Classify:** type (Bug / Feature / Task / …), severity/priority if labels encode them, area
3. **Repro & outcomes:** steps, actual, expected (skip or lighten for non-Bug)
4. **Cause & fix:** known root cause? proposed direction? related issues?
5. **Ship metadata:** labels, milestone, parent, blockers, assignees
6. **Confirm gate:** show title + metadata table + rendered body; create / edit / abort

`--auto`: skip the confirm gate only after rounds 1–5 are filled with best-effort defaults (and log
assumptions). Still write the OKF draft.

**Code peek (optional, bounded):** if the user points at a file/error, a short investigate pass may
fill Root cause / Proposed fix / test AC. Keep it under the context budget — no whole-tree reads;
prefer the failing test or stack frame.

### D7 · Dedup before create

Before the confirm gate:

1. `gh issue list --state open --search "<key symptoms>"` (and/or title keywords).
2. If a likely duplicate exists, show it and ask: link as related / comment instead / create anyway /
   abort.

### D8 · Flat alias + bootstrap

Ship `references/skill-aliases/wit-add-issue/SKILL.md` (forwarder like wit-scan). Extend scan's
plugin-bootstrap / alias install list so Copilot / Codex / Grok get `/wit-add-issue` and
`$wit-add-issue`. Update `AGENTS.md` and platform tool maps to list add-issue as user-facing.

### D9 · Local OKF shape

```markdown
---
type: Issue Draft
title: "<same as GitHub title>"
description: "<one-line summary>"
timestamp: <YYYY-MM-DD>
status: draft | filed | abandoned
repo: <owner/name>
github_issue:           # filled after create
url:
issue_type: Bug
labels: [bug, area:ship]
assignees: []
milestone:
parent:
blocked_by: []
blocking: []
project:
tags: [issue, bug]
---

# <title>

## Summary
…
```

Slug: short kebab from title (`ship-pr-body-frontmatter`), uniquified if needed.

## Procedure sketch (what `SKILL.md` would say)

1. Resolve plugin root (Grok/Copilot protocol); confirm `gh auth status` and repo (`gh repo view`).
2. Dialogue + optional bounded code peek.
3. Dedup search.
4. Write `.wit/issues/<slug>.md`.
5. Confirm gate (unless `--auto`).
6. `gh issue create` with metadata; on partial failure, edit what can be set.
7. Update draft frontmatter; report URL + skipped capabilities + optional `/wit:dev` handoff.

Design rationale (the "why") lives later in `docs/design-notes/add-issue.md` after acceptance — not
loaded at runtime.

## Acceptance criteria (for implementing *this* skill)

1. `skills/add-issue/SKILL.md` exists, `user-invocable: true`, description triggers on natural language
   bug/issue filing.
2. Body template enforces the seven sections above; Bug AC requires ≥1 new-test criterion (validated by
   skill text + a unit/fixture test on any helper that checks drafts).
3. Create path uses `gh issue create` with `--body-file` after stripping OKF frontmatter (same awk
   pattern as ship).
4. Metadata: type, labels, assignees, milestone, project, parent, blocked-by, blocking are attempted
   when provided; unsupported capabilities degrade with an explicit skip log.
5. Flat alias `wit-add-issue` ships; scan bootstrap installs it; AGENTS.md + tool maps mention it.
6. Dedup step runs before confirm; documented in the skill.
7. `python scripts/validate.py` + existing tests green; new tests cover draft frontmatter strip and
   section presence.
8. No AI attribution in the GitHub issue body.

## Open questions (for review)

These are the discussion points before we lock the design:

1. **Scope of types:** Bug-only skill, or first-class Feature / Task / Chore with section variants
   (e.g. Feature drops "Steps to reproduce" or renames to "Motivation")?
2. **Repo issue templates:** Prefer wit's body always, start from `.github/ISSUE_TEMPLATE/*` when
   present, or ask each time?
3. **Commit the draft?** Always commit `.wit/issues/*.md` on main (wit-directory project rule), never,
   or only when constitution allows wit commits?
4. **Roadmap hook:** For the witloop repo itself, also append a row to `docs/roadmap.md`? For other
   repos, write/update `.wit/roadmap.md` if present?
5. **Severity model:** Encode severity only via labels, or add a `severity:` frontmatter field +
   body callout?
6. **Multi-issue / epic mode:** One parent + N sub-issue drafts in one session, or always one issue
   per invocation?
7. **`--draft`:** GitHub issues aren't draft-PRs; do we keep "draft" as local-only until confirm, or
   create immediately as open and rely on labels like `needs-triage`?
8. **Test AC strictness:** Always require a new test for Bug, or allow "manual repro checklist only"
   with an explicit user override at the gate?
9. **Naming:** Stick with `add-issue`, or prefer `file-issue` / `bug` / `report`?

## Out of scope follow-ups

- `wit:triage` — batch label/milestone/parent cleanup.
- Auto-closing issues from ship (`Closes #n` already lives in ship PR bodies).
- Syncing GitHub → `.wit/issues/` for issues created outside wit.

## Citations

1. GitHub Changelog — Issues hierarchy/types/deps in CLI (2026-06-10):
   https://github.blog/changelog/2026-06-10-manage-sub-issues-types-and-dependencies-from-github-cli/
2. GitHub CLI 2.94.0 — `gh issue create --type / --parent / --blocked-by / --blocking`
3. wit ship body-strip pattern — `skills/ship/SKILL.md` (PR.md → `gh pr create --body-file`)
4. OKF profile — `docs/specs/2026-06-14-okf-knowledge-format.md`
5. Flat aliases — `skills/scan/references/plugin-bootstrap.md`, `references/skill-aliases/`
