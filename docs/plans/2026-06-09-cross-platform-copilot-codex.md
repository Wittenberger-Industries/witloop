# Cross-platform wi (Codex CLI + Copilot CLI) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the wi plugin run unmodified-in-spirit on OpenAI Codex CLI and GitHub Copilot CLI from one shared skill source, by flattening the repo to a root-manifest plugin, adding per-platform packaging + a portability layer, and parameterizing wi's autonomy spine (`/goal`, subagents, worktrees) per platform.

**Architecture:** One canonical `skills/` + `agents/` tree at the repo root. Each platform discovers it natively: Claude via `.claude-plugin/` (convention), Codex via `.codex-plugin/plugin.json` (+ it reads `.claude-plugin/marketplace.json`), Copilot via whole-repo `/skills add`. Skills keep `${CLAUDE_PLUGIN_ROOT}` (native on Claude, compat var on Codex, mapped to the repo root on Copilot via `AGENTS.md` + tool-map). The `/goal` handoff becomes platform-conditional (Claude/Codex native `/goal`; Copilot Autopilot flags).

**Tech Stack:** Markdown skills (`SKILL.md` + YAML frontmatter, the agentskills.io standard), JSON manifests, Python 3 stdlib `scripts/validate.py` (PyYAML optional), `git` / `gh`.

**Spec:** `docs/specs/2026-06-09-cross-platform-copilot-codex-design.md` (read it first — capability matrix, decisions, risks R1–R5).

**Conventions for this plan:** This is a docs/manifest port, so most "tests" are `python scripts/validate.py` passing plus exact grep/JSON/`git` verification commands rather than unit tests. Where `validate.py` itself changes, add the check first and watch it fail (RED) before creating the artifact (GREEN). One task → one commit. Never weaken a check to make it pass.

---

## Task 1: Flatten to a root-manifest plugin

**Files:**
- Move (git mv): `plugins/wi/skills/` → `skills/`, `plugins/wi/agents/` → `agents/`, `plugins/wi/.claude-plugin/plugin.json` → `.claude-plugin/plugin.json`, `plugins/wi/README.md` → `README-wi.md` (temporary; merged in Task 8)
- Modify: `.claude-plugin/marketplace.json` (line 13, `source`), `.gitignore`, `scripts/validate.py:32-81`
- Delete (after move): the now-empty `plugins/` tree

- [ ] **Step 1: Confirm the starting layout**

Run: `git ls-files plugins/ | head` and `git ls-files | wc -l`
Expected: files listed under `plugins/wi/...`; remember the count to confirm the move preserves files.

- [ ] **Step 2: Move skills and agents to the root with history preserved**

```bash
git mv plugins/wi/skills skills
git mv plugins/wi/agents agents
git mv plugins/wi/.claude-plugin/plugin.json .claude-plugin/plugin.json
git mv plugins/wi/README.md README-wi.md
```

Then remove the leftover empty dirs (git mv leaves `plugins/wi/.claude-plugin/` empty):
```bash
rmdir plugins/wi/.claude-plugin plugins/wi plugins 2>/dev/null; true
```

- [ ] **Step 3: Point the marketplace at the repo root**

In `.claude-plugin/marketplace.json`, change the plugin source from the nested path to root:
- Old: `      "source": "./plugins/wi",`
- New: `      "source": "./",`

(Leave `name`, `description`, `version`, `keywords` as they are.)

- [ ] **Step 4: Update the .gitignore whitelist for the flat layout**

Replace the published-paths block in `.gitignore` so the new top-level dirs are tracked. The file should read:

```gitignore
# Whitelist approach: ignore everything by default...
*

# ...but descend into directories so nested whitelist rules can match...
!*/

# ...then re-include only the plugin's published paths.
!/.claude-plugin/**
!/.codex-plugin/**
!/skills/**
!/agents/**
!/references/**
!/hooks/**
!/scripts/**
!/docs/**
!/AGENTS.md
!/README.md
!/.gitignore
```

