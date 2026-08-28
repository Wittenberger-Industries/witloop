"""Generic ${PLUGIN_ROOT} placeholder and resolve-once protocol (ADR-0003)."""
from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT = REPO_ROOT / "plugins" / "wit"
CAPABILITIES = ROOT / "references" / "capabilities.md"
AGENTS = ROOT / "AGENTS.md"
VALIDATE = ROOT / "scripts" / "validate.py"
DEV = ROOT / "skills" / "dev" / "SKILL.md"
LIVE_DIRS = ("skills", "agents", "references")
LIVE_FILES = (AGENTS, ROOT / "README.md")
PLACEHOLDER = "${PLUGIN_ROOT}"
LEGACY = "${CLAUDE_PLUGIN_ROOT}"


def live_markdown() -> list[Path]:
    files = []
    for name in LIVE_DIRS:
        files.extend((ROOT / name).rglob("*.md"))
    files.extend(LIVE_FILES)
    return [path for path in files if path.is_file()]


class PluginRootPlaceholderTests(unittest.TestCase):
    def test_live_docs_use_plugin_root_not_claude_placeholder(self):
        found_new = False
        for path in live_markdown():
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(LEGACY, text, path.relative_to(ROOT).as_posix())
            if PLACEHOLDER in text:
                found_new = True
        self.assertTrue(found_new, "no live doc uses ${PLUGIN_ROOT}")

    def test_validate_py_resolves_plugin_root_and_rejects_legacy(self):
        src = VALIDATE.read_text(encoding="utf-8")
        self.assertIn("PLUGIN_ROOT", src)
        self.assertIn("leftover", src)
        self.assertIn(r"\$\{PLUGIN_ROOT\}", src)
        self.assertIn("{CLAUDE_PLUGIN_ROOT}", src)


class PluginRootProtocolTests(unittest.TestCase):
    def test_capabilities_plugin_root_is_generic_resolve_once(self):
        text = CAPABILITIES.read_text(encoding="utf-8")
        self.assertIn("## Plugin root", text)
        self.assertIn(PLACEHOLDER, text)
        self.assertIn("PLUGIN_ROOT", text)
        self.assertIn("WIT_PLUGIN_ROOT", text)
        self.assertIn("CLAUDE_PLUGIN_ROOT", text)
        self.assertIn("GROK_PLUGIN_ROOT", text)
        self.assertIn("Never pass an unexpanded", text)
        self.assertIn('if Claude, keep the env; else', text)
        matrix_line = next(
            line for line in text.splitlines() if line.startswith("| plugin_root |")
        )
        cells = [cell.strip() for cell in matrix_line.strip("|").split("|")]
        self.assertEqual(cells[0], "plugin_root")
        self.assertEqual(set(cells[1:]), {"resolve-once"})

    def test_agents_does_not_frame_plugin_root_as_not_claude(self):
        text = AGENTS.read_text(encoding="utf-8")
        self.assertIn("## Plugin root", text)
        self.assertIn(PLACEHOLDER, text)
        self.assertNotIn("If you are not Claude Code", text)
        self.assertIn("including Claude", text)

    def test_dev_host_probe_does_not_key_off_claude_env_emptiness(self):
        text = DEV.read_text(encoding="utf-8")
        self.assertIn("plugin-root env vars are empty", text)
        self.assertNotIn("and `CLAUDE_PLUGIN_ROOT` is empty", text)
        self.assertIn("never pass unexpanded", text.lower())


if __name__ == "__main__":
    unittest.main()
