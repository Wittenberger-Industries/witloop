---
type: Pitfalls
title: "Pitfalls: First-class Cursor host via a capability table"
description: The failure modes that genuinely apply to this change, each with its preventing task.
feature: 0001-cursor-capability-table
timestamp: 2026-08-19
---

# Pitfalls: First-class Cursor host via a capability table

- **API & compatibility (validate.py tripwires):** how it could bite *here*: task 7 drops `autopilot`/`grok` from SKILL bodies while `validate.py` still requires those strings, so CI goes red on a cite-only edit. Prevented by: task 7 retargets those checks in the same task as the SKILL edits.
- **API & compatibility (Claude Host stamp):** how it could bite *here*: unstamped Host fail-safes to unavailable, so a Claude run that forgets the probe loses orchestrator tokens. Prevented by: task 7 detection recipe stamps `claude` | `codex` | `copilot` | `grok` | `cursor` (never copy this feature's Cursor stamp).
- **Testing gaps (foreign transcript bind):** how it could bite *here*: `find_transcript` cwd-scope still binds a leftover `~/.claude` session on the same project. Prevented by: task 5 plants `HOME/.claude` and asserts `token_report.py` is not invoked on `Host: cursor`.
- **Testing gaps (all-unavailable ledger):** how it could bite *here*: Duration placeholders `<dur>` fail `check_tokens.py` even when orchestrator is honestly unavailable. Prevented by: task 5 fills Duration from `progress.md` and re-runs `test_tokens_guardrail`.
- **Errors & resilience (Grok finalize still SystemExit):** how it could bite *here*: dispatcher must not turn a missing Grok session into a silent Cursor-style unavailable if Host is `grok`. Prevented by: task 5 delegates `grok` to `grok_token_report.py` unchanged; `test_grok_token_report` stays in Verify.
- **Ops & rollout (source repo vs marketplace cache):** how it could bite *here*: resolving plugin root to `~/.cursor/plugins/cache/.../1.13.4` while editing this source tree runs stale skills. Prevented by: ADR-0001 walk-up-before-cache; task 2 documents it in `cursor-tools.md`.
- **Process (host prose in SKILL bodies):** how it could bite *here*: Cursor-optimal details land in `dev/SKILL.md` and blow the always-loaded tax. Prevented by: task 7 pointer-only; constitution + brief non-goal; checker coverage of AC 8.
- **Process (PowerShell UTF-16 logs):** how it could bite *here*: `>` redirects in PowerShell 5.1 write UTF-16 LE, so later `grep` on `.logs/` misreads. Prevented by: not adding a third helper this PR (YAGNI); `ensure_logdir.py` is UTF-8; pitfalls note only. Follow-up if a real run corrupts a log.
- **Concurrency & state (named Task types flicker):** how it could bite *here*: a session without the plugin loaded has no `wit-*` types; treating that as fatal blocks Cursor. Prevented by: task 7 inline fallback; missing types are not a hard failure.
- **Auth & security:** none. No new secrets, no dashboard scrape.
