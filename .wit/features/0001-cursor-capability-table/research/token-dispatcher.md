---
type: Research Note
title: "ship:6 token dispatcher for Host: cursor"
description: How ship:6 picks token parsers today, and the smallest dispatcher that writes the unavailable sentinel on Cursor without invoking token_report.py while still filling Duration from progress.md.
feature: 0001-cursor-capability-table
timestamp: 2026-08-19
valid_until: 2026-09-18
---

# ship:6 token dispatcher (Cursor unavailable path)

## Responsibility Map

Plugin scripts under `skills/ship/scripts/` (not an app frontend/backend). ship:6 is the only caller. `_ledger.py` owns the `tokens.md` byte format; host-specific parsers stay Claude (`token_report.py`) and Grok (`grok_token_report.py`); the new dispatcher is the single ship:6 entrypoint. Host probe / capability table / `cursor-tools.md` are sibling charters; this note only consumes the `Host:` stamp they write.

## Question

How does ship:6 pick token parsers today, and what is the smallest dispatcher that given `Host: cursor` writes `unavailable`, never runs `token_report.py`, and still fills Duration totals from `progress.md`?

## Today's pick (prose, not code)

There is no Python dispatcher. ship:6 names Claude's CLI as the default; other hosts are expected to override from their platform tool map. [VERIFIED: skills/ship/SKILL.md:277-287]

1. **Always-loaded default (Claude Code).** `python ${CLAUDE_PLUGIN_ROOT}/skills/ship/scripts/token_report.py --write .wit/features/<slug>/tokens.md` (optional `--transcript` / `--progress`). Auto-detects `~/.claude/projects/<encoded-cwd>/**/*.jsonl`. [VERIFIED: skills/ship/SKILL.md:278-279; skills/ship/scripts/token_report.py:75-106]
2. **Non-Claude override (operator/model reads the tool map).** "a non-Claude host runs the one its platform tool map names". [VERIFIED: skills/ship/SKILL.md:280-282; skills/research/references/wit-directory.md:236-238]
3. **Grok Build.** `grok_token_report.py --write` **INSTEAD OF** `token_report.py --write`. [VERIFIED: references/grok-tools.md:148-157]
4. **Copilot CLI.** No dedicated finalizer script. Per-task rows are `unavailable`; `/usage` may be copied verbatim into `## Orchestrator`; else the sentinel. Duration "still finalize[s] normally" via wit stamps, not the platform. [VERIFIED: references/copilot-tools.md:61-77]
5. **Codex CLI.** No tokens/ledger section in the tool map. Relies on the v1.13.4 gate accepting a finalized zero-dispatch / all-unavailable ledger. [VERIFIED: references/codex-tools.md (no token section); skills/ship/scripts/_ledger.py:255-257; docs/roadmap.md:72-77]
6. **Cursor.** Not a documented host. A real Cursor dry-run invoked the SKILL default (`token_report.py --write`) and bound a foreign Claude transcript. v1.13.4 scoped `find_transcript` to the encoded cwd, which stops *cross-project* binds, not *same-cwd leftover Claude sessions on a Cursor run*. [VERIFIED: docs/plans/2026-07-19-learnings-lifecycle-dryrun.md:18,45-46; tests/test_tokens_guardrail.py:432-463; skills/ship/scripts/token_report.py:75-80]

`check_tokens.py` does not pick a parser. It scaffolds (`--init`) and verifies. Honest `unavailable` (orchestrator, a duration cell, or a total) passes; `_PENDING` fails. Zero integer-token rows with sum `0` and filled totals pass (v1.13.4). [VERIFIED: skills/ship/scripts/check_tokens.py:7-16; skills/ship/scripts/_ledger.py:236-261; tests/test_tokens_guardrail.py:131-140]

## Host forks (orchestrator source)

