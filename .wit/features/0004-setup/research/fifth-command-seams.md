---
type: Research Note
title: "Fifth advertised command: setup wiring seams"
description: How to add user-invocable setup with the least lockstep breakage across tests, aliases, manifests, and docs.
feature: 0004-setup
timestamp: 2026-08-27
valid_until: 2026-09-26
---

# Fifth advertised command: setup wiring seams

## Question

How to add a fifth advertised user-invocable command `setup` (`/wit:setup`, aliases `/wit-setup` /
`$wit-setup`) with the least lockstep breakage.

Out of scope here: scan first-run vs `--refresh` split and strings to move from scan/dev/rpa; tokens
ledger skip honor points and `models.md` ledger key shape.

## Responsibility Map

Plugin surface only (not an app). The new command is a skill + flat alias + advertised-command
lockstep. Host discovery is directory-based. Project state stays in `.wit/` (sibling questions).

| Capability | Layer |
|------------|--------|
| Slash command `/wit:setup` | `skills/setup/SKILL.md` (`name: setup`, user-invocable by omitting `user-invocable: false`) |
| Flat aliases `/wit-setup` `$wit-setup` | `references/skill-aliases/wit-setup/SKILL.md` copied to `~/.agents/skills/` |
| Advertised-command contract | README table, AGENTS wording, two test tuples, three manifest descriptions |
| Host invoke rows | `references/{codex,copilot,grok}-tools.md` (Cursor has no alias list) |
| Alias copy offer list | `skills/scan/references/plugin-bootstrap.md` today (sibling may retarget the offer) |
| Source-memory pins | `.wit/overview.md`, `.wit/architecture.md`, `.wit/repo-map.md` |
| Public contract record | `.wit/adr/ADR-0004-*.md` + `index.md` |

## Recommendation

**Copy the add-issues advertised-skill pattern. Do not add a command registry.** Create
`skills/setup/` and `references/skill-aliases/wit-setup/` first. Then one serial wiring task updates
every four-command pin to five, using the two existing tuple conventions:

- `USER_COMMANDS` stays **filesystem-alpha** (must equal `user_invocable_skill_names()`).
- README `ADVERTISED` stays **lifecycle order**, with **setup first**.

Do not set `user-invocable: true` explicitly. Do not list skills in manifests. Do not add
`skills/setup/SKILL.md` as a plugin-root tell (keep `skills/scan/SKILL.md`). Do not touch `.gitignore`
(`!/skills/**` and `!/references/**` already cover the new paths).

## Why this wins

1. `scripts/validate.py` already globs `skills/**/SKILL.md` and `references/skill-aliases/**/SKILL.md`.
   It does not enumerate advertised names. A new hardcoded list would be a new lockstep source.
   `[VERIFIED: scripts/validate.py fm_files glob + Codex `"skills": "./skills/"`; Claude plugin.json
   has no skills array]`
2. add-issues is the last advertised command and already proved the pattern: skill dir + omit
   `user-invocable: false` + `wit-*` forwarder + bootstrap copy list + README/AGENTS/host maps +
   membership pins in `test_work_type_release.py`. `[VERIFIED: skills/add-issues/SKILL.md,
   references/skill-aliases/wit-add-issues/SKILL.md, tests/test_work_type_release.py]`
3. Two tuples already disagree on order. Unifying them to one order would reshuffle the README table
   or break the sorted-name assertion. Keep both conventions; only extend each. `[VERIFIED:
   USER_COMMANDS = ("add-issues", "dev", "rpa", "scan"); ADVERTISED = ("scan", "dev", "rpa",
   "add-issues")]`
4. 0003 learning: create the files always-loaded bodies will `${PLUGIN_ROOT}`-point at, then serial
   wire. Scan/dev/rpa pointers at `skills/setup/SKILL.md` are sibling Q2, but the file must exist
   first or validate check 3 fails. `[VERIFIED: .wit/learnings/0003-work-type-routing.md; validate.py
   check 3]`

## Tuple orders (lock these)

**USER_COMMANDS** (alpha; `tuple(sorted(names))` in `user_invocable_skill_names()`):

```python
USER_COMMANDS = ("add-issues", "dev", "rpa", "scan", "setup")
```

**ADVERTISED** (README command table, parsed by `readme_command_table_slugs`):

```python
ADVERTISED = ("setup", "scan", "dev", "rpa", "add-issues")
```

README table order is setup-first, not alpha and not append-last.

- Alpha would put `add-issues` before `dev` and fight the current table. `[VERIFIED: README.md
  command table is scan, dev, rpa, add-issues]`
- Append-last (`scan` still row 1) keeps the old first-run slot after scan becomes refresh-only.
  The table is already lifecycle order; first-run is now setup. `[VERIFIED: brief acceptance:
  setup advertised next to the four; scan refresh-only]`
