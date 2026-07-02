import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "ship" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import moa_review  # noqa: E402


FULL_CONFIG = """---
type: MoA Config
title: MoA model assignments — demo
description: Per-role model assignments for wi-dispatched agents.
preset: smart
timestamp: 2026-07-02
---

# MoA model assignments

## Roles
| Role | Model | Notes |
|------|-------|-------|
| orchestrator | fable | informational — session model |
| execution | sonnet | default for wi-dispatched sub-agents |
| checker | inherit | goal-level checker agent |
| reviewer | gpt-5 | cross-provider code review |

## Reviewer provider
| Key | Value |
|-----|-------|
| provider | openai |
| base_url | https://api.openai.com/v1 |
| model | gpt-5 |
| api_key_env | OPENAI_API_KEY |
| review_points | at-finish |

## Per-agent overrides
| Agent | Model |
|-------|-------|
| wi-researcher | haiku |
"""

SIMPLE_CONFIG = """---
type: MoA Config
title: MoA model assignments — demo
description: Per-role model assignments for wi-dispatched agents.
preset: simple
timestamp: 2026-07-02
---

# MoA model assignments

## Roles
| Role | Model | Notes |
|------|-------|-------|
| orchestrator | opus | informational |
| execution | sonnet | default |
| checker | inherit | goal checker |
| reviewer | none | Simple preset — no MoA reviewer |
"""


class ParseConfigTest(unittest.TestCase):
    def test_roles_parsed(self):
        cfg = moa_review.parse_moa_config(FULL_CONFIG)
        self.assertEqual(cfg["preset"], "smart")
        self.assertEqual(cfg["roles"]["orchestrator"], "fable")
        self.assertEqual(cfg["roles"]["execution"], "sonnet")
        self.assertEqual(cfg["roles"]["checker"], "inherit")
        self.assertEqual(cfg["roles"]["reviewer"], "gpt-5")

    def test_reviewer_provider_parsed(self):
        cfg = moa_review.parse_moa_config(FULL_CONFIG)
        rp = cfg["reviewer_provider"]
        self.assertEqual(rp["provider"], "openai")
        self.assertEqual(rp["base_url"], "https://api.openai.com/v1")
        self.assertEqual(rp["model"], "gpt-5")
        self.assertEqual(rp["api_key_env"], "OPENAI_API_KEY")
        self.assertEqual(rp["review_points"], "at-finish")

    def test_overrides_parsed(self):
        cfg = moa_review.parse_moa_config(FULL_CONFIG)
        self.assertEqual(cfg["overrides"]["wi-researcher"], "haiku")

    def test_reviewer_none_means_disabled(self):
        cfg = moa_review.parse_moa_config(SIMPLE_CONFIG)
        self.assertEqual(cfg["roles"]["reviewer"], "none")
        self.assertFalse(moa_review.reviewer_enabled(cfg))

    def test_reviewer_enabled_with_provider(self):
        cfg = moa_review.parse_moa_config(FULL_CONFIG)
        self.assertTrue(moa_review.reviewer_enabled(cfg))

    def test_missing_sections_default(self):
        cfg = moa_review.parse_moa_config(SIMPLE_CONFIG)
        self.assertEqual(cfg["overrides"], {})
        # provider defaults exist even when the section is absent
        self.assertEqual(cfg["reviewer_provider"]["api_key_env"], "OPENAI_API_KEY")
        self.assertEqual(cfg["reviewer_provider"]["provider"], "openai")


class ModelForTest(unittest.TestCase):
    def test_override_beats_role(self):
        cfg = moa_review.parse_moa_config(FULL_CONFIG)
        self.assertEqual(moa_review.model_for("wi-researcher", cfg), "haiku")

    def test_falls_back_to_execution_role(self):
        cfg = moa_review.parse_moa_config(FULL_CONFIG)
        self.assertEqual(moa_review.model_for("wi-task-runner", cfg), "sonnet")

    def test_checker_uses_checker_role(self):
        cfg = moa_review.parse_moa_config(FULL_CONFIG)
        self.assertEqual(moa_review.model_for("wi-code-checker", cfg), "inherit")

    def test_bare_checker_key_still_maps_to_checker_role(self):
        cfg = moa_review.parse_moa_config(FULL_CONFIG)
        self.assertEqual(moa_review.model_for("checker", cfg), "inherit")

    def test_no_config_inherits(self):
        self.assertEqual(moa_review.model_for("wi-task-runner", None), "inherit")


if __name__ == "__main__":
    unittest.main()
