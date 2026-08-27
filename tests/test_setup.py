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
SCAN = ROOT / "skills" / "scan" / "SKILL.md"
SCAN_NOTES = ROOT / "docs" / "design-notes" / "scan.md"
CAPABILITIES = ROOT / "references" / "capabilities.md"
WORKFLOW = ROOT / "references" / "workflow.md"
INTEGRATIONS = ROOT / "skills" / "research" / "references" / "integrations.md"
ADD_ISSUES = ROOT / "skills" / "add-issues" / "SKILL.md"
ARCHITECTURE = ROOT / ".wit" / "architecture.md"
SETUP_ALIAS = ROOT / "references" / "skill-aliases" / "wit-setup" / "SKILL.md"
PLUGIN_BOOTSTRAP = ROOT / "skills" / "scan" / "references" / "plugin-bootstrap.md"
GROK_TOOLS = ROOT / "references" / "grok-tools.md"
COPILOT_TOOLS = ROOT / "references" / "copilot-tools.md"
CODEX_TOOLS = ROOT / "references" / "codex-tools.md"
DEV = ROOT / "skills" / "dev" / "SKILL.md"
RPA = ROOT / "skills" / "rpa" / "SKILL.md"
INVESTIGATION = ROOT / "skills" / "dev" / "references" / "investigation.md"
MODELS = ROOT / "references" / "models.md"
DEV_NOTES = ROOT / "docs" / "design-notes" / "dev.md"
RPA_NOTES = ROOT / "docs" / "design-notes" / "rpa.md"
EM_DASH = "\u2014"
RUNTIME_NEVER = re.compile(
    r"runtime never reads this file|never loaded at runtime",
    re.IGNORECASE,
)

