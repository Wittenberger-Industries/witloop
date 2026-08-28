"""Tests for skills/research/scripts/discover_skills.py (skill-root union)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT = REPO_ROOT / "plugins" / "wit"
SCRIPT = ROOT / "skills" / "research" / "scripts" / "discover_skills.py"
sys.path.insert(0, str(SCRIPT.parent))

import discover_skills  # noqa: E402

INTEGRATIONS = ROOT / "skills" / "research" / "references" / "integrations.md"


def _write_skill(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# skill\n", encoding="utf-8")
    return path


class SessionPathsTest(unittest.TestCase):
    def test_argv_wins_over_stdin(self):
        got = discover_skills.session_paths(["/sess/a"], "ignored\n")
        self.assertEqual(got, [Path("/sess/a")])

    def test_stdin_when_argv_empty(self):
        got = discover_skills.session_paths([], "/sess/a\n/sess/b\n")
        self.assertEqual(got, [Path("/sess/a"), Path("/sess/b")])

    def test_blank_stdin_lines_dropped(self):
        self.assertEqual(discover_skills.session_paths([], "\n  \n"), [])


class DiscoverUnionTest(unittest.TestCase):
    def test_cursor_cache_skill_is_present_without_claude_registry(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            skill = _write_skill(
                home / ".cursor" / "plugins" / "cache" / "cursor-public"
                / "superpowers" / "deadbeef" / "skills" / "brainstorming" / "SKILL.md"
            )
            roots = discover_skills.discover_skill_roots(home)
            self.assertTrue(discover_skills.skill_is_present("brainstorming", roots))
            self.assertFalse(discover_skills.skill_is_present("frontend-design", roots))
            self.assertTrue(any(p.name == "skills" and "cursor" in str(p) for p in roots))
            self.assertTrue(skill.is_file())

    def test_session_path_counts_as_present(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            skill = _write_skill(Path(td) / "session" / "frontend-design" / "SKILL.md")
            roots = discover_skills.discover_skill_roots(home, [skill])
            self.assertTrue(discover_skills.skill_is_present("frontend-design", roots))

    def test_claude_registry_install_path(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            plugin = home / "claude-plug"
            _write_skill(plugin / "skills" / "systematic-debugging" / "SKILL.md")
            registry = home / ".claude" / "plugins" / "installed_plugins.json"
            registry.parent.mkdir(parents=True, exist_ok=True)
            registry.write_text(
                json.dumps({
                    "version": 2,
                    "plugins": {
                        "superpowers@market": [{
                            "scope": "user",
                            "installPath": str(plugin),
                        }],
                    },
                }),
                encoding="utf-8",
            )
            roots = discover_skills.discover_skill_roots(home)
            self.assertTrue(discover_skills.skill_is_present("systematic-debugging", roots))

    def test_copilot_install_dir(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            _write_skill(
                home / ".copilot" / "installed-plugins" / "org" / "wit"
                / "skills" / "find-skills" / "SKILL.md"
            )
            roots = discover_skills.discover_skill_roots(home)
            self.assertTrue(discover_skills.skill_is_present("find-skills", roots))

    def test_agents_flat_dir(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            _write_skill(home / ".agents" / "skills" / "wit-dev" / "SKILL.md")
            roots = discover_skills.discover_skill_roots(home)
            self.assertTrue(discover_skills.skill_is_present("wit-dev", roots))

    def test_union_order_session_claude_cursor_copilot_agents(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            session = _write_skill(Path(td) / "session" / "sess-skill" / "SKILL.md")
            claude_plug = home / "claude-plug"
            _write_skill(claude_plug / "skills" / "claude-skill" / "SKILL.md")
            registry = home / ".claude" / "plugins" / "installed_plugins.json"
            registry.parent.mkdir(parents=True, exist_ok=True)
            registry.write_text(
                json.dumps({"plugins": {"p": [{"installPath": str(claude_plug)}]}}),
                encoding="utf-8",
            )
            cursor_skill = _write_skill(
                home / ".cursor" / "plugins" / "cache" / "pub" / "plug" / "h"
                / "skills" / "cursor-skill" / "SKILL.md"
            )
            copilot_skill = _write_skill(
                home / ".copilot" / "installed-plugins" / "org" / "plug"
                / "skills" / "copilot-skill" / "SKILL.md"
            )
            agents_skill = _write_skill(
                home / ".agents" / "skills" / "agents-skill" / "SKILL.md"
            )

            roots = discover_skills.discover_skill_roots(home, [session.parent])

            def idx(pred):
                for i, p in enumerate(roots):
                    if pred(p):
                        return i
                self.fail("root not found for {}".format(pred))

            i_session = idx(lambda p: p.resolve() == session.parent.resolve())
            i_claude = idx(lambda p: p.resolve() == claude_plug.resolve())
            i_cursor = idx(lambda p: p.resolve() == cursor_skill.parent.parent.resolve())
            i_copilot = idx(
                lambda p: "installed-plugins" in str(p) or p.resolve() == copilot_skill.parent.parent.resolve()
            )
            i_agents = idx(lambda p: p.resolve() == agents_skill.parent.parent.resolve())
            self.assertLess(i_session, i_claude)
            self.assertLess(i_claude, i_cursor)
            self.assertLess(i_cursor, i_copilot)
            self.assertLess(i_copilot, i_agents)

    def test_missing_skill_is_absent_only_after_union(self):
        with tempfile.TemporaryDirectory() as td:
            roots = discover_skills.discover_skill_roots(td)
            self.assertFalse(discover_skills.skill_is_present("brainstorming", roots))

    def test_invalid_registry_is_skipped(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            registry = home / ".claude" / "plugins" / "installed_plugins.json"
            registry.parent.mkdir(parents=True, exist_ok=True)
            registry.write_text("{not json", encoding="utf-8")
            self.assertEqual(discover_skills.claude_install_paths(home), [])


class CliTest(unittest.TestCase):
    def test_cli_name_present_from_cursor_cache(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            _write_skill(
                home / ".cursor" / "plugins" / "cache" / "pub" / "plug" / "h"
                / "skills" / "brainstorming" / "SKILL.md"
            )
            r = subprocess.run(
                [sys.executable, str(SCRIPT), "--home", str(home), "--name", "brainstorming"],
                capture_output=True, text=True,
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(r.stdout.strip(), "present")

    def test_cli_name_absent(self):
        with tempfile.TemporaryDirectory() as td:
            r = subprocess.run(
                [sys.executable, str(SCRIPT), "--home", td, "--name", "nope"],
                capture_output=True, text=True,
            )
            self.assertEqual(r.returncode, 1)
            self.assertEqual(r.stdout.strip(), "absent")


class IntegrationsDocTest(unittest.TestCase):
    def test_documents_union_order_and_forbids_absent_before_search(self):
        text = INTEGRATIONS.read_text(encoding="utf-8")
        markers = [
            "argv or stdin",
            "installed_plugins.json",
            "~/.cursor/plugins/cache",
            "~/.copilot/installed-plugins",
            "~/.agents/skills",
        ]
        positions = [text.find(m) for m in markers]
        self.assertTrue(all(p >= 0 for p in positions), positions)
        self.assertEqual(positions, sorted(positions))
        self.assertIn("(skill absent)", text)
        self.assertIn("discover_skills.py", text)
        forbid = text.lower()
        self.assertIn("never stamp", forbid)
        self.assertIn("before", forbid)
