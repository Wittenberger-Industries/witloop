"""Contract tests for bug-fix checker matrix rows and ship PR evidence.

Independently loads agents/wit-code-checker.md and skills/ship/SKILL.md as text.
Does not import other repo modules (several run checks on import).
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT = REPO_ROOT / "plugins" / "wit"
CHECKER = ROOT / "agents" / "wit-code-checker.md"
SHIP = ROOT / "skills" / "ship" / "SKILL.md"

TOOLS_LINE = 'tools: ["Read", "Grep", "Glob", "Bash", "Write"]'
PASSED = "## CHECK PASSED"
ISSUES = "## ISSUES FOUND"

BUG_FIX_ROWS = (
    {
        "item": "Repro contract / named surface",
        "plan": "task Verify names it",
        "result": "diff + logs use it",
        "severity": "BLOCKER",
    },
    {
        "item": "Root cause recorded",
        "plan": "spec / repro note",
        "result": "PR names it",
        "severity": "BLOCKER",
    },
    {
        "item": "Same-surface fail-then-pass",
        "plan": "tasks include the verify",
        "result": "both stamps + matching surface; after-run exists",
        "severity": "BLOCKER",
    },
    {
        "item": "Smallest justified fix",
        "plan": "planned change is the evidence-backed minimum",
        "result": "PR names it",
        "severity": "BLOCKER",
    },
    {
        "item": "Regression test or impractical rationale",
        "plan": "a task or an explicit out",
        "result": "test present or rationale still in spec/PR",
        "severity": "BLOCKER",
    },
)


def load(path: Path) -> str:
    if not path.is_file():
        raise AssertionError("%s is missing" % path.relative_to(ROOT))
    return path.read_text(encoding="utf-8")


def frontmatter(text: str) -> str:
    if not text.startswith("---"):
        raise AssertionError("no frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise AssertionError("unterminated frontmatter")
    return parts[1]


def _split_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return []
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def markdown_tables(text: str) -> list[list[list[str]]]:
    tables: list[list[list[str]]] = []
    current: list[list[str]] = []
    for line in text.splitlines():
        cells = _split_row(line)
        if not cells:
            if current:
                tables.append(current)
                current = []
            continue
        if all(set(cell.replace(":", "")) <= set("-") and cell for cell in cells):
            continue
        current.append(cells)
    if current:
        tables.append(current)
    return tables


def bug_fix_matrix(text: str) -> dict[str, dict[str, str]]:
    for table in markdown_tables(text):
        header = [cell.lower() for cell in table[0]]
        if not header:
            continue
        if "item" not in header[0]:
            continue
        if not any("plan" in cell for cell in header):
            continue
        if not any("result" in cell for cell in header):
            continue
        if not any("severity" in cell for cell in header):
            continue
        plan_i = next(i for i, cell in enumerate(header) if "plan" in cell)
        result_i = next(i for i, cell in enumerate(header) if "result" in cell)
        sev_i = next(i for i, cell in enumerate(header) if "severity" in cell)
        rows: dict[str, dict[str, str]] = {}
        for row in table[1:]:
            if len(row) <= max(plan_i, result_i, sev_i):
                continue
            rows[row[0]] = {
                "plan": row[plan_i],
                "result": row[result_i],
                "severity": row[sev_i],
            }
        return rows
    raise AssertionError("no bug-fix coverage matrix table in checker charter")


class CheckerPreservedContractTests(unittest.TestCase):
    def test_tools_list_unchanged(self):
        fm = frontmatter(load(CHECKER))
        self.assertIn(TOOLS_LINE, fm)
        listed = re.search(r"tools:\s*\[([^\]]*)\]", fm)
        self.assertIsNotNone(listed)
        tools = [t.strip().strip('"').strip("'") for t in listed.group(1).split(",")]
        self.assertEqual(tools, ["Read", "Grep", "Glob", "Bash", "Write"])

    def test_last_line_markers_required(self):
        text = load(CHECKER)
        self.assertIn("`%s`" % PASSED, text)
        self.assertIn("`%s`" % ISSUES, text)
        self.assertIn("last line", text)
        self.assertIn("type: Verification", text)
        self.assertIn("type: Agent", frontmatter(text))

    def test_plan_and_result_modes_still_present(self):
        text = load(CHECKER)
        self.assertIn("## Modes", text)
        self.assertIn("**`plan`**", text)
        self.assertIn("**`result`**", text)
        self.assertIn("before the design gate", text)
        self.assertIn("at ship", text.lower())

    def test_moa_rpa_and_overbuild_warning_preserved(self):
        text = load(CHECKER)
        self.assertIn("## MoA dispatches", text)
        self.assertIn("`MoA role: proposer", text)
        self.assertIn("`MoA role: aggregator`", text)
        self.assertIn("spec.md` → **`sdd.md`**", text)
        self.assertIn("**Hunt over-build**", text)
        self.assertIn("**WARNING**, not BLOCKER.", text)
        self.assertIn("Max 2 rounds.", text)


class CheckerBugFixMatrixTests(unittest.TestCase):
    def test_bug_fix_rows_are_work_type_gated(self):
        text = load(CHECKER)
        self.assertRegex(text, r"Work type is [`']?bug-fix")
        self.assertIn("bug-fix", text)
        lower = text.lower()
        self.assertIn("missing", lower)
        self.assertIn("feature", lower)

    def test_additive_rows_blocker_for_omissions(self):
        rows = bug_fix_matrix(load(CHECKER))
        self.assertEqual(len(rows), len(BUG_FIX_ROWS), rows.keys())
        for expected in BUG_FIX_ROWS:
            self.assertIn(expected["item"], rows, rows.keys())
            got = rows[expected["item"]]
            self.assertEqual(got["plan"], expected["plan"], expected["item"])
            self.assertEqual(got["result"], expected["result"], expected["item"])
            self.assertIn("BLOCKER", got["severity"], expected["item"])

    def test_extra_might_help_stays_warning(self):
        text = load(CHECKER)
        self.assertIn("might help", text)
        self.assertIn("WARNING", text)
        hunt = text[text.index("**Hunt over-build**") : text.index("**Stay adversarial.**")]
        self.assertIn("WARNING", hunt)
        self.assertNotIn("BLOCKER", hunt.split("WARNING", 1)[0])


class ShipBugFixEvidenceTests(unittest.TestCase):
    def test_summary_names_root_cause_and_smallest_fix(self):
        text = load(SHIP)
        self.assertIn("## 5 · PR description", text)
        self.assertRegex(text, r"Work type is [`']?bug-fix")
        self.assertIn("root cause", text)
        self.assertIn("smallest fix", text)
        summary = text[text.index("### Summary") : text.index("### Acceptance criteria")]
        self.assertIn("root cause", summary)
        self.assertIn("smallest fix", summary)

    def test_testing_pastes_same_surface_fail_then_pass(self):
        text = load(SHIP)
        testing = text[text.index("### Testing") : text.index("### Verification")]
        self.assertRegex(testing, r"fail then pass|fail-then-pass")
        self.assertRegex(testing, r"same named surface|same surface")

    def test_verification_carries_result_mode_matrix(self):
        text = load(SHIP)
        verification = text[text.index("### Verification") : text.index("### Risk & rollout")]
        self.assertIn("result-mode matrix", verification)


class ShipRulesInventoryTests(unittest.TestCase):
    def test_conditional_rules_inventory_heading(self):
        text = load(SHIP)
        self.assertRegex(text, r"(?m)^## Rules inventory\s*$")
        self.assertRegex(text, r"(?i)conditional|only (include|when)|omit")
        self.assertIn("Do not require it for every PR", text)
        self.assertIn("rule text", text)
        self.assertIn("before/after", text)
        self.assertIn("loaded alone", text)
        self.assertIn("skills", text)
        self.assertIn("agents", text)
        self.assertIn("references", text)


if __name__ == "__main__":
    unittest.main()