(`.codex-plugin/`, `references/`, `hooks/`, `AGENTS.md` are added now so later tasks' files are tracked; `plugins/` is intentionally dropped.)

- [ ] **Step 5: Update validate.py to the flat layout**

In `scripts/validate.py`, replace the three discovery blocks (manifests, frontmatter files, cross-refs) with root-relative versions.

Replace the manifests block (currently lines 32-33):
```python
manifests = [
    ROOT / ".claude-plugin" / "marketplace.json",
    ROOT / ".claude-plugin" / "plugin.json",
]
```

Replace the frontmatter glob (currently line 44):
```python
fm_files = sorted(ROOT.glob("skills/**/SKILL.md")) + sorted(ROOT.glob("agents/*.md"))
```

Replace the cross-ref block (currently lines 74-81) — `${CLAUDE_PLUGIN_ROOT}/<path>` now resolves against the repo root:
```python
rx = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\s`)\]]+)")
ref_md = (
    list(ROOT.glob("skills/**/*.md"))
    + list(ROOT.glob("agents/*.md"))
    + list(ROOT.glob("references/*.md"))
    + [ROOT / "AGENTS.md", ROOT / "README.md"]
)
for md in ref_md:
    if not md.is_file():
        continue
    for ref in rx.findall(md.read_text(encoding="utf-8")):
        if not (ROOT / ref).exists():
            errors.append(f"{md.relative_to(ROOT)}: broken ref ${{CLAUDE_PLUGIN_ROOT}}/{ref}")
