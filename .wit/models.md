---
type: Model Routing Config
title: Model assignments (Witloop)
description: Per-role model assignments for wit-dispatched agents (preset: custom).
preset: custom
timestamp: 2026-08-19
---

# Model assignments

Owner override (2026-08-19): every dispatch uses Cursor Grok 4.6 xhigh. Canonical tiers stay `fable` so the checker floor and researcher/task-runner rules are not silently weaker; the Cursor column maps every tier to the same concrete id.

## Roles
| Role | Model | Notes |
|------|-------|-------|
| orchestrator | fable | informational: session model (Cursor Grok 4.6 xhigh) |
| wit-code-checker | fable | never below orchestrator; same Cursor id |
| wit-researcher | fable | owner: not one-tier-below |
| wit-task-runner | fable | owner: not the cheaper volume tier |

## Cross-provider config
| Key | Value |
|-----|-------|
| provider | none |
| base_url | |
| model | |
| api_key_env | |
| check_points | at-finish |

## Per-agent overrides
| Agent | Model |
|-------|-------|

## Mixture of Agents
| Key | Value |
|-----|-------|
| points | none |
| proposers | opus, sonnet, sonnet |
| layers | 1 |
| aggregator | opus |

## Platform model map
| Tier | grok | cursor |
|------|------|--------|
| fable | grok-4.5 | cursor-grok-4.6-xhigh |
| opus | grok-4.5 | cursor-grok-4.6-xhigh |
| sonnet | grok-composer-2.5-fast | cursor-grok-4.6-xhigh |
| haiku | grok-composer-2.5-fast | cursor-grok-4.6-xhigh |
