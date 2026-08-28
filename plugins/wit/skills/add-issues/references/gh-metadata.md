---
type: Reference
title: "add-issues: gh metadata matrix"
description: >
  Create-time and post-create gh issue flags for type, labels, milestone, assignees, parent,
  blocked-by/blocking, and projects; version gates and the degradation contract.
timestamp: 2026-07-19
tags: [add-issues, github, gh, metadata]
---

# gh metadata matrix

Probe once per session: `gh --version`. Hierarchy, dependency, and type flags ship in
**gh ≥ 2.94.0** and work only where the repo/org has the corresponding feature enabled
(issue types are configured at the org level; GHES lags GitHub.com).

## Create-time flags

| Capability | Flag on `gh issue create` | Needs | Post-create fallback | On failure |
|---|---|---|---|---|
| Title | `--title` | - | `gh issue edit --title` | required - abort |
| Body | `--body-file` | - | `gh issue edit --body-file` | required - abort |
| Issue type | `--type Bug` | gh ≥ 2.94, org types configured | `gh issue edit` type flags | skip + log |
| Labels | `--label a --label b` | labels must already exist | `gh issue edit --add-label` | skip + log |
| Assignees | `--assignee login,@me` | - | `gh issue edit --add-assignee` | skip + log |
| Milestone | `--milestone "<title>"` | open milestone exists | `gh issue edit --milestone` | skip + log |
| Parent (sub-issue) | `--parent <n or url>` | gh ≥ 2.94 | `gh issue edit <parent> --add-sub-issue <n>` or `gh issue edit <n> --set-parent` | skip + log |
| Blocked by | `--blocked-by 200,201` | gh ≥ 2.94 | `gh issue edit --add-blocked-by` | skip + log |
| Blocking | `--blocking 300` | gh ≥ 2.94 | `gh issue edit --add-blocking` | rarely known at create - v2, only on explicit user mention |
| Project | `--project "<title>"` | Projects v2 + `project` auth scope | `gh project item-add` | v2 - commonly fails on missing scope; log `skipped project (needs: gh auth refresh -s project)` |
| Repo template | `--template "<name>"` | `.github/ISSUE_TEMPLATE/` | - | explicit user request only |

## Degradation contract

1. Attempt create with everything supplied.
2. On a failing flag: drop it, create with what works.
3. Try the post-create fallback for each dropped capability.
4. Anything still unset → `skipped <capability> (<reason>)` in the confirm gate preview and
   the final report.

Never let optional metadata block creation.

## Discovery commands

- Labels: `gh label list --limit 100`
- Milestones: `gh api repos/{owner}/{repo}/milestones --jq '.[].title'`
- Issue types: no list command needed - attempt `--type`; an error means the org has none
  configured, so skip and log.
- Existing issues (dedup): `gh issue list --state open --search "<terms>" --limit 10`
