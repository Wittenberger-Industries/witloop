#!/usr/bin/env python3
"""
strip_frontmatter.py: write markdown body without YAML frontmatter as UTF-8.

Usage: strip_frontmatter.py <in.md> <out.md>
Writes the body to <out.md>. Never prints the body (PowerShell > is UTF-16).
Opening line-1 --- after CR strip is required to treat YAML; a missing closer
exits 1 without writing <out.md>. No opening --- emits the whole file, LF-normalized.
Stdlib only.
"""
import sys
from pathlib import Path


def strip_body(raw):
    text = raw.decode("utf-8")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    if lines and lines[0] == "---":
        closer = None
        for index, line in enumerate(lines[1:], start=1):
            if line == "---":
                closer = index
                break
        if closer is None:
            raise ValueError("unclosed frontmatter")
        text = "\n".join(lines[closer + 1 :])
    return text.encode("utf-8")


def main(argv):
    if len(argv) != 3:
        print("usage: strip_frontmatter.py <in.md> <out.md>", file=sys.stderr)
        return 1
    src = Path(argv[1])
    dst = Path(argv[2])
    try:
        raw = src.read_bytes()
        body = strip_body(raw)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    try:
        dst.write_bytes(body)
    except OSError as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
