"""Portability-file tuple in scripts/validate.py (assert the list in source).

Does not import validate.py (it runs checks on import) and does not temp-rename
files (unsafe in a parallel wave that shares this worktree).
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT = REPO_ROOT / "plugins" / "wit"
VALIDATE = ROOT / "scripts" / "validate.py"

# Existing hosts plus the Cursor adapter and the capability table.
REQUIRED = (
    "references/codex-tools.md",
    "references/copilot-tools.md",
    "references/grok-tools.md",
    "references/cursor-tools.md",
    "references/capabilities.md",
    "AGENTS.md",
)


def _portability_tuple_from_source(src: str) -> tuple[str, ...]:
    match = re.search(r"for tm in \(([^)]*)\):", src)
    if match is None:
        raise AssertionError("validate.py has no `for tm in (...):` portability tuple")
    return tuple(re.findall(r'"([^"]+)"', match.group(1)))


class ValidatePortabilityTest(unittest.TestCase):
    def test_portability_tuple_includes_cursor_and_capabilities(self):
        src = VALIDATE.read_text(encoding="utf-8")
        files = _portability_tuple_from_source(src)
        self.assertTrue(files, "portability tuple is empty")
        for path in REQUIRED:
            self.assertIn(path, files, "missing from validate.py portability tuple: " + path)


if __name__ == "__main__":
    unittest.main()
