"""Keep-alive templates keyed by keep_alive cell, not product name."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "references" / "capabilities.md"
KEEP_ALIVE = ROOT / "references" / "keep-alive.md"

CELLS = ("predicate_goal", "model_judged_goal", "relaunch", "none")


def _split_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return []
    return [cell.strip().strip("`") for cell in stripped.strip("|").split("|")]


def keep_alive_cell_for(host: str) -> str:
    """Select the stamped keep_alive cell for a host from the capability table."""
    headers: list[str] | None = None
    for line in CAPABILITIES.read_text(encoding="utf-8").splitlines():
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
        if cells[0] != "keep_alive":
            continue
        idx = headers.index(host)
        return cells[idx]
    raise AssertionError("no keep_alive row for host %r" % host)


def print_blocks(text: str) -> dict[str, str]:
    """First fenced template under each ## <cell> heading (what skills print)."""
    headings = list(re.finditer(r"^## (" + "|".join(CELLS) + r")\s*$", text, re.M))
    blocks: dict[str, str] = {}
    for i, match in enumerate(headings):
        start = match.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        section = text[start:end]
        fence = re.search(r"```(?:[^\n]*)\n(.*?)```", section, re.S)
        if fence is None:
            continue
        blocks[match.group(1)] = fence.group(1)
    return blocks


def print_block_for_host(host: str) -> str:
    cell = keep_alive_cell_for(host)
    blocks = print_blocks(KEEP_ALIVE.read_text(encoding="utf-8"))
    if cell not in blocks:
        raise AssertionError("keep-alive.md has no print block for cell %r" % cell)
    return blocks[cell]


class KeepAliveCapabilityTests(unittest.TestCase):
    def test_file_keys_templates_by_cell_not_product(self):
        text = KEEP_ALIVE.read_text(encoding="utf-8")
        self.assertIn("stamped `keep_alive` cell", text)
        for cell in CELLS:
            self.assertRegex(text, r"(?m)^## %s\s*$" % cell, msg=cell)

    def test_cursor_selects_none_without_goal_print_or_autopilot(self):
        self.assertEqual(keep_alive_cell_for("cursor"), "none")
        block = print_block_for_host("cursor")
        for line in block.splitlines():
            self.assertFalse(
                line.lstrip().startswith("/goal"),
                "/goal must not be the print command on none: %r" % line,
            )
        self.assertNotIn("/goal", block)
        self.assertNotIn("autopilot", block.lower())
        self.assertIn("/loop", block)

    def test_hosts_share_cells(self):
        self.assertEqual(keep_alive_cell_for("claude"), "predicate_goal")
        self.assertEqual(keep_alive_cell_for("codex"), "predicate_goal")
        self.assertEqual(keep_alive_cell_for("copilot"), "relaunch")
        self.assertEqual(keep_alive_cell_for("grok"), "model_judged_goal")
        self.assertEqual(
            print_block_for_host("claude"),
            print_block_for_host("codex"),
        )

    def test_predicate_and_model_judged_print_goal(self):
        text = KEEP_ALIVE.read_text(encoding="utf-8")
        pred = print_block_for_host("claude")
        self.assertTrue(pred.lstrip().startswith("/goal"))
        judged = print_block_for_host("grok")
        self.assertTrue(judged.lstrip().startswith("/goal"))
        self.assertIn("update_goal", text)
        self.assertIn("Grok Build", text)

    def test_relaunch_keeps_autopilot_and_unattended_warning(self):
        text = KEEP_ALIVE.read_text(encoding="utf-8")
        block = print_block_for_host("copilot")
        self.assertIn("--autopilot", block)
        self.assertIn("--no-ask-user", block)
        self.assertIn("--allow-all", text)

    def test_fill_rules_stay(self):
        text = KEEP_ALIVE.read_text(encoding="utf-8")
        self.assertIn("fill `<slug>`", text)
        self.assertIn("<lint + test commands", text)
        self.assertIn("`n/a - not configured`", text)
        self.assertIn("`UNKNOWN - ask`", text)
        self.assertIn("don't arm anything", text)
        pred = print_block_for_host("claude")
        self.assertIn("<slug>", pred)
        self.assertIn("<lint + test commands from repo-map.md>", pred)


if __name__ == "__main__":
    unittest.main()
