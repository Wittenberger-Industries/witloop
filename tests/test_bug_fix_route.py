"""Contract tests for the reproduce-first bug-fix overlay (independently loaded rules)."""
from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT = REPO_ROOT / "plugins" / "wit"
BUG_FIX = ROOT / "skills" / "dev" / "references" / "bug-fix.md"
BRAINSTORM = ROOT / "skills" / "brainstorm" / "SKILL.md"
RESEARCH = ROOT / "skills" / "research" / "SKILL.md"
BUILD = ROOT / "skills" / "build" / "SKILL.md"
WORKFLOW = ROOT / "references" / "workflow.md"

PLUGIN_BUG_FIX = "${PLUGIN_ROOT}/skills/dev/references/bug-fix.md"
OPENED = "design gate opened"
BYPASS_STAMP = "design gate bypassed (narrow-fix)"
AUTO_STAMP = "design gate auto-approved (--auto)"
APPROVED_STAMP = "design gate approved"
PHASE_ORDER = (
    "Phase order: brainstorm repro, research debug, plan+checker, "
    "then gate/bypass, then build."
)
SKIP_CONTRACT = (
    "never for feature; bug-fix only when the narrow-fix predicate "
    "and audit stamp are recorded"
)
PREDICATE_CONJUNCTS = (
    "Work type exactly bug-fix",
    "Root cause from runtime evidence",
    "Public behavior unchanged",
    "Architecture unchanged",
    "Blast radius = files tasks.md names",
    "Plan-mode checker has no BLOCKER",
    "Smallest evidence-backed fix",
)
GATE_BYPASS_FIELDS = (
    "**Status:** narrow-fix",
    "**Public behavior unchanged:**",
    "**Architecture unchanged:**",
    "**Root cause:**",
    "**Why skip:**",
    "**Checker (plan mode):**",
    "**Surface:**",
)


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


class BugFixReferenceLoadTests(unittest.TestCase):
    def test_bug_fix_is_okf_reference_and_decides_alone(self):
        text = load(BUG_FIX)
        self.assertTrue(text.startswith("---\n"))
        self.assertIn("type: Reference", frontmatter(text))
        self.assertIn("Load when Work type is bug-fix", text)
        self.assertIn("This file is enough to decide when loaded alone", text)
        self.assertIn("missing Work type", text)
        self.assertIn("today's loop", text)
        self.assertIn("never consult Gate bypass", text)

    def test_feature_and_missing_work_type_are_feature_default(self):
        text = load(BUG_FIX)
        self.assertIn("Feature / missing Work type = today's loop", text)
        self.assertIn("missing Work type = feature", text)
        self.assertIn("never `feature`", text)

    def test_brainstorm_repro_contract_fields(self):
        text = load(BUG_FIX)
        self.assertIn("## Repro contract", text)
        self.assertIn("**Surface:**", text)
        self.assertIn("**Trigger:**", text)
        self.assertIn("Observed", text)
        self.assertIn("expected", text.lower())
        self.assertIn("**Force strategy**", text)
        self.assertIn("four must-asks", text)
        self.assertIn("Brainstorm never skipped", text)
        self.assertIn("superpowers:brainstorming", text)

    def test_research_debug_before_fan_out(self):
        text = load(BUG_FIX)
        self.assertIn("before approach fan-out", text)
        self.assertIn("systematic-debugging", text)
        self.assertIn(
            "debug via superpowers:systematic-debugging",
            text,
        )
        self.assertIn(
            "debug via wit fallback (systematic-debugging absent)",
            text,
        )
        self.assertIn("research/repro.md", text)
        self.assertIn(".logs/repro-before.txt", text)
        self.assertIn("`repro failed on <surface>`", text)
        self.assertIn("`repro passed on <surface>`", text)
        self.assertIn("THE SAME surface string", text)
        self.assertIn("does not enter build", text)

    def test_plan_and_checker_always_run(self):
        text = load(BUG_FIX)
        self.assertIn("Plan + plan-mode checker ALWAYS run", text)
        self.assertIn("Narrow plans small", text)
        self.assertIn("First Verify is the Surface", text)


