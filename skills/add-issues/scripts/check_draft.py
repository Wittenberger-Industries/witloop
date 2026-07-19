#!/usr/bin/env python3
"""Validate an add-issue draft before the confirm gate.

Checks (stdlib only, no PyYAML):
  1. OKF frontmatter block exists and declares a known issue_type.
  2. All required sections for that type are present.
  3. Bug drafts have >= 1 acceptance-criteria checkbox naming a test
     (skippable with --allow-no-test after an explicit user override).

Exit 0 = draft ok, exit 1 = problems (listed on stdout).
"""

import argparse
import re
import sys

REQUIRED = {
    "bug": [
        "Summary",
        "Steps to reproduce",
        "Actual results",
        "Expected results",
        "Root cause",
        "Proposed fix",
        "Acceptance criteria",
    ],
    "feature": ["Summary", "Motivation", "Proposed solution", "Acceptance criteria"],
    "task": ["Summary", "Context", "Acceptance criteria"],
}


def acceptance_section(body: str) -> str:
    """Return the text of '## Acceptance criteria' up to the next H2 (or EOF)."""
    parts = re.split(r"(?m)^##\s+Acceptance criteria\s*$", body, maxsplit=1)
    if len(parts) < 2:
        return ""
    return re.split(r"(?m)^##\s", parts[1], maxsplit=1)[0]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("draft", help="path to .wit/issues/<slug>.md")
    ap.add_argument(
        "--allow-no-test",
        action="store_true",
        help="skip the Bug new-test criterion check (explicit user override only)",
    )
    args = ap.parse_args()

    try:
        with open(args.draft, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        sys.exit(f"ERROR: cannot read draft: {exc}")

    errors = []

    fm_match = re.match(r"(?s)^---\n(.*?)\n---\n", text)
    if not fm_match:
        sys.exit("DRAFT CHECK FAILED:\n  - missing OKF frontmatter block (--- ... ---)")
    frontmatter, body = fm_match.group(1), text[fm_match.end():]

    type_match = re.search(r"(?m)^issue_type:\s*([A-Za-z]+)", frontmatter)
    issue_type = type_match.group(1).lower() if type_match else ""

    if issue_type not in REQUIRED:
        errors.append(
            f"issue_type must be one of {sorted(t.capitalize() for t in REQUIRED)} "
            f"(got: {issue_type or 'none'})"
        )
    else:
        headings = re.findall(r"(?m)^##\s+(.+?)\s*$", body)
        for section in REQUIRED[issue_type]:
            if section not in headings:
                errors.append(f"missing section: ## {section}")

        if issue_type == "bug" and not args.allow_no_test:
            boxes = re.findall(
                r"(?m)^\s*-\s*\[[ xX]\]\s*(.+)$", acceptance_section(body)
            )
            if not any("test" in item.lower() for item in boxes):
                errors.append(
                    "Bug needs >= 1 acceptance criterion naming a new automated test "
                    "(rerun with --allow-no-test only after an explicit user override)"
                )

    if errors:
        print("DRAFT CHECK FAILED:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    print("draft ok")


if __name__ == "__main__":
    main()
