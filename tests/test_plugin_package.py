"""Packaging contract: marketplace at repo root, plugin at plugins/wit."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "wit"
PLUGIN_SOURCE = "./plugins/wit"
REQUIRED_PLUGIN_DIRS = ("agents", "references", "scripts", "skills")

MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"
VALIDATE = PLUGIN_ROOT / "scripts" / "validate.py"


class PluginPackageTests(unittest.TestCase):
    def test_marketplace_parses_and_points_at_standalone_plugin(self):
        data = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        self.assertEqual(data.get("name"), "witloop")
        wit = next(p for p in data["plugins"] if p.get("name") == "wit")
        self.assertEqual(wit.get("source"), PLUGIN_SOURCE)
        source_dir = (REPO_ROOT / wit["source"]).resolve()
        self.assertTrue(source_dir.is_dir(), wit["source"])
        self.assertEqual(source_dir, PLUGIN_ROOT.resolve())

    def test_plugin_metadata_is_valid(self):
        claude = json.loads((PLUGIN_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        copilot = json.loads((PLUGIN_ROOT / "plugin.json").read_text(encoding="utf-8"))
        codex = json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        wit = next(p for p in marketplace["plugins"] if p.get("name") == "wit")
        self.assertEqual(claude.get("name"), "wit")
        self.assertEqual(copilot.get("name"), "wit")
        self.assertEqual(codex.get("name"), "wit")
        versions = {claude["version"], copilot["version"], codex["version"], wit["version"]}
        self.assertEqual(len(versions), 1, versions)
        self.assertTrue((PLUGIN_ROOT / "skills").is_dir())
        skills = copilot.get("skills") or "skills/"
        self.assertTrue((PLUGIN_ROOT / skills).is_dir())
        self.assertTrue((PLUGIN_ROOT / (codex.get("skills") or "skills/")).is_dir())

    def test_convention_dirs_are_inside_plugin_root_only(self):
        for name in REQUIRED_PLUGIN_DIRS:
            inside = PLUGIN_ROOT / name
            self.assertTrue(inside.is_dir(), name)
            leftover = REPO_ROOT / name
            if leftover.exists():
                self.assertEqual(leftover.resolve(), inside.resolve(), name)

    def test_validate_py_lives_in_plugin_and_mentions_source(self):
        self.assertTrue(VALIDATE.is_file())
        src = VALIDATE.read_text(encoding="utf-8")
        self.assertIn(PLUGIN_SOURCE, src)
        self.assertIn("required plugin dir left outside plugin root", src)
        self.assertIn("MARKETPLACE", src)

    def test_plugin_root_refs_still_resolve(self):
        self.assertTrue((PLUGIN_ROOT / "AGENTS.md").is_file())
        self.assertTrue((PLUGIN_ROOT / "scripts" / "validate.py").is_file())
        self.assertTrue((PLUGIN_ROOT / "skills" / "dev" / "SKILL.md").is_file())
        self.assertTrue((PLUGIN_ROOT / "agents" / "wit-task-runner.md").is_file())
        self.assertTrue((PLUGIN_ROOT / "references" / "capabilities.md").is_file())
        self.assertFalse((REPO_ROOT / "skills").exists())
        self.assertFalse((REPO_ROOT / "agents").exists())
        self.assertFalse((REPO_ROOT / ".codex-plugin").exists())
        self.assertFalse((REPO_ROOT / ".claude-plugin" / "plugin.json").exists())
        self.assertTrue(MARKETPLACE.is_file())
