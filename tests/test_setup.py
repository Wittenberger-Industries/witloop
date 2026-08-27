"""Contract tests for /wit:setup first-run (0004-setup).

Pins the user-invocable setup skill, first-run ownership, --auto simple plus
ledger | on, missing repo-map.md as the empty-project path, and the plugin-root
tell. Does not import scripts/validate.py (that module runs checks on import).
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETUP = ROOT / "skills" / "setup" / "SKILL.md"
SETUP_NOTES = ROOT / "docs" / "design-notes" / "setup.md"
CAPABILITIES = ROOT / "references" / "capabilities.md"
ARCHITECTURE = ROOT / ".wit" / "architecture.md"
EM_DASH = "\u2014"
RUNTIME_NEVER = re.compile(
    r"runtime never reads this file|never loaded at runtime",
    re.IGNORECASE,
)

OWNED = (SETUP, SETUP_NOTES)


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


class SetupSkillTests(unittest.TestCase):
    def test_setup_skill_exists_and_is_user_invocable(self):
        text = load(SETUP)
        fm = frontmatter(text)
        self.assertIn("type: Skill", fm)
        self.assertRegex(fm, r"(?m)^name:\s*setup\s*$")
        self.assertNotRegex(fm, r"(?m)^user-invocable:")
        self.assertIn("/wit:setup", text)

    def test_description_auto_triggers_include_set_up_wit_and_bootstrap(self):
        fm = frontmatter(load(SETUP))
        self.assertIn("set up wit here", fm)
        self.assertIn("bootstrap wit", fm)

    def test_owns_first_run_repo_docs_constitution_plugin_models_ledger(self):
        text = load(SETUP)
        self.assertIn("repo-map.md", text)
        self.assertIn("constitution.md", text)
        self.assertIn("plugin-bootstrap.md", text)
        self.assertIn(".wi", text)
        self.assertIn("greenfield", text)
        self.assertIn("models.md", text)
        self.assertIn("First-run setup", text)
        self.assertIn("## Token ledger", text)
        self.assertIn("ledger", text)
        self.assertIn("chore(wit): setup", text)

    def test_auto_writes_simple_and_ledger_on(self):
        text = load(SETUP)
        self.assertIn("--auto", text)
        self.assertIn("simple", text)
        self.assertIn("ledger | on", text)

    def test_missing_repo_map_is_the_empty_project_path(self):
        text = load(SETUP)
        self.assertRegex(
            text,
            r"(?i)missing `?\.wit/repo-map\.md`? is the empty-project path",
        )
        self.assertNotRegex(
            text,
            r"(?i)missing `?\.wit/`? directory is the empty-project path",
        )

    def test_no_em_dashes_in_owned_files(self):
        for path in OWNED:
            text = load(path)
            self.assertNotIn(EM_DASH, text, path)


class SetupDesignNotesTests(unittest.TestCase):
    def test_design_notes_exist_and_are_not_loaded_at_runtime(self):
        text = load(SETUP_NOTES)
        fm = frontmatter(text)
        self.assertIn("type: Design Notes", fm)
        self.assertRegex(text, RUNTIME_NEVER)
        self.assertIn("skills/setup/SKILL.md", text)

    def test_skill_points_at_design_notes_as_maintainer_doc(self):
        text = load(SETUP)
        self.assertIn("docs/design-notes/setup.md", text)
        self.assertRegex(text, RUNTIME_NEVER)


class PluginRootAndCaptionTests(unittest.TestCase):
    def test_plugin_root_tell_stays_scan_skill(self):
        text = load(CAPABILITIES)
        self.assertIn("skills/scan/SKILL.md", text)
        self.assertIn(
            "`skills/` + `.claude-plugin/` + `skills/scan/SKILL.md`",
            text,
        )
        self.assertNotIn("skills/setup/SKILL.md", text)

    def test_architecture_plugin_root_caption_stays_1_16_0(self):
        text = load(ARCHITECTURE)
        self.assertIn("generic PLUGIN_ROOT (1.16.0)", text)


class ImportGuardTests(unittest.TestCase):
    def test_does_not_import_validate_py(self):
        this = Path(__file__).read_text(encoding="utf-8")
        self.assertNotRegex(this, r"(?m)^(?:import validate|from validate import)")
        self.assertIn("Does not import", this)


if __name__ == "__main__":
    unittest.main()
