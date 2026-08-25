"""Contract tests for semantic work-type routing (orchestrator judgment)."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEV_SKILL = ROOT / "skills" / "dev" / "SKILL.md"
WORK_TYPES = ROOT / "skills" / "dev" / "references" / "work-types.md"
WIT_DEV_ALIAS = ROOT / "references" / "skill-aliases" / "wit-dev" / "SKILL.md"
FEATURE_FOLDER = ROOT / "references" / "feature-folder-cases.md"
WIT_DIRECTORY = ROOT / "skills" / "research" / "references" / "wit-directory.md"
INTEGRATIONS = ROOT / "skills" / "research" / "references" / "integrations.md"
VALIDATE = ROOT / "scripts" / "validate.py"
ADD_ISSUES = ROOT / "skills" / "add-issues" / "SKILL.md"
SCAN = ROOT / "skills" / "scan" / "SKILL.md"
RPA = ROOT / "skills" / "rpa" / "SKILL.md"

ANNOUNCE = (
    "Work type: <type> (<source>). Override: --kind feature|bug-fix|investigation"
)
FOLDER_CLASSES = (
    "new / resume / in-flight-overlap / done-collision / roadmap-row"
)
PLUGIN_INVESTIGATION = (
    "${CLAUDE_PLUGIN_ROOT}/skills/dev/references/investigation.md"
)
PLUGIN_BUG_FIX = "${CLAUDE_PLUGIN_ROOT}/skills/dev/references/bug-fix.md"
PLUGIN_WORK_TYPES = "${CLAUDE_PLUGIN_ROOT}/skills/dev/references/work-types.md"
USER_COMMANDS = ("add-issues", "dev", "rpa", "scan")


def frontmatter(text: str) -> str:
    if not text.startswith("---"):
        raise AssertionError("no frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise AssertionError("unterminated frontmatter")
    return parts[1]


def folded_description(text: str) -> str:
    fm = frontmatter(text)
    match = re.search(r"(?ms)^description:\s*>\s*\n((?:[ \t].*\n)+)", fm)
    if match:
        return " ".join(
            line.strip() for line in match.group(1).splitlines() if line.strip()
        )
    match = re.search(r'(?m)^description:\s*"([^"]*)"', fm)
    if match:
        return match.group(1)
    match = re.search(r"(?m)^description:\s*(.+)$", fm)
    if match:
        return match.group(1).strip().strip("\"'")
    raise AssertionError("no description")


def skill_description(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml
    except ImportError:
        return folded_description(text)
    data = yaml.safe_load(frontmatter(text))
    if not isinstance(data, dict) or not isinstance(data.get("description"), str):
        raise AssertionError("%s: description missing" % path)
    return data["description"]


def prelude(text: str) -> str:
    match = re.search(r"(?m)^1\. \*\*Host probe", text)
    if match is None:
        raise AssertionError("dev SKILL.md has no numbered Host probe step")
    return text[: match.start()]


class WorkTypesReferenceTests(unittest.TestCase):
    def test_work_types_is_okf_reference(self):
        self.assertTrue(WORK_TYPES.is_file(), "skills/dev/references/work-types.md is missing")
        text = WORK_TYPES.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        self.assertIn("type: Reference", frontmatter(text))

    def test_semantic_orchestrator_judgment_not_keyword_classifier(self):
        text = WORK_TYPES.read_text(encoding="utf-8")
        self.assertIn("semantic orchestrator judgment", text)
        self.assertIn("keyword-only runtime classifier", text)
        self.assertRegex(text, r"(?i)forbid|not a keyword-only|never a keyword-only")
        self.assertNotIn("classify_work_type.py", text)

    def test_conservative_tells_for_all_three_types(self):
        text = WORK_TYPES.read_text(encoding="utf-8")
        self.assertIn("feature", text)
        self.assertIn("bug-fix", text)
        self.assertIn("investigation", text)
        self.assertIn("I want a feature", text)
        self.assertIn("fix this bug", text)
        self.assertIn("why does X fail", text)
        self.assertIn("how does X work", text)
        self.assertIn("explain this architecture", text)

    def test_mixed_unclear_defaults_to_announced_feature(self):
        text = WORK_TYPES.read_text(encoding="utf-8")
        self.assertRegex(text, r"mixed|unclear")
        self.assertIn("feature", text)
        self.assertIn("ambiguous-default", text)
        self.assertIn("Never ask", text)

    def test_invalid_kind_stops_with_valid_set(self):
        text = WORK_TYPES.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?i)invalid `--kind`")
        self.assertRegex(text, r"stop")
        self.assertIn("feature|bug-fix|investigation", text)

    def test_always_announce_string_and_precedence(self):
        text = WORK_TYPES.read_text(encoding="utf-8")
        self.assertIn(ANNOUNCE, text)
        self.assertIn("kind", text)
        self.assertIn("inferred", text)
        self.assertIn("ambiguous-default", text)
        self.assertRegex(
            text,
            r"`--kind`\s*>\s*inferred\s*>\s*ambiguous-default",
        )

    def test_resume_honors_stamp_unless_kind_missing_means_feature(self):
        text = WORK_TYPES.read_text(encoding="utf-8")
        self.assertIn("Work type:", text)
        self.assertRegex(text, r"resume", re.I)
        self.assertIn("--kind", text)
        self.assertIn("missing Work type: stamp means feature", text)

    def test_after_announce_points_to_plugin_root_routes(self):
        text = WORK_TYPES.read_text(encoding="utf-8")
        after = text[text.index("## After announce") :]
        self.assertIn("load `%s` and exit" % PLUGIN_INVESTIGATION, after)
        self.assertRegex(after, r"(?i)after the folder classifier")
        self.assertIn("load `%s`" % PLUGIN_BUG_FIX, after)
        self.assertRegex(after, r"(?i)do not load.{0,80}bug-fix\.md")
        self.assertNotIn("classify_work_type.py", text)


class DevSkillPreludeTests(unittest.TestCase):
    def test_prelude_before_host_probe_loads_work_types_only(self):
        text = DEV_SKILL.read_text(encoding="utf-8")
        head = prelude(text)
        self.assertIn(PLUGIN_WORK_TYPES, head)
        self.assertIn(PLUGIN_INVESTIGATION, head)
        self.assertLess(
            head.index(PLUGIN_WORK_TYPES),
            head.index(PLUGIN_INVESTIGATION),
        )
        self.assertIn(ANNOUNCE, head)
        self.assertIn("--kind", head)
        self.assertIn("--auto", head)
        self.assertIn("load `%s` and exit" % PLUGIN_INVESTIGATION, head)
        self.assertIn(PLUGIN_INVESTIGATION, text)
        self.assertIn(PLUGIN_BUG_FIX, text)
        self.assertNotIn(PLUGIN_BUG_FIX, head)
        self.assertIn(FOLDER_CLASSES, text)
        self.assertLess(text.index(FOLDER_CLASSES), text.index(PLUGIN_BUG_FIX))
        self.assertIn("Work type is bug-fix", text)
        self.assertRegex(text, r"(?i)do not load.{0,80}bug-fix\.md")
        self.assertNotIn("classify_work_type.py", text)

    def test_folder_classifier_and_auto_parse_still_present(self):
        text = DEV_SKILL.read_text(encoding="utf-8")
        self.assertIn(FOLDER_CLASSES, text)
        self.assertIn("--auto", text)
        self.assertIn("Parse flags", text)


class AliasKindForwardTests(unittest.TestCase):
    def test_alias_forwards_kind_beside_auto(self):
        text = WIT_DEV_ALIAS.read_text(encoding="utf-8")
        self.assertIn("--auto", text)
        self.assertIn("--kind", text)
        self.assertRegex(text, r"passing `--auto`.*`--kind`|`--auto`.*`--kind`")


class ResumeAndTemplateTests(unittest.TestCase):
    def test_resume_honors_work_type_stamp(self):
        text = FEATURE_FOLDER.read_text(encoding="utf-8")
        self.assertIn("## Resume detection", text)
        self.assertIn("Work type:", text)
        self.assertIn("--kind", text)
        self.assertIn("missing Work type: line means feature", text)

    def test_progress_template_has_optional_work_type(self):
        text = WIT_DIRECTORY.read_text(encoding="utf-8")
        start = text.index("## `progress.md` template")
        end = text.index("## `tokens.md` template")
        template = text[start:end]
        self.assertIn("**Work type:**", template)
        self.assertIn("feature | bug-fix", template)
        self.assertIn("a missing line means feature", template)


class IntegrationsIndependentlyLoadedTests(unittest.TestCase):
    def test_understand_pre_fix_debug_and_chat_only_exception(self):
        text = INTEGRATIONS.read_text(encoding="utf-8")
        self.assertIn("understand", text)
        self.assertRegex(text, r"\bhow\b")
        self.assertRegex(text, r"REQUIRED when installed")
        self.assertRegex(text, r"\bwhy\b")
        self.assertRegex(text, r"OPTIONAL")
        self.assertRegex(text, r"motivational")
        self.assertIn("investigation", text)
        self.assertIn("does NOT capture into `.wit/`", text)
        self.assertIn("chat-only", text)
        self.assertIn("debug (any phase)", text)
        self.assertIn("pre-fix", text)
        self.assertIn("systematic-debugging", text)
        self.assertIn("verify absence", text.lower())


class FourCommandAndDescriptionTests(unittest.TestCase):
    def test_four_advertised_commands_unchanged(self):
        names = []
        for skill_dir in sorted((ROOT / "skills").iterdir()):
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                continue
            fm = frontmatter(skill_md.read_text(encoding="utf-8"))
            if re.search(r"(?m)^user-invocable:\s*false\s*$", fm):
                continue
            match = re.search(r"(?m)^name:\s*(\S+)", fm)
            self.assertIsNotNone(match, skill_md)
            names.append(match.group(1))
        self.assertEqual(tuple(sorted(names)), USER_COMMANDS)

    def test_add_issues_keeps_file_a_bug_others_have_no_kind(self):
        self.assertIn("file a bug", ADD_ISSUES.read_text(encoding="utf-8"))
        self.assertNotIn("file a bug", skill_description(DEV_SKILL))
        self.assertNotIn("file a bug", skill_description(WIT_DEV_ALIAS))
        for path in (SCAN, RPA, ADD_ISSUES):
            self.assertNotIn("--kind", skill_description(path), path)
        for name in ("wit-scan", "wit-rpa", "wit-add-issues"):
            alias = ROOT / "references" / "skill-aliases" / name / "SKILL.md"
            self.assertNotIn("--kind", skill_description(alias), alias)

    def test_dev_and_alias_descriptions_under_cap_with_conservative_tells(self):
        src = VALIDATE.read_text(encoding="utf-8")
        cap_match = re.search(r"DESC_CAP = (\d+)", src)
        self.assertIsNotNone(cap_match)
        cap = int(cap_match.group(1))
        self.assertEqual(cap, 1024)
        for path in (DEV_SKILL, WIT_DEV_ALIAS):
            desc = skill_description(path)
            self.assertLessEqual(len(desc), cap, "%s description is %s chars" % (path, len(desc)))
            self.assertIn("fix this bug", desc)
            self.assertIn("why does X fail", desc)
            self.assertIn("how does X work", desc)
            self.assertIn("explain this architecture", desc)


class FeatureContractTests(unittest.TestCase):
    def test_existing_feature_contract_still_present(self):
        text = DEV_SKILL.read_text(encoding="utf-8")
        self.assertIn("never skipped", text)
        self.assertIn("design gate", text)
        self.assertIn(FOLDER_CLASSES, text)
        self.assertIn("brainstorm", text.lower())


class ValidateSourceAnchorTests(unittest.TestCase):
    def test_validate_pins_announce_string_and_work_types_file(self):
        src = VALIDATE.read_text(encoding="utf-8")
        self.assertIn(ANNOUNCE, src)
        self.assertIn("skills/dev/references/work-types.md", src)
        self.assertIn("skills/dev/SKILL.md", src)
        this = Path(__file__).read_text(encoding="utf-8")
        self.assertNotRegex(this, r"(?m)^(?:import validate|from validate import)")


if __name__ == "__main__":
    unittest.main()