| Host | ship:6 today | Orchestrator | Subagent tokens | Duration totals | Invokes `token_report.py`? |
|------|----------------|--------------|-----------------|-----------------|----------------------------|
| Claude Code | SKILL default CLI | JSONL `usage` on the session transcript | exact from completion notifications; `--write` also appends `## Subagent detail` from sidecars | Σ compute from Duration cells; wall-clock from `progress.md` spans | **yes** (the default) |
| Grok Build | tool map replaces the CLI | sentinel + context occupancy (not cumulative I/O) | exact `subagent_finished.tokens_used` backfilled at finalize | compute from session split durations; wall-clock from `progress.md` minus in-window `wait_ms` | **no** (if the model follows grok-tools.md) |
| Copilot | SKILL default unless the model follows copilot-tools.md | `/usage` paste or sentinel | `unavailable` per task | claimed "normal" finalize from wit stamps | **yes unless overridden** (no Copilot script) |
| Codex | SKILL default; no map section | sentinel | `unavailable` | only if something still runs `--write` to fill totals | **yes unless overridden** |
| Cursor | undocumented; falls through to SKILL default | must be sentinel (no local usage field) | `unavailable` / inline-role / 0 | must still fill from `progress.md` | **must become no** |

[VERIFIED: table cells from the files cited in the previous section; Cursor "must" rows from `.wit/features/0001-cursor-capability-table/brief.md` Tokens / Acceptance]

### Why v1.13.4 cwd-scope is not enough for Cursor

`find_transcript(cwd)` returns the newest jsonl under `~/.claude/projects/<encode(cwd)>/`. A Cursor run in a repo that previously (or concurrently) had Claude Code sessions for that same path will parse those `usage` objects and write them as this run's orchestrator. [VERIFIED: token_report.py:75-106 plus FindTranscriptTests only covering a *different* encoded project, tests/test_tokens_guardrail.py:432-453]

That is the remaining defect. Same-cwd Claude leftovers are not "foreign" to the path encoder; they are foreign to **this host**.

Copilot/Codex have the same hole today: they inherit the SKILL default, so a Windows machine with both Copilot and Claude Code will also bind that transcript unless the model remembers the tool map. The capability-table fix is one dispatcher that does not rely on the model skipping a command.

## What already fills Duration without a transcript

`token_report.run_write` already writes the sentinel when parse fails **and still** fills Σ compute + wall-clock from ledger rows + sibling `progress.md`. [VERIFIED: token_report.py:386-404; tests/test_timing_report.py:201-213]

Span boundaries (same in both parsers):

- span1 = first `phase = research` → first `design gate opened`
- span2 = last `design gate approved` / `design gate auto-approved` → last `PR opened` (else last `phase = done`)
- date-only or missing/negative → that span is `None`; wall = sum of present spans else `unavailable`

[VERIFIED: token_report.py:176-217; grok_token_report.py:284-323; tests/test_timing_report.py:48-75]

Grok additionally subtracts `events.jsonl` `permission_resolved.wait_ms` inside those windows. Cursor has no such file; do not port that subtraction. [VERIFIED: grok_token_report.py:326-351, 480-487]

`_ledger.UNAVAILABLE` must stay the exact string `Orchestrator: unavailable for this run`. [VERIFIED: _ledger.py:21]

## Stamp the dispatcher will read

This feature's `progress.md` already carries the contract the host-probe sibling is expected to keep:

```
- **Host:** cursor
- **Plugin root (resolved):** D:\ClaudeCowork\wi-plugin\wi-plugin
```

[VERIFIED: .wit/features/0001-cursor-capability-table/progress.md:19-20]

Parse Host from a header bullet `^\s*-\s*\*\*Host:\*\*\s*(\S+)`, casefold. Do not parse Log lines (span regex is line-initial ISO). Plugin-root is out of scope for this charter.

## Recommendation

**One new stdlib CLI `skills/ship/scripts/finalize_tokens.py --write TOKENS_MD` as the only ship:6 token command.** It reads `Host:` from the sibling `progress.md` (override `--host`, `--progress`) and routes:

| `Host:` (casefold) | Action | May import / call |
|--------------------|--------|-------------------|
| `cursor`, `copilot`, `codex` | `run_unavailable_write` | `_ledger` only (+ span helper in `_ledger`) |
| `grok`, `grok-build` | `grok_token_report.run_write` after `resolve_session_dir` | `grok_token_report` |
| `claude`, `claude-code` | `token_report.run_write` (transcript auto-detect unchanged) | `token_report` |
| missing or unknown | **same as cursor** (`run_unavailable_write`) | `_ledger` only |