OWNED = (SETUP, SETUP_NOTES)
SCAN_OWNED = (
    SCAN,
    SCAN_NOTES,
    WORKFLOW,
    CAPABILITIES,
    INTEGRATIONS,
    ADD_ISSUES,
)
ALIAS_OWNED = (
    SETUP_ALIAS,
    PLUGIN_BOOTSTRAP,
    GROK_TOOLS,
    COPILOT_TOOLS,
    CODEX_TOOLS,
)
INVOKE_OWNED = (
    DEV,
    RPA,
    INVESTIGATION,
    MODELS,
    DEV_NOTES,
    RPA_NOTES,
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


class ScanRefreshTests(unittest.TestCase):
    def test_description_is_refresh_only_not_from_scratch_bootstrap(self):
        fm = frontmatter(load(SCAN))
        self.assertIn("/wit:scan", fm)
        self.assertIn("--refresh", fm)
        self.assertNotIn("bootstrap", fm.lower())
        self.assertNotIn("from scratch", fm.lower())
        self.assertNotIn("set up wit here", fm)
        self.assertNotIn("document this codebase", fm)

    def test_bare_invoke_is_silent_refresh_abc(self):
        text = load(SCAN)
        self.assertRegex(text, r"silent `--refresh`")
        self.assertIn("### A", text)
        self.assertIn("### B", text)
        self.assertIn("### C", text)
        self.assertIn("chore(wit): scan refresh", text)

    def test_missing_repo_map_runs_setup_no_tell_redoc_or_chain(self):
        text = load(SCAN)
        self.assertRegex(text, r"(?i)\*\*run setup\*\*")
        self.assertRegex(text, r"(?i)do not merely tell")
        self.assertRegex(text, r"(?i)do not re-document")
        self.assertRegex(text, r"(?i)do not chain a refresh")
        self.assertNotIn("this IS a first scan", text)
        self.assertNotIn("run the full procedure", text)
        self.assertNotIn("Two jobs", text)
        self.assertNotIn("## `repo-map.md` template", text)
        self.assertNotIn("## `overview.md` template", text)
        self.assertNotIn("## `architecture.md` template", text)

    def test_mermaid_traps_live_in_refresh_body(self):
        text = load(SCAN)
        self.assertNotIn("rules above", text)
        self.assertIn("check_mermaid.py", text)
        self.assertIn("never use a mermaid reserved word as an ID", text)
        self.assertIn("graph", text)
        self.assertIn("subgraph", text)

    def test_design_notes_are_refresh_not_first_run(self):
        text = load(SCAN_NOTES)
        self.assertRegex(text, RUNTIME_NEVER)
        self.assertIn("skills/scan/SKILL.md", text)
        self.assertNotIn("one-time groundwork so `/wit:dev`", text)
        self.assertIn("silent `--refresh`", text)
        self.assertRegex(text, r"(?i)run setup")

    def test_workflow_retargets_scan_off_first_run(self):
        text = load(WORKFLOW)
        self.assertNotIn("scan (once, project-level)", text)
        self.assertNotRegex(text, r"\| scan \| scan \| one-time \|")
        self.assertIn("setup (once, project-level)", text)
        self.assertIn("scan (refresh)", text)

    def test_capabilities_entry_includes_setup(self):
        text = load(CAPABILITIES)
        self.assertIn("setup / scan / dev / rpa", text)
        self.assertIn("skills/scan/SKILL.md", text)
        self.assertNotIn("skills/setup/SKILL.md", text)

    def test_integrations_and_add_issues_retarget_bootstrap_off_scan(self):
        integ = load(INTEGRATIONS)
        self.assertNotRegex(integ, r"(?i)`scan` offers to install")
        self.assertRegex(integ, r"(?i)`setup` offers to install")
        self.assertNotRegex(integ, r"(?i)When `scan` flags a frontend")
        self.assertRegex(integ, r"(?i)When `setup` flags a frontend")
        self.assertNotRegex(integ, r"whatever `scan` recorded")
        self.assertRegex(integ, r"whatever `setup` recorded")
        issues = load(ADD_ISSUES)
        self.assertNotIn("scan only seeds that on greenfield", issues)
        self.assertIn("setup only seeds that on greenfield", issues)

    def test_no_em_dashes_in_owned_files(self):
        for path in SCAN_OWNED:
            text = load(path)
            self.assertNotIn(EM_DASH, text, path)


class SetupAliasTests(unittest.TestCase):
    def test_wit_setup_forwarder_exists_and_passes_auto(self):
        text = load(SETUP_ALIAS)
        fm = frontmatter(text)
        self.assertIn("type: Skill", fm)
        self.assertRegex(fm, r"(?m)^name:\s*wit-setup\s*$")
        self.assertIn("/wit-setup", text)
        self.assertIn("$wit-setup", text)
        self.assertIn("skills/setup/SKILL.md", text)
        self.assertIn("--auto", text)
        self.assertRegex(text, r"passing `--auto`")

    def test_alias_description_forwards_to_setup_not_bootstrap_a_folder(self):
        fm = frontmatter(load(SETUP_ALIAS))
        self.assertIn("setup entry point", fm)
        self.assertNotIn("bootstrap a folder", fm.lower())
        self.assertNotIn("scan entry point", fm)

    def test_plugin_bootstrap_copy_list_includes_wit_setup(self):
        text = load(PLUGIN_BOOTSTRAP)
        self.assertIn("wit-setup/", text)
        self.assertIn("/wit-setup", text)
        self.assertIn("$wit-setup", text)

    def test_host_maps_mention_wit_setup(self):
        self.assertIn("/wit-setup", load(COPILOT_TOOLS))
        self.assertIn("/wit-setup", load(GROK_TOOLS))
        self.assertIn("$wit-setup", load(CODEX_TOOLS))

    def test_grok_notes_branded_wit_setup_if_bare_setup_clashes(self):
        text = load(GROK_TOOLS)
        self.assertRegex(text, r"branded `/wit-setup`")
        self.assertRegex(text, r"bare `/setup`")
        self.assertRegex(text, r"(?i)clash")

    def test_no_em_dashes_in_owned_files(self):
        for path in ALIAS_OWNED:
            text = load(path)
            self.assertNotIn(EM_DASH, text, path)


class SetupInvokeTests(unittest.TestCase):
    def test_scan_dev_rpa_missing_repo_map_run_setup_first(self):
        scan = load(SCAN)
        self.assertRegex(scan, r"(?i)\*\*run setup\*\*")
        for path in (DEV, RPA):
            text = load(path)
            self.assertRegex(
                text,
                r"(?i)If `?\.wit/repo-map\.md`? is missing, run \*\*setup\*\* first",
            )
            self.assertRegex(text, r"forward `--auto`")
            self.assertRegex(text, r"(?i)then continue")
            self.assertNotRegex(
                text,
                r"(?i)If `?\.wit/repo-map\.md`? is missing, run \*\*scan\*\* first",
            )

    def test_add_issues_does_not_invoke_setup(self):
        text = load(ADD_ISSUES)
        self.assertNotRegex(text, r"(?i)\*\*run setup\*\*")
        self.assertNotRegex(text, r"(?i)run setup first")
        self.assertNotIn("skills/setup/SKILL.md", text)
        self.assertNotRegex(text, r"(?i)If `?\.wit/repo-map\.md`? is missing")

    def test_investigation_exits_before_setup(self):
        prelude = load(DEV)
        self.assertRegex(
            prelude,
            r"(?s)If the work type is `investigation`.+exit",
        )
        self.assertRegex(prelude, r"no host probe, setup")
        inv = load(INVESTIGATION)
        self.assertRegex(inv, r"(?i)do not run setup")
        self.assertNotRegex(inv, r"(?i)\*\*run setup\*\* first")

    def test_dev_and_rpa_drop_models_write_keep_resolve_once(self):
        for path in (DEV, RPA):
            text = load(path)
            self.assertNotRegex(text, r"(?i)Model routing first-run setup")
            self.assertNotIn("set up `.wit/models.md` if absent", text)
            self.assertIn("## Model routing (resolved)", text)
            self.assertRegex(text, r"(?i)resolve the routing once")
            self.assertNotRegex(
                text,
                r"(?i)write the file \*\*and commit it\*\*",
            )

    def test_models_first_run_is_setup_entry_with_auto_simple_and_ledger_on(self):
        text = load(MODELS)
        self.assertIn("## First-run setup (setup)", text)
        self.assertNotIn("## First-run setup (dev / rpa entry points)", text)
        start = text.find("## First-run setup")
        end = text.find("## Dispatch rule")
        self.assertGreaterEqual(start, 0)
        self.assertGreater(end, start)
        section = text[start:end]
        self.assertIn("--auto", section)
        self.assertIn("simple", section)
        self.assertIn("ledger | on", section)

    def test_token_ledger_heading_key_on_or_skip_absent_is_on(self):
        text = load(MODELS)
        self.assertIn("## Token ledger", text)
        self.assertRegex(text, r"(?m)^\|\s*ledger\s*\|")
        self.assertRegex(text, r"`on`\s*\|\s*`skip`")
        self.assertRegex(text, r"(?i)absent or not-exact-`skip` is `on`")

    def test_absent_models_with_map_runs_setup_models_ledger_slice_only(self):
        for path in (DEV, RPA):
            text = load(path)
            self.assertRegex(text, r"(?i)models\+ledger slice")
            self.assertRegex(text, r"(?i)slice only")

    def test_design_notes_sync_setup_first_and_resolve_once(self):
        dev = load(DEV_NOTES)
        self.assertRegex(dev, r"(?i)setup-first")
        self.assertNotIn("Why scan-first is a hard precondition", dev)
        self.assertIn("## Model routing (resolved)", dev)
        self.assertRegex(dev, r"(?i)models\+ledger")
        rpa = load(RPA_NOTES)
        self.assertRegex(rpa, r"(?i)run setup")
        self.assertRegex(rpa, r"(?i)repo-map")
        self.assertNotIn(
            "Why the first-run setup is a trigger plus a citation",
            rpa,
        )

    def test_no_em_dashes_in_owned_files(self):
        for path in INVOKE_OWNED:
            text = load(path)
            self.assertNotIn(EM_DASH, text, path)


if __name__ == "__main__":
    unittest.main()

