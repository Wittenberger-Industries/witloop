---
type: Research Note
title: POSIX snippets vs PowerShell, and the now.py helpers this PR must ship
description: Repo-question audit of skills/references/agents for POSIX recipes that fail on Cursor-on-Windows PowerShell, plus the minimum stdlib helper set.
feature: 0001-cursor-capability-table
timestamp: 2026-08-19
valid_until: 2026-09-18
---

# POSIX helpers for Cursor-on-Windows

## Responsibility Map

Plugin markdown + stdlib Python under `skills/*/scripts/` (not an app; no frontend/backend split). Helpers are invoked by ship, add-issues, and the workflow output-house-rule, the same way `now.py` already is.

## Question

Which POSIX snippets in this repo fail on PowerShell, and which tiny Python helpers (the `now.py` pattern) must ride along to unblock Cursor-on-Windows?

Out of scope (siblings): table placement, token dispatcher, cursor adapter (keep-alive / models / discovery). Worktrees staying at `../<repo>-wit-<slug>` is a separate issue.

## Decision

Ship **two new** stdlib CLIs next to the existing `now.py`, and point the POSIX recipes at them. Do not rewrite the rest of the shell surface.

| Helper | Path | Status |
|--------|------|--------|
| `now.py` | `skills/ship/scripts/now.py` | already ships `[VERIFIED: skills/ship/scripts/now.py]` |
| `ensure_logdir.py` | `skills/ship/scripts/ensure_logdir.py` | **must add this PR** |
| `strip_frontmatter.py` | `skills/ship/scripts/strip_frontmatter.py` | **must add this PR** |

Issue #89 names exactly this trio (`now.py` done; the other two named under finding `g-posix`). `[CITED: https://github.com/Wittenberger-Industries/witloop/issues/89]`

## Why this is the minimum

Cursor's reviewed shell on this machine is **Windows PowerShell 5.1** (`5.1.26100.9168`, Desktop edition; `pwsh` not on PATH). `[VERIFIED: spike 2026-08-19 in %TEMP%, then deleted]`

The three side effects that **must** land as exact bytes on disk (ISO stamp, `*\n` gitignore, UTF-8 PR/issue body) currently go through POSIX one-liners that do not run here. `now.py` already covers stamps. The other two recipes still fail closed.

A full POSIX-to-Python rewrite (tail/grep/`echo $?`/redirect wrapper/worktree add) is rejected: constitution Simplicity, issue #89 "can ride along only if it unblocks Cursor-on-Windows", brief "tiny Python helpers".

## Inventory (skills/, references/, agents/)

Grep targets: `date -Iseconds`, `mkdir -p`, `printf`, `mktemp`, `awk`, `uname`, `chmod`, `&&`, heredoc, `/goal` paste.

### Fail on PowerShell 5.1 and have in-repo callers (must unblock)

| Snippet | Callers | Spike result `[VERIFIED: spike 2026-08-19]` | Helper |
|---------|---------|-----------------------------------------------|--------|
| `date -Iseconds` | `skills/dev/SKILL.md:49`; `skills/ship/SKILL.md:22-23`; `skills/research/references/wit-directory.md:128-129` | `Get-Date`: parameter `Iseconds` not found. `cmd date` is interactive "enter new date". | **existing** `now.py` (citation: lead with it, drop POSIX as the instruction) |
| `mkdir -p DIR && printf '*\n' > DIR/.gitignore` | `references/workflow.md:103`; `skills/ship/SKILL.md:336`; `skills/add-issues/SKILL.md:40` | `&&` parse error ("not a valid statement separator in this version"). `printf` not found. `mkdir -p` creates nested dirs but **errors if DIR already exists** (`ResourceExists`), so the advertised idempotent path fails. `>` writes **UTF-16 LE with BOM** (`FF FE`). | **new** `ensure_logdir.py` |
| `body=$(mktemp); awk '…' FILE > "$body"; rm -f "$body"` | `skills/ship/SKILL.md:300-304` (fenced `bash`); recovery one-liner `:314`; `skills/add-issues/SKILL.md:93-98` (same awk, inlined) | `mktemp` not found. `awk` not found. Even if the body were printed from Python, PowerShell `>` would UTF-16 the file `gh --body-file` consumes. | **new** `strip_frontmatter.py` (helper **writes** the UTF-8 file; do not redirect stdout with `>`) |

