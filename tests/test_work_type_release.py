"""Release contract for work-type routing 1.15.0.

Pins lockstep plugin versions, five advertised commands, three work types,
source-memory routing, and the three named agents. Does not import
scripts/validate.py (that module runs checks on import).
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CODEX = ROOT / ".codex-plugin" / "plugin.json"
VALIDATE = ROOT / "scripts" / "validate.py"
OVERVIEW = ROOT / ".wit" / "overview.md"
ARCHITECTURE = ROOT / ".wit" / "architecture.md"
REPO_MAP = ROOT / ".wit" / "repo-map.md"
AGENTS_DIR = ROOT / "agents"
SKILLS_DIR = ROOT / "skills"

RELEASE = "1.16.4"
MARKETPLACE_CATALOG = "0.2.0"
USER_COMMANDS = ("add-issues", "dev", "rpa", "scan", "setup")
NAMED_AGENTS = ("wit-code-checker", "wit-researcher", "wit-task-runner")
WORK_TYPES = ("feature", "bug-fix", "investigation")
KIND = "--kind feature|bug-fix|investigation"
HOSTS = ("Claude Code", "Codex CLI", "Copilot CLI", "Grok Build", "Cursor")
EM_DASH = "\u2014"


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


def user_invocable_skill_names() -> tuple[str, ...]:
    names = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        fm = frontmatter(skill_md.read_text(encoding="utf-8"))
        if re.search(r"(?m)^user-invocable:\s*false\s*$", fm):
            continue
        match = re.search(r"(?m)^name:\s*(\S+)", fm)
        if match is None:
            raise AssertionError("%s: missing name" % skill_md)
        names.append(match.group(1))
    return tuple(sorted(names))


def wit_plugin_version(marketplace: dict) -> str | None:
    for plugin in marketplace.get("plugins", []):
        if plugin.get("name") == "wit":
            return plugin.get("version")
    return None


class ManifestLockstepTests(unittest.TestCase):
    def test_three_plugin_versions_are_exactly_1_16_4(self):
        plugin = json.loads(load(PLUGIN))
        marketplace = json.loads(load(MARKETPLACE))
        codex = json.loads(load(CODEX))
        v_plugin = plugin.get("version")
        v_codex = codex.get("version")
        v_market = wit_plugin_version(marketplace)
        self.assertEqual(v_plugin, RELEASE)
        self.assertEqual(v_codex, RELEASE)
        self.assertEqual(v_market, RELEASE)
        self.assertEqual({v_plugin, v_codex, v_market}, {RELEASE})
        self.assertEqual(marketplace.get("metadata", {}).get("version"), MARKETPLACE_CATALOG)

    def test_manifest_descriptions_keep_five_commands_and_five_hosts(self):
        plugin = json.loads(load(PLUGIN))
        marketplace = json.loads(load(MARKETPLACE))
        wit = next(p for p in marketplace["plugins"] if p.get("name") == "wit")
        codex = json.loads(load(CODEX))
        src = VALIDATE.read_text(encoding="utf-8")
        cap_match = re.search(r"DESC_CAP = (\d+)", src)
        self.assertIsNotNone(cap_match)
        cap = int(cap_match.group(1))
        self.assertEqual(cap, 1024)
        for desc in (plugin["description"], wit["description"], codex["description"]):
            self.assertLessEqual(len(desc), cap)
            for host in HOSTS:
                self.assertIn(host, desc, host)
            for command in (
                "/wit:setup",
                "/wit:scan",
                "/wit:dev",
                "/wit:rpa",
                "/wit:add-issues",
            ):
                self.assertIn(command, desc, command)
            self.assertIn("keep-alive", desc)
            self.assertNotIn("/wit:investigate", desc)
            self.assertNotIn("/wit:how", desc)
            self.assertNotIn(EM_DASH, desc)
        self.assertIn(": plugin description is", VALIDATE.read_text(encoding="utf-8"))


class FiveCommandTests(unittest.TestCase):
    def test_five_user_invocable_skill_names(self):
        names = user_invocable_skill_names()
        self.assertEqual(names, USER_COMMANDS)
        self.assertEqual(len(names), 5)
        self.assertNotIn("investigate", names)
        self.assertNotIn("how", names)


class SourceMemoryTests(unittest.TestCase):
    def test_overview_routes_work_types_at_1_16_4(self):
        text = load(OVERVIEW)
        self.assertIn(RELEASE, text)
        self.assertNotIn("1.16.3", text)
        self.assertNotIn("1.16.2", text)
        self.assertNotIn("1.16.1", text)
        self.assertNotIn("1.16.0", text)
        self.assertNotIn("1.14.1", text)
        self.assertRegex(text, r"(?i)work type")
        for work_type in WORK_TYPES:
            self.assertIn(work_type, text, work_type)
        self.assertRegex(text, r"(?i)before write-capable setup")
        self.assertRegex(text, r"(?i)investigation.{0,80}read-only|read-only.{0,80}investigation")
        self.assertRegex(text, r"(?i)bug-fix.{0,80}overlay|overlay.{0,80}bug-fix")
        self.assertRegex(text, r"five user-facing|user-facing `setup`")
        self.assertIn("setup", text)
        self.assertIn("scan", text)
        self.assertIn("dev", text)
        self.assertIn("rpa", text)
        self.assertIn("add-issues", text)
        self.assertNotIn(EM_DASH, text)

    def test_architecture_loads_work_type_refs_from_dev(self):
        text = load(ARCHITECTURE)
        self.assertIn("```mermaid", text)
        self.assertIn("work-types", text)
        self.assertIn("investigation", text)
        self.assertIn("bug-fix", text)
        self.assertRegex(text, r"(?i)on-demand")
        entry = text.split("subgraph phases", 1)[0]
        self.assertIn('setup_sk["setup"]', entry)
        self.assertIn('scan_sk["scan"]', entry)
        self.assertIn('dev_sk["dev"]', entry)
        self.assertIn('rpa_sk["rpa"]', entry)
        self.assertIn('addissues["add-issues"]', entry)
        self.assertNotIn("investigate", entry)
        self.assertIn("Five entry skills", text)
        self.assertIn("generic PLUGIN_ROOT (1.16.0)", text)
        named = text[text.find('subgraph named') : text.find("subgraph py")]
        self.assertIn("wit-researcher", named)
        self.assertIn("wit-task-runner", named)
        self.assertIn("wit-code-checker", named)
        self.assertEqual(named.count("wit-"), 3)
        self.assertNotIn(EM_DASH, text)

    def test_repo_map_records_kind_flag_and_work_type_files(self):
        text = load(REPO_MAP)
        self.assertIn(KIND, text)
        self.assertIn("/wit:dev", text)
        self.assertIn("skills/dev/references/work-types.md", text)
        self.assertIn("skills/dev/references/investigation.md", text)
        self.assertIn("skills/dev/references/bug-fix.md", text)
        self.assertRegex(text, r"three-manifest|version parity|lockstep")
        for command in ("/wit:setup", "/wit:scan", "/wit:rpa", "/wit:add-issues"):
            self.assertIn(command, text, command)
        self.assertNotIn("/wit:investigate", text)
        self.assertNotIn(EM_DASH, text)


class AgentAndLayoutTests(unittest.TestCase):
    def test_three_named_agents_only(self):
        names = tuple(sorted(path.stem for path in AGENTS_DIR.glob("*.md")))
        self.assertEqual(names, NAMED_AGENTS)
        self.assertEqual(len(names), 3)

    def test_no_investigate_skill_directory(self):
        self.assertFalse((SKILLS_DIR / "investigate").exists())
        self.assertFalse((SKILLS_DIR / "how").exists())

    def test_does_not_import_validate_py(self):
        this = Path(__file__).read_text(encoding="utf-8")
        self.assertNotRegex(this, r"(?m)^(?:import validate|from validate import)")
        self.assertIn("Does not import", this)


if __name__ == "__main__":
    unittest.main()
