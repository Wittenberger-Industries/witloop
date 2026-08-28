---
type: Pitfalls
title: "Pitfalls: Marketplace plugin descriptions under 1024 chars"
description: Failure modes for the description cap, each with the preventing task.
feature: 0005-marketplace-json-cap
timestamp: 2026-08-28
---

# Pitfalls: Marketplace plugin descriptions under 1024 chars

- **Testing gaps / weakened pin:** dropping a host, `/wit:` command, or `keep-alive` to squeeze under 1024 would go green on length and fail advertised-copy. Prevented by: task 1 keeps every existing assert and adds Codex to the same loop; wording is the 678-char paragraph that already contains every pin.
- **API & compatibility / advertised copy drift:** shortened text that says "scan bootstraps" would fail `test_manifests_say_scan_refreshes_not_bootstraps`. Prevented by: task 1 keeps `refreshes the map` and forbids `documents and bootstraps`.
- **Process / skill-ideas OKF:** `python scripts/validate.py` currently exits 1 on untracked `docs/skill-ideas/` missing frontmatter. "Fixing" those files or treating exit 1 as this bug would expand scope. Prevented by: task 1 Verify judges plugin-description-cap absence + live lengths, not the whole OKF list.
- **Process / lockstep miss:** bumping JSON versions but leaving `RELEASE`, overview, or README at 1.16.2. Prevented by: task 1 Files list includes those four plus the three manifests; overview test asserts not `1.16.2`.
- **Testing gaps / import validate.py:** importing validate.py runs the whole gate on the live tree. Prevented by: task 1 Do forbids import/subprocess; length is live-file `assertLessEqual` plus a source-anchor for `: plugin description is`.
- **Process / identity pin:** asserting the three descriptions are equal would be a new constraint the brief rejected. Prevented by: task 1 may copy the same paragraph but must not `assertEqual` across files.
- **0004 advertised-copy learning:** shortening manifests without keeping command names. Prevented by: task 1 pin list + the canned paragraph.
- **0001 ensure_logdir:** writing repro logs into the feature folder would gitignore the dossier. Prevented by: surface logs stay in `.wit/features/0005-marketplace-json-cap/.logs/` (already created).
