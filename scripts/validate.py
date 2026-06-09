#!/usr/bin/env python3
"""
validate.py — pre-release check for the wi plugin marketplace. Run from anywhere:

    python3 scripts/validate.py

Checks (from the repo root, detected automatically):
  1. JSON validity of `.claude-plugin/marketplace.json` and every `plugins/*/.claude-plugin/plugin.json`.
  2. Every `SKILL.md` / agent `.md` has valid YAML frontmatter with `name` + `description`
     — this catches the col-0 `<example>` / block-scalar bug that stopped the agents loading.
     Needs PyYAML for the full parse (`pip install pyyaml`); without it, the YAML parse is skipped
     and only delimiters + key presence are checked.
  3. Every `${CLAUDE_PLUGIN_ROOT}/<path>` reference in a plugin's `.md` files resolves to a real file.

Exit 0 if all pass; non-zero otherwise. Stdlib only (PyYAML optional).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # repo root (holds .claude-plugin/)
errors = []

try:
    import yaml
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False

# 1. JSON manifests --------------------------------------------------------
manifests = [ROOT / ".claude-plugin" / "marketplace.json"]
manifests += sorted(ROOT.glob("plugins/*/.claude-plugin/plugin.json"))
for m in manifests:
    if not m.is_file():
        errors.append(f"missing manifest: {m.relative_to(ROOT)}")
        continue
    try:
        json.loads(m.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"invalid JSON {m.relative_to(ROOT)}: {e}")

# 2. Frontmatter on SKILL.md + agents -------------------------------------
fm_files = sorted(ROOT.glob("plugins/*/skills/**/SKILL.md")) + sorted(ROOT.glob("plugins/*/agents/*.md"))
for f in fm_files:
    txt = f.read_text(encoding="utf-8")
    rel = f.relative_to(ROOT)
    if not txt.startswith("---"):
        errors.append(f"{rel}: no frontmatter (must start with '---')")
        continue
    parts = txt.split("---", 2)
    if len(parts) < 3:
        errors.append(f"{rel}: unterminated frontmatter")
        continue
    fm = parts[1]
    if HAVE_YAML:
        try:
            d = yaml.safe_load(fm)
        except Exception as e:
            errors.append(f"{rel}: frontmatter YAML error: {e}")
            continue
        if not isinstance(d, dict):
            errors.append(f"{rel}: frontmatter is not a mapping")
            continue
        for k in ("name", "description"):
            if not d.get(k):
                errors.append(f"{rel}: frontmatter missing '{k}'")
    else:
        for k in ("name:", "description:"):
            if k not in fm:
                errors.append(f"{rel}: frontmatter missing '{k.rstrip(':')}'")

# 3. ${CLAUDE_PLUGIN_ROOT} cross-refs resolve (per plugin) ------------------
rx = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\s`)\]]+)")
for plugin_dir in sorted(ROOT.glob("plugins/*")):
    if not plugin_dir.is_dir():
        continue
    for md in plugin_dir.rglob("*.md"):
        for ref in rx.findall(md.read_text(encoding="utf-8")):
            if not (plugin_dir / ref).exists():
                errors.append(f"{md.relative_to(ROOT)}: broken ref ${{CLAUDE_PLUGIN_ROOT}}/{ref}")

# Report -------------------------------------------------------------------
note = "" if HAVE_YAML else "  [PyYAML absent → YAML parse skipped; `pip install pyyaml` for the full check]"
print(f"validate.py — {len(manifests)} manifest(s), {len(fm_files)} frontmatter file(s){note}")
if errors:
    print(f"\n[FAIL] {len(errors)} issue(s):")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("[OK] all checks passed")
sys.exit(0)
