---
type: Pitfalls
title: "Pitfalls: /wit-setup first-run"
description: Failure modes that apply to this change, each with a preventing task.
feature: 0004-setup
timestamp: 2026-08-27
---

# Pitfalls: /wit-setup first-run

- **Glob vs four-command tests:** Creating user-invocable `skills/setup/SKILL.md` before updating
  `USER_COMMANDS` and README fails the wave-end suite. Prevented by: Task 1 (skill + advertised
  lockstep + 1.16.2 in one sitting).
- **Directory tell vs add-issues:** Gating on missing `.wit/` fires after add-issues mkdirs
  `.wit/issues/`. Prevented by: Task 4 (tell is missing `repo-map.md`).
- **Scan tell-only:** Scan must **run** setup on a missing map, not print a hint. Prevented by:
  Task 2 (invoke setup; no chained refresh).
- **Refresh A.3 dangling "rules above":** Scan's mermaid trap lives in first-run procedure text.
  After the move, refresh still says "rules above". Prevented by: Task 2 (copy the trap into the
  remaining refresh body).
- **Inherit-all upgrade hole:** A pre-setup scan has a map and no `models.md`. Next dev would
  inherit-all and never ask. Prevented by: Task 4 (absent models.md → setup models+ledger slice).
- **Investigation calls setup:** Work-type prelude must still skip write-capable setup.
  Prevented by: Task 4 (investigation does not invoke setup).
- **Skip still inits tokens.md:** RPA "tokens.md is mandatory" and ship:8 seven-file dossier would
  ignore `ledger: skip`. Prevented by: Task 5 (honor skip in those lists and `--init` sites).
- **Plugin-root tell swapped to setup:** Walk-up keys on `skills/scan/SKILL.md`. Prevented by: Task 1
  (keep that tell; tests pin it).
- **New PLUGIN_ROOT always-loaded file:** Serial wiring trap. Prevented by: ledger in project
  `.wit/models.md` (learning 0003-work-type-routing).
- **Mid-run ledger toggle:** A skip after `--init` leaves PENDING tokens.md. Prevented by: no
  mid-run toggle (setup writes once; edit the file by hand is out of band).
- **Grok `/setup` clash:** Bare name may lose to a builtin. Prevented by: Task 1/3 (advertise
  `/wit-setup`; grok-tools notes the branded form).
- **Architecture 1.16.0 caption:** Overview moves to 1.16.2; historical PLUGIN_ROOT caption must
  stay if still present. Prevented by: Task 1 (do not retarget that caption).
