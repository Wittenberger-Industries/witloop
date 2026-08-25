"""Contract tests for user docs and maintainer design-notes on work-type routing.

Asserts README/AGENTS descriptions, four advertised commands, five hosts, and the
design-note ownership split. Frozen archives (docs/plans/, docs/specs/) are not
this feature's files; this module does not open them for writes.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
AGENTS = ROOT / "AGENTS.md"
DEV_NOTES = ROOT / "docs" / "design-notes" / "dev.md"
RESEARCH_NOTES = ROOT / "docs" / "design-notes" / "research.md"
BUILD_NOTES = ROOT / "docs" / "design-notes" / "build.md"
SHIP_NOTES = ROOT / "docs" / "design-notes" / "ship.md"
CHECKER_NOTES = ROOT / "docs" / "design-notes" / "wit-code-checker.md"

DOC_FILES = (
    README,
    AGENTS,
    DEV_NOTES,
    RESEARCH_NOTES,
    BUILD_NOTES,
    SHIP_NOTES,
    CHECKER_NOTES,
)
ADVERTISED = ("scan", "dev", "rpa", "add-issues")
HOSTS = ("Claude", "Codex", "Copilot", "Grok", "Cursor")
KIND = "--kind feature|bug-fix|investigation"
WORK_TYPES = ("feature", "bug-fix", "investigation")
BYPASS = "design gate bypassed (narrow-fix)"
RUNTIME_NEVER = re.compile(
    r"runtime never reads this file|never loaded at runtime",
    re.IGNORECASE,
)
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


def readme_command_table_slugs(text: str) -> list[str]:
    in_table = False
    slugs: list[str] = []
    for line in text.splitlines():
        if line.startswith("| Command"):
            in_table = True
            continue
        if not in_table:
            continue
        if not line.startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells:
            continue
        if set(cells[0].replace("-", "").replace(":", "")) == set():
            continue
        match = re.search(r"/wit:([a-z0-9-]+)", cells[0])
        if match:
            slugs.append(match.group(1))
    return slugs


class DocSetTests(unittest.TestCase):
    def test_files_are_only_the_listed_docs(self):
        expected = {
            "README.md",
            "AGENTS.md",
            "docs/design-notes/dev.md",
            "docs/design-notes/research.md",
            "docs/design-notes/build.md",
            "docs/design-notes/ship.md",
            "docs/design-notes/wit-code-checker.md",
        }
        got = {path.relative_to(ROOT).as_posix() for path in DOC_FILES}
        self.assertEqual(got, expected)
        for path in DOC_FILES:
            self.assertTrue(path.is_file(), path)

    def test_frozen_archives_are_not_this_features_files(self):
        src = Path(__file__).read_text(encoding="utf-8")
        self.assertIn("docs/plans/", src)
        self.assertIn("docs/specs/", src)
        for path in DOC_FILES:
            rel = path.relative_to(ROOT).as_posix()
            self.assertFalse(rel.startswith("docs/plans/"), rel)
            self.assertFalse(rel.startswith("docs/specs/"), rel)
        self.assertTrue((ROOT / "docs" / "plans").is_dir())
        self.assertTrue((ROOT / "docs" / "specs").is_dir())
        self.assertNotRegex(src, r"(?m)^\s*(DOC_FILES|README|AGENTS).*=.*docs/(plans|specs)")

    def test_no_em_dashes_in_owned_docs(self):
        for path in DOC_FILES:
            text = load(path)
            self.assertNotIn(EM_DASH, text, path)


class ReadmeUserDocsTests(unittest.TestCase):
    def test_four_advertised_commands_and_no_fifth(self):
        text = load(README)
        slugs = readme_command_table_slugs(text)
        self.assertEqual(tuple(slugs), ADVERTISED)
        self.assertEqual(len(slugs), 4)
        self.assertRegex(text, r"Only these four entry points")
        table = "\n".join(
            line
            for line in text.splitlines()
            if line.startswith("| **`/wit:")
        )
        self.assertNotIn("/wit:how", table)
        self.assertNotIn("/wit:investigate", table)

    def test_five_hosts_remain(self):
        text = load(README)
        for host in HOSTS:
            self.assertIn(host, text, host)
        self.assertIn("five hosts", text)

    def test_three_work_types_and_kind_flag(self):
        text = load(README)
        self.assertIn(KIND, text)
        for work_type in WORK_TYPES:
            self.assertIn(work_type, text, work_type)
        self.assertRegex(text, r"(?i)work types?")

    def test_investigation_is_read_only_cited_exit(self):
        text = load(README)
        lower = text.lower()
        self.assertIn("investigation", lower)
        self.assertIn("read-only", lower)
        self.assertIn("cited", lower)
        self.assertIn("dossier", lower)
        self.assertIn("keep-alive", lower)
        self.assertRegex(text, r"(?i)\bPR\b")
        self.assertRegex(
            text,
            r"(?i)no dossier.*(?:gate|keep-alive|PR)|investigation.*read-only",
        )

    def test_bug_fix_repro_same_surface_and_narrow_bypass(self):
        text = load(README)
        self.assertIn("bug-fix", text)
        self.assertRegex(text, r"(?i)repro")
        self.assertRegex(text, r"same-surface|same surface")
        self.assertRegex(text, r"fail-then-pass|fail then pass")
        self.assertIn(BYPASS, text)
        self.assertIn("--auto", text)
        self.assertRegex(text, r"(?i)auto-approve")
        self.assertRegex(
            text,
            r"(?i)(distinct|separate).{0,40}`?--auto`?|`?--auto`?.{0,40}(distinct|separate)",
        )

    def test_add_issues_is_where_to_file_a_bug(self):
        text = load(README)
        self.assertIn("/wit:add-issues", text)
        self.assertIn("file a bug", text.lower())
        add_row = next(
            line
            for line in text.splitlines()
            if "/wit:add-issues" in line and line.startswith("|")
        )
        self.assertRegex(add_row, r"(?i)bug")

    def test_auto_still_auto_approves_the_design_gate(self):
        text = load(README)
        self.assertIn("`--auto`", text)
        self.assertRegex(text, r"(?i)auto-approve the (design )?gate")


class AgentsBootstrapTests(unittest.TestCase):
    def test_four_user_facing_commands_wording(self):
        text = load(AGENTS)
        self.assertRegex(
            text,
            r"Only scan/dev/rpa/add-issues are user-facing",
        )
        for name in ADVERTISED:
            self.assertIn(name, text, name)
        table_slugs = readme_command_table_slugs(text)
        self.assertEqual(table_slugs, [], "AGENTS.md must not duplicate the README command table")

    def test_five_hosts_and_brief_work_type_routing(self):
        text = load(AGENTS)
        for host in HOSTS:
            self.assertIn(host, text, host)
        self.assertIn(KIND, text)
        for work_type in WORK_TYPES:
            self.assertIn(work_type, text, work_type)
        self.assertRegex(text, r"(?i)work types?")
        self.assertIn("read-only", text.lower())
        self.assertIn(BYPASS, text)
        self.assertIn("--auto", text)

    def test_add_issues_keeps_file_a_bug(self):
        text = load(AGENTS)
        self.assertIn("add-issues", text)
        self.assertIn("file a bug", text.lower())
        self.assertIn("GitHub issue", text)

    def test_agents_is_cross_platform_bootstrap(self):
        text = load(AGENTS)
        fm = frontmatter(text)
        self.assertIn("type: Bootstrap", fm)
        self.assertIn("cross-platform", text.lower())
        self.assertIn("README.md", text)


class DesignNoteOwnershipTests(unittest.TestCase):
    def test_design_notes_are_not_loaded_at_runtime(self):
        for path in (
            DEV_NOTES,
            RESEARCH_NOTES,
            BUILD_NOTES,
            SHIP_NOTES,
            CHECKER_NOTES,
        ):
            text = load(path)
            self.assertRegex(text, RUNTIME_NEVER, path)

    def test_dev_notes_why_prelude_and_semantic_judgment(self):
        text = load(DEV_NOTES)
        self.assertRegex(text, r"(?i)before write-capable setup")
        self.assertRegex(text, r"(?i)investigation exits")
        self.assertRegex(text, r"(?i)semantic")
        self.assertRegex(text, r"(?i)keyword")
        self.assertRegex(text, r"(?i)prelude")
        self.assertRegex(text, r"(?i)folder classifier")
        self.assertIn("work-types.md", text)
        self.assertIn("investigation.md", text)
        self.assertIn("skills/dev/SKILL.md", text)

    def test_research_notes_why_plan_checker_and_fail_closed_bypass(self):
        text = load(RESEARCH_NOTES)
        self.assertRegex(text, r"(?i)plan-mode checker")
        self.assertRegex(text, r"(?i)fail-closed|fail closed")
        self.assertIn("--auto", text)
        self.assertIn("design gate opened", text)
        self.assertIn(BYPASS, text)
        self.assertIn("bug-fix.md", text)
        self.assertIn("skills/research/SKILL.md", text)

    def test_build_notes_why_bypass_precondition_and_reopen(self):
        text = load(BUILD_NOTES)
        self.assertRegex(text, r"(?i)precondition")
        self.assertIn(BYPASS, text)
        self.assertRegex(text, r"(?i)architecture")
        self.assertRegex(text, r"(?i)reopen")
        self.assertRegex(text, r"missing Work type\s*=\s*feature")
        self.assertIn("skills/build/SKILL.md", text)

    def test_ship_notes_why_bug_fix_pr_evidence_and_conditional_inventory(self):
        text = load(SHIP_NOTES)
        self.assertRegex(text, r"(?i)bug-fix")
        self.assertRegex(text, r"(?i)root cause")
        self.assertRegex(text, r"(?i)smallest fix")
        self.assertRegex(text, r"same-surface|same named surface|same surface")
        self.assertRegex(text, r"(?i)Rules inventory")
        self.assertRegex(text, r"(?i)conditional")
        self.assertIn("skills/ship/SKILL.md", text)

    def test_checker_notes_why_additive_rows_markers_tools_unchanged(self):
        text = load(CHECKER_NOTES)
        self.assertRegex(text, r"(?i)additive")
        self.assertRegex(text, r"(?i)bug-fix")
        self.assertRegex(text, r"(?i)matrix")
        self.assertRegex(text, r"(?i)markers")
        self.assertRegex(text, r"(?i)tools")
        self.assertIn("agents/wit-code-checker.md", text)
        self.assertIn("## CHECK PASSED", text)
        self.assertIn("## ISSUES FOUND", text)


if __name__ == "__main__":
    unittest.main()
