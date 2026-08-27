---
type: ADR
title: Generic PLUGIN_ROOT on every host
description: Skills use ${PLUGIN_ROOT}; every host including Claude resolve-once then stamps an absolute path. CLAUDE_PLUGIN_ROOT is an env alias, not a special case.
feature: plugin-root-generic
status: accepted
timestamp: 2026-08-27
---

# ADR-0003: Generic PLUGIN_ROOT on every host

- **Status:** accepted
- **Date:** 2026-08-27
- **Deciders:** owner
- **Amends:** ADR-0001 plugin-root order (env-first cell)

## Context

Skills were written with `${CLAUDE_PLUGIN_ROOT}` because Claude Code injects that env. Other hosts
were told: if you are not Claude, rewrite the placeholder. That made Claude the default and every
other host a fork. Cursor and Grok usually have an empty env anyway, so the rewrite was the real
protocol. The Claude-branded name kept agents treating non-Claude as second-class.

## Decision

1. The placeholder in skills, agents, and references is `${PLUGIN_ROOT}`.
2. Every host including Claude follows the same resolve-once order in
   `references/capabilities.md` **Plugin root**, then uses the stamped absolute path.
   Never pass an unexpanded `${PLUGIN_ROOT}` into the shell.
3. Env aliases for step 1, first non-empty that is a wit root: `PLUGIN_ROOT`,
   `WIT_PLUGIN_ROOT`, `CLAUDE_PLUGIN_ROOT`, `GROK_PLUGIN_ROOT`. Claude's native
   `CLAUDE_PLUGIN_ROOT` is one alias, not a host if-tree.
4. `validate.py` resolves `${PLUGIN_ROOT}/...` refs and rejects leftover
   `${CLAUDE_PLUGIN_ROOT}` placeholders in live skills, agents, references, AGENTS.md, and README.md.

## Consequences

- **Positive:** one protocol. Claude still works when its env is set (step 1 hits). Cursor, Grok,
  and Copilot stop pretending they must "replace Claude's variable."
- **Negative / costs:** Claude agents must stamp and use the absolute path instead of relying on
  shell expansion of `CLAUDE_PLUGIN_ROOT`. Frozen archives (`docs/plans/`, `docs/specs/`) keep the
  old placeholder.
- **Follow-ups:** none required. Host cache paths stay in adapters (step 3).
