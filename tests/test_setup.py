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
HAS_DOCS = (ROOT / "docs").is_dir()
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
README = ROOT / "README.md"
AGENTS = ROOT / "AGENTS.md"
GLOSSARY = ROOT / ".wit" / "glossary.md"
SCAN_ALIAS = ROOT / "references" / "skill-aliases" / "wit-scan" / "SKILL.md"
CURSOR_TOOLS = ROOT / "references" / "cursor-tools.md"
PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"
CODEX_PLUGIN = ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
SHIP = ROOT / "skills" / "ship" / "SKILL.md"
BUILD = ROOT / "skills" / "build" / "SKILL.md"
RESEARCH = ROOT / "skills" / "research" / "SKILL.md"
WIT_DIRECTORY = ROOT / "skills" / "research" / "references" / "wit-directory.md"
RPA_DIRECTORY = ROOT / "skills" / "rpa" / "references" / "rpa-directory.md"
CONSTITUTION_TEMPLATE = ROOT / "skills" / "scan" / "references" / "constitution-template.md"
RPA_CONSTITUTION_TEMPLATE = (
    ROOT / "skills" / "rpa" / "references" / "rpa-constitution-template.md"
)
VERIFICATION_GATE = ROOT / "skills" / "rpa" / "references" / "verification-gate.md"
BUILD_UIPATH = ROOT / "skills" / "rpa" / "references" / "build-uipath.md"
BUILD_MAESTRO = ROOT / "skills" / "rpa" / "references" / "build-maestro.md"
CHECK_TOKENS = ROOT / "skills" / "ship" / "scripts" / "check_tokens.py"
EM_DASH = "\u2014"
LEDGER_SKIP = re.compile(r"ledger:\s*`?skip`?")
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
LEDGER_OWNED = (
    SHIP,
    BUILD,
    RESEARCH,
    RPA,
    DEV,
    WIT_DIRECTORY,
    RPA_DIRECTORY,
    CONSTITUTION_TEMPLATE,
    RPA_CONSTITUTION_TEMPLATE,
    VERIFICATION_GATE,
    BUILD_UIPATH,
    BUILD_MAESTRO,
)


def load(path: Path) -> str:
    if not path.is_file():
        raise AssertionError("%s is missing" % path.relative_to(ROOT))
    return path.read_text(encoding="utf-8")


def skip_near(text: str, needle: str, window: int = 800) -> bool:
    skip = r"ledger:\s*`?skip`?"
    escaped = re.escape(needle)
    flags = re.DOTALL | re.IGNORECASE
    return bool(
        re.search(skip + r".{0,%d}%s" % (window, escaped), text, flags)
        or re.search(escaped + r".{0,%d}%s" % (window, skip), text, flags)
    )


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

    def test_interactive_models_write_omits_token_ledger_until_step_7(self):
        text = load(SETUP)
        self.assertIn("omits", text)
        self.assertIn("## Token ledger", text)
        models = load(MODELS)
        self.assertIn("without", models)
        self.assertIn("## Token ledger", models)

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
            if not path.is_file():
                continue
            text = load(path)
            self.assertNotIn(EM_DASH, text, path)


class SetupDesignNotesTests(unittest.TestCase):
    @unittest.skipUnless(HAS_DOCS, "docs/ is local-only")
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

    @unittest.skipUnless(HAS_DOCS, "docs/ is local-only")
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
            if not path.is_file():
                continue
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

    def test_plugin_bootstrap_offer_runs_on_first_setup(self):
        text = load(PLUGIN_BOOTSTRAP)
        self.assertIn("On first setup", text)
        self.assertNotIn("On first scan", text)

    def test_host_maps_attribute_alias_copy_to_setup_bootstrap(self):
        for path in (GROK_TOOLS, COPILOT_TOOLS, CODEX_TOOLS):
            text = load(path)
            self.assertNotIn("scan's bootstrap", text, path)
            self.assertIn("setup's bootstrap", text)

    def test_copilot_invoke_list_includes_setup(self):
        self.assertIn("/wit setup", load(COPILOT_TOOLS))

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

    @unittest.skipUnless(HAS_DOCS, "docs/ is local-only")
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
            if not path.is_file():
                continue
            text = load(path)
            self.assertNotIn(EM_DASH, text, path)