- `test_work_type_docs.py` asserts `tuple(slugs) == ADVERTISED` and `len == 4`. Change both together.
  Keep the negative pins `/wit:how` and `/wit:investigate`. `[VERIFIED: test_four_advertised_commands_and_no_fifth]`

AGENTS.md must still have **no** README-style command table (`table_slugs == []`). Wording pin
becomes `Only setup/scan/dev/rpa/add-issues are user-facing` (same slash-separated style as today).
`[VERIFIED: test_four_user_facing_commands_wording]`

Do not confuse **four hosts** (README; Codex excluded) with **five commands**. Leave
`test_advertised_hosts_exclude_codex` alone. `[VERIFIED: README_HOSTS vs ADVERTISED are separate]`

## New alias directory (copy wit-scan, pass `--auto` like wit-dev)

Path: `references/skill-aliases/wit-setup/SKILL.md`

Copy the wit-scan forwarder shape, not a new installer:

1. Frontmatter `type: Skill`, `name: wit-setup`, `description` listing Copilot `/wit-setup`, Codex
   `$wit-setup`, Grok `/wit-setup`. Stay under the 1024-char description cap.
   `[VERIFIED: validate.py DESC_CAP = 1024]`
2. Body: locate wit plugin root (`skills/` + `agents/` + `.claude-plugin/`); read `AGENTS.md`; follow
   `skills/setup/SKILL.md`; pass `--auto` through if given (brief: `--auto` writes simple preset +
   ledger on). No setup logic in the alias.
3. If no plugin root: point at `https://github.com/Wittenberger-Industries/witloop`; do not improvise.

`plugin-bootstrap.md` copy list today is prose `wit-scan/`, `wit-dev/`, `wit-rpa/`, `wit-add-issues/`
under `${PLUGIN_ROOT}/references/skill-aliases/` (that directory already exists, so adding
`wit-setup/` to the i.e. list does not create a new check-3 path unless someone writes a full
`${PLUGIN_ROOT}/references/skill-aliases/wit-setup/SKILL.md` pointer). Add `wit-setup/` to every
enumerated alias list in the same serial task. Cursor still skips the copy. `[VERIFIED:
skills/scan/references/plugin-bootstrap.md; references/cursor-tools.md "No ~/.agents/skills/ alias
copy"]`

Skill frontmatter for `skills/setup/SKILL.md`: match scan/dev/rpa/add-issues (omit
`user-invocable: false`). `user_invocable_skill_names()` skips only an explicit false.
`[VERIFIED: tests/test_work_type_release.py]`

## Serial wiring (least lockstep breakage)

From `.wit/learnings/0003-work-type-routing.md`: parallel tasks must not `${PLUGIN_ROOT}`-point at
files that do not exist yet; always-loaded / hotspot edits stay serial.

**Wave A (create only; no pointers from other skills):**

- `skills/setup/SKILL.md`
- `docs/design-notes/setup.md` (runtime never reads this file; same banner as `docs/design-notes/scan.md`)
- `references/skill-aliases/wit-setup/SKILL.md`

Do not add setup.md to `test_work_type_docs.py` `DOC_FILES` (that tuple is the work-type ownership
set, not a global docs registry). `[VERIFIED: test_files_are_only_the_listed_docs]`

**Wave B (one serial task after Wave A):** every four-command pin in one change. Splitting README vs
tests vs manifests across parallel tasks is how this lockstep breaks.

**Wave C (sibling Q2, after Wave A):** scan/dev/rpa `${PLUGIN_ROOT}/skills/setup/SKILL.md` for missing
`.wit/`. Not designed here. Plan must keep those pointers out of Wave A.

Hotspots stay serial: `skills/dev/SKILL.md`, `references/workflow.md`. `[VERIFIED: constitution.md
Architecture & dependencies]`

## Files that must change together

Contract tests (extend in place; do not add a third advertised-command tuple):

| File | Change |
|------|--------|
| `tests/test_work_type_release.py` | `USER_COMMANDS` five-tuple alpha; `FourCommandTests` / `test_four_user_invocable_skill_names` rename to five; `RELEASE = "1.16.2"`; manifest membership adds `/wit:setup`; overview/architecture/repo-map assertions add setup |
| `tests/test_work_type_docs.py` | `ADVERTISED` setup-first; `test_four_advertised_commands_and_no_fifth` -> five / no sixth; `Only these four` / AGENTS only-line |

User docs:

| File | Change |
|------|--------|
| `README.md` | Command table setup-first; "Only these five entry points"; frontmatter description; "How a run works" lead with `/wit:setup`; mermaid; This-repo `skills/` list; install prompt currently "confirm a scan command"; "one of those four commands" under Work types |
| `AGENTS.md` | Skills parenthetical (today omits `add-issues`; add `add-issues` and `setup`); new invoke bullet for setup; "Only setup/scan/dev/rpa/add-issues"; "once scan's bootstrap installed aliases" will be wrong after Q2 moves the offer, but this question still adds `wit-setup` to the advertised set |