Design note already admits the awk pipeline is POSIX/Git Bash, not Copilot: `docs/design-notes/ship.md:79-82`. `[VERIFIED: docs/design-notes/ship.md]` Cursor-on-Windows is the same class of host.

### Fail on PowerShell but do **not** get a helper this PR

| Snippet | Callers | Spike | Why not a helper |
|---------|---------|-------|------------------|
| `echo $?` | `references/workflow.md:105` only | prints `False`/`True`, not the exit code. `$LASTEXITCODE` is the native analog (7 after `cmd /c exit 7`). | Cursor Shell already returns `exit_code` in the tool result. Reword the recipe to "the command's exit code", do not add `echo_status.py`. |
| `tail -n 30` | `references/workflow.md:105`; `skills/ship/SKILL.md:34`; `skills/build/SKILL.md:95` | `tail` not found | Log is already on disk. Cursor `Read` (or `Get-Content -Tail 30`) is enough. No `tail.py`. |
| `grep -n -B1 -A3 -iE 'fail\|error'` | `references/workflow.md:106` | not spiked; Git grep/`Select-String`/Cursor Grep exist | Cursor Grep tool. No `grep.py`. |
| `<cmd> > log.txt 2>&1` | `references/workflow.md:105` | PowerShell `>` is UTF-16 LE (`FF FE`). A `python -c "print('*')"` redirected in this shell also wrote `FF FE 2A 00`. | Pitfall for `cursor-tools.md` (sibling): never use PS `>` to persist bytes. Do **not** add `run_logged.py` this PR (issue named two new helpers, not a command runner). Follow-up if agents keep UTF-16-ing CI logs. |

### Present in the grep list, no runtime callers in skills/references/agents

| Snippet | Result |
|---------|--------|
| `uname`, `chmod` | **zero matches** in `skills/`, `references/`, `agents/`. `[VERIFIED: grep]` Fail on PS if used; nothing to change. |
| heredoc (`<<'EOF'`, `cat <<`) | **zero matches** in those trees. Plans under `docs/plans/` have commit heredocs (authoring, not agent runtime). `[VERIFIED: grep]` |
| `&&` besides the mkdir/printf recipes | only the awk `NR==1&&$0=="---"` *inside* the awk program (same two skills). Replacing awk removes both. |

### `/goal` paste

`references/keep-alive.md` "Print and paste as **one line**" is a **host product command**, not a POSIX snippet. It does not fail because of PowerShell; it fails because Cursor has no `/goal`. Sibling keep-alive/cursor-adapter owns the `none` (or `/loop`) template. **No helper.**

### Already portable (leave alone)

- Every bundled script is already invoked as `python ${CLAUDE_PLUGIN_ROOT}/…` with workflow.md "Script invocation" fallback `py -3` / `python3`. `validate.py` bans `python3 ${CLAUDE_PLUGIN_ROOT}` invocations (`PY3_INVOKE`). `[VERIFIED: scripts/validate.py:325,345]` New helpers inherit that.
- `git rm -f`, `git worktree add`, `gh …` are Git/GitHub CLIs, not POSIX. Worktree path is out of scope.
- `skills/ship/references/verification-gate.md:44` already documents POSIX `< /dev/null` vs PowerShell `-NonInteractive`. Leave it.

`agents/*.md`: no POSIX recipes. `[VERIFIED: grep]`

## Prior art: the `now.py` pattern

