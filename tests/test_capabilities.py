"""Contract tests for the host capability table and progress.md probe fields."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "references" / "capabilities.md"
WORKFLOW = ROOT / "references" / "workflow.md"
WIT_DIRECTORY = ROOT / "skills" / "research" / "references" / "wit-directory.md"

HOSTS = ("claude", "codex", "copilot", "grok", "cursor")
CAPABILITY_ROWS = (
    "plugin_root",
    "subagent",
    "keep_alive",
    "tokens",
    "ask",
    "shell",
    "skill_invoke",
)


def _split_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return []
    return [cell.strip().strip("`") for cell in stripped.strip("|").split("|")]


def parse_matrix(text: str) -> dict[str, dict[str, str]]:
    headers: list[str] | None = None
    matrix: dict[str, dict[str, str]] = {}
    for line in text.splitlines():
        cells = _split_row(line)
        if not cells:
            if headers is not None:
                break
            continue
        if all(set(cell.replace(":", "")) <= set("-") and cell for cell in cells):
            continue
        if headers is None:
            if cells[0].lower() != "capability":
                continue
            headers = [cell.lower() for cell in cells]
            continue
        cap = cells[0]
        matrix[cap] = {
            headers[i]: cells[i] for i in range(1, min(len(headers), len(cells)))
        }
    return matrix


class CapabilityTableTests(unittest.TestCase):
    def test_capabilities_file_is_okf_reference(self):
        text = CAPABILITIES.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        self.assertIn("type: Reference", text.split("---", 2)[1])

    def test_matrix_covers_hosts_and_capabilities(self):
        matrix = parse_matrix(CAPABILITIES.read_text(encoding="utf-8"))
        self.assertEqual(set(matrix), set(CAPABILITY_ROWS))
        for cap in CAPABILITY_ROWS:
            self.assertEqual(set(matrix[cap]), set(HOSTS), cap)

    def test_cursor_keep_alive_tokens_ask(self):
        matrix = parse_matrix(CAPABILITIES.read_text(encoding="utf-8"))
        self.assertEqual(matrix["keep_alive"]["cursor"], "none")
        self.assertEqual(matrix["tokens"]["cursor"], "unavailable")
        self.assertEqual(matrix["ask"]["cursor"], "AskQuestion")

    def test_keep_alive_cells_from_adapters(self):
        matrix = parse_matrix(CAPABILITIES.read_text(encoding="utf-8"))
        self.assertEqual(matrix["keep_alive"]["claude"], "predicate_goal")
        self.assertEqual(matrix["keep_alive"]["codex"], "predicate_goal")
        self.assertEqual(matrix["keep_alive"]["copilot"], "relaunch")
        self.assertEqual(matrix["keep_alive"]["grok"], "model_judged_goal")

    def test_claude_ask_and_unavailable_tokens(self):
        matrix = parse_matrix(CAPABILITIES.read_text(encoding="utf-8"))
        self.assertEqual(matrix["ask"]["claude"], "AskUserQuestion")
        self.assertEqual(matrix["tokens"]["codex"], "unavailable")
        self.assertEqual(matrix["tokens"]["copilot"], "unavailable")

    def test_workflow_points_at_table_without_embedding_it(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("**the capability table**", text)
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/references/capabilities.md", text)
        self.assertNotIn("| capability |", text)

    def test_progress_template_has_host_probe_fields(self):
        text = WIT_DIRECTORY.read_text(encoding="utf-8")
        start = text.index("## `progress.md` template")
        end = text.index("## `tokens.md` template")
        template = text[start:end]
        self.assertIn("**Host:**", template)
        self.assertIn("**Plugin root (resolved):**", template)
        self.assertIn("## Capabilities (resolved)", template)

    def test_rpa_progress_template_has_host_probe_fields(self):
        text = (ROOT / "skills" / "rpa" / "references" / "rpa-directory.md").read_text(
            encoding="utf-8"
        )
        start = text.index("## `progress.md` template")
        template = text[start:]
        self.assertIn("**Host:**", template)
        self.assertIn("**Plugin root (resolved):**", template)
        self.assertIn("## Capabilities (resolved)", template)

    def test_ledger_rule_names_finalize_tokens_as_ship_cli(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("finalize_tokens.py", workflow)
        self.assertNotIn("ship's `token_report.py`", workflow)
        text = WIT_DIRECTORY.read_text(encoding="utf-8")
        start = text.index("## `tokens.md` template")
        template = text[start:]
        self.assertIn("finalize_tokens.py --write", template)


if __name__ == "__main__":
    unittest.main()