class PredicateConjunctTests(unittest.TestCase):
    def test_every_predicate_conjunct_is_named(self):
        text = load(BUG_FIX)
        self.assertIn("FAIL-CLOSED", text)
        self.assertIn("any missing field = false", text)
        self.assertIn("All must be true", text)
        for name in PREDICATE_CONJUNCTS:
            with self.subTest(conjunct=name):
                self.assertIn(name, text)

    def test_bypass_refused_when_any_conjunct_missing(self):
        text = load(BUG_FIX)
        self.assertIn("Bypass is refused when any conjunct is missing", text)
        self.assertIn("any missing field = false", text)
        for name in PREDICATE_CONJUNCTS:
            with self.subTest(conjunct=name):
                self.assertIn(name, text)
                self.assertIn("All must be true", text)
        self.assertIn("never `feature`", text)
        self.assertIn("never missing", text)
        self.assertIn("WARNING", text)
        self.assertIn("copied into the bypass block", text)

    def test_work_type_feature_never_satisfies_predicate(self):
        text = load(BUG_FIX)
        self.assertIn("Work type exactly bug-fix (never feature, never missing)", text)


class StampAndBypassBlockTests(unittest.TestCase):
    def test_bypass_stamp_distinct_from_auto(self):
        text = load(BUG_FIX)
        self.assertIn(BYPASS_STAMP, text)
        self.assertIn(AUTO_STAMP, text)
        self.assertIn("NEVER reuse `design gate auto-approved (--auto)`", text)
        self.assertIn("`--auto` stays separate", text)
        self.assertNotEqual(BYPASS_STAMP, AUTO_STAMP)
        self.assertNotIn(
            "design gate auto-approved (--auto), phase = build` for a narrow-fix",
            text,
        )

    def test_design_gate_opened_before_bypass(self):
        text = load(BUG_FIX)
        self.assertIn("Always stamp `design gate opened` first", text)
        opened_at = text.index("Always stamp `design gate opened` first")
        bypass_at = text.index(
            "design gate bypassed (narrow-fix): <one-line reason>, phase = build"
        )
        self.assertLess(opened_at, bypass_at)
        self.assertIn("do not ask", text)

    def test_gate_bypass_block_fields(self):
        text = load(BUG_FIX)
        self.assertIn("## Gate bypass", text)
        for field in GATE_BYPASS_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, text)

    def test_same_surface_and_regression_rule(self):
        text = load(BUG_FIX)
        self.assertIn("Same-surface fail then pass", text)
        self.assertIn(".logs/repro-after.txt", text)
        self.assertIn("regression test", text.lower())
        self.assertIn("impractical", text.lower())
        self.assertIn("spec.md", text)

    def test_phase_ordering(self):
        text = load(BUG_FIX)
        self.assertIn(PHASE_ORDER, text)
        start = text.index(PHASE_ORDER)
        self.assertGreaterEqual(start, 0)

    def test_reopen_path_when_architecture_or_public_contract_changes(self):
        text = load(BUG_FIX)
        self.assertIn("revoke the bypass", text)
        self.assertIn("reopen the existing design gate", text)
        self.assertIn("architecture", text.lower())
        self.assertIn("public-contract", text)

    def test_predicate_fail_under_auto_keeps_auto_path(self):
        text = load(BUG_FIX)
        self.assertIn(
            "If the predicate fails under `--auto`, keep today's auto-approve path",
            text,
        )


class BrainstormIndependentlyLoadedTests(unittest.TestCase):
    def test_bug_fix_repro_contract_pointer(self):
        text = load(BRAINSTORM)
        self.assertIn("Work type is bug-fix", text)
        self.assertIn(PLUGIN_BUG_FIX, text)
        self.assertIn("repro contract", text.lower())
        self.assertIn("superpowers:brainstorming", text)

    def test_feature_path_unchanged_and_never_consults_bypass(self):
        text = load(BRAINSTORM)
        self.assertIn("Feature path unchanged", text)
        self.assertIn("**Scope**", text)
        self.assertIn("**Behavior**", text)
        self.assertIn("**Acceptance**", text)
        self.assertIn("**Hard constraints**", text)
        self.assertIn("never skipped", text.lower())
        self.assertIn("missing Work type", text)
        self.assertIn("never consult Gate bypass", text)


