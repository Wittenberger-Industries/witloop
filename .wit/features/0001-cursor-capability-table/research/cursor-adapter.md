---
type: Research Note
title: "Cursor adapter cells: keep-alive, skill discovery, ask, subagent, models"
description: "How those five capabilities currently fork on host names, and the single recommended Cursor row plus keep-alive reshape."
feature: 0001-cursor-capability-table
timestamp: 2026-08-19
valid_until: 2026-08-26
---

# Cursor adapter: keep-alive, skill discovery, ask, subagent, models

Repo-question charter. Table placement, token dispatcher, and POSIX helpers are sibling scope; this note only fills the five cells named above plus the adapter/wiring they require.

## Responsibility Map

Plugin/docs layer (not an app frontend/backend): keep-alive templates, host tool maps, skill-discovery search order, model platform map, bootstrap offer. Runtime stamp lives in `progress.md`. Python that already parses the platform map (`skills/ship/scripts/cross_review.py`) is a consumer of the models cell, not new product code.

## How it branches today (host names)

There is no capability table. Four hosts are named in adapters and always-loaded skills. Cursor is live but unnamed. [VERIFIED: README.md platform table; AGENTS.md; `references/keep-alive.md`; issue #89]

| Capability | Claude | Codex | Copilot | Grok | Cursor today |
|---|---|---|---|---|---|
| `plugin_root` | native `${CLAUDE_PLUGIN_ROOT}` | compat env | install dir / clone | resolve-once (env usually empty; `installed_plugins.json`) | env empty; undocumented |
| `subagent` | named Agent/Task | inline `spawn_agent` | `task` / `/fleet` | inline `spawn_subagent` (`general-purpose`) | undocumented; both named and inline observed |
| `keep_alive` | predicate `/goal` | predicate `/goal` | Autopilot relaunch | model-judged `/goal` (`update_goal`) | undocumented; chat already persists |
| `ask` | `AskUserQuestion` | (no map row) | (no map row) | `ask_user_question` | undocumented; Cursor `AskQuestion` exists |
| `skill_invoke` | `/wit:dev` plugin namespace | `$wit-dev` / `$dev` | `/wit-dev` / `/wit dev` | `/wit-dev` / `/dev` | plugin skills + NL auto-trigger (observed) |
| `models` | Claude tier tokens as-is | claude-tier host (no column) | claude-tier host (no column) | `## Platform model map` `grok` column; host = "following grok-tools.md" | `.wit/models.md` already has a `cursor` column; `references/models.md` does not document it |

### keep-alive: three host-named blocks

`references/keep-alive.md` is the SSOT. It is keyed by product, not capability. [VERIFIED: `references/keep-alive.md`]

1. **Claude Code / Codex CLI**: one-line `/goal` predicate. Multi-line paste is a documented footgun (only the first line registers).
2. **GitHub Copilot CLI**: `copilot --autopilot --max-autopilot-continues <N> --no-ask-user --allow-all -p "..."`. Unattended-run warning is mandatory.
3. **Grok Build**: same `/goal` text as (1) but labeled **model-judged** (`update_goal`). Third family added in #43; validate.py hard-requires `"Grok Build"` + `"update_goal"` in this file. [VERIFIED: `scripts/validate.py` lines 156-158]

Callers still pick a block by guessing the host:

- `skills/dev/SKILL.md` step 4: "print the keep-alive handoff for the **current platform** verbatim from keep-alive.md" and lists `/goal` / Grok `/goal` / Autopilot. Go-signal is hard-coded: "Pasting the `/goal` line is the go." [VERIFIED: `skills/dev/SKILL.md`]
- `skills/research/SKILL.md` step 4: same host list; "Pasting the `/goal` line is the go." [VERIFIED: `skills/research/SKILL.md`]
- `AGENTS.md` persistence bullet and README install/platform table repeat the same three names. Cursor is absent. [VERIFIED: `AGENTS.md`; `README.md`]
- `references/workflow.md` mermaid still says "kept alive by `/goal` or Autopilot". [VERIFIED: `references/workflow.md`]

validate.py also requires the strings `autopilot` and `grok` inside `skills/dev/SKILL.md` and `skills/research/SKILL.md`. [VERIFIED: `scripts/validate.py` lines 160-165] That is the host-fork tax: adding Cursor as a fifth named branch in those SKILL bodies would be the rejected #43 copy.

Cursor Autopilot is a **different product**: the Cursor `autopilot` skill triages an existing PR (conflicts, comments, CI). It is not wit persistence. [VERIFIED: `C:\Users\sergi\.cursor\skills-cursor\autopilot\SKILL.md`; constitution Out of scope; issue #89]

Cursor `/loop` exists (fixed or dynamic sentinel wake). It can re-wake a chat; it is optional documentation, not the keep-alive capability. [VERIFIED: Cursor `loop` skill + this session's `/loop` command]

### skill discovery: Claude-registry shaped

`skills/research/references/integrations.md` "How to detect an available skill": session skills list **or** directory under a known path. Deterministic sources named today: `~/.claude/plugins/installed_plugins.json` (`installPath` / `skills/`) and flat `~/.agents/skills/`. Grok is told to read the same Claude registry. **Never stamp `(skill absent)` from memory.** [VERIFIED: `skills/research/references/integrations.md`]

`skills/scan/references/plugin-bootstrap.md` is looser for the install **offer** (treat unsure as missing) and stricter for run-time delegation (point at integrations.md). The offer itself prints Claude `/plugin marketplace add` + `/plugin install`. [VERIFIED: `plugin-bootstrap.md` Recommended set + The offer]

Missing from the union: `~/.cursor/plugins/cache/**/skills`. This machine has Superpowers and wit there. A run that only checks the Claude registry can stamp Superpowers absent while it is loaded. [VERIFIED: this session's skill list includes `C:\Users\sergi\.cursor\plugins\cache\cursor-public\superpowers\...` and `C:\Users\sergi\.cursor\plugins\cache\wittenberger-industries-witloop\wit\<hash>\skills\...`; issue #89]

### ask: Claude name in skills, one Grok map row

Always-loaded skills say `AskUserQuestion` (scan, brainstorm, research design gate, plugin-bootstrap). [VERIFIED: those SKILL.md / reference files] Only `references/grok-tools.md` maps it (`ask_user_question`). Codex and Copilot maps have no Ask row.

Cursor's fixed-choice tool is `AskQuestion`. Cursor's own skills require it for option lists and fall back to prose if it is missing. [VERIFIED: Cursor `onboard` / `create-skill` SKILL.md] Exact JSON field names are not in this repo; the brief/issue lock `id` + `prompt` + `options`.

### subagent: four host sentences, named vs inline already split

`skills/build/references/worktrees-and-subagents.md` "Subagent dispatch": Claude named `wit-task-runner`; Codex/Grok inline the charter because named registration is unreliable (Codex across builds; Grok `color` drop). Copilot uses `task` / `/fleet`. Prompt **content** is inline on every platform; the dispatch **target** differs. [VERIFIED: `worktrees-and-subagents.md`; `references/grok-tools.md` "Subagent dispatch (inline, Codex-style)"; `references/codex-tools.md` "Subagent caveat"]

Agent frontmatter (`agents/*.md`): `name: wit-*`, `model: inherit`, Claude tool lists (`Read`, `Grep`, `Glob`, `Bash`, `Write` / `Edit`). Constitution: do not change charter tool lists unless the spec names that. [VERIFIED: the three agent files; constitution Architecture]

Cursor evidence, two states of the same contract:

- 2026-07-19 dry-run: "Host: Cursor; no `wit-*` subagent types, so researcher / task-runner / checker ran inline." [VERIFIED: `docs/plans/2026-07-19-learnings-lifecycle-dryrun.md`]
- 2026-08-19 this session: Task `subagent_type` enum includes `wit-code-checker`, `wit-researcher`, `wit-task-runner`. [VERIFIED: this session Task tool]

Missing named types is already a successful fallback. Making named types a hard failure would regress July 19.

### models: grok column + "else claude"; cursor column already in this repo's config

`references/models.md` "Platform model resolution": canonical tiers `fable|opus|sonnet|haiku`. Optional `## Platform model map` columns are host names. **Host detection today:** host is `grok` when the run follows `references/grok-tools.md`; otherwise `claude`. Codex/Copilot stay claude-tier unless they gain a column. [VERIFIED: `references/models.md`]

Parser already treats extra columns as hosts: `platform_model_for(agent, cfg, host)` looks up `cfg["platform_map"][host][tier]`. [VERIFIED: `skills/ship/scripts/cross_review.py` `parse_models_config` / `platform_model_for`] Tests only cover `grok` and `claude`. [VERIFIED: `tests/test_models_config.py` `PlatformMapTest`]

This project's `.wit/models.md` already has `| Tier | grok | cursor |` and maps **every** Cursor tier to `cursor-grok-4.6-xhigh` (owner override 2026-08-19). [VERIFIED: `.wit/models.md`] This feature's `progress.md` resolved block already records those concrete ids. [VERIFIED: `.wit/features/0001-cursor-capability-table/progress.md`]

Live Task model slugs this session: `inherit`, `composer-2.5-fast`, `cursor-grok-4.6-xhigh` (plus other vendor ids wit must not auto-pick). [VERIFIED: this session Task tool] The workspace fallback id `cursor-grok-4.5-high` (AGENTS.md subagent rule when `.wit/models.md` is absent) is **not** on that list. Adapter ids must be the live slugs, not the stale fallback.

## Cursor plugin-root (needed to fill the row)

`CLAUDE_PLUGIN_ROOT`, `PLUGIN_ROOT`, and `CURSOR_PLUGIN_ROOT` are all empty in this Cursor agent shell. [VERIFIED: this session env] Same class of bug Grok hit (hook-only / unset). [VERIFIED: `references/grok-tools.md` resolve-once]

This run stamped `Plugin root (resolved): D:\ClaudeCowork\wi-plugin\wi-plugin` (the source tree), not the marketplace cache hash. [VERIFIED: this feature `progress.md`] Cache **does** exist: `C:\Users\sergi\.cursor\plugins\cache\wittenberger-industries-witloop\wit\<hash>\` with `skills/` + `.claude-plugin/` (marketplace copy at 1.13.4). [VERIFIED: cache listing + that copy's `plugin.json`]

Issue #89 / the dispatch list env then cache then walk-up. **Do not follow that order blindly.** If cache beats walk-up, a Cursor session opened **on the wit source repo** binds the stale marketplace copy. Recommend Grok's validate-the-winner rule with a Cursor-specific cwd-first step:

1. `$CLAUDE_PLUGIN_ROOT` / `$PLUGIN_ROOT` / `$CURSOR_PLUGIN_ROOT` if non-empty **and** the path contains `skills/` + `.claude-plugin/` + `skills/scan/SKILL.md`.
2. If **cwd itself** is a wit root (same three tells), use cwd. This is how source-repo dogfood stays on the tree being edited.
3. Else the Cursor plugin cache: under `~/.cursor/plugins/cache/`, a directory that validates as a wit root (observed layout `wittenberger-industries-witloop/wit/<hash>/`). Prefer the install that matches plugin id `wit`.
4. Walk up from cwd for an ancestor wit root (clone / `--plugin-dir` when cwd is a nested folder).
5. Stamp `Plugin root (resolved): <abs>` in `progress.md` once; later phases read it. Never pass an unexpanded `${CLAUDE_PLUGIN_ROOT}` into the shell.

## Recommended Cursor capability cells

| Capability | Cursor cell (lock this) |
|---|---|
| `plugin_root` | resolve-once order above; env usually empty |
| `subagent` | `Task` with `subagent_type=wit-task-runner` / `wit-researcher` / `wit-code-checker` **when those names appear in this session's Task list**; else generic Task + inlined `agents/*.md`. Missing named types is not a hard failure. |
| `keep_alive` | `none`. Chat persists. Optional `/loop` documented for after `Phase=done`. Never Claude `/goal`. Never Copilot Autopilot. Never Cursor Autopilot. |
| `ask` | `AskQuestion` (`id` + `prompt` + `options`). If the tool is absent, same question in prose (Cursor onboard already requires that fallback). |
| `skill_invoke` | plugin skills (Cursor marketplace cache) + natural-language auto-trigger from skill `description`. Slash forms are adapter sugar; descriptions are the real entry. No `~/.agents/skills` alias copy required on Cursor. |
| `models` | `cursor` column in `## Platform model map`. Resolve from stamped `Host: cursor` through `platform_model_for(..., "cursor")`. Concrete ids live in `cursor-tools.md`: `cursor-grok-4.6-xhigh`, `composer-2.5-fast`, `inherit`. This repo maps every tier to `cursor-grok-4.6-xhigh`. |

Tokens / shell are sibling cells. Adapter still needs a short tokens policy section so ship does not guess: Orchestrator `unavailable`; do not run `token_report.py`; Duration from `progress.md`. Details owned by token-dispatcher.

## Decision: keep-alive.md reshape (capability keys, not a fifth host fork)

**Use this.** Rewrite `references/keep-alive.md` as a table keyed by capability. Hosts are an index onto a key, not a new template.

| keep_alive | Hosts | What to print | Go-signal (move out of dev/research SKILL bodies) |
|---|---|---|---|
| `predicate_goal` | claude, codex | existing one-line `/goal` | pasting `/goal` (platform echoes Goal set) |
| `model_judged_goal` | grok | existing `/goal` text + model-judged / `update_goal` warning | pasting `/goal` |
| `relaunch` | copilot | existing Autopilot command + unattended warning | running the Autopilot command |
| `none` | cursor | template below | answering the ask-capability question "Ready to hand off?" |

dev:4 / research:4 become: read stamped `keep_alive` (from the host probe / capability table), print **that** block from keep-alive.md. No "current platform" sentence. No "Pasting `/goal` is the go" in the SKILL body (that line is false on Cursor and on Copilot).

### `none` template text (print this)

```
Keep-alive: none. This Cursor chat already persists until you close it. Do not paste Claude `/goal`. Do not relaunch Copilot Autopilot. Do not treat Cursor Autopilot as wit persistence (that skill triages an existing PR; it does not drive research -> build -> ship). Optional: after Phase is done you may use Cursor `/loop` to re-wake this chat; that is not wit keep-alive.

Done when: the <slug> PR is open with its remote checks green (or none configured) and its branch passes <lint + test commands from repo-map.md>; .wit/features/<slug>/progress.md Phase is done. Constraints: only files named in tasks.md change; never force-push; tests are never weakened to pass.
```

Fill rules stay: drop `n/a - not configured` commands; no remote → print nothing (ship:7 local close-out). Interactive still asks ready-to-hand-off via `ask`; auto-approve skips the reprint the same as today.

### Rejected keep-alive options

- **Fifth host bullet "Cursor"** in keep-alive.md, mirroring Grok's additive branch. Fast, and validate.py already thinks in host strings. Rejected: issue #89 and the brief forbid another product fork; Gemini would be a sixth rewrite. Grok already proved a third family does not scale. [VERIFIED: issue #89; `docs/roadmap.md` #43 note]
- **Treat `/loop` as keep-alive.** It can persist a chat, but it is a Cursor skill the user opts into, not a predicate wit arms at brainstorm. Rejected as the capability value; allowed as optional docs inside `none`.
- **Treat Cursor Autopilot as `relaunch`.** Wrong product. [VERIFIED: autopilot SKILL.md]

## Decision: skill-discovery search order

Stamp `(skill absent)` only after this union fails. Session list still wins when it lists the skill.

1. Session skills list.
2. Resolved plugin root `skills/<name>/SKILL.md` (the stamped `Plugin root`).
3. `~/.cursor/plugins/cache/**/skills/<name>/SKILL.md` (and nested plugin skill dirs). **This is the Cursor-specific insert; it must run before the absent stamp.**
4. `~/.claude/plugins/installed_plugins.json` `installPath` / `skills/` (unchanged; still needed for Claude-compat and Grok).
5. Copilot `~/.copilot/installed-plugins/**/skills/` when that tree exists.
6. Flat `~/.agents/skills/<name>/` (aliases + Codex/Copilot/Grok).

Do not invent a new Python helper in this charter unless a sibling already lands one; document the order in `integrations.md` and repeat the Cursor cache glob in `cursor-tools.md`. Delegation remains mandatory when present.

## Decision: `references/cursor-tools.md` sections and wiring

New file, same job as `grok-tools.md`. Suggested headings (keep it an adapter, not a SKILL):

1. **`${CLAUDE_PLUGIN_ROOT}`: resolve once**: empty env; order in "Cursor plugin-root" above; stamp `progress.md`.
2. **Install & marketplace**: Cursor marketplace / Settings plugins; cache path `~/.cursor/plugins/cache/<publisher>/wit/<hash>/`. Never Claude `/plugin marketplace add`.
3. **Tools**: wit/skill name → Cursor: Read; Write; Edit → `StrReplace`; Bash → `Shell`; Grep/Glob; dispatch → `Task`; AskUserQuestion → `AskQuestion`; WebSearch/WebFetch as present.
4. **Named vs inline subagent dispatch**: named `subagent_type=wit-*` when the session list has them; else inline `agents/*.md`. Prompt skeleton stays in `worktrees-and-subagents.md`.
5. **Keep-alive**: pointer: capability `none`; print the keep-alive.md `none` block. Explicit NEVER list.
6. **Tokens policy** (pointer only) : Orchestrator unavailable; no `token_report.py`; Duration from `progress.md`. Sibling owns the dispatcher.
7. **Plugin-cache paths / skill discovery**: glob in the search order above.
8. **Models**: live ids `cursor-grok-4.6-xhigh`, `composer-2.5-fast`, `inherit`; resolve from stamped Host + platform map. Do not document `cursor-grok-4.5-high`.
9. **Skill invoke**: plugin skills + NL auto-trigger; no required alias copy.

Wire:

- `AGENTS.md`: add a Cursor bullet under "If you are not Claude Code" pointing at `references/cursor-tools.md`. Persistence bullet must not list only `/goal` / Autopilot; point at keep-alive.md capabilities (or "see the tool map").
- `README.md`: Install **Cursor** section (marketplace, not `/plugin`); Platform differences table gains a Cursor column; tool-map sentence lists `cursor-tools.md`.
- `scripts/validate.py` portability loop (today `codex-tools.md`, `copilot-tools.md`, `grok-tools.md`, `AGENTS.md`) **adds** `references/cursor-tools.md`. [VERIFIED: `scripts/validate.py` line 152]
- Reshape the keep-alive **anchors**: keep requiring `model_judged_goal` semantics (`update_goal`) inside keep-alive.md so Grok does not regress; stop requiring the words `autopilot` and `grok` inside always-loaded SKILL bodies. Require the four capability keys (`predicate_goal`, `model_judged_goal`, `relaunch`, `none`) in keep-alive.md, and a pointer to keep-alive.md in dev/research. Requiring `cursor` inside `skills/dev/SKILL.md` would recreate the fork this PR exists to kill.

`worktrees-and-subagents.md` may add one Cursor sentence **or** (preferred) "dispatch target is the stamped `subagent` capability; see the host tool map." Same for `references/models.md` host detection: **stamped `Host:`**, not "following grok-tools.md".

`skills/research/references/wit-directory.md` `progress.md` template currently has no `Host:` / `Plugin root (resolved):` lines. This run already stamps them. Template update belongs with the host-probe work (table-placement sibling may own the table file; the template still needs the two fields). [VERIFIED: wit-directory.md template vs this `progress.md`]

## Decision: plugin-bootstrap on Cursor

On Cursor, **do not** offer Claude `/plugin marketplace add` / `/plugin install`. That is the wrong command and looks like a failed install when wit is already in `~/.cursor/plugins/cache/`. [VERIFIED: `plugin-bootstrap.md`; issue #89 c-bootstrap; this cache]

Offer instead: Cursor marketplace / already-installed plugin cache for Superpowers; `npx skills add` remains valid for skills.sh entries. Skip the `~/.agents/skills` alias copy on Cursor (plugin skills + NL are enough). Keep AskUserQuestion in the skill text; the ask capability maps it to `AskQuestion`.

Do not put a new `if cursor` tree in `skills/scan/SKILL.md`; put the host-specific install commands in `plugin-bootstrap.md` keyed by stamped host / `skill_invoke` capability, and have scan:5 stay "follow plugin-bootstrap.md".

## Don't-Hand-Roll

| Problem | Do not build | Use instead | Why |
|---|---|---|---|
| Cursor keep-alive | Claude `/goal` paste or Copilot flags | `none` template | Chat already persists; wrong go-signal |
| Cursor persistence | Cursor Autopilot skill | nothing (optional `/loop` docs) | Autopilot triages a PR, does not run wit |
| Skill absent on Cursor | Memory / Claude registry only | union including `~/.cursor/plugins/cache/**/skills` | Superpowers lives in that cache here |
| Ask on Cursor | `AskUserQuestion` as a Cursor tool name | `AskQuestion` via the tool map | Skills keep the Claude name; adapter maps |
| Named agents missing | Hard-fail dispatch | inline `agents/*.md` | July 19 Cursor dry-run |
| Model ids in SKILL bodies | `if cursor` model strings | platform map `cursor` column + adapter list | Tiers stay abstract; ids drift |
| Bootstrap | `/plugin marketplace add` on Cursor | Cursor marketplace / cache | Claude command does not install Cursor plugins |

## State of the Art (this repo)

| Old way | Current way (this PR) | When it changed |
|---|---|---|
| keep-alive.md keyed by host (2 then 3 product blocks) | keyed by capability (`predicate_goal` / `model_judged_goal` / `relaunch` / `none`) | #43 added the third family; this feature stops a fourth fork |
| Host detection = which tool-map you are following | stamped `Host:` + capability row | this feature (host probe) |
| models.md "grok else claude" | `Host:` selects a map column; cursor column already parses | parser ready [VERIFIED: `platform_model_for`]; docs/tests not |
| Skill presence = Claude registry + `~/.agents/skills` | union + Cursor cache before absent | this feature |

## Comparison (how to fill the cells)

| Option | Complexity | Blast radius | Reversible | Why it loses / wins |
|---|---|---|---|---|
| **A. Capability-keyed keep-alive + cursor-tools.md filling the Cursor row** | Medium (reshape keep-alive + validate anchors) | keep-alive.md, AGENTS, README, validate, integrations, plugin-bootstrap, models.md prose; SKILL bodies stay pointers | Yes (git) but the public contract wants an ADR | **Wins.** Matches brief, constitution (adapters not SKILL bodies), issue #89. Next host is a row. |
| B. Additive "Cursor" bullet in keep-alive.md + cursor-tools.md, skills still say "current platform" | Low | Same files, plus `if cursor` risk in SKILL bodies | Yes | Ships Cursor faster; repeats #43; validate.py keeps host-string tax. Rejected by brief. |
| C. Named Task types only (no inline fallback) | Low | Dispatch docs | Yes | Breaks Cursor sessions without plugin-registered agents (July 19). Rejected. |

Close call? No for the keep-alive reshape vs a fifth bullet. Close call on plugin-root **cwd-before-cache** vs issue #89's cache-before-walk-up: cwd-first is the only order that matches this dogfood stamp. Record it in the ADR.

Hard-to-reverse? **Yes** (constitution: host capability table + keep-alive capability keys are ADR-class).

## Assumptions Log

| Claim | Why assumed | Load-bearing? |
|---|---|---|
| `AskQuestion` JSON is `id` + `prompt` + `options` (options as strings or `{id,label}`) | Brief/issue specify the fields; Cursor onboard shows prompt+options but no schema file in-repo; this subagent session has no `AskQuestion` tool to inspect | Yes. Build must confirm against the parent Cursor tool descriptor. Fallback: prose ask if the tool is missing (already Cursor policy). |
| Cursor marketplace UI label / click-path for installing wit | Cache path verified; no official install command in this repo | Yes for README/bootstrap wording. Do not invent a `/plugin` equivalent. Point at Cursor's plugin marketplace + the verified cache glob. |
| `composer-2.5-fast` remains the cheap Cursor id | On this session's Task slug list; this repo does not use it (all tiers → xhigh) | No for this repo's map; yes for the adapter's documented cheap id. |

## Risks / unknowns (plan must consume)

1. **AskQuestion schema** not captured from a live tool descriptor this session. Confirm `id` / `prompt` / `options` before writing the cursor-tools.md Ask row. Pitfall: inventing Claude-style `AskUserQuestion` fields.
2. **validate.py host-string anchors** (`autopilot` / `grok` in SKILL bodies) will fail if skills drop host names without updating the checker. Plan must change the anchors to capability keys in the same PR.
3. **Plugin-root cwd-vs-cache.** Issue #89 listed cache before walk-up. Cwd-first is required for source-repo dogfood. Pitfall: consumer repo with a nested folder named like a wit root, or a stale cache chosen when cwd is not a wit root (step 3 still needed).
4. **Named Task types flicker.** Same machine: July 19 none, Aug 19 present. Dispatch docs and tests must cover both; never fail closed.
5. **Stale model id** `cursor-grok-4.5-high` in the workspace fallback rule vs live `cursor-grok-4.6-xhigh`. Adapter and resolved block must use live slugs. `.wit/models.md` already does.
6. **`references/models.md` host detection** still says "following grok-tools.md". If left as-is, a Cursor run can resolve claude tiers instead of the cursor column even though the column parses. Host must come from the stamp.
7. **progress.md template** lacks Host / Plugin root fields; this run already uses them. If the template is not updated, later seeds omit the stamp and ship/keep-alive guess again.
8. Sibling-owned: token finalize must not run `token_report.py` on `Host: cursor` (July 19 foreign-transcript bind). Mentioned only so cursor-tools.md tokens section does not contradict it.

## Dependency Legitimacy

None added. No new package.

## Citations

- https://github.com/Wittenberger-Industries/witloop/issues/89
- `references/keep-alive.md`, `references/models.md`, `references/grok-tools.md`, `references/codex-tools.md`, `references/copilot-tools.md`
- `skills/research/references/integrations.md`, `skills/scan/references/plugin-bootstrap.md`
- `skills/build/references/worktrees-and-subagents.md`
- `skills/dev/SKILL.md`, `skills/research/SKILL.md`, `AGENTS.md`, `README.md`, `scripts/validate.py`
- `docs/plans/2026-07-19-learnings-lifecycle-dryrun.md`
- Live Cursor session 2026-08-19: empty plugin-root env; Task `wit-*` types present; cache path `~/.cursor/plugins/cache/wittenberger-industries-witloop/`
