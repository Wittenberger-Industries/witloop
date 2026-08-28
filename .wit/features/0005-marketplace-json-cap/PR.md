---
type: PR Description
title: Marketplace plugin descriptions under 1024 chars
description: Cap JSON plugin descriptions at 1024
feature: 0005-marketplace-json-cap
timestamp: 2026-08-28
---

## fix: cap plugin JSON descriptions at 1024 chars (v1.16.3)

### Summary
Plugin `description` fields in marketplace.json, plugin.json, and the Codex manifest grew past the 1024-character marketplace/install ceiling (1357 / 1396 / 1396). `DESC_CAP` already capped SKILL.md only. Root cause: check 7a never walked those JSON fields. Smallest fix: a sibling 7a-json loop using the same `DESC_CAP`, shortened live copy that still names the five commands, five hosts, and keep-alive, and lockstep 1.16.3.

### Acceptance criteria
- [x] Same-surface fail then pass on `python scripts/validate.py` (before: no plugin-description-cap error while over 1024; after: lengths 678, exit 0, no `plugin description is`)
- [x] Root cause recorded: DESC_CAP 7a walked SKILL.md only; 7a-json now exists
- [x] Smallest fix: sibling loop, no new checker, no fixture ROOT, no identity pin
- [x] Regression: lockstep description test keeps every pin, adds Codex, live `len(desc) <= cap`, source-anchor `: plugin description is`
- [x] Advertised copy still has five `/wit:` commands, five hosts, `keep-alive`, `refreshes the map`
- [x] Versions lockstep at 1.16.3; marketplace catalog stays 0.2.0

### Changes
- `scripts/validate.py`: 7a-json after SKILL 7a
- Three plugin `description` fields shortened to 678 chars
- `tests/test_work_type_release.py`: Codex in the pin loop, DESC_CAP live length, source-anchor, RELEASE 1.16.3
- README and `.wit/overview.md` current-release tells

### Testing
- Format / lint / typecheck: n/a - not configured
- `python -m unittest discover -s tests` → 369 OK (`.logs/gate-tests.txt`)
- `python scripts/validate.py` → `[OK] all checks passed` (`.logs/gate-ci.txt`)
- Fail then pass on `python scripts/validate.py`: before lengths 1357/1396/1396 with no cap error (`research/repro.md`); after lengths 678, exit 0, no `plugin description is` (`.logs/repro-after.txt`)

### Safety fact
- Claim: the three plugin JSON `description` fields are ≤1024 and validate.py flags an over-cap
- Proof: `python scripts/validate.py` (this session; exit 0; lengths 678; 7a-json wired at `scripts/validate.py:334-351`)

### Verification
Result-mode checker: PASS. All six ACs, bug-fix rows, and the safety fact wired. Line-level: no BLOCKER / WARNING / INFO. Learnings 0001 and 0004 honored. No ADRs. No waived findings.

### Risk & rollout
Patch 1.16.3. Revert the PR to restore 1.16.2. No migration.

### Decisions
No ADR (nothing hard to reverse).