class ResearchIndependentlyLoadedTests(unittest.TestCase):
    def test_evidence_step_always_plan_checker_and_opened_before_bypass(self):
        text = load(RESEARCH)
        self.assertIn("Work type is bug-fix", text)
        self.assertIn(PLUGIN_BUG_FIX, text)
        self.assertIn("before approach fan-out", text)
        self.assertIn("systematic-debugging", text)
        self.assertIn("plan-mode checker", text)
        self.assertIn("Always stamp `design gate opened` first", text)
        self.assertIn(BYPASS_STAMP, text)
        self.assertIn(AUTO_STAMP, text)
        self.assertIn(APPROVED_STAMP, text)
        self.assertIn("`--auto` stays separate", text)
        opened_at = text.index("Always stamp `design gate opened` first")
        bypass_at = text.index(BYPASS_STAMP)
        self.assertLess(opened_at, bypass_at)

    def test_keeps_existing_approve_and_auto_wording(self):
        text = load(RESEARCH)
        self.assertIn(
            "design gate approved, phase = build",
            text,
        )
        self.assertIn(
            "design gate auto-approved (--auto), phase = build",
            text,
        )
        self.assertIn(
            "If the predicate fails under `--auto`, keep today's auto-approve path",
            text,
        )
        self.assertIn("NEVER reuse `design gate auto-approved (--auto)`", text)

    def test_feature_never_consults_gate_bypass(self):
        text = load(RESEARCH)
        self.assertIn("missing Work type = feature", text)
        self.assertIn("never consult Gate bypass", text)


class BuildIndependentlyLoadedTests(unittest.TestCase):
    def test_precondition_accepts_narrow_fix_bypass(self):
        text = load(BUILD)
        self.assertIn("tasks.md", text)
        self.assertIn("Work type bug-fix", text)
        self.assertIn("## Gate bypass", text)
        self.assertIn("Status narrow-fix", text)
        self.assertIn(BYPASS_STAMP, text)
        self.assertIn("auto-approve", text)
        self.assertIn("Refuse to build without it", text)

    def test_same_surface_after_proof(self):
        text = load(BUILD)
        self.assertIn("`repro passed on <surface>`", text)
        self.assertIn("same", text.lower())
        self.assertIn(".logs/repro-after.txt", text)

    def test_revoke_and_reopen_on_architecture_or_public_contract_change(self):
        text = load(BUILD)
        self.assertIn("revoke the bypass", text)
        self.assertIn("reopen the existing design gate", text)
        self.assertIn("architecture", text.lower())
        self.assertIn("public-contract", text)

    def test_missing_work_type_is_feature_and_refuses_bypass(self):
        text = load(BUILD)
        self.assertIn("missing Work type = feature", text)
        self.assertIn("refuse bypass", text.lower())


class WorkflowIndependentlyLoadedTests(unittest.TestCase):
    def test_design_gate_skip_contract(self):
        text = load(WORKFLOW)
        self.assertIn(SKIP_CONTRACT, text)
        self.assertIn("Feature never bypasses", text)
        self.assertIn("Two gates, both deliberate", text)
        self.assertIn("/wit:dev --auto", text)

    def test_feature_never_skip_and_rule_two_stays(self):
        text = load(WORKFLOW)
        self.assertIn("never for feature", text)
        self.assertIn("Rule 2 stays for feature", text)
        self.assertIn("Two gates, both deliberate", text)
        self.assertNotIn("May skip when | never\n", text)


class FeatureCompatibilityTests(unittest.TestCase):
    def test_missing_work_type_is_feature_across_overlay_files(self):
        for path in (BUG_FIX, BRAINSTORM, RESEARCH, BUILD, WORKFLOW):
            with self.subTest(path=path.name):
                text = load(path)
                self.assertIn("missing Work type", text)
                if path is WORKFLOW:
                    self.assertIn("never for feature", text)
                else:
                    self.assertIn("feature", text.lower())

    def test_workflow_never_skip_for_feature(self):
        text = load(WORKFLOW)
        self.assertIn("never for feature", text)
        self.assertIn("Feature never bypasses", text)


class HygieneTests(unittest.TestCase):
    def test_this_module_does_not_import_validate(self):
        this = Path(__file__).read_text(encoding="utf-8")
        self.assertNotRegex(this, r"(?m)^(?:import validate|from validate import)")

    def test_does_not_require_checker_charter_edits(self):
        loaded = (BUG_FIX, BRAINSTORM, RESEARCH, BUILD, WORKFLOW)
        self.assertEqual(len(loaded), 5)
        self.assertTrue(all(path.suffix == ".md" for path in loaded))
        self.assertTrue(all("agents" not in path.parts for path in loaded))


if __name__ == "__main__":
    unittest.main()
