---
type: Reference
title: "Investigation: read-only cited exit"
description: "How /wit:dev finishes a read-only investigation after work type is announced: detect how and optional why, delegate or fall back, cite sources, and stop without .wit/ state or a PR."
timestamp: 2026-08-25
tags: [dev, investigation, understand, how, reference]
---

# Investigation: read-only cited exit

This file is enough to decide when loaded alone. Work type is already announced as `investigation`.
Follow this file, finish this turn, and STOP. Do not re-classify. `--auto` is a no-op (there is no
gate). The announcement is already printed; do not invent a second work-type line.

There is no skills/investigate/ skill and none should be created. Who initiates: wit, not
description-match. Investigation is an exit, not a loop phase.

## Skip writes

Skip all of these this turn:

- setup (do not run setup; no first-run writes)
- scan writes (`repo-map.md`, constitution, and any `--refresh` write)
- `.wit/models.md` create
- `.wi/` rename
- keep-alive print (no keep-alive block)
- token ledger
- feature folder, dossier seed, and `progress.md` create

If `.wit/repo-map.md`, constitution, or `.wit/adr/` already exist, **read** them as evidence. If they
do not, explore the live tree. Do not run setup or scan to create them.

Host and plugin-root resolve may run **in memory** so `discover_skills.py` can be invoked. Do not
stamp `progress.md`.

## Detect optional skills

Run the full union (never stamp absent from memory; stamp absent only after the union misses):

```shell
python ${PLUGIN_ROOT}/skills/research/scripts/discover_skills.py --name how
```

If the question is motivational, also run:

```shell
python ${PLUGIN_ROOT}/skills/research/scripts/discover_skills.py --name why
```

Delegation is mandatory when `how` is present. Resolve the `SKILL.md` path in memory (pointer
protocol). Do not write progress.md Skill paths. Read that `SKILL.md` and follow Explain (default)
or a recommendation-shaped Critique. Do not dispatch pinned runners for this exit.

`why` is OPTIONAL extra for motivational questions only. Never a required MCP sweep. Skip if absent
or if the question is mechanical ("how does X work?"). If `why` is present and the question is
motivational, wit initiates it; if it no-ops without MCPs, still cite git / `gh` / in-repo docs and
label gaps.

Do not add `how` or `why` to scan's recommended install set from this route. Investigation must work
standalone.

## Mode line (in the reply, not progress.md)

Print exactly one of these in the chat reply (not progress.md):

- `investigation via how`
- `investigation via how + why`
- `investigation via wit fallback (how absent)`

Use `how` when that skill is present. Add `+ why` only when `why` actually ran. Use the fallback line
when `how` is absent.

## Portable fallback (when `how` is absent)

Encode the method here. Do not vendor external prompt files. No new named agent.

- **Simple** (one module, one symbol, one flow): the orchestrator explores with Read / Grep / Glob /
  read-only git and writes the answer. No subagent. When in doubt, lean simple.
- **Complex** (cross-cutting subsystem): at most two generic read-only explorer dispatches (generic
  Task / host `subagent` cell; NOT `wit-researcher`, NOT `wit-task-runner`, NOT `wit-code-checker`),
  then the orchestrator synthesizes. Cap 2. Explorers return components, flow, files read, and
  non-obvious notes. The explainer output is the user-facing how-shape.

Do not document `readonly: true` as universal. Host Task schemas lack a uniform readonly flag. The
portable guarantee is this prompt contract plus the deny-list.

## Output contract

Announcement already printed. Then the mode line. Then one of:

- **Explain:** Overview; Key Concepts; How It Works; Where Things Live; Gotchas.
- **Decide:** a recommendation plus a short tradeoffs table, then the same Sources block.

**Citations (every non-obvious claim):**

- Code: `path:N` or `path:symbol` locators (constitution `name:N` form; never the section sign).
- Git: commit hash and/or `gh` PR number when used.
- External: URL. Training-data claims are labeled inference, not fact.
- Close with `## Sources` (files, commits, PRs, gaps). Null searches are first-class when a
  why-shaped question was asked.

Apply unslop to the reply. Do not require critic panels or an arena.

## Hand-back

If the user actually needs a change: say so, name `--kind feature` or `--kind bug-fix`, and
do not start brainstorm. Hand back. Do not open a dossier from this turn.

## Deny-list (explicit forbids)

The route must not:

- Create or edit `.wit/features` (no feature dossier)
- Write `progress.md`
- Write `brief.md`, `tokens.md`, ADRs, `roadmap.md`, or `.wit/models.md`
- Run scan writes
- Invoke setup
- Print or arm keep-alive
- Create a branch, worktree, commit, or PR
- Make product-file edits
- Dispatch `wit-researcher`, `wit-task-runner`, or `wit-code-checker`
- Invoke brainstorm / research / plan / build / ship

Allowed: Read, Grep, Glob, WebSearch/WebFetch, `discover_skills.py`, read-only git (`status`, `log`,
`blame`, `show`, `rev-parse`), `gh view` / list. Shell must not redirect into the repo.

Exit check: `git status --porcelain` (or host equivalent). Ignore pre-existing dirt. New paths under
`.wit/features` or edited product files from this turn are a defect; stop and do not present the
answer as successful until those writes are undone. Do not `git checkout` user files to "clean" them.

## Exit

Success is a cited answer in this turn, git state for product plus `.wit/` unchanged by this turn,
and the session not armed to continue into research. There is no Phase = done because there is no
`progress.md`. Do not invent a shadow log. No keep-alive block.

Mid-run "how does X work?" during an in-flight feature is out of scope (that is a later `understand`
call from research). This file only covers `/wit:dev` classified as investigation from the start.
