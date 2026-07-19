---
type: Plan
title: "Learnings lifecycle (#78-#80, #83) Implementation Plan"
description: "Literal skill/agent edits for learnings coverage, causal format, counters, and polish; ships as wit v1.13.1."
timestamp: 2026-07-19
tags: [plan, learnings, ship, scan, checker]
---

# Learnings lifecycle (#78-#80, #83) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the learnings recall→enforcement gap and land causal format, evidence counters, and three polish one-liners as wit `v1.13.1` (issues #78, #79, #80, #83).

**Architecture:** Literal additive edits to skill/agent markdown only. research stamps applicable learnings; checker matrix enforces them; ship harvests causal triples with counters; scan refresh promotes/retires on evidence. No new scripts or agents.

**Tech Stack:** Markdown skills/agents; `scripts/validate.py` for parity/OKF checks; GitHub issues #78-#83.

**Design spec:** `docs/specs/2026-07-19-learnings-lifecycle-design.md`

## Global Constraints

- Version bump this PR: `1.13.0` → `1.13.1` on all three manifests together.
- No em-dashes in shipped text, commits, or PR bodies (roadmap standing rule).
- No new agents, gates, or Python parsers.
- Existing freeform learnings left as-is; new format is forward-looking.
- No live dry-run in this PR (full dry-run after #82 / `v1.13.3`).
- Agent charter edits: additive only; do not alter report caps, output markers, verification-gate contracts, or tool lists.
- Hotspot files (`ship/SKILL.md`, `wit-directory.md`, `wit-code-checker.md`): single branch.

## File map

| File | Responsibility |
|------|----------------|
| `skills/research/SKILL.md` | Stamp applicable learnings; pass them into plan-mode checker dispatch |
| `agents/wit-code-checker.md` | Matrix Learnings row; plan-mode pre-mortem |
| `skills/ship/SKILL.md` | Result-mode dispatch inputs; waiver pointer; §4 causal+counters; §5 Verification |
| `skills/scan/SKILL.md` | B1 WHEN-dedupe; B2 counter thresholds; B3 enforced-by |
| `skills/research/references/wit-directory.md` | Counters clause on learnings recall |
| `skills/plan/references/spec-template.md` | Test-level rule |
| Three plugin manifests | Version `1.13.1` |
| `docs/roadmap.md` | Record shipped / remaining queue |

---

### Task 1: research - applicable learnings stamp + plan-mode dispatch

**Files:**
- Modify: `skills/research/SKILL.md` (§1a after settled-check; §2 Pre-gate check dispatch inputs)
- Test: grep + `python scripts/validate.py`

**Interfaces:**
- Produces: Log line format `applicable learnings: … | none` for ship/checker consumers
- Consumes: existing `.wit/learnings.md` recall in §1a

- [ ] **Step 1: Confirm current §1a / §2 text**

Read `skills/research/SKILL.md` around the settled-check (`**a · Check what's already settled.**`) and the Pre-gate check block under `### 2 - Plan`.

- [ ] **Step 2: Extend §1a with the stamp**

After the learnings recall sentences in §1a (the lines that open detail files when hooks are relevant), append:

```markdown
After the settled-check, record the shortlist as a stamped Log line in `progress.md`:
`- <ts> **Update** applicable learnings: <slug: ~10-word hook; …> | none`.
This line is the single source later dispatches read - do not re-derive at ship.
```

Use a hyphen (not an em-dash) in "single source…".

- [ ] **Step 3: Extend §2 Pre-gate dispatch inputs**

In the Pre-gate check paragraph (dispatch of wit-code-checker in plan mode), add the applicable-learnings line to the input list. Current text lists `spec.md` + `tasks.md` + `pitfalls.md` + `constitution.md` + ADRs (+ Runtime State Inventory). Change to also include:

```markdown
+ the applicable learnings from `progress.md`'s `applicable learnings:` Log line
```

Exact insertion: after the existing artifact list, before "It builds a feature-backward coverage matrix".

- [ ] **Step 4: Verify phrases exist**

Run:

```powershell
Select-String -Path skills/research/SKILL.md -Pattern "applicable learnings:"
Select-String -Path skills/research/SKILL.md -Pattern "progress.md's ``applicable learnings:``|applicable learnings from"
python scripts/validate.py
```

Expected: both greps hit; validate exits 0.

- [ ] **Step 5: Commit**

```bash
git add skills/research/SKILL.md
git commit -m "$(cat <<'EOF'
feat(research): stamp applicable learnings for checker dispatch

EOF
)"
```

On Windows PowerShell without bash HEREDOC, use:

```powershell
git add skills/research/SKILL.md
git commit -m "feat(research): stamp applicable learnings for checker dispatch"
```

---

### Task 2: wit-code-checker - Learnings matrix row + pre-mortem (#78, #83)

**Files:**
- Modify: `agents/wit-code-checker.md` ("Build the coverage matrix"; plan-mode "How you verify" / Stay adversarial area)
- Test: grep + `python scripts/validate.py`

**Interfaces:**
- Consumes: `applicable learnings:` from dispatch / progress.md (Task 1)
- Produces: Learnings row in verification.md matrix; WARNING on ignored DO/AVOID

- [ ] **Step 1: Extend coverage matrix inputs**

In `agents/wit-code-checker.md`, item **2. Build the coverage matrix.**, change the enumerated inputs so they include applicable learnings. Replace the sentence that lists criteria/constitution/ADR/glossary/Runtime State Inventory/pitfalls with one that also names learnings, e.g.:

```markdown
2. **Build the coverage matrix.** Every `spec.md` acceptance criterion, applicable constitution rule, ADR
   decision, glossary term that must be honored, **Runtime State Inventory** row (rename/migration
   features), `pitfalls.md` entry, and **applicable learning named in the dispatch** (from
   `progress.md`'s `applicable learnings:` line; or an explicit "none applicable") must map to a
   covering task (plan) or a covering change (result). An unmapped item is a finding. **Learnings
   are the exception to the mapping rule:** "covered" for a learning means the plan or diff
   **honors** it - no covering task is required. A plan or diff that hits a learning's context and
   ignores its action is a finding with evidence (the hook + offending task # / `file:line`);
   severity **WARNING**; a learning that does not apply to this feature passes with a one-line note
   in the matrix. If the lesson was already promoted to a
   constitution rule, the existing constitution row makes it a **BLOCKER** - no new severity logic.
   (Prohibitive constitution rules, the Simplicity constraints, don't map to a task; they're verified
   in (4), not here.) Put the matrix in your report.
```

- [ ] **Step 2: Add plan-mode pre-mortem bullet (#83)**

Under **How you verify**, in the plan-mode adversarial section (after or as part of item **5. Stay adversarial.**), add:

```markdown
   **Pre-mortem (plan mode):** assume the build stalled mid-implementation; name the plan line that
   caused it - an untestable Verify, a hidden file overlap between parallel tasks, or a missing
   dependency edge. Findings take the normal severities.
```

- [ ] **Step 3: Modes input lists (if present)**

If Modes (`plan` / `result`) name explicit input lists, add "applicable learnings from the dispatch" there too. If Modes only name files to read, add a one-line note under Modes that the dispatch may carry `applicable learnings: … | none` and the matrix must include a Learnings row.

- [ ] **Step 4: Verify**

```powershell
Select-String -Path agents/wit-code-checker.md -Pattern "applicable learning"
Select-String -Path agents/wit-code-checker.md -Pattern "Pre-mortem"
python scripts/validate.py
```

Expected: hits; validate 0.

- [ ] **Step 5: Commit**

```powershell
git add agents/wit-code-checker.md
git commit -m "feat(checker): learnings coverage matrix row and plan pre-mortem"
```

---

### Task 3: ship §4 - causal format + counters + sharpen (#79, #80, #78)

**Files:**
- Modify: `skills/ship/SKILL.md` (section `## 4 · Compound`)
- Test: grep + validate

**Interfaces:**
- Consumes: checker violated-learning findings; existing index hooks
- Produces: causal detail bullets; `(seen: N, last: …)` / `reinforces` index convention

- [ ] **Step 1: Update the detail-file template + guidance**

In the substantial-learnings template under §4, keep the three headings. After the template fence (or inside Gotchas section as a comment line in the guidance prose above the template), add guidance:

```markdown
Phrase each behavioral bullet as a causal triple where the lesson is behavioral; keep prose for
narrative context:

`WHEN <context> → DO/AVOID <action> → BECAUSE <observed outcome>`

Example under Gotchas:

- WHEN parallel tasks share a file → AVOID scheduling them in the same wave → BECAUSE the worktree merge fights the second writer
```

Also note for index hooks: where natural, compress to `WHEN <context> → AVOID <action>` so the hook alone is actionable at recall.

- [ ] **Step 2: Add index counter / reinforce rule**

Immediately before or after the index template block, add:

```markdown
**Index rule (before adding a line):** check whether the new learning matches an existing hook
(same WHEN-context). Match → do not duplicate the detail file: increment or append
`(seen: N, last: NNNN-<slug>)` on the original index line, sharpen its wording if this cycle refined
it, and write the current feature's mandatory index line as a reference:
`- <slug> (<YYYY-MM-DD>): reinforces <earlier-slug>'s <hook>`.
New nuance goes into the original detail file. The reinforce line stands alone as the feature's
index line only when the reinforcement is its sole harvest; a feature that also produced a
genuinely new lesson gets its normal line (± detail file), with the `reinforces …` note appended
to that line. No match → current behavior (new line ± detail file).

If the checker flagged a learning as violated-again this run, sharpen the existing hook's wording
instead of adding a second lesson for the same WHEN.
```

- [ ] **Step 3: Verify**

```powershell
Select-String -Path skills/ship/SKILL.md -Pattern "WHEN <context>"
Select-String -Path skills/ship/SKILL.md -Pattern "seen: N"
Select-String -Path skills/ship/SKILL.md -Pattern "reinforces"
Select-String -Path skills/ship/SKILL.md -Pattern "violated-again|sharpen the existing"
python scripts/validate.py
```

- [ ] **Step 4: Commit**

```powershell
git add skills/ship/SKILL.md
git commit -m "feat(ship): causal learnings format, counters, and sharpen-not-duplicate"
```

---

### Task 4: ship §2 / §5 - checker dispatch inputs + waiver pointer (#78, #83)

**Files:**
- Modify: `skills/ship/SKILL.md` (§2 Review dispatch; §2 deferred findings; §5 PR.md Verification)
- Test: grep + validate

**Interfaces:**
- Consumes: Task 1 Log line; Task 2 WARNING findings
- Produces: dispatch input; roadmap-or-issue pointer on waived findings

- [ ] **Step 1: Pass applicable learnings into result-mode dispatch**

In §2 where wit-code-checker is dispatched in result mode, add that the dispatch includes the applicable learnings from `progress.md`'s `applicable learnings:` Log line (same source as research §2).

- [ ] **Step 2: Waiver pointer on deferred findings**

Where §2 says remaining findings go into `PR.md`'s Verification / "note anything deliberately deferred", require:

```markdown
A WARNING carried into `PR.md` as waived or deferred requires a pointer - a `roadmap.md` line or a
GitHub issue (via `/wit:add-issues`) - not prose alone. Record the pointer in Verification.
```

- [ ] **Step 3: Update §5 PR.md Verification stub**

Change the Verification placeholder under the PR.md template to require the pointer, e.g.:

```markdown
### Verification
<checker result-mode verdict: every acceptance criterion + locked decision delivered and wired; any
waived/deferred findings with severity AND a pointer (roadmap.md line or issue #). Distilled from
verification.md; the dossier tidy (ship:6) then prunes it.>
```

- [ ] **Step 4: Verify**

```powershell
Select-String -Path skills/ship/SKILL.md -Pattern "applicable learnings"
Select-String -Path skills/ship/SKILL.md -Pattern "roadmap.md line or"
python scripts/validate.py
```

- [ ] **Step 5: Commit**

```powershell
git add skills/ship/SKILL.md
git commit -m "feat(ship): pass learnings to result checker; require waiver pointers"
```

---

### Task 5: scan --refresh B1/B2/B3 (#79, #80)

**Files:**
- Modify: `skills/scan/SKILL.md` (section `### B · Memory hygiene`)
- Test: grep + validate

**Interfaces:**
- Consumes: ship §4 counter / WHEN conventions (Tasks 3)
- Produces: refresh behavior for dedupe / promote / retire

- [ ] **Step 1: Rewrite B1 dedupe**

Replace step 1 **Dedupe** with:

```markdown
1. **Dedupe:** index lines (or detail files) describing the same gotcha → merge into one, keep the
   clearest hook, fix the links. Match on **WHEN-context** (the situation the lesson fires in), not
   on surface wording alone.
```

- [ ] **Step 2: Rewrite B2 promote**

Replace step 2 **Promote** so counter thresholds are the evidence:

```markdown
2. **Promote:** use the index counter as promotion evidence - promote at `seen ≥ 3` (`≥ 2` for
   rule-shaped lessons). Fold the rule into its source of truth (`constitution.md`, user-owned:
   confirm with the user; `repo-map.md`; or `glossary.md`), then shrink the index line to a
   tombstone: `- <hook> → promoted to constitution (<date>)`. Delete the detail file once promoted.
```

- [ ] **Step 3: Extend B3 prune**

Keep the existing "code/tool gone" trigger. Add the second trigger:

```markdown
3. **Prune / retire:** (a) the code/tool the learning warns about is gone (verify against the repo,
   not memory) → delete the detail file and its index line; or (b) the lesson is now structurally
   enforced - verify the named test, CI check, or constitution rule actually exists in the repo,
   then tombstone the line as `- <hook> → enforced by <check> (<date>)` and delete the detail file.
```

Renumber **Target** to stay step 4 if needed.

- [ ] **Step 4: Verify**

```powershell
Select-String -Path skills/scan/SKILL.md -Pattern "WHEN-context"
Select-String -Path skills/scan/SKILL.md -Pattern "seen ≥ 3|seen >= 3"
Select-String -Path skills/scan/SKILL.md -Pattern "enforced by"
python scripts/validate.py
```

Prefer `seen ≥ 3` only if the file already uses unicode ≥ elsewhere; otherwise use `seen >= 3` for ASCII safety. Match existing scan style.

- [ ] **Step 5: Commit**

```powershell
git add skills/scan/SKILL.md
git commit -m "feat(scan): WHEN-dedupe, counter promotion, enforced-by retirement"
```

---

### Task 6: wit-directory + spec-template polish (#80, #83)

**Files:**
- Modify: `skills/research/references/wit-directory.md` (Learnings recall bullet)
- Modify: `skills/plan/references/spec-template.md` (Test plan)
- Test: grep + validate

**Interfaces:**
- Documents Task 3 counter convention; adds test-level rule for plans

- [ ] **Step 1: wit-directory counters clause**

In the **Learnings recall is via the index.** bullet, append one clause, e.g.:

```markdown
Index lines may carry `(seen: N, last: NNNN-<slug>)` when a later feature re-confirms a lesson;
`reinforces <slug>'s <hook>` lines satisfy the close-out checklist without duplicating a detail file.
```

- [ ] **Step 2: spec-template test-level rule**

Under `## Test plan`, add as the first bullet (or a lead sentence before the Unit/Integration list):

```markdown
- **Level rule:** choose the cheapest level that can assert each criterion (unit > integration > e2e > manual); never assert the same thing at two levels.
```

- [ ] **Step 3: Verify**

```powershell
Select-String -Path skills/research/references/wit-directory.md -Pattern "seen: N"
Select-String -Path skills/plan/references/spec-template.md -Pattern "Level rule"
python scripts/validate.py
```

- [ ] **Step 4: Commit**

```powershell
git add skills/research/references/wit-directory.md skills/plan/references/spec-template.md
git commit -m "docs: learnings counter recall note and test-level rule"
```

---

### Task 7: version bump, roadmap, validate, PR

**Files:**
- Modify: `.claude-plugin/plugin.json` (`version`)
- Modify: `.claude-plugin/marketplace.json` (wit plugin `version`)
- Modify: `.codex-plugin/plugin.json` (`version`)
- Modify: `docs/roadmap.md` (queue: note #78-#80/#83 shipping / remaining #81 #82)
- Create: PR via `gh`

**Interfaces:**
- Produces: released `1.13.1` string parity (validate enforces)

- [ ] **Step 1: Bump all three manifests to `1.13.1`**

Set `"version": "1.13.1"` in:
- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`
- `.claude-plugin/marketplace.json` (the `plugins[]` entry with `"name": "wit"`)

Do not change marketplace catalog version `0.2.0` unless the repo's Maintaining rule says otherwise.

- [ ] **Step 2: Update roadmap**

In `docs/roadmap.md`, record that #78 #79 #80 #83 ship as `v1.13.1`; leave #81 / #82 queued for `v1.13.2` / `v1.13.3`. Follow existing table style. No em-dashes. Name the deferred verification explicitly (e.g. `#79 dry-run AC deferred to the post-#82 full dry-run`) so the deferral carries a pointer (the #83 discipline applied to ourselves).

- [ ] **Step 3: Full validate**

```powershell
python scripts/validate.py
```

Expected: exit 0; includes manifest version parity at `1.13.1`.

- [ ] **Step 4: Commit version + roadmap + design/plan docs**

```powershell
git add .claude-plugin/plugin.json .claude-plugin/marketplace.json .codex-plugin/plugin.json docs/roadmap.md docs/specs/2026-07-19-learnings-lifecycle-design.md docs/plans/2026-07-19-learnings-lifecycle.md docs/superpowers/plans/2026-07-19-learnings-lifecycle.md
git commit -m "chore: bump wit to 1.13.1 (learnings lifecycle)"
```

(If plan/spec were already committed earlier, only stage what changed.)

- [ ] **Step 5: Push and open PR**

Branch name suggestion: `feat/learnings-lifecycle-78-83`.

Write the body to a temp file outside the repo and use `--body-file` (ship's own pattern); a
here-string nested inside `$( )` is fragile across PS 5.1 / PS 7.

```powershell
git push -u origin HEAD
$body = Join-Path $env:TEMP "pr-body-learnings-lifecycle.md"
@'
## Summary
- Close learnings recall→enforcement gap: research stamps applicable learnings; checker matrix verifies them (#78)
- Causal WHEN→DO/AVOID→BECAUSE lesson format + scan WHEN-dedupe (#79)
- Evidence counters, reinforce-not-duplicate, promote/retire on evidence (#80)
- Polish: test-level rule, checker pre-mortem, waiver pointer (#83)
- Version bump 1.13.0 → 1.13.1

Closes #78
Closes #79
Closes #80
Closes #83

## Test plan
- [ ] `python scripts/validate.py` green
- [ ] Grep confirms new phrases in research / checker / ship / scan / wit-directory / spec-template
- [ ] No live dry-run in this PR (deferred until after #82; #79's dry-run AC tracked in docs/roadmap.md)
'@ | Set-Content -Encoding utf8 $body
gh pr create --title "feat: learnings lifecycle coverage, causal format, counters (v1.13.1)" --body-file $body
Remove-Item $body
```

---

## Self-review (plan author)

1. **Spec coverage:** #78 stamp/dispatch/matrix/sharpen → Tasks 1-4; #79 causal+B1 → Tasks 3,5; #80 counters/B2/B3/wit-directory → Tasks 3,5,6; #83 three polish → Tasks 2,4,6; version → Task 7.
2. **Placeholders:** none intentional beyond runtime `<ts>` / `<slug>` in the skill text itself.
3. **Consistency:** Log line key is always `applicable learnings:`; counter form always `(seen: N, last: NNNN-<slug>)`; waiver pointer always roadmap-or-issue.
4. **Review pass (2026-07-19, applied):** learnings carved out of the matrix mapping rule (covered = honored, no task required; non-applicable passes with a note); reinforce line scoped to sole-harvest features; PR opened via temp `--body-file` instead of a nested here-string; roadmap names the deferred #79 dry-run AC.