Manifests (version lockstep 1.16.2; membership test, not prose order). Lead descriptions with
`/wit:setup` because scan currently leads as first-run. `[VERIFIED: .claude-plugin/plugin.json,
marketplace.json wit.version, .codex-plugin/plugin.json all 1.16.1; test pins RELEASE]`

| File | Change |
|------|--------|
| `.claude-plugin/plugin.json` | version `1.16.2`; description adds `/wit:setup` |
| `.claude-plugin/marketplace.json` | wit plugin version `1.16.2`; description adds `/wit:setup`; catalog `metadata.version` stays `0.2.0` `[VERIFIED: MARKETPLACE_CATALOG = "0.2.0"]` |
| `.codex-plugin/plugin.json` | version `1.16.2`; description adds `/wit:setup`; `skills` stays `./skills/` |

Host adapters and bootstrap:

| File | Change |
|------|--------|
| `skills/scan/references/plugin-bootstrap.md` | Claude `/wit:setup`; Copilot `/wit setup`; Codex `$setup`; Grok `/setup`; alias lists include `wit-setup/` `/wit-setup` `$wit-setup` |
| `references/codex-tools.md` | invoke cell `$wit-setup` |
| `references/copilot-tools.md` | invoke cell + Command namespace (`/wit setup`, `/wit-setup`; today's namespace line still omits add-issues, fix both) |
| `references/grok-tools.md` | bare `/setup` + branded `/wit-setup` in both the Install paragraph and the invoke cell |
| `references/cursor-tools.md` | no alias list; optional "scan / dev / rpa entry" stamp line includes setup |
| `references/capabilities.md` | "Resolve once at scan / dev / rpa entry" and Host probe same phrase. Plugin-root tell stays `skills/scan/SKILL.md` `[VERIFIED: capabilities.md:46]` |
| `references/workflow.md` | state machine still starts at scan-once; hotspot, serial. Sibling Q2 owns scan vs setup semantics; this wave at least must not advertise scan as the only project-level entry |

Source-memory (release test opens these):

| File | Change |
|------|--------|
| `.wit/overview.md` | user-facing list includes `setup`; version string `1.16.2`; test currently `assertNotIn("1.16.0")` / `"1.14.1"`; when RELEASE becomes 1.16.2, also drop leftover `1.16.1` and extend `four user-facing` regex |
| `.wit/architecture.md` | `subgraph entry` add `setup_sk["setup"]` before `subgraph phases` (parser splits on that marker); legend "Five entry skills" |
| `.wit/repo-map.md` | Entry points add `/wit:setup`; Layout `skills/` list |

`validate.py`: no skill-name list to edit. `[VERIFIED]`

`.gitignore`: no change. `[VERIFIED: !/skills/** !/references/**]`

Do not add `skills/setup/SKILL.md` to the env-is-a-wit-root tell. Scan remains the tell so older
checkouts and plugin-root resolution stay stable. `[VERIFIED: capabilities.md Plugin root order 1]`

## ADR-0002 does not freeze four commands; ADR-0004 is still required

ADR-0002 (`ADR-0002-route-work-by-intent.md`) rejected a fifth command **for investigate / bug-fix**.
Context: "without ... adding a fifth command". Alternative: "New `/wit:investigate` or bug-fix
command: breaks the four-command surface". That is a work-type decision, not a cardinality freeze.
`[VERIFIED: .wit/adr/ADR-0002-route-work-by-intent.md]`

Constitution: any hard-to-reverse **public skill contract** requires an ADR. `[VERIFIED:
constitution.md Architecture & dependencies]` Next id is ADR-0004 (index has 0001, 0002, 0003).
`[VERIFIED: .wit/adr/index.md]`

**ADR is required.** Brief already wants ADR-0004. Record: advertised entry `setup`; host forms
`/wit:setup` `/wit-setup` `$wit-setup`; does **not** reopen work types as extra commands (ADR-0002
stands for that). Hard-to-reverse: **yes** (public slash command + marketplace copy + machine-local
aliases).

## Alternatives considered

| Option | Rejected because |
|--------|------------------|
| Append setup as README row 5, keep scan first | Preserves a first-run slot that the brief removes; more user-facing breakage than a table reorder the tests already own as an exact tuple |
| One alpha order everywhere | Breaks README lifecycle convention; `add-issues` would jump above `dev` |
| Registry in `validate.py` or a shared `USER_COMMANDS` import | New lockstep source; validate already globs; tests already have two tuples for two orders; YAGNI `[VERIFIED: constitution Simplicity]` |
| `user-invocable: true` on setup only | Diverges from scan/dev/rpa/add-issues; the test only cares about not-false |
| Fold setup into scan as a flag, no fifth command | Brief non-goal ("folding setup back into scan") |
| List skills in plugin.json | Claude/Codex do not; add-issues shipped without it |

## Don't-Hand-Roll

| Problem | Do not build | Use instead | Why |
|---------|--------------|-------------|-----|
| Discover advertised skills | Hardcoded list in validate.py | Glob `skills/*/SKILL.md` minus `user-invocable: false` | Already how `user_invocable_skill_names()` and validate work |
| Copilot/Codex/Grok invoke | Custom installer | Flat `wit-setup` forwarder + existing `~/.agents/skills/` copy | add-issues pattern; aliases are version-independent |
| Plugin-root detection | New tell `skills/setup/SKILL.md` | Keep `skills/scan/SKILL.md` | Scan stays a published skill; changing the tell is unrelated lockstep |
| Command table vs test sort | Unify to one tuple | Keep ADVERTISED vs USER_COMMANDS | They already encode different orders |

## Runtime State Inventory (alias copy, not a rename)

Not a rename. Machine-local alias copies still will not gain `wit-setup` until bootstrap recopy.

1. **Stored data:** none keyed on command cardinality. `[VERIFIED: no DB/queue/enum of four commands]`
2. **Live service config outside git:** marketplace plugin descriptions (in-repo manifests, bumped
   1.16.2). No extra dashboard keys. `[VERIFIED: three manifests]`
3. **OS / platform-registered state:** `~/.agents/skills/wit-{scan,dev,rpa,add-issues}/` on machines
   that accepted the copy. `wit-setup` is absent until recopy. Bootstrap already says overwriting
   `wit-*` is fine and the copy is one-time. Setup (or the moved offer) must offer the fifth dir.
   Cursor never copies. `[VERIFIED: plugin-bootstrap.md; cursor-tools.md]`
4. **Secrets & env-var names:** none. Plugin-root env names unchanged. `[VERIFIED: capabilities.md]`
5. **Build / installed artifacts:** published plugin id stays `wit`. Installed cache is version-keyed;
   1.16.2 is a new cache dir. No lockfile. `[VERIFIED: README "installed cache is keyed by version"]`

## Assumptions Log

| Claim | Why assumed | Load-bearing? |
|-------|-------------|---------------|
| Grok has no blocking built-in `/setup` that would hide the skill | Not probed this session; grok-tools say built-ins win and branded `/wit-setup` is the collision-free form `[VERIFIED: references/grok-tools.md invoke cell]` | No (branded alias is the advertised Copilot/Grok/Codex form) |
| Hosts auto-load a new `skills/setup/` without a manifest skills array | add-issues shipped that way; Codex points at `./skills/`; Claude plugin.json has no skills list `[VERIFIED for Claude/Codex manifests; add-issues prior art]` | No (prior art) |

No load-bearing `[ASSUMED]` rows to promote.

## Risks / unknowns (plan must consume)

- Overview/release test mixes version pins with command pins: bump `RELEASE` to `1.16.2` in the same
  serial task as the fifth name, and scrub leftover `1.16.1` from overview.
- AGENTS.md skills parenthetical already omits `add-issues`. Fix while adding `setup` or the
  parenthetical stays a silent fourth-command fossil.
- Copilot Command namespace still lists only `/wit scan|dev|rpa`. Add `/wit setup` and `/wit add-issues`
  in the same edit.
- Wave C (Q2) `PLUGIN_ROOT` pointers at `skills/setup/SKILL.md` will fail validate if Wave A has not
  landed. Plan: files first, pointers later.
- Existing `~/.agents/skills/` installs lack `wit-setup` until recopy. Offer must include the new dir
  (sibling may move the offer into setup).
- Do not add a new always-loaded `${PLUGIN_ROOT}` target for project state (brief). Setup is an
  on-invoke skill, not a prelude file every phase loads.
- Description + host-form lists must stay under 1024 chars on both `skills/setup/SKILL.md` and
  `wit-setup` alias.
- `test_work_type_docs.py` `test_four_advertised_commands_and_no_fifth` also pins `Only these four
  entry points`. Count words and table rows in one edit.
- architecture mermaid: new node must sit in `subgraph entry` (before `subgraph phases`) or
  `test_architecture_loads_work_type_refs_from_dev` misses it.

## Dependency Legitimacy

None added.

## Verified

- Repo-only. `USER_COMMANDS` / `ADVERTISED` / manifests / validate globs / ADR-0002 / plugin-bootstrap
  alias list / add-issues alias pattern / 0003 serial-wiring learning. Docs fetched 2026-08-27 from
  this tree. No spike.

## Hard-to-reverse?

Yes. Public skill contract. ADR-0004 required. ADR-0002 is not a four-command freeze; ADR-0004 records
the onboarding command without reopening work-type routing as extra slash commands.