```1:11:skills/ship/scripts/now.py
#!/usr/bin/env python3
"""
now.py: print the OS clock as ISO-8601 with offset, e.g. 2026-07-10T18:23:45+02:00.
...
"""
from datetime import datetime

if __name__ == "__main__":
    print(datetime.now().astimezone().isoformat(timespec="seconds"))
```

Rules to copy `[VERIFIED: now.py + tests/test_timing_report.py::NowHelperTests]`:

- Stdlib only; shebang `python3` is decorative; **invoke** as `python <path>`.
- Tiny CLI, `if __name__ == "__main__"`, stdout is the contract.
- Tests drive it as a **subprocess** (`sys.executable`), not an import.
- Lives under `skills/ship/scripts/` even when other skills cite it (dev, wit-directory, rpa, build already cite ship scripts).
- No third-party deps. `[VERIFIED: constitution.md Language & tooling; repo-map.md]`

Do **not** import `_ledger.parse_frontmatter` for the PR-body strip: that helper returns a key dict, does not emit the body, and is not an entrypoint. `[VERIFIED: skills/ship/scripts/_ledger.py:222-233]` A second caller (add-issues) already exists for the awk, so a shared CLI is justified (constitution: no abstraction until a second caller).

## Helper contracts (prescribe)

### 1. `now.py` (exists; citation-only this PR)

- **Path:** `skills/ship/scripts/now.py`
- **Argv:** none. **Stdout:** one ISO-8601-with-offset line, seconds precision. **Exit:** 0.
- **Skill lines:** keep the script; stop leading with `date -Iseconds`.
  - `skills/dev/SKILL.md:49` (Created stamp)
  - `skills/ship/SKILL.md:22-23` (ship engine stamp)
  - `skills/research/references/wit-directory.md:128-129` (Log convention)
- **Test:** already `tests/test_timing_report.py::NowHelperTests.test_now_prints_iso_with_offset`. No new test required unless the script changes.

### 2. `ensure_logdir.py` (new)

