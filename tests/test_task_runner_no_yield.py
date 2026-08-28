"""Contract tests: task-runners never yield to the user; build continues the DAG.

Independently loads charter, build skill, skeleton, host adapters, and design notes as text.
Does not import other repo modules (several run checks on import).
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HAS_DOCS = (ROOT / "docs").is_dir()
RUNNER = ROOT / "agents" / "wit-task-runner.md"
RUNNER_NOTES = ROOT / "docs" / "design-notes" / "wit-task-runner.md"
BUILD = ROOT / "skills" / "build" / "SKILL.md"
BUILD_NOTES = ROOT / "docs" / "design-notes" / "build.md"
SKELETON = ROOT / "skills" / "build" / "references" / "worktrees-and-subagents.md"
GROK = ROOT / "references" / "grok-tools.md"
CURSOR = ROOT / "references" / "cursor-tools.md"
MODELS = ROOT / "references" / "models.md"
EM_DASH = "\u2014"
TOOLS_LINE = 'tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]'
COMPLETE = "## TASK COMPLETE"
BLOCKED = "## TASK BLOCKED"
AUTH = "## TASK AUTH-GATE"


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


def skeleton_block(text: str) -> str:
    start = text.find("### Task-runner prompt skeleton")
    if start < 0:
        raise AssertionError("missing Task-runner prompt skeleton")
    end = text.find("### Parallel dispatch", start)
    if end < 0:
        raise AssertionError("missing Parallel dispatch after skeleton")
    return text[start:end]


class RunnerPreservedContractTests(unittest.TestCase):
    def test_tools_list_unchanged(self):
        fm = frontmatter(load(RUNNER))
        self.assertIn(TOOLS_LINE, fm)
        listed = re.search(r"tools:\s*\[([^\]]*)\]", fm)
        self.assertIsNotNone(listed)
        tools = [t.strip().strip('"').strip("'") for t in listed.group(1).split(",")]
        self.assertEqual(tools, ["Read", "Write", "Edit", "Bash", "Grep", "Glob"])

    def test_report_cap_self_check_no_commit_no_progress(self):
        text = load(RUNNER)
        self.assertIn("~15 lines", text)
        self.assertIn("Self-Check: PASS", text)
        self.assertIn("Don't commit", text)
        self.assertIn("progress.md", text)
        self.assertRegex(text, r"do \*\*not\*\* touch `progress.md`")

    def test_three_attempt_cap_and_auth_gate_and_landmines(self):
        text = load(RUNNER)
        self.assertIn("Cap auto-fix attempts at 3", text)
        self.assertIn(AUTH, text)
        self.assertIn("No `git stash`", text)
        self.assertIn("No `git clean`", text)


class RunnerNoYieldTests(unittest.TestCase):
    def test_stop_and_ask_retired_architecture_is_task_blocked(self):
        text = load(RUNNER)
        self.assertNotIn("STOP and ask", text)
        self.assertIn(BLOCKED, text)
        self.assertRegex(text, r"(?i)architectural")
        self.assertIn("Notes", text)
        self.assertIn("Never address the user", text)

    def test_every_generation_ends_on_exactly_one_marker(self):
        text = load(RUNNER)
        self.assertIn("Every generation ends on a last-line marker", text)
        self.assertIn("exactly one of", text.lower())
        for marker in (COMPLETE, BLOCKED, AUTH):
            self.assertIn(marker, text)
        self.assertIn("let me know if you want me to continue", text)

    def test_complete_requires_verify_this_generation(self):
        text = load(RUNNER)
        self.assertIn("If Verify has not run in this generation", text)
        self.assertIn(BLOCKED, text)
        self.assertIn(AUTH, text)
        self.assertRegex(
            text,
            r"only `%s` or `%s`" % (re.escape(BLOCKED), re.escape(AUTH)),
        )

    def test_failed_verify_is_not_a_user_prompt(self):
        text = load(RUNNER)
        self.assertIn("A failed Verify is not a user prompt", text)
        self.assertIn(BLOCKED, text)
        self.assertIn("Cap auto-fix attempts at 3", text)

    def test_auth_gate_is_the_only_human_pause(self):
        text = load(RUNNER)
        self.assertIn("only allowed pause for a human", text)
        self.assertIn(AUTH, text)

    def test_no_em_dash(self):
        self.assertNotIn(EM_DASH, load(RUNNER))


class BuildNoYieldTests(unittest.TestCase):
    def test_same_turn_tick_commit_dispatch_no_wrap_up(self):
        text = load(BUILD)
        self.assertIn("No yield while the DAG has work", text)
        self.assertIn("this same turn", text)
        self.assertIn("Do not write a user-facing wrap-up", text)
        self.assertIn("dispatch the next ready set", text)

    def test_do_not_background_or_end_turn_except_auth_or_gate(self):
        text = load(BUILD)
        self.assertIn("Do not background a `wit-task-runner`", text)
        self.assertIn(
            "Do not end the parent turn while `tasks.md` still has unticked items",
            text,
        )
        self.assertIn(AUTH, text)
        self.assertIn("AskQuestion", text)

    def test_grok_pull_at_wave_gate(self):
        text = load(BUILD)
        self.assertIn("get_command_or_subagent_output", text)
        self.assertRegex(text, r"(?i)Host grok")
        self.assertRegex(text, r"(?i)wave gate")

    def test_no_em_dash(self):
        self.assertNotIn(EM_DASH, load(BUILD))


class SkeletonNoYieldTests(unittest.TestCase):
    def test_skeleton_requires_last_line_markers_and_no_user_address(self):
        block = skeleton_block(load(SKELETON))
        for marker in (COMPLETE, BLOCKED, AUTH):
            self.assertIn(marker, block)
        self.assertRegex(block, r"(?i)never address the user")
        self.assertIn("failed Verify", block)
        self.assertNotIn("STOP and ask", block)

    def test_no_em_dash(self):
        self.assertNotIn(EM_DASH, load(SKELETON))


class HostAdapterNoYieldTests(unittest.TestCase):
    def test_grok_no_background_pull_at_wave_gate(self):
        text = load(GROK)
        self.assertIn("background: true", text)
        self.assertIn("get_command_or_subagent_output", text)
        self.assertRegex(text, r"(?i)wave gate")
        self.assertIn("wit-task-runner", text)
        self.assertNotIn(EM_DASH, text)

    def test_cursor_no_run_in_background_on_task_runner(self):
        text = load(CURSOR)
        self.assertIn("run_in_background", text)
        self.assertIn("wit-task-runner", text)
        self.assertNotIn(EM_DASH, text)

    def test_models_cites_task_blocked_not_stop_and_ask(self):
        text = load(MODELS)
        self.assertIn(BLOCKED, text)
        self.assertNotIn("stop and ask", text)
        self.assertNotIn(EM_DASH, text)


@unittest.skipUnless(HAS_DOCS, "docs/ is local-only")
class DesignNotesNoYieldTests(unittest.TestCase):
    def test_runner_notes_retire_stop_and_ask(self):
        text = load(RUNNER_NOTES)
        self.assertIn(BLOCKED, text)
        self.assertRegex(text, r"(?i)every generation")
        self.assertNotIn(EM_DASH, text)

    def test_build_notes_why_no_yield_and_grok_pull(self):
        text = load(BUILD_NOTES)
        self.assertRegex(text, r"(?i)no yield")
        self.assertIn("get_command_or_subagent_output", text)
        self.assertNotIn(EM_DASH, text)


if __name__ == "__main__":
    unittest.main()
