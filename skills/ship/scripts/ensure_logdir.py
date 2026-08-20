#!/usr/bin/env python3
"""
ensure_logdir.py: create a self-gitignored directory (feature .logs/ or .wit/issues).

Usage: ensure_logdir.py <dir>
Creates <dir> (parents ok, existing ok) and writes <dir>/.gitignore as UTF-8
bytes of star then newline, with no BOM. Overwrites an existing gitignore.
Silent on success.
Stdlib only.
"""
import sys
from pathlib import Path


def main(argv):
    if len(argv) != 2:
        print("usage: ensure_logdir.py <dir>", file=sys.stderr)
        return 1
    try:
        target = Path(argv[1])
        target.mkdir(parents=True, exist_ok=True)
        (target / ".gitignore").write_bytes(b"*\n")
    except OSError as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