- **Path:** `skills/ship/scripts/ensure_logdir.py`
- **Argv:** one positional directory path (relative or absolute). Used for `.wit/features/<slug>/.logs` **and** `.wit/issues` (same recipe; name follows issue #89).
- **Stdin:** unused.
- **Behavior:** `Path.mkdir(parents=True, exist_ok=True)`; write `<dir>/.gitignore` as UTF-8 **no BOM**, bytes exactly `*\n` (overwrite, matching `printf '*\n' >`). Do not add `!.gitignore`.
- **Stdout:** silent (or the dir path; prefer silent like a side-effect tool). **Stderr:** errors. **Exit:** 0 on success; 1 if argv missing or mkdir/write fails.
- **Skill / reference lines that change to call it** (replace the POSIX one-liner; do not leave it as the instruction):

```
python ${CLAUDE_PLUGIN_ROOT}/skills/ship/scripts/ensure_logdir.py .wit/features/<slug>/.logs
python ${CLAUDE_PLUGIN_ROOT}/skills/ship/scripts/ensure_logdir.py .wit/issues
```

  1. `references/workflow.md:103` (canonical output-house-rule; **this is the one other files should cite**)
  2. `skills/ship/SKILL.md:336` (ship:8 re-create after tidy pruned `.logs`)
  3. `skills/add-issues/SKILL.md:40` (preflight `.wit/issues`)

- **Unittest** (`tests/test_shell_helpers.py`, subprocess + `tempfile.TemporaryDirectory`, same `run()` style as `NowHelperTests`):
  - `test_creates_nested_dir_and_gitignore_star`: nested path, dir exists, file bytes `b"*\n"`
  - `test_idempotent_when_dir_already_exists`: pre-create dir; exit 0 (the PS `mkdir -p` failure mode)
  - `test_overwrites_existing_gitignore`: junk content becomes `*\n`
  - `test_gitignore_has_no_utf16_bom`: first bytes are not `FF FE` / `EF BB BF`
  - `test_missing_argv_exits_1`

### 3. `strip_frontmatter.py` (new)

- **Path:** `skills/ship/scripts/strip_frontmatter.py`
- **Argv:** `INPUT.md`. Optional `--out OUTPUT.md`. Default: write a `tempfile.NamedTemporaryFile(prefix="wit-body-", suffix=".md", delete=False)` itself.
- **Stdin:** unused (input is a path, matching awk-on-file).
- **Stdout:** absolute path of the UTF-8 **no BOM**, LF body file (one line). Never the body text. Skills/agents pass that path to `gh … --body-file`. **Do not** `>` the stdout; PS `>` is UTF-16. `[VERIFIED: spike]`
- **Semantics vs awk** (`sub(/\r$/,"")` then skip a leading `---` … `---` block). `[VERIFIED: skills/ship/SKILL.md:302]`
  - Opening delimiter must be line 1 `---` after CR strip.
  - Closing `---` is omitted from output; remainder is the body.
  - No opening `---`: emit the whole file (LF-normalized). Same as awk.
  - Opening `---` with **no closer**: **exit 1** (awk would swallow the file; constitution: do not silently lose the PR/issue body).
- **Exit:** 0 success; 1 missing/unreadable input, unclosed frontmatter, or cannot write output.
- **Skill lines:**
  1. Replace the fenced `bash` block `skills/ship/SKILL.md:300-304` and the recovery one-liner `:314` with:

```
python ${CLAUDE_PLUGIN_ROOT}/skills/ship/scripts/strip_frontmatter.py .wit/features/<slug>/PR.md
```

     stdout path -> `gh pr create --title "<…>" --body-file <path>` (`--draft` unchanged). Drop `rm -f`; the file is in the OS temp dir.
  2. Replace `skills/add-issues/SKILL.md:93-98` the same way, input `.wit/issues/<slug>.md`, then `gh issue create --body-file <path>`.
  3. Keep the prose that OKF frontmatter is dossier metadata, not GitHub text (`ship/SKILL.md:207-208`, add-issues:89-91).

- **Unittest** (same new `tests/test_shell_helpers.py`):
  - `test_strips_okf_and_prints_path`: fixture with `type: PR Description`; body file starts with the H1, contains no `type:`; stdout is an existing path
  - `test_crlf_delimiters_still_strip`: `---\r\n` open/close (the `core.autocrlf` bug class in design-notes/ship.md:81-82)
  - `test_no_frontmatter_emits_whole_file`
  - `test_unclosed_frontmatter_exits_1`
  - `test_output_is_utf8_lf_no_bom`
  - `test_missing_file_exits_1`

`validate.py` will require the new `${CLAUDE_PLUGIN_ROOT}/skills/ship/scripts/…` paths to exist once skills cite them. `[VERIFIED: scripts/validate.py:137-150]`

## Comparison

| Option | Complexity | Blast radius | Reversibility | Why rejected / kept |
|--------|------------|--------------|---------------|---------------------|
| **A. Two new CLIs + now.py citations** (winner) | two small files + one test module + 3+3 citation sites | ship/add-issues/workflow only | delete the scripts, restore one-liners | Matches #89 `g-posix`, `now.py` prior art, constitution stdlib ladder |
| B. Document PowerShell translations in `cursor-tools.md` only | zero Python | skills still contain copy-paste `bash` that agents will run | easy | Rejected: the recipes **fail** on the reviewed shell; UTF-16 `>` corrupts `.gitignore` and `gh --body-file` even after a translation. Skills would still lead with POSIX. |
| C. Full POSIX-to-Python rewrite (`tail.py`, `run_logged.py`, worktree helper, …) | large | every skill that mentions a shell | hard | Rejected: YAGNI; worktrees out of scope; Cursor Read/Grep/Shell already cover logs. |

Not a close call.

## Don't-Hand-Roll

| Problem | Don't build | Use instead | Why |
|---------|-------------|-------------|-----|
| ISO stamp | `date -Iseconds` / `Get-Date` format string | `now.py` | already the Log source of truth; PS `date` is `Get-Date` |
| self-gitignored dir | `mkdir -p && printf` / `New-Item` + `Set-Content` | `ensure_logdir.py` | must be idempotent + UTF-8 `*\n`; PS is neither |
| OKF-strip for `gh --body-file` | `mktemp`+`awk` / hand-edit | `strip_frontmatter.py` | awk/mktemp absent; helper must write the file |
| last 30 log lines | `tail.py` | Cursor Read / host tail | file already on disk |
| exit code | `echo_status.py` | Shell tool `exit_code` / `$LASTEXITCODE` | already in the tool result |

## State of the Art (this repo)

| Old way | Current way | When it changed |
|---------|-------------|-----------------|
| Assume Git Bash (`date -Iseconds`, mkdir/printf, mktemp+awk) | Stdlib CLIs invoked with `python` | `now.py` in #35 (`docs/plans/2026-07-10-issue-35-timing-and-cost.md`); rest named in #89 `g-posix` / `c-shell` |
| `python3 ${CLAUDE_PLUGIN_ROOT}/…` | `python` + workflow fallback | Windows Store stub ban in `validate.py` |

checked CPython 3.13.2 on PATH (`python --version`), docs/repo fetched 2026-08-19. No third-party package. `[VERIFIED: spike + repo-map.md]`

## Dependency Legitimacy

None added (stdlib `pathlib`, `tempfile`, `argparse`, `sys`). Verdict: n/a.

## Spike

One throwaway probe in `%TEMP%\wit-posix-spike-20260819` (deleted after). Results in the inventory table. Extra finding that drives `--out`/self-written files: PowerShell `>` is UTF-16 LE.

## Risks / unknowns (plan must consume)

1. **UTF-16 `>` on remaining log redirects** (`workflow.md:105`). Not a helper this PR; `cursor-tools.md` must warn, and pitfalls.md should say "PS `>` is not a byte-safe redirect". Follow-up `run_logged.py` only if Cursor agents keep writing UTF-16 CI logs into `.logs/`.
2. **`gh --body-file` + Windows temp paths.** `[ASSUMED]` GitHub CLI on Windows accepts `C:\Users\…\wit-body-….md`. Verify during build with a dry `gh pr create --body-file` against a fixture (or skip network: assert the file is UTF-8 and `gh` help accepts `--body-file`).
3. **Unclosed-frontmatter exit 1** is stricter than awk. PR.md/issue drafts always have closers in templates `[VERIFIED: ship/SKILL.md:210-217; add-issues/references/templates.md]`. If a truncated write ships, fail closed is correct; mention in pitfalls.md.
4. **Skill bodies must not keep the old `bash` fence as the runnable recipe** or agents will still copy it. Replace, do not dual-list POSIX first.
5. **`ensure_logdir.py` name vs `.wit/issues`.** Keep the issue name; argv is any dir. Do not split into two scripts.
6. Could not verify `gh` body-file encoding on this host this session (no network PR). Build verifies.

## Assumptions Log

| Claim | Why assumed | Load-bearing? |
|-------|-------------|---------------|
| `gh --body-file` accepts a Windows absolute temp path | not executed against GitHub this session | yes -> spec Open question / ADR Citations |
| Cursor Shell tool result is UTF-8 text (so `now.py` / printed body path are safe without `>`) | this session's Shell tool returned UTF-8 text for python stdout | no (observed here) |
| Agents will follow the Python citation if the bash fence is removed | they copy the remaining recipe | no (process) |

## Citations

- https://github.com/Wittenberger-Industries/witloop/issues/89 (findings `c-shell`, `g-posix`; named helpers)
- `skills/ship/scripts/now.py` + `tests/test_timing_report.py::NowHelperTests`
- `docs/design-notes/ship.md` ship:7 awk/CRLF rationale
- `references/workflow.md` output house rule + Script invocation
- Spike: Windows PowerShell 5.1.26100.9168, 2026-08-19
