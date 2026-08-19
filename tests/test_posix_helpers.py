"""POSIX helper CLIs: ensure_logdir.py and strip_frontmatter.py (subprocess, stdlib)."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "ship" / "scripts"
ENSURE = SCRIPTS / "ensure_logdir.py"
STRIP = SCRIPTS / "strip_frontmatter.py"


def run(*args):
    return subprocess.run(
        [sys.executable, *map(str, args)], capture_output=True, text=True
    )


OKF = """---
type: PR Description
title: example
---
# Heading

The body.
"""


class EnsureLogdirTests(unittest.TestCase):
    def test_creates_nested_dir_and_gitignore_star(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "feat" / ".logs"
            r = run(ENSURE, target)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(r.stdout, "")
            self.assertTrue(target.is_dir())
            self.assertEqual((target / ".gitignore").read_bytes(), b"*\n")

    def test_idempotent_when_dir_already_exists(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "already"
            target.mkdir()
            r = run(ENSURE, target)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual((target / ".gitignore").read_bytes(), b"*\n")

    def test_overwrites_existing_gitignore(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "logs"
            target.mkdir()
            junk = target / ".gitignore"
            junk.write_bytes(b"not-star\n")
            r = run(ENSURE, target)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(junk.read_bytes(), b"*\n")

    def test_gitignore_has_no_utf16_bom(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "logs"
            r = run(ENSURE, target)
            self.assertEqual(r.returncode, 0, r.stderr)
            head = (target / ".gitignore").read_bytes()[:3]
            self.assertFalse(head.startswith(b"\xff\xfe"))
            self.assertFalse(head.startswith(b"\xef\xbb\xbf"))
            self.assertEqual((target / ".gitignore").read_bytes(), b"*\n")

    def test_missing_argv_exits_1(self):
        r = run(ENSURE)
        self.assertEqual(r.returncode, 1)


class StripFrontmatterTests(unittest.TestCase):
    def test_strips_okf_and_writes_out_not_stdout(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "in.md"
            out = Path(d) / "out.md"
            src.write_text(OKF, encoding="utf-8")
            r = run(STRIP, src, out)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(r.stdout, "")
            body = out.read_text(encoding="utf-8")
            self.assertTrue(body.startswith("# Heading"), body)
            self.assertNotIn("type:", body)
            self.assertIn("The body.", body)

    def test_crlf_delimiters_still_strip(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "in.md"
            out = Path(d) / "out.md"
            src.write_bytes(b"---\r\ntype: Issue Draft\r\n---\r\n# Title\r\n")
            r = run(STRIP, src, out)
            self.assertEqual(r.returncode, 0, r.stderr)
            body = out.read_bytes()
            self.assertTrue(body.startswith(b"# Title"), body)
            self.assertNotIn(b"type:", body)
            self.assertNotIn(b"\r", body)

    def test_no_frontmatter_emits_whole_file(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "in.md"
            out = Path(d) / "out.md"
            src.write_bytes(b"# Just markdown\n\nA later ---\n")
            r = run(STRIP, src, out)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(out.read_bytes(), b"# Just markdown\n\nA later ---\n")

    def test_unclosed_frontmatter_exits_1(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "in.md"
            out = Path(d) / "out.md"
            src.write_text("---\ntype: PR Description\n# no closer\n", encoding="utf-8")
            r = run(STRIP, src, out)
            self.assertEqual(r.returncode, 1)
            self.assertFalse(out.exists())

    def test_output_is_utf8_lf_no_bom(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "in.md"
            out = Path(d) / "out.md"
            src.write_bytes(b"# caf\xc3\xa9\n")
            r = run(STRIP, src, out)
            self.assertEqual(r.returncode, 0, r.stderr)
            raw = out.read_bytes()
            self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))
            self.assertFalse(raw.startswith(b"\xff\xfe"))
            self.assertNotIn(b"\r", raw)
            self.assertEqual(raw, b"# caf\xc3\xa9\n")

    def test_missing_file_exits_1(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "missing.md"
            out = Path(d) / "out.md"
            r = run(STRIP, src, out)
            self.assertEqual(r.returncode, 1)
            self.assertFalse(out.exists())

    def test_missing_argv_exits_1(self):
        r = run(STRIP)
        self.assertEqual(r.returncode, 1)
        r2 = run(STRIP, "only-in.md")
        self.assertEqual(r2.returncode, 1)


if __name__ == "__main__":
    unittest.main()