`run_unavailable_write` (Cursor path; this is the whole Cursor implementation):

1. Require an existing `tokens.md` (same as today's `--write`: no create; exit 1 if absent).
2. `body = _ledger.UNAVAILABLE` plus two ASCII note lines: `- host: <id>` and `- NOTE: this host exposes no local orchestrator usage field; Duration totals come from progress.md Log stamps. Never a dashboard scrape.`
3. `_ledger.replace_tail(text, body)` with **no** `## Subagent detail`.
4. `_ledger.set_subagents_sum(text, _ledger.sum_data_rows(text))` (0 when there are no integer-token rows).
5. Spans from `progress.md` via `_ledger.parse_progress_spans` (lifted; see below). Wall = `sum(present spans) if any else None`. Σ compute from `_ledger.sum_row_durations`.
6. `_ledger.set_compute_totals(...)`. Write UTF-8. Print an ASCII timing line like `token_report.run_write`.
7. **Never** call `token_report.find_transcript`, `encode_claude_project_path`, or `parse_transcript`. **Never** `subprocess` `token_report.py`. **Never** HTTP / cursor.com / Usage dashboard.

ship:6 always-loaded body becomes one command (capability-table cite, no host if-tree):

`python ${CLAUDE_PLUGIN_ROOT}/skills/ship/scripts/finalize_tokens.py --write .wit/features/<slug>/tokens.md`

Grok/Copilot/Codex adapters then say "ship:6 runs `finalize_tokens.py`; do not invoke `token_report.py` yourself." Direct `token_report.py` / `grok_token_report.py` CLIs stay for print-mode and tests.

### Lift `parse_progress_spans` into `_ledger.py`

The function is already duplicated in `token_report.py` and `grok_token_report.py`. A third copy in the dispatcher would drift. Move `STAMP_RE` + `_iso` + `parse_progress_spans` into `_ledger.py`. Re-export `parse_progress_spans` from `token_report.py` so `tests/test_timing_report.py` stays green. Grok keeps `_progress_marks` (needs the 4-tuple for approval-wait); its `parse_progress_spans` can wrap the shared helper or keep calling `_progress_marks` locally. Cursor never imports `token_report`.

### Ledger rule (unchanged, now host-keyed)

Exact figure or `unavailable`. Never a substitute, estimate, invented number, or scraped dashboard. Copilot's optional on-screen `/usage` paste stays **adapter prose after finalize**, not something this script fetches. Cursor has no equivalent paste in this PR.

### Missing `Host:` is fail-safe unavailable, not Claude

Today's SKILL default is Claude. After this PR, an unstamped `progress.md` on a Cursor+Claude machine would reintroduce the dry-run bug if missing meant Claude. Host-probe (sibling) must stamp every host (`claude` / `grok` / `copilot` / `codex` / `cursor`) before ship:6. Tests for Claude/Grok pass `--host` or a stamped fixture, not an unstamped file.

## Alternatives (rejected)

**A. Thin ship:6 prose fork** (`if Host cursor: skip; else token_report.py`). Rejected: product-name if-tree in an always-loaded SKILL body (constitution + brief). One missed branch re-runs `token_report.py` on Cursor. Copilot/Codex stay on the Claude default.

**B. `--host cursor` flag on `token_report.py`.** Rejected: acceptance is "does not invoke `token_report.py`". That file also owns Claude prices, sidecar layout, and `find_transcript`; a skip-flag still binds Cursor to the Claude CLI name and makes SKILL.md keep advertising it.

**C. Copilot-style "copy /usage or write sentinel by hand" with no script.** Rejected: Duration totals would stay `<dur>` placeholders and `check_tokens.py` would fail. Duration fill is what `--write` is for; it must stay a script. Dashboard paste is forbidden for Cursor.

## Don't-Hand-Roll

| Problem | Do not build | Use instead | Why |
|---------|--------------|-------------|-----|
| Cursor orchestrator tokens | HTTP scrape of cursor.com / Admin API / guessed usage | `_ledger.UNAVAILABLE` | ledger rule; constitution out-of-scope; brief forbids dashboard scrape |
| Duration / wall-clock | new time parser, `now.py` at ship:6, awk over Log | `_ledger.parse_progress_spans` + `set_compute_totals` (same boundaries as today) | already implemented and tested |
| Subagents sum on a zero-row ledger | require a fake integer row | `set_subagents_sum(..., 0)` | v1.13.4 gate [VERIFIED: _ledger.py:255-257] |
| Pick parser | SKILL if-tree per host | `finalize_tokens.py` keyed on `Host:` | one command; table row not fork |
| Same-cwd Claude leftovers | tighter `find_transcript` heuristics | never call it on Cursor | cwd-scope cannot distinguish host |

## Comparison

| | Complexity | Blast radius | Reversibility | Fit |
|---|------------|--------------|---------------|-----|
| **finalize_tokens.py (chosen)** | one new stdlib CLI + span lift | ship:6 one-line; `_ledger.TEMPLATE` PENDING text; adapter one-liners; new tests | revert the SKILL line to `token_report.py` | matches existing `check_tokens` / `token_report` split; no host if-tree |
| Prose ship:6 fork | zero Python | SKILL.md hotspot grows a Cursor branch | easy | fights constitution (procedure in always-loaded body) |
| Flag on token_report.py | smallest Python | Cursor still "runs token_report.py" | easy | fails acceptance (a) |

Not a close call. The new file is the second caller of the finalize ritual (Claude vs everyone else already existed as Grok's separate script). Constitution "no abstraction until a second caller" is already satisfied.

## Plan must include these tests

New `tests/test_finalize_tokens.py` (unittest, temp dirs, subprocess the CLI like `test_tokens_guardrail.py`). Plant `HOME` via env in the child so `Path.home()` cannot see the real `~/.claude`.

**(a) Host: cursor does not bind a foreign `~/.claude` session.** Fixture: `progress.md` with `- **Host:** cursor` and Log stamps; `tokens.md` scaffold + optional unavailable rows; `HOME/.claude/projects/<encode(cwd)>/session.jsonl` containing distinctive usage (e.g. `output_tokens: 424242`) plus a newer foreign-project jsonl. Run `finalize_tokens.py --write`. Assert: `Orchestrator: unavailable for this run` present; `424242` absent; no `transcript:` line; `_PENDING` absent; `check_tokens.py` exit 0. Optionally assert child argv / module: `token_report.py` was not the executed script.

**(b) No Claude transcript still fills Duration.** Same Host: cursor, **no** `~/.claude` tree. `progress.md` uses the `PROGRESS_FIXTURE` stamps from `tests/test_timing_report.py` (wall 1971+3012 = 4983s = `1h23m03s`). One ledger row with Duration `1m00s`. Assert Σ compute `1m00s` / wall-clock `1h23m03s` / orchestrator sentinel / `check_tokens.py` 0.

**(c) Existing Claude and Grok paths stay green.** `--host claude --transcript <fixture>` matches today's `TokenReportWriteTests.test_write_fills_orchestrator_and_sum_and_passes_gate` (parsed usage, sum, totals). `--host grok` with `GROK_HOME` pointing at `tests/test_grok_token_report.py`'s `make_session` matches `FinalizeWriteTest` (sentinel + exact sum 300 + wall from progress). Existing `tests/test_tokens_guardrail.py`, `test_grok_token_report.py`, `test_timing_report.py` remain unmodified in behavior (re-export keeps `token_report.parse_progress_spans` importable).

**Also (gate contract, v1.13.4):** Host: cursor, zero integer-token rows, sum 0, sentinel, filled totals (compute/wall may be `unavailable` if no stamps/rows) → `check_tokens.py` 0. Missing `tokens.md` → exit 1, create nothing. Second `--write` idempotent. Missing `Host:` with a planted Claude transcript → sentinel, **not** the planted usage (fail-safe).

Do not add a test that fetches or parses a Cursor dashboard HTML/JSON.

## ship:6 / template wiring (planner)

- SKILL.md ship:6.3: replace the `token_report.py --write` command with `finalize_tokens.py --write`; drop the "non-Claude host runs the one its platform tool map names" sentence from the always-loaded body; point at the capability table / `finalize_tokens.py` docstring for routing.
- `_ledger.TEMPLATE` PENDING paragraph: name `finalize_tokens.py --write` as the ship command (Claude/Grok remain implementation details of that script).
- `references/grok-tools.md` / `copilot-tools.md`: "do not invoke `token_report.py`; ship:6 runs `finalize_tokens.py`."
- `check_tokens.py` unchanged.
- Stdlib only. No new dependency.

## Assumptions Log

| Claim | Why assumed | Load-bearing? |
|-------|-------------|---------------|
| Host-probe stamps `- **Host:** <id>` on **every** host (not only cursor) before ship:6 | brief requires the stamp; this feature's progress.md already has it; Claude/Grok green tests will pass `--host` but live runs need the bullet | **yes** → spec Open questions |
| Cursor exposes no local per-turn usage file worth parsing in this PR | brief: "orchestrator is unavailable (no local usage field)"; no Cursor session parser exists in-repo | **yes** → spec Open questions (if a file appears later, add a table row, do not scrape) |
| Copilot `/usage` paste remains adapter-only, after finalize | copilot-tools.md already describes a human copy; dispatcher must not fetch | no (decision) |
| Grok `Host:` aliases `grok` and `grok-build` | grok-tools.md says "Grok Build"; progress stamp id is not specified in this charter | **yes** if host-probe picks a different slug → lock the id in spec |
| `--host` CLI override is allowed for tests | not in the brief; needed to test Claude/Grok without a full progress header | no |

## Dependency Legitimacy

None added. Stdlib only (`argparse`, `re`, `sys`, `pathlib`). Verdict n/a.

## Risks / unknowns (plan must consume)

1. **Unstamped Host on a live Claude run** after this PR yields unavailable instead of a transcript parse. Mitigate: host-probe stamps `Host: claude`; pitfalls.md "forgot the Host bullet, ledger went unavailable."
2. **Grok session resolve still `SystemExit`s** when `Host: grok` but no `~/.grok/sessions` (today's CLI). Dispatcher must not swallow that into a Cursor-style sentinel unless spec says so. Default: keep Grok's current failure (exit non-zero) so a mis-stamped `Host: grok` on Cursor does not silently look "fine."
3. **Span helper lift** can break `test_timing_report.py` if re-export is forgotten. Task: re-export + run that file.
4. **SKILL.md / TEMPLATE still advertising `token_report.py`** would keep Cursor agents invoking the old CLI. Task: those two strings plus grok/copilot adapter one-liners; pitfalls.md "shipped the script, left the old command in the skill."
5. **Same-machine Claude+Cursor** is the production case; tests must set `HOME` in the subprocess, not only pass `--transcript` (that flag would skip auto-detect and miss the bug).
6. No Cursor usage schema was verified this session (repo-question; none in-tree). If one appears, it is a new parser row, not a scrape.

## Sources (repo-only)

- `skills/ship/SKILL.md` ship:6.3, ship:8 check_tokens gate
- `skills/ship/scripts/{token_report,grok_token_report,check_tokens,_ledger}.py`
- `tests/{test_tokens_guardrail,test_grok_token_report,test_timing_report}.py`
- `references/{grok-tools,copilot-tools,codex-tools}.md`
- `skills/research/references/wit-directory.md` tokens.md template / ledger rule
- `docs/roadmap.md` v1.13.4; `docs/plans/2026-07-19-learnings-lifecycle-dryrun.md`
- `.wit/features/0001-cursor-capability-table/{brief.md,progress.md}`

checked wit@1.13.4 (plugin.json), repo-only, 2026-08-19. No spike (read settled it: `run_write` already fills Duration on parse failure; Cursor needs that path without `find_transcript`).
