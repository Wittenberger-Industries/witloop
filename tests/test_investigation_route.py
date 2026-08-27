"""Contract tests for the read-only investigation exit (on-demand reference)."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVESTIGATION = ROOT / "skills" / "dev" / "references" / "investigation.md"
INTEGRATIONS = ROOT / "skills" / "research" / "references" / "integrations.md"
DISCOVER = (
    "python ${PLUGIN_ROOT}/skills/research/scripts/discover_skills.py --name how"
)
VIA_HOW = "investigation via how"
VIA_HOW_WHY = "investigation via how + why"
VIA_FALLBACK = "investigation via wit fallback (how absent)"
DENY = (
    ".wit/features",
    "progress.md",
    "brief.md",
    "tokens.md",
    "roadmap.md",
    "models.md",
    "keep-alive",
    "worktree",
    "wit-researcher",
    "wit-task-runner",
    "wit-code-checker",
    "brainstorm",
    "research",
    "plan",
    "build",
    "ship",
)


def frontmatter(text: str) -> str:
    if not text.startswith("---"):
        raise AssertionError("no frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise AssertionError("unterminated frontmatter")
    return parts[1]


def load_investigation() -> str:
    if not INVESTIGATION.is_file():
        raise AssertionError("skills/dev/references/investigation.md is missing")
    return INVESTIGATION.read_text(encoding="utf-8")


class InvestigationReferenceTests(unittest.TestCase):
    def test_investigation_is_okf_reference(self):
        self.assertTrue(
            INVESTIGATION.is_file(),
            "skills/dev/references/investigation.md is missing",
        )
        text = load_investigation()
        self.assertTrue(text.startswith("---\n"))
        self.assertIn("type: Reference", frontmatter(text))
        self.assertRegex(
            text,
            r"enough to decide when loaded alone|loaded alone",
        )

    def test_exits_this_turn_without_reclassify_or_writes(self):
        text = load_investigation()
        self.assertRegex(text, r"(?i)\bSTOP\b")
        self.assertRegex(text, r"(?i)do not re-classify|not re-classify")
        self.assertIn("--auto", text)
        self.assertRegex(text, r"no-op")
        self.assertRegex(text, r"(?i)scan")
        self.assertIn("models.md", text)
        self.assertRegex(text, r"\.wi/")
        self.assertIn("keep-alive", text)
        self.assertRegex(text, r"(?i)token ledger")
        self.assertRegex(text, r"(?i)feature folder")
        self.assertRegex(text, r"(?i)this turn")


class DelegationAndFallbackTests(unittest.TestCase):
    def test_discovers_how_via_union_and_delegates(self):
        text = load_investigation()
        self.assertIn(DISCOVER, text)
        self.assertIn("discover_skills.py --name why", text)
        self.assertRegex(text, r"(?i)full union")
        self.assertRegex(text, r"(?i)never stamp absent from memory")
        self.assertRegex(text, r"(?i)delegation is mandatory when `how` is present")
        self.assertRegex(text, r"(?i)in memory")
        self.assertRegex(text, r"(?i)Skill paths")
        self.assertIn("progress.md", text)

    def test_why_is_optional_motivational_not_required_mcp(self):
        text = load_investigation()
        self.assertRegex(text, r"OPTIONAL")
        self.assertRegex(text, r"(?i)motivational")
        self.assertRegex(text, r"(?i)never a required MCP sweep")
        self.assertRegex(text, r"(?i)skip if absent")
        self.assertRegex(text, r"(?i)mechanical")

    def test_mode_lines_in_reply_not_progress(self):
        text = load_investigation()
        self.assertIn(VIA_HOW, text)
        self.assertIn(VIA_HOW_WHY, text)
        self.assertIn(VIA_FALLBACK, text)
        self.assertRegex(text, r"(?i)reply")
        self.assertRegex(text, r"(?i)not progress\.md")

    def test_fallback_caps_explorers_at_two_and_forbids_named_agents(self):
        text = load_investigation()
        self.assertRegex(text, r"(?i)no subagent")
        self.assertIn("Read", text)
        self.assertIn("Grep", text)
        self.assertIn("Glob", text)
        self.assertRegex(text, r"(?i)read-only git")
        self.assertRegex(text, r"(?i)at most (two|2)")
        self.assertRegex(text, r"(?i)Cap 2")
        self.assertRegex(text, r"(?i)explorer")
        self.assertRegex(text, r"(?i)no new named agent")
        self.assertIn("wit-researcher", text)
        self.assertIn("wit-task-runner", text)
        self.assertIn("wit-code-checker", text)
        self.assertRegex(text, r"(?i)do not document")
        self.assertIn("readonly: true", text)
        self.assertRegex(text, r"(?i)universal")

    def test_who_initiates_is_wit_not_description_match(self):
        text = load_investigation()
        self.assertRegex(text, r"(?i)who initiates")
        self.assertRegex(text, r"(?i)\bwit\b")
        self.assertRegex(text, r"(?i)description-match")


class DenyListTests(unittest.TestCase):
    def test_deny_list_strings_are_explicit_forbids(self):
        text = load_investigation()
        self.assertRegex(text, r"(?i)deny-list|forbid")
        lowered = text.lower()
        self.assertTrue(
            "must not" in lowered or "do not" in lowered or "forbid" in lowered
        )
        for needle in DENY:
            self.assertIn(needle, text, "deny-list missing %s" % needle)
        self.assertRegex(text, r"(?i)product-file|product files")
        self.assertRegex(text, r"(?i)\bbranch\b")
        self.assertRegex(text, r"(?i)\bcommit\b")
        self.assertRegex(text, r"\bPR\b")
        self.assertRegex(text, r"(?i)\bADR\b")
        self.assertRegex(text, r"(?i)scan")

    def test_allowed_tools_and_exit_git_status(self):
        text = load_investigation()
        self.assertIn("WebSearch", text)
        self.assertIn("WebFetch", text)
        self.assertIn("discover_skills.py", text)
        self.assertRegex(text, r"(?i)gh view")
        self.assertRegex(text, r"(?i)list")
        self.assertIn("git status --porcelain", text)
        self.assertRegex(text, r"(?i)pre-existing dirt")
        self.assertRegex(text, r"(?i)defect")
        self.assertIn(".wit/features", text)

    def test_no_keep_alive_block_or_phase_done(self):
        text = load_investigation()
        self.assertRegex(text, r"(?i)no keep-alive block")
        self.assertRegex(text, r"(?i)Phase\s*=\s*done")
        self.assertRegex(text, r"(?i)no skills/investigate")


class OutputContractTests(unittest.TestCase):
    def test_explain_or_decide_with_sources_and_path_n_citations(self):
        text = load_investigation()
        self.assertIn("Overview", text)
        self.assertIn("Key Concepts", text)
        self.assertIn("How It Works", text)
        self.assertIn("Where Things Live", text)
        self.assertIn("Gotchas", text)
        self.assertRegex(text, r"(?i)recommendation")
        self.assertRegex(text, r"(?i)tradeoffs")
        self.assertIn("## Sources", text)
        self.assertIn("path:N", text)
        self.assertIn("path:symbol", text)
        self.assertRegex(text, r"(?i)inference")
        self.assertNotIn("\u00a7", text)
        self.assertRegex(text, r"(?i)never.{0,40}section sign|not the section sign")

    def test_hand_back_to_kind_feature_or_bug_fix(self):
        text = load_investigation()
        self.assertIn("--kind feature", text)
        self.assertIn("--kind bug-fix", text)
        self.assertRegex(text, r"(?i)hand back")
        self.assertRegex(text, r"(?i)do not start brainstorm")


class SurfaceAndIntegrationsTests(unittest.TestCase):
    def test_no_skills_investigate_directory(self):
        self.assertFalse(
            (ROOT / "skills" / "investigate").exists(),
            "skills/investigate/ must not exist",
        )

    def test_does_not_import_validate(self):
        this = Path(__file__).read_text(encoding="utf-8")
        self.assertNotRegex(this, r"(?m)^(?:import validate|from validate import)")

    def test_integrations_already_has_understand_chat_only_exception(self):
        text = INTEGRATIONS.read_text(encoding="utf-8")
        self.assertIn("understand", text)
        self.assertIn("chat-only", text)
        self.assertIn("does NOT capture into `.wit/`", text)
        self.assertRegex(text, r"\bhow\b")
        self.assertRegex(text, r"OPTIONAL")
        self.assertRegex(text, r"(?i)motivational")


if __name__ == "__main__":
    unittest.main()
