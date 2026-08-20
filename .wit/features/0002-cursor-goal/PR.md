## Summary
- Cursor now has native `/goal`. After 1.14.0 (#90) shipped Cursor keep-alive as `none`, this patch puts Cursor on `model_judged_goal` with Grok: the same one-line `/goal` paste, with `CreateGoal` / `UpdateGoal` named in `references/cursor-tools.md`.
- `none` stays a valid unused key. Grok headless CLI (`grok -p`, `--always-approve`) moved to `grok-tools.md` so a Cursor print cannot emit it.
- Three manifests bump **1.14.0 → 1.14.1**. ADR-0001.4 amended in place (accepted ADR; cell value only).

## Test plan
- [x] `python -m unittest tests.test_keep_alive tests.test_capabilities`
- [x] `python scripts/validate.py`
- [x] `python -m unittest discover -s tests` (147 tests)
- [ ] CI Validate workflow green on this PR
- [ ] A Cursor `/wit:dev` handoff prints `/goal`, not keep-alive none

## Rules inventory
| File | Before | After | Loaded-alone still decides? |
|---|---|---|---|
| `references/keep-alive.md` | Cursor index = `none` | Cursor+Grok share `model_judged_goal`; `none` unused | Yes: print by stamped cell |
| `references/cursor-tools.md` | Keep-alive none; never paste `/goal` | `CreateGoal` once on paste; `UpdateGoal` `complete` after audit | Yes |
| `references/capabilities.md` | Cursor `keep_alive=none` | Cursor `model_judged_goal` | Yes |
| `references/grok-tools.md` | Pointer only | Owns headless CLI | Yes |
| `AGENTS.md` / `README.md` | Cursor: none | Cursor: model-judged `/goal` | Yes |
| `skills/ship/SKILL.md` | Armed loop = Claude/Codex `/goal` or Autopilot | Armed loop = stamped `keep_alive` | Yes |
| `scripts/validate.py` | `Grok Build`+`update_goal` | Also four keys + `CreateGoal`/`UpdateGoal` in cursor-tools | Yes |
| `.wit/glossary.md` / ADR-0001.4 | Keep-alive none is Cursor | Model-judged `/goal` is Grok+Cursor | Yes |