class LedgerSkipTests(unittest.TestCase):
    def test_research_build_skip_no_init_no_append(self):
        for path in (RESEARCH, BUILD):
            text = load(path)
            self.assertRegex(text, LEDGER_SKIP)
            self.assertTrue(skip_near(text, "--init"), path)
            self.assertRegex(text, r"(?i)do not(?: run)? `--init`")
            self.assertRegex(text, r"(?i)do not append")

    def test_ship_skip_no_finalize_table_or_check_tokens_gate(self):
        text = load(SHIP)
        self.assertRegex(text, LEDGER_SKIP)
        self.assertTrue(skip_near(text, "finalize_tokens.py"))
        self.assertTrue(skip_near(text, "check_tokens.py"))
        self.assertRegex(text, r"(?i)do not run.*finalize_tokens")
        self.assertRegex(text, r"(?i)omit the \*\*token table\*\*")
        self.assertIn("autonomous total", text)
        self.assertIn("Σ subagent compute", text)
        self.assertRegex(text, r"(?i)omit the two tokens\.md-sourced timing lines")
        self.assertRegex(text, r"(?i)(?:omit|n/a).{0,80}checkbox|checkbox.{0,80}(?:omit|n/a)")
        self.assertRegex(text, r"(?i)do not call the script")
        self.assertRegex(text, r"(?i)keep-alive must not wait")
        self.assertRegex(text, r"six files")

    def test_dev_token_table_only_when_ledger_on(self):
        text = load(DEV)
        self.assertRegex(text, r"token table only when `ledger: on`")

    def test_rpa_skill_skip_no_init_report_not_gate(self):
        text = load(RPA)
        self.assertRegex(text, LEDGER_SKIP)
        self.assertTrue(skip_near(text, "--init"))
        self.assertTrue(skip_near(text, "check_tokens.py"))
        self.assertRegex(text, r"(?i)do not(?: run)? `--init`")
        self.assertRegex(text, r"(?i)do not append")
        self.assertRegex(text, r"(?i)not mandatory")
        self.assertRegex(text, r"(?i)not a gate")

    def test_wit_directory_seven_on_six_skip_keeps_tokens_heading(self):
        text = load(WIT_DIRECTORY)
        self.assertIn("## `tokens.md` template", text)
        self.assertIn("seven-file dossier", text)
        self.assertRegex(text, r"six files")
        self.assertIn("drop `tokens.md`", text)
        self.assertIn("present when ledger is on", text)
        self.assertRegex(
            text,
            r"check_tokens\.py `--init`.{0,80}research:0.{0,40}when ledger is on",
        )

    def test_resolved_routing_stamps_ledger_on_both_directory_templates(self):
        for path in (WIT_DIRECTORY, RPA_DIRECTORY):
            text = load(path)
            self.assertIn("· ledger: <on | skip>", text)

    def test_rpa_directory_omits_tokens_on_skip(self):
        text = load(RPA_DIRECTORY)
        self.assertRegex(text, LEDGER_SKIP)
        self.assertRegex(text, r"(?i)omits `tokens\.md`")

    def test_verification_gate_carves_out_check_tokens_when_skip(self):
        text = load(VERIFICATION_GATE)
        self.assertIn("passes `check_tokens.py`", text)
        self.assertRegex(text, LEDGER_SKIP)
        self.assertRegex(text, r"(?i)does not apply")

    def test_rpa_build_refs_carve_out_mandatory_and_init(self):
        for path in (BUILD_UIPATH, BUILD_MAESTRO):
            text = load(path)
            self.assertIn("tokens.md` is **mandatory**", text)
            self.assertRegex(text, LEDGER_SKIP)
            self.assertTrue(skip_near(text, "--init"), path)
            self.assertRegex(text, r"(?i)do not(?: run)? `--init`")

    def test_rpa_constitution_template_carves_out_skip(self):
        text = load(RPA_CONSTITUTION_TEMPLATE)
        self.assertIn("passes `check_tokens.py`", text)
        self.assertRegex(text, LEDGER_SKIP)

    def test_scan_constitution_template_has_no_skip_rule(self):
        text = load(CONSTITUTION_TEMPLATE)
        self.assertNotRegex(text, LEDGER_SKIP)
        self.assertNotIn("## Token ledger", text)
        self.assertNotIn("what `scan` detected", text)
        self.assertIn("what `setup` detected", text)

    def test_wit_directory_retargets_scan_off_first_run(self):
        text = load(WIT_DIRECTORY)
        self.assertNotIn("Written once by scan", text)
        self.assertIn("Written once by setup", text)
        self.assertNotIn("seeded by a greenfield scan", text)

    def test_fail_closed_missing_stamp_and_no_mid_run_toggle(self):
        text = load(WIT_DIRECTORY)
        self.assertRegex(text, r"(?i)exact `skip`")
        self.assertRegex(text, r"(?i)fail-clos")
        self.assertRegex(text, r"(?i)missing `ledger:`")
        self.assertRegex(text, r"(?i)mid-run toggle")

    def test_honor_reads_stamp_does_not_reopen_models_at_append(self):
        for path in (RESEARCH, BUILD, SHIP, RPA):
            text = load(path)
            self.assertIn("· ledger:", text)
            self.assertRegex(text, r"(?i)do not re-open `.wit/models.md`")
            self.assertRegex(text, r"(?i)missing `ledger:`")

    def test_check_tokens_stays_format_only_no_skip_flag(self):
        text = load(CHECK_TOKENS)
        self.assertNotIn("--skip", text)
        self.assertNotIn("skip", text.lower())
        self.assertIn("--init", text)
        self.assertIn("add_argument", text)

    def test_no_em_dashes_in_owned_files(self):
        for path in LEDGER_OWNED:
            text = load(path)
            self.assertNotIn(EM_DASH, text, path)


