"""Contract tests for ship safety-fact rows (checker, then ship, then RPA).

Independently loads agents/wit-code-checker.md as text.
Does not import other repo modules (several run checks on import).
"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "agents" / "wit-code-checker.md"
CHECKER_NOTES = ROOT / "docs" / "design-notes" / "wit-code-checker.md"
SHIP = ROOT / "skills" / "ship" / "SKILL.md"
GATE = ROOT / "skills" / "ship" / "references" / "verification-gate.md"
SHIP_NOTES = ROOT / "docs" / "design-notes" / "ship.md"
EM_DASH = "\u2014"

RUNTIME_PATHS = (
    "skills/",
    "agents/",
    "scripts/",
    "tests/",
    "references/",
    ".claude-plugin/",
    ".codex-plugin/",
    "AGENTS.md",
)

SAFETY_FACT_ROWS = (
    {
        "item": "Safety fact heading",
        "plan": "skip",
        "result": "`### Safety fact` in `PR.md` when that file exists",
        "severity": "BLOCKER",
    },
    {
        "item": "Safety fact matrix row",
        "plan": "skip",
        "result": "write the row into verification.md",
        "severity": "BLOCKER",
    },
    {
        "item": "Proof token",
        "plan": "skip",
        "result": "this-session command, `unproven`, or `n/a`",
        "severity": "BLOCKER if writeup-only",
    },
    {
        "item": "Honest unproven",
        "plan": "skip",
        "result": "Proof is `unproven`",
        "severity": "INFO",
    },
    {
        "item": "Valid docs-only n/a",
        "plan": "skip",
        "result": "Proof `n/a` plus reason; no runtime-path touch",
        "severity": "INFO",
    },
    {
        "item": "n/a on runtime-behavior diff",
        "plan": "skip",
        "result": "`n/a` while diff touches a runtime path",
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


def item_plan_result_tables(text: str) -> list[dict[str, dict[str, str]]]:
    found: list[dict[str, dict[str, str]]] = []
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
        found.append(rows)
    return found


def safety_fact_matrix(text: str) -> dict[str, dict[str, str]]:
    tables = item_plan_result_tables(text)
    if len(tables) < 2:
        raise AssertionError(
            "need a second Item/Plan/Result/Severity table after the bug-fix matrix"
        )
    return tables[1]


class CheckerSafetyFactTests(unittest.TestCase):
    def test_does_not_import_validate(self):
        src = Path(__file__).read_text(encoding="utf-8")
        self.assertNotRegex(src, r"(?m)^(?:import validate|from validate import)")

    def test_safety_fact_table_is_after_bug_fix_table(self):
        tables = item_plan_result_tables(load(CHECKER))
        self.assertGreaterEqual(len(tables), 2, "safety-fact table must follow the bug-fix table")
        self.assertEqual(len(tables[0]), 5, tables[0].keys())
        self.assertNotIn("Safety fact heading", tables[0])
        self.assertIn("Safety fact heading", tables[1])

    def test_always_on_result_mode_rows_match_lock(self):
        rows = safety_fact_matrix(load(CHECKER))
        self.assertEqual(len(rows), len(SAFETY_FACT_ROWS), rows.keys())
        for expected in SAFETY_FACT_ROWS:
            self.assertIn(expected["item"], rows, rows.keys())
            got = rows[expected["item"]]
            self.assertEqual(got["plan"], expected["plan"], expected["item"])
            self.assertEqual(got["result"], expected["result"], expected["item"])
            self.assertEqual(got["severity"], expected["severity"], expected["item"])

    def test_missing_heading_when_pr_exists_is_blocker(self):
        heading = safety_fact_matrix(load(CHECKER))["Safety fact heading"]
        self.assertIn("PR.md", heading["result"])
        self.assertIn("exists", heading["result"])
        self.assertIn("BLOCKER", heading["severity"])

    def test_omitted_matrix_row_is_blocker(self):
        row = safety_fact_matrix(load(CHECKER))["Safety fact matrix row"]
        self.assertIn("verification.md", row["result"])
        self.assertIn("BLOCKER", row["severity"])

    def test_writeup_only_proof_is_blocker(self):
        row = safety_fact_matrix(load(CHECKER))["Proof token"]
        self.assertIn("unproven", row["result"])
        self.assertIn("n/a", row["result"])
        self.assertIn("writeup-only", row["severity"])
        self.assertIn("BLOCKER", row["severity"])

    def test_honest_unproven_is_info(self):
        row = safety_fact_matrix(load(CHECKER))["Honest unproven"]
        self.assertEqual(row["severity"], "INFO")
        self.assertIn("unproven", row["result"])

    def test_valid_docs_only_na_is_info(self):
        row = safety_fact_matrix(load(CHECKER))["Valid docs-only n/a"]
        self.assertEqual(row["severity"], "INFO")
        self.assertIn("n/a", row["result"])

    def test_na_on_runtime_behavior_diff_is_blocker(self):
        row = safety_fact_matrix(load(CHECKER))["n/a on runtime-behavior diff"]
        self.assertIn("BLOCKER", row["severity"])
        self.assertIn("runtime", row["result"])

    def test_plan_mode_skips_safety_fact_rows(self):
        text = load(CHECKER)
        rows = safety_fact_matrix(text)
        for name, row in rows.items():
            self.assertEqual(row["plan"], "skip", name)
        self.assertRegex(text, r"(?i)skip.{0,40}plan")

    def test_glossary_carve_out_for_safety_fact_and_unproven(self):
        text = load(CHECKER)
        self.assertIn("Safety fact", text)
        self.assertIn("Unproven", text)
        self.assertRegex(text, r"(?i)carve-out")

    def test_absent_pr_md_still_writes_row_not_a_miss(self):
        text = load(CHECKER)
        self.assertRegex(text, r"(?i)PR\.md.{0,80}absent|absent.{0,80}PR\.md")
        self.assertRegex(text, r"(?i)not a miss")
        row = safety_fact_matrix(text)["Safety fact matrix row"]
        self.assertIn("verification.md", row["result"])

    def test_runtime_paths_pinned(self):
        text = load(CHECKER)
        for path in RUNTIME_PATHS:
            self.assertIn(path, text, path)

    def test_no_em_dash_in_edited_files(self):
        for path in (CHECKER, CHECKER_NOTES, Path(__file__)):
            self.assertNotIn(EM_DASH, load(path), path.name)


class ShipSafetyFactTests(unittest.TestCase):
    def test_safety_fact_heading_between_testing_and_verification(self):
        text = load(SHIP)
        testing = text.index("### Testing")
        safety = text.index("### Safety fact")
        verification = text.index("### Verification")
        self.assertLess(testing, safety)
        self.assertLess(safety, verification)

    def test_template_has_claim_proof_and_optional_not_run(self):
        block = load(SHIP)[
            load(SHIP).index("### Safety fact") : load(SHIP).index("### Verification")
        ]
        self.assertIn("Claim", block)
        self.assertIn("Proof", block)
        self.assertIn("Not-run", block)
        self.assertIn("unproven", block)
        self.assertRegex(block, r"`n/a`")

    def test_ship5_copies_checker_matrix_row(self):
        text = load(SHIP)
        section = text[text.index("## 5 · PR description") : text.index("## 6 ·")]
        self.assertRegex(section, r"(?i)cop(y|ies).{0,80}matrix row")
        self.assertIn("### Safety fact", section)

    def test_ship8_checkbox_for_heading_and_legal_proof(self):
        text = load(SHIP)
        section = text[text.index("## 8 ·") :]
        self.assertIn("### Safety fact", section)
        self.assertRegex(section, r"(?i)legal Proof|this-session command")

    def test_ship1_points_at_gate_honesty(self):
        text = load(SHIP)
        section = text[text.index("## 1 ·") : text.index("## 2 ·")]
        self.assertRegex(section, r"(?i)honesty")

    def test_gate_honesty_unproven_does_not_skip_and_five_run_steps(self):
        text = load(GATE)
        self.assertRegex(text, r"(?i)honesty")
        self.assertRegex(text, r"(?i)unproven does not skip")
        self.assertIn("n/a - not configured", text)
        run = text[text.index("## Run, in this order") : text.index("## Run commands")]
        self.assertIn("1. **Format", run)
        self.assertIn("5. **CI-equivalent", run)
        self.assertNotIn("6. **", run)

    def test_testing_na_not_configured_is_not_safety_fact_na(self):
        ship = load(SHIP)
        testing = ship[ship.index("### Testing") : ship.index("### Safety fact")]
        safety = ship[ship.index("### Safety fact") : ship.index("### Verification")]
        self.assertIn("n/a - not configured", testing)
        self.assertRegex(safety, r"`n/a`")
        self.assertNotIn("n/a - not configured", safety)

    def test_fail_then_pass_stays_inside_testing(self):
        ship = load(SHIP)
        testing = ship[ship.index("### Testing") : ship.index("### Safety fact")]
        self.assertRegex(testing, r"fail then pass|fail-then-pass")

    def test_no_em_dash_in_ship_files(self):
        for path in (SHIP, GATE, SHIP_NOTES, Path(__file__)):
            self.assertNotIn(EM_DASH, load(path), path.name)


if __name__ == "__main__":
    unittest.main()