```

Also update the module docstring (lines 7-13) to describe the flat layout instead of `plugins/*/...`.

- [ ] **Step 6: Run validation — expect GREEN**

Run: `python scripts/validate.py`
Expected: `[OK] all checks passed`, with manifest/frontmatter counts that match the moved files (8 skills + 2 agents = 10 frontmatter files; 2 manifests). If a `${CLAUDE_PLUGIN_ROOT}` ref now reports broken, it points outside `skills/`/`agents/` — confirm the target exists at the repo root and fix the ref or the path.

- [ ] **Step 7: Confirm no files were lost**

Run: `git status --short` and `git ls-files | wc -l`
Expected: renames (`R`) for moved files, the modified `.gitignore`/`marketplace.json`/`validate.py`; total tracked-file count unchanged from Step 1 (minus none — moves don't change the count).

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "refactor: flatten wi to a root-manifest plugin"
```

---

## Task 2: Add the Codex plugin manifest

**Files:**
- Create: `.codex-plugin/plugin.json`
- Modify: `scripts/validate.py` (add `.codex-plugin/plugin.json` to manifests + a key check)

- [ ] **Step 1 (RED): Add the Codex manifest to validation before creating it**

In `scripts/validate.py`, append to the `manifests` list and add a content check right after the JSON-validity loop:

```python
manifests.append(ROOT / ".codex-plugin" / "plugin.json")
```

And after the manifest JSON loop, add:
```python
# Codex manifest must declare name/version/skills, and skills must resolve
codex = ROOT / ".codex-plugin" / "plugin.json"
if codex.is_file():
    try:
        cd = json.loads(codex.read_text(encoding="utf-8"))
        for k in ("name", "version", "skills"):
            if not cd.get(k):
                errors.append(f".codex-plugin/plugin.json: missing '{k}'")
        skills_path = cd.get("skills", "")
        if skills_path and not (ROOT / skills_path).is_dir():
            errors.append(f".codex-plugin/plugin.json: skills path '{skills_path}' is not a dir")
    except Exception:
        pass  # JSON validity already reported by the loop above
```

- [ ] **Step 2 (RED): Run validation — expect FAIL**

Run: `python scripts/validate.py`
Expected: `[FAIL]` with `missing manifest: .codex-plugin/plugin.json`.

- [ ] **Step 3 (GREEN): Create `.codex-plugin/plugin.json`**

```json
{
  "name": "wi",
  "version": "0.7.0",
  "description": "An opinionated, low-token engineering loop: /wi:scan documents and bootstraps a repo; /wi:dev brainstorms a feature with you then designs and builds it to an open PR; /wi:rpa turns a UiPath PDD into a built REFramework solution. Spec-driven, parallel subagent waves, isolated worktrees, ADR log, token report. Runs on Claude Code, Codex CLI, and Copilot CLI from one source.",
  "skills": "./skills/"
}
```

(No `hooks` pointer yet — `hooks/` is conditional; Task 9 adds the pointer only if a hook is created.)

- [ ] **Step 4 (GREEN): Run validation — expect PASS**

Run: `python scripts/validate.py`
Expected: `[OK] all checks passed`; manifest count now 3.

- [ ] **Step 5: Commit**

```bash
git add .codex-plugin/plugin.json scripts/validate.py
git commit -m "feat: add Codex CLI plugin manifest (.codex-plugin/plugin.json)"
```

---

## Task 3: Add cross-platform tool-name maps

**Files:**
- Create: `references/codex-tools.md`, `references/copilot-tools.md`
- Modify: `scripts/validate.py` (require both files exist)

- [ ] **Step 1 (RED): Require the tool maps in validation**

In `scripts/validate.py`, after the cross-ref block, add:
```python
for tm in ("references/codex-tools.md", "references/copilot-tools.md", "AGENTS.md"):
    if not (ROOT / tm).is_file():
        errors.append(f"missing portability file: {tm}")
```

Run: `python scripts/validate.py` → Expected: `[FAIL]` listing the three missing files. (AGENTS.md is created in Task 4; this task makes the two tool maps pass and leaves AGENTS.md failing until Task 4 — that's expected and fine to carry one task forward. If you prefer a green commit here, add AGENTS.md in Task 4 before committing the validation change; either order works as long as the final state is green.)

- [ ] **Step 2 (GREEN): Create `references/codex-tools.md`**

```markdown
# Codex CLI — tool & capability mapping for wi

wi's skills are written with Claude Code names. On Codex CLI, use these equivalents.

## ${CLAUDE_PLUGIN_ROOT}
`${CLAUDE_PLUGIN_ROOT}` is the **wi plugin root** — the directory holding `skills/`, `agents/`, and
`.claude-plugin/`. Codex sets `CLAUDE_PLUGIN_ROOT` (and `PLUGIN_ROOT`) for compatibility, so most refs
resolve as-is. If a ref doesn't resolve in a skill context, treat it as the installed wi plugin dir and
read the file by its path under that root. This covers cross-skill refs (e.g. `ship` reading
`${CLAUDE_PLUGIN_ROOT}/skills/scan/scripts/check_mermaid.py`).

## Tools
| wi/skill says | Codex equivalent |
|---|---|
| Read / Write / Edit a file | native file tools / `apply_patch` |
| Bash / run a command | `shell` |
| Grep / Glob | native search (`shell` with `rg`/`grep`/`find`) |
| dispatch a subagent / task-runner | `spawn_agent` (parallel: multiple `spawn_agent`, or `spawn_agents_on_csv`) |
| parallel waves | `spawn_agent` bounded by `[agents] max_threads` (default 6); inline the task-runner/researcher prompt — do not rely on named-role dispatch |
| TodoWrite | `update_plan` |
| WebFetch / WebSearch | `web_search` |
| invoke a wi skill | skills load natively — `$skill-name` or `/skills`; just follow its instructions |

## /goal keep-alive
Codex has a native `/goal`. Use the same condition line wi prints. For non-interactive runs, `codex exec`
with `--ask-for-approval never --sandbox workspace-write`.

## Worktrees
If the sandbox blocks branch/push (detached HEAD / externally managed worktree), do **not** fail: commit
all work in place and hand the user a suggested branch name, commit message, and PR body to apply via the
app's native controls. Detect with read-only `git rev-parse --git-dir`/`--git-common-dir` and
`git branch --show-current` before creating a worktree.

## Subagent caveat
Repo-local custom-agent *roles* are not reliably selectable by name across Codex builds. wi's build/research
fan-out passes the agent prompt inline to a generic worker, so this caveat does not block wi.
```

- [ ] **Step 3 (GREEN): Create `references/copilot-tools.md`**

```markdown
# Copilot CLI — tool & capability mapping for wi

wi's skills are written with Claude Code names. On Copilot CLI, use these equivalents.

## ${CLAUDE_PLUGIN_ROOT}
Copilot has no plugin-root variable. `${CLAUDE_PLUGIN_ROOT}` means the **wi plugin root** — the directory
holding `skills/`, `agents/`, and `.claude-plugin/` (i.e. the cloned wi repo). Install wi **whole** (clone +
`/skills add <repo>/skills`) so that root exists, then resolve every `${CLAUDE_PLUGIN_ROOT}/…` against it.
This is why per-skill `gh skill install` is discouraged: cross-skill refs (`ship` →
`skills/scan/scripts/check_mermaid.py`) and the plugin-version read (`research` →
`.claude-plugin/plugin.json`) need the shared root.

## Tools
| wi/skill says | Copilot equivalent |
|---|---|
| Read | `view` |
| Write | `create` |
| Edit | `edit` / `apply_patch` |
| Bash | `bash` |
| Grep / Glob | `grep` / `glob` |
| dispatch a subagent / task-runner | `task` tool (custom agent) |
| parallel waves | `/fleet` (monitor with `/tasks`) |
| WebFetch | `web_fetch` |
| WebSearch | no equivalent — use `web_fetch` with a search URL |
| invoke a wi skill | skills load natively — `/<skill-name>` or auto-trigger by description |

## /goal keep-alive
Copilot has no predicate `/goal`. Use **Autopilot**: relaunch with the completion condition in the prompt —
`copilot --autopilot --max-autopilot-continues <N> --no-ask-user -p "<prompt incl. done-condition>"`.
Completion is model-judged and continuation-capped, not a hard predicate.

## Command namespace
`/wi:dev` etc. do not exist (Copilot has no custom slash commands). Invoke the skill as `/<skill-name>`
(e.g. `/dev`, `/scan`) or let it auto-trigger from its `description`.
```

- [ ] **Step 4: Commit** (defer the run to Task 4, which adds the last required file)

```bash
git add references/codex-tools.md references/copilot-tools.md scripts/validate.py
git commit -m "docs: add Codex + Copilot tool-name and capability maps"
```

---

## Task 4: Add the AGENTS.md bootstrap

**Files:**
- Create: `AGENTS.md`

- [ ] **Step 1 (GREEN): Create `AGENTS.md`**

```markdown
# wi — cross-platform bootstrap

This repository **is** the wi plugin: an opinionated, low-token, spec-driven dev loop. Its capabilities
are delivered as skills under `skills/` (`scan`, `dev`, `research`, `plan`, `build`, `ship`, `brainstorm`,
`rpa`) plus two subagent prompt templates under `agents/`.

## If you are not Claude Code
wi's skills use Claude Code tool names and the `${CLAUDE_PLUGIN_ROOT}` variable. Before following a skill,
read the mapping for your platform and apply it as you go:

- **Codex CLI:** `references/codex-tools.md`
- **GitHub Copilot CLI:** `references/copilot-tools.md`

Key rule: **`${CLAUDE_PLUGIN_ROOT}` is this repo's root** (the directory holding `skills/`, `agents/`,
`.claude-plugin/`). Resolve every `${CLAUDE_PLUGIN_ROOT}/…` path against it.

## Invoking wi
- Start a feature: the `dev` skill (`/wi:dev` on Claude, `/dev` or `$dev` elsewhere, or describe the
  feature and let it auto-trigger).
- Bootstrap a repo first with the `scan` skill.
- Persistence: wi hands off to a keep-alive loop at the end of brainstorm — Claude/Codex use built-in
  `/goal`; Copilot uses Autopilot flags (see the tool map). wi runs without it too, just less robustly.

These skills auto-trigger from their `description` fields. When a user's request matches one, use it.
```

- [ ] **Step 2 (GREEN): Run validation — expect PASS**

Run: `python scripts/validate.py`
Expected: `[OK] all checks passed` (the three portability files from Task 3's check now all exist).

- [ ] **Step 3: Commit**

```bash
git add AGENTS.md
git commit -m "feat: add AGENTS.md cross-platform bootstrap"
```

---

## Task 5: Make the `/goal` handoff platform-aware

**Files:**
- Modify: `skills/dev/SKILL.md` (step 4 handoff block, ~lines 34-50; frontmatter line 8)
- Modify: `skills/research/SKILL.md` (§4 handoff, ~lines 82-94; frontmatter line 9-10)
- Modify: `skills/ship/SKILL.md` (§7 close-out `/goal` line, ~line 139)
- Modify: `scripts/validate.py` (assert the Copilot/Autopilot branch exists in dev + research)

- [ ] **Step 1: Replace the handoff block in `skills/dev/SKILL.md`**

Replace step 4's body (the "Hand off — and arm the built-in `/goal`" paragraph and its single `/goal`
code block) with a platform-conditional handoff. The new block:

````markdown
4. **Hand off — and arm persistence (platform-aware).** Recap the brief in 3-5 lines, then print the
   keep-alive handoff for the current platform:

   - **Claude Code / Codex CLI** (both have a built-in `/goal`):

     ```
     /goal The <slug> PR is open and its branch passes <lint + test commands from repo-map.md>;
     .wi/goals/<slug>/progress.md Phase is done. Constraints: only files named in tasks.md change;
     never force-push; tests are never weakened to pass.
     ```

   - **GitHub Copilot CLI** (no `/goal` — use Autopilot, condition in the prompt):

     ```
     copilot --autopilot --max-autopilot-continues <N> --no-ask-user -p "Drive the <slug> goal to done:
     build then ship until the <slug> PR is open, its branch passes <lint + test commands>, and
     .wi/goals/<slug>/progress.md Phase is done. Only files named in tasks.md change; never force-push;
     never weaken tests."
     ```

   Armed, the run continues across turns until the condition holds (wi works without it, just less
   robustly through a stalled turn). The mechanism per platform is in
   `${CLAUDE_PLUGIN_ROOT}/references/codex-tools.md` / `copilot-tools.md`. **Then branch on Gate mode
   (from `progress.md`):**
````

(Keep the existing "auto-approve / interactive" bullets that follow unchanged.)

- [ ] **Step 2: Update the dev frontmatter description**

In `skills/dev/SKILL.md` frontmatter, change the sentence that says it prints a line for "Claude Code's
BUILT-IN /goal command" to be platform-neutral:
- New phrasing: `At handoff it arms a keep-alive loop so the run continues across turns until the PR condition is met — Claude Code and Codex CLI use their built-in /goal, Copilot CLI uses Autopilot.`

- [ ] **Step 3: Replace the §4 handoff in `skills/research/SKILL.md`**

Replace the single `/goal` code block under "### 4 - Hand off to implementation" with the same
two-platform block from Step 1 (Claude/Codex `/goal` + Copilot Autopilot), and change the surrounding
prose "If the built-in `/goal` wasn't armed" → "If persistence wasn't armed at handoff". Update the
trailing sentence "The built-in `/goal` is the persistence wrapper" → "The keep-alive loop (/goal or
Autopilot) is the persistence wrapper".

- [ ] **Step 4: Update the research frontmatter description**

In `skills/research/SKILL.md` frontmatter, change "with Claude Code's BUILT-IN /goal command as the
recommended keep-alive wrapper" → "with a keep-alive loop (Claude/Codex /goal, or Copilot Autopilot) as
the recommended persistence wrapper".

- [ ] **Step 5: Update the close-out line in `skills/ship/SKILL.md`**

Change the final sentence of §7 — "If the built-in `/goal` is armed, this is the state in which its
condition holds and the loop clears." → "If a keep-alive loop is armed (Claude/Codex `/goal` or Copilot
Autopilot), this is the state in which its condition holds and the loop clears."

- [ ] **Step 6 (RED→GREEN): Assert the Autopilot branch exists**

In `scripts/validate.py`, add a content check:
```python
for s in ("skills/dev/SKILL.md", "skills/research/SKILL.md"):
    if "autopilot" not in (ROOT / s).read_text(encoding="utf-8").lower():
        errors.append(f"{s}: missing Copilot Autopilot handoff branch")
```
Run `python scripts/validate.py` after adding the check but before the edits to see it FAIL (if you edited first, it passes immediately — acceptable). Final state: PASS.

- [ ] **Step 7: Run validation + sanity grep**

Run: `python scripts/validate.py` → Expected: `[OK]`.
Run: `grep -rl "autopilot" skills/dev skills/research` → Expected: both files listed.

- [ ] **Step 8: Commit**

```bash
git add skills/dev/SKILL.md skills/research/SKILL.md skills/ship/SKILL.md scripts/validate.py
git commit -m "feat: platform-aware /goal handoff (Codex /goal, Copilot Autopilot)"
```

---

## Task 6: Subagent dispatch note + worktree sandbox fallback

**Files:**
- Modify: `skills/build/references/worktrees-and-subagents.md` (Variants list ~lines 38-43; Subagent dispatch ~lines 51-55)

- [ ] **Step 1: Add the sandbox/detached-HEAD fallback to the Variants list**

In the "### Variants" bullet list under "## Git worktrees", add a new bullet after the "Restricted
filesystems" one:

```markdown
- **Sandboxed / no-branch environments (e.g. Codex sandbox):** if `git rev-parse --git-dir` differs from
  `--git-common-dir` (already in a linked worktree) or `git branch --show-current` is empty (detached
  HEAD), do **not** create a worktree or try to push. Work in place, commit per task, and at ship hand the
  user a suggested branch name, commit message, and PR body to apply via the platform's native controls.
  Note "Worktree: - (sandboxed)" in progress.md.
```

- [ ] **Step 2: Make the subagent-dispatch paragraph platform-aware**

In "## Subagent dispatch", after the sentence "Use the `task-runner` agent (`agents/task-runner.md`).",
add:

```markdown
The dispatch mechanism is platform-specific (see `${CLAUDE_PLUGIN_ROOT}/references/codex-tools.md` /
`copilot-tools.md`): Claude uses the Agent/Task tool, Copilot uses the `task` tool and `/fleet` for waves,
Codex uses `spawn_agent` bounded by `[agents] max_threads`. On every platform, pass the task-runner prompt
**inline** to a generic worker — do not depend on a pre-registered named agent (Codex named-role dispatch
is unreliable across builds).
```

- [ ] **Step 3: Run validation**

Run: `python scripts/validate.py` → Expected: `[OK]` (no broken `${CLAUDE_PLUGIN_ROOT}` refs — the two
`references/*.md` targets exist from Task 3).

- [ ] **Step 4: Commit**

```bash
git add skills/build/references/worktrees-and-subagents.md
git commit -m "feat: document Codex sandbox worktree fallback + per-platform subagent dispatch"
```

---

## Task 7: Copilot fallbacks for plugin-root reads

**Files:**
- Modify: `skills/research/SKILL.md` (§0 version read, ~line 34)

- [ ] **Step 1: Add a fallback to the plugin-version read**

In `skills/research/SKILL.md` §0, the line reads the version from
`${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`. Append a fallback clause so it degrades on platforms
where that file isn't present at the resolved root (e.g. a per-skill Copilot install):

- Change: `reading <version> from ${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json (don't guess)`
- To: `reading <version> from ${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json (don't guess; if that file isn't reachable — e.g. a per-skill Copilot install — omit the version rather than inventing one)`

- [ ] **Step 2: Run validation**

Run: `python scripts/validate.py` → Expected: `[OK]`.

- [ ] **Step 3: Commit**

```bash
git add skills/research/SKILL.md
git commit -m "fix: degrade plugin-version read when plugin root is unreachable (Copilot)"
```

---

## Task 8: README — merge, per-platform install, capability note

**Files:**
- Modify: `README.md` (root marketplace README)
- Delete: `README-wi.md` (folded in; the wi plugin README content merges into the root README's relevant sections)
- Modify: `.claude-plugin/marketplace.json` + `.claude-plugin/plugin.json` descriptions (drop "for Claude Code" exclusivity)

- [ ] **Step 1: Add an Install section covering all three platforms**

In `README.md`, replace the current single "## Install" block with:

````markdown
## Install

**Claude Code**
```
/plugin marketplace add Wittenberger-Industries/wi-plugin
/plugin install wi@wi
```

**Codex CLI** — Codex reads this repo's `.claude-plugin/marketplace.json` and `.codex-plugin/plugin.json`.
Add the marketplace/repo via Codex's plugin flow (`/plugins`) and enable `wi`. Native `/goal` and
`CLAUDE_PLUGIN_ROOT` compatibility work out of the box.

**GitHub Copilot CLI** — clone the repo and register the whole skills dir (recommended, because wi skills
are interdependent):
```
git clone https://github.com/Wittenberger-Industries/wi-plugin
# in Copilot CLI:
/skills add <path-to-clone>/skills
```
Invoke skills as `/dev`, `/scan`, … (Copilot has no `wi:` command namespace). Persistence uses Autopilot
(`--autopilot --max-autopilot-continues N`) instead of `/goal`.
````

- [ ] **Step 2: Add a short capability-differences note**

Add a subsection after Install:

```markdown
## Platform differences

wi is one source across three harnesses; only the autonomy spine differs:

| | Claude Code | Codex CLI | Copilot CLI |
|---|---|---|---|
| Skills | plugin | `.codex-plugin` (+ reads `.claude-plugin/marketplace.json`) | whole-repo `/skills add` |
| Keep-alive | built-in `/goal` | native `/goal` | Autopilot flags |
| Command namespace | `/wi:dev` | `$dev` / `/skills` | `/dev` |
| `${CLAUDE_PLUGIN_ROOT}` | native | compat var | = the cloned repo root |
```

- [ ] **Step 3: Fold the wi plugin README into the root and remove the temp file**

Merge any unique content from `README-wi.md` (the `.wi/` directory layout, skills table, philosophy) into
`README.md` where it fits, then:
```bash
git rm README-wi.md
```

- [ ] **Step 4: De-Claude-exclusive the manifest descriptions**

In `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`, change "for Claude Code" / "built
for /goal-driven work" phrasing in the `description` to note tri-platform support (mirror the
`.codex-plugin/plugin.json` description from Task 2). Keep them valid JSON.

- [ ] **Step 5: Run validation + commit**

Run: `python scripts/validate.py` → Expected: `[OK]`.
```bash
git add -A
git commit -m "docs: per-platform install, capability note, merge plugin README"
```

---

## Task 9: Decide the bootstrap hook (R5) + final validate.py sweep

**Files:**
- Possibly create: `hooks/hooks.json`, `hooks/session-start` (+ pointer in both plugin manifests)
- Modify: `scripts/validate.py` (final review)

- [ ] **Step 1: Test whether AGENTS.md alone auto-triggers skills (R5)**

On each available platform, open a clean session and send a build-intent message (e.g. "let's add a small
feature to this project"). Observe whether the `dev`/`brainstorm` skill auto-triggers.
- If **yes** → no hook needed; record the result and skip to Step 3.
- If **no** → add a light SessionStart bootstrap in Step 2.

- [ ] **Step 2 (only if needed): Add a platform-aware session-start hook**

Create `hooks/hooks.json` (Claude/Copilot SessionStart format) and `hooks/session-start` that injects a
one-paragraph "use wi's skills; see AGENTS.md + your tool map" context, detecting the platform via env vars
(`CLAUDE_PLUGIN_ROOT` vs `COPILOT_CLI`) and emitting the matching JSON field — model this on superpowers'
`hooks/session-start`. Add `"hooks": "./hooks/hooks.json"` to `.codex-plugin/plugin.json` and the Claude
plugin manifest. Re-run the Step 1 acceptance test to confirm it now triggers.

- [ ] **Step 3: Final validate.py review + full run**

Confirm `scripts/validate.py` checks, end to end: 3 manifests valid; 10 frontmatter files with name+desc;
all `${CLAUDE_PLUGIN_ROOT}` refs resolve from root; codex manifest keys; tool maps + AGENTS.md present;
Autopilot branch in dev+research. Run: `python scripts/validate.py` → Expected: `[OK]`.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "chore: finalize bootstrap decision (R5) and validation sweep"
```

---

## Task 10: Empirical verification of R1–R5 (per platform)

This task is verification, not code; it requires the actual CLIs. Record results in
`docs/specs/2026-06-09-cross-platform-copilot-codex-design.md` under a new "## 14. Verification results"
section. Do what the environment allows; explicitly note any check that couldn't be run.

- [ ] **R1 — Claude install from flat layout:** `/plugin marketplace add <local path>` then
  `/plugin install wi@wi`; confirm skills load and `/wi:dev` runs the brainstorm. Record PASS/FAIL.
- [ ] **R2 — `${CLAUDE_PLUGIN_ROOT}` in Codex skill context:** in a Codex session, have a skill resolve a
  `${CLAUDE_PLUGIN_ROOT}/skills/.../references/*.md` path; confirm it reads. If not, confirm the
  tool-map's root rule covers it. Record.
- [ ] **R3 — Copilot skill discovery:** clone + `/skills add <repo>/skills`; confirm `/dev` (or
  auto-trigger) runs and a cross-skill ref (`ship` → `scan/scripts/check_mermaid.py`) resolves. Record.
- [ ] **R4 — Codex parallel fan-out:** run a multi-task build wave; confirm `spawn_agent` parallelism
  respects `max_threads` and the sandbox fallback triggers under a no-branch sandbox. Record.
- [ ] **R5 — auto-trigger:** result already captured in Task 9 Step 1; copy it here.
- [ ] **Commit** the verification-results section:
  ```bash
  git add docs/specs/2026-06-09-cross-platform-copilot-codex-design.md
  git commit -m "docs: record R1-R5 cross-platform verification results"
  ```

---

## Self-review (completed by plan author)

**Spec coverage:** §4 layout → Task 1; §5 Codex/Copilot packaging → Tasks 2, 8; §6.1 `/goal` → Task 5;
§6.2 subagents → Task 6; §6.3 worktrees → Task 6; §7.1 paths → Tasks 3, 4, 7; §7.2 tool maps → Task 3;
§7.3 bootstrap → Task 4 (+ Task 9 hook if needed); §8 docs+validate → Tasks 8, 9; §10 risks R1–R5 →
Task 10; §11 acceptance criteria → covered by Tasks 1–10. No spec requirement left without a task.

**Placeholder scan:** `<slug>`, `<N>`, `<version>`, `<path-to-clone>` are intentional runtime
placeholders inside example commands/skill prose, not unfilled plan steps. All file contents are concrete.

**Consistency:** validate.py changes are additive and ordered (Task 1 rewrites discovery; Tasks 2/3/5/9
append checks against artifacts created in the same or prior task). The `${CLAUDE_PLUGIN_ROOT}` = repo-root
rule is stated identically in both tool maps, AGENTS.md, and the spec. `hooks/` is whitelisted in Task 1
but only created conditionally in Task 9 — consistent with §7.3.
