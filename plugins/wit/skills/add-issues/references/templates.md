---
type: Reference
title: "add-issues: per-type draft templates"
description: >
  Body templates and draft frontmatter for Bug, Feature, and Task issues filed by add-issues.
  Each complete example is what lands in .wit/issues/<slug>.md before the confirm gate.
timestamp: 2026-07-19
tags: [add-issues, templates, github, okf]
---

# add-issues templates

Read the section for the classified type. Every draft is a complete Markdown file: OKF
frontmatter (carries what gets passed to `gh issue create`) plus the type's body sections in
the given order. Frontmatter is stripped before publish; the whole file is deleted once the
issue is live - drafts never outlive the run.

Optional trailing sections (any type) - include only when non-empty:
`## Environment` · `## Evidence` · `## Out of scope` · `## References`

## Bug

```markdown
---
type: Issue Draft
title: "<area>: <symptom in user terms>"
description: "<one-line summary>"
timestamp: <YYYY-MM-DD>
issue_type: Bug
labels: []
assignees: []
milestone:
parent:
blocked_by: []
---

# <area>: <symptom in user terms>

## Summary
<2-5 sentences: what breaks and who it hurts. No log dumps here.>

## Steps to reproduce
1. <numbered, concrete commands / inputs>

## Actual results
<observable behavior>

## Expected results
<observable behavior>

## Root cause
<code pointer or evidence-backed hypothesis - else: Unknown - needs investigation>

## Proposed fix
<optional direction. If several viable approaches exist, list them briefly and recommend one
with the why. TBD allowed.>

## Acceptance criteria
- [ ] New test `<suite / path / test id>` fails on the bug and passes after the fix
- [ ] <behavior restored, stated observably>
- [ ] <no regression in the adjacent area>
```

## Feature

```markdown
---
type: Issue Draft
title: "<area>: <outcome in user terms>"
description: "<one-line summary>"
timestamp: <YYYY-MM-DD>
issue_type: Feature
labels: []
assignees: []
milestone:
parent:
blocked_by: []
---

# <area>: <outcome in user terms>

## Summary
<2-5 sentences: the capability and its value>

## Motivation
<problem being solved, who hits it, why now>

## Proposed solution
<user-visible behavior; a sketch, not a design doc>

## Alternatives considered
<optional - include only if real alternatives were discussed; omit the heading when empty>

## Acceptance criteria
- [ ] <observable behavior>
- [ ] Tests cover the new behavior in `<area>`   ← required whenever code behavior changes
```

## Task

```markdown
---
type: Issue Draft
title: "<area>: <what gets done>"
description: "<one-line summary>"
timestamp: <YYYY-MM-DD>
issue_type: Task
labels: []
assignees: []
milestone:
parent:
blocked_by: []
---

# <area>: <what gets done>

## Summary
<what gets done>

## Context
<why this work exists; link parent / spec / ADR>

## Acceptance criteria
- [ ] <definition of done as observable checkboxes>
```

## Filing notes

- Titles: `<area>: <symptom or outcome>` - e.g. `ship: PR body keeps OKF frontmatter`,
  `scan: support GHES capability probe`.
- Checklist items are observable done-states, not activities - "returns 403 for expired
  tokens", not "look into auth".
- "Chore" and "refactor" requests map to Task unless the org defines a dedicated issue type.
