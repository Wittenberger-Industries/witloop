#!/usr/bin/env python3
"""Union known skill roots. Stamp (skill absent) only after this union misses.

Search order:
  1. Session-list paths (argv operands, or stdin lines when argv is empty)
  2. installPath values from ~/.claude/plugins/installed_plugins.json
  3. ~/.cursor/plugins/cache/**/skills
  4. Copilot ~/.copilot/installed-plugins/ (the install dir and **/skills)
  5. Flat ~/.agents/skills/

Stdlib only. Presence is a named skill dir or SKILL.md under any of those roots.

Usage:
    python discover_skills.py [--home DIR] [--name SKILL] [session_path ...]
"""

import argparse
import json
import sys
from pathlib import Path


def session_paths(argv, stdin_text=""):
    """Session-list paths: argv wins; stdin lines only when argv is empty."""
    argv_paths = [a for a in argv if a]
    if argv_paths:
        return [Path(a) for a in argv_paths]
    return [Path(ln.strip()) for ln in stdin_text.splitlines() if ln.strip()]


def _install_paths_from_registry(data):
    if not isinstance(data, dict):
        return []
    plugins = data.get("plugins", data)
    if not isinstance(plugins, dict):
        return []
    paths = []
    for _key, entries in plugins.items():
        if isinstance(entries, dict):
            entries = [entries]
        elif isinstance(entries, str):
            if entries:
                paths.append(entries)
            continue
        if not isinstance(entries, list):
            continue
        for ent in entries:
            if isinstance(ent, str) and ent:
                paths.append(ent)
            elif isinstance(ent, dict):
                ip = ent.get("installPath") or ent.get("install_path")
                if ip:
                    paths.append(ip)
    return paths


def claude_install_paths(home):
    registry = Path(home) / ".claude" / "plugins" / "installed_plugins.json"
    if not registry.is_file():
        return []
    try:
        data = json.loads(registry.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return [Path(p) for p in _install_paths_from_registry(data)]


def cursor_skill_dirs(home):
    cache = Path(home) / ".cursor" / "plugins" / "cache"
    if not cache.is_dir():
        return []
    return sorted(p for p in cache.glob("**/skills") if p.is_dir())


def copilot_skill_dirs(home):
    base = Path(home) / ".copilot" / "installed-plugins"
    if not base.is_dir():
        return []
    found = [base]
    found.extend(sorted(p for p in base.glob("**/skills") if p.is_dir()))
    return found


def agents_skill_dirs(home):
    p = Path(home) / ".agents" / "skills"
    return [p] if p.is_dir() else []


def _add_unique(out, seen, paths):
    for raw in paths:
        p = Path(raw)
        key = str(p)
        if p.exists():
            try:
                key = str(p.resolve())
            except OSError:
                pass
        if key in seen:
            continue
        seen.add(key)
        out.append(p)


def discover_skill_roots(home, session=()):
    """Ordered unique roots: session, Claude registry, Cursor cache, Copilot, agents."""
    home = Path(home)
    out = []
    seen = set()
    _add_unique(out, seen, session)
    _add_unique(out, seen, claude_install_paths(home))
    _add_unique(out, seen, cursor_skill_dirs(home))
    _add_unique(out, seen, copilot_skill_dirs(home))
    _add_unique(out, seen, agents_skill_dirs(home))
    return out


def skill_is_present(name, roots):
    """True if `name` is a skill dir or SKILL.md under any discovered root."""
    want = (name or "").strip().strip("/")
    if not want:
        return False
    for raw in roots:
        if _root_has_skill(Path(raw), want):
            return True
    return False


def _root_has_skill(root, name):
    if root.is_file() and root.name.lower() == "skill.md":
        return root.parent.name == name
    if not root.is_dir():
        return False
    if root.name == name and (root / "SKILL.md").is_file():
        return True
    if (root / name / "SKILL.md").is_file():
        return True
    if (root / "skills" / name / "SKILL.md").is_file():
        return True
    return False


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Union known skill roots; optionally check one skill name."
    )
    ap.add_argument("--home", default="", help="HOME override (tests)")
    ap.add_argument("--name", default="", help="skill directory name to look up")
    ap.add_argument("session", nargs="*", default=[], help="session-list skill paths")
    args = ap.parse_args(argv)
    home = args.home or str(Path.home())
    stdin_text = ""
    if not args.session and not sys.stdin.isatty():
        stdin_text = sys.stdin.read()
    session = session_paths(args.session, stdin_text)
    roots = discover_skill_roots(home, session)
    if args.name:
        ok = skill_is_present(args.name, roots)
        print("present" if ok else "absent")
        return 0 if ok else 1
    for root in roots:
        print(root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