class AdvertisedScanRetargetTests(unittest.TestCase):
    def test_readme_scan_row_is_refresh_only(self):
        text = load(README)
        table = "\n".join(
            line for line in text.splitlines() if line.startswith("| **`/wit:")
        )
        scan_row = next(line for line in table.splitlines() if "/wit:scan" in line)
        self.assertNotIn("bootstraps", scan_row)
        self.assertIn("Refresh-only", scan_row)
        self.assertIn("setup", scan_row)

    def test_wit_scan_alias_is_refresh_not_bootstrap(self):
        fm = frontmatter(load(SCAN_ALIAS))
        self.assertIn("refresh", fm.lower())
        self.assertNotIn("bootstrap wit in", fm.lower())

    def test_manifests_say_scan_refreshes_not_bootstraps(self):
        for path in (PLUGIN_JSON, CODEX_PLUGIN, MARKETPLACE):
            text = load(path)
            self.assertNotIn("documents and bootstraps", text, path)
            self.assertIn("refreshes the map", text)

    def test_glossary_setup_tell_is_missing_repo_map(self):
        text = load(GLOSSARY)
        self.assertIn("repo-map.md", text)
        self.assertNotIn("Missing `.wit/` at scan", text)

    def test_dev_preflight_and_ship_point_at_setup_not_scan(self):
        self.assertIn("setup's guided setup", load(DEV))
        self.assertNotIn("scan's guided setup", load(DEV))
        ship = load(SHIP)
        self.assertIn("setup's template", ship)
        self.assertNotIn("scan's template", ship)

    def test_agents_and_readme_alias_copy_is_setup_bootstrap(self):
        self.assertIn("setup's bootstrap", load(AGENTS))
        self.assertNotIn("scan's bootstrap", load(AGENTS))
        self.assertIn("after setup copies aliases", load(README))

    def test_cursor_stamp_list_includes_setup(self):
        text = load(CURSOR_TOOLS)
        self.assertIn("setup / scan / dev / rpa", text)

    def test_wit_directory_tree_attributes_docs_to_setup(self):
        text = load(WIT_DIRECTORY)
        self.assertIn("(setup; absent for greenfield)", text)
        self.assertIn("(setup; kept current by ship's docs-sync)", text)


if __name__ == "__main__":
    unittest.main()

