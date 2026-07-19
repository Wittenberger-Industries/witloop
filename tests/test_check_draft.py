"""Tests for skills/add-issues/scripts/check_draft.py."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "add-issues" / "scripts" / "check_draft.py"

BUG_OK = """---
type: Issue Draft
title: "ship: example failure"
description: "demo bug"
timestamp: 2026-07-19
issue_type: Bug
labels: []
assignees: []
milestone:
parent:
blocked_by: []
---

# ship: example failure

## Summary
Something breaks.

## Steps to reproduce
1. Run the command

## Actual results
It fails

## Expected results
It works

## Root cause
Unknown - needs investigation

## Proposed fix
TBD

## Acceptance criteria
- [ ] New test `tests/test_ship.py::test_example` fails on the bug and passes after the fix
- [ ] Behavior restored
"""

BUG_NO_TEST = BUG_OK.replace(
    "- [ ] New test `tests/test_ship.py::test_example` fails on the bug and passes after the fix\n",
    "- [ ] Manual repro checklist only\n",
)

FEATURE_OK = """---
type: Issue Draft
title: "scan: add capability"
description: "demo feature"
timestamp: 2026-07-19
issue_type: Feature
labels: []
assignees: []
milestone:
parent:
blocked_by: []
---

# scan: add capability

## Summary
Add a thing.

## Motivation
Users need it.

## Proposed solution
Ship the thing.

## Acceptance criteria
- [ ] Thing is available
- [ ] Tests cover the new behavior in `scan`
"""


class CheckDraftCliTests(unittest.TestCase):
    def _write(self, text: str) -> Path:
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        path = Path(td.name) / "draft.md"
        path.write_text(text, encoding="utf-8")
        return path

    def _run(self, path: Path, *extra: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(path), *extra],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_bug_ok(self):
        r = self._run(self._write(BUG_OK))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("draft ok", r.stdout)

    def test_bug_missing_new_test(self):
        r = self._run(self._write(BUG_NO_TEST))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("DRAFT CHECK FAILED", r.stdout)
        self.assertIn("new automated test", r.stdout)

    def test_bug_allow_no_test(self):
        r = self._run(self._write(BUG_NO_TEST), "--allow-no-test")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_feature_ok(self):
        r = self._run(self._write(FEATURE_OK))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_missing_section(self):
        bad = BUG_OK.replace("## Proposed fix\nTBD\n\n", "")
        r = self._run(self._write(bad))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Proposed fix", r.stdout)

    def test_missing_frontmatter(self):
        r = self._run(self._write("# no frontmatter\n\n## Summary\n"))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("missing OKF frontmatter", r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
