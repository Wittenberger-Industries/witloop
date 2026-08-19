#!/usr/bin/env python3
"""
finalize_tokens.py: ship:6 token dispatcher. Route by progress.md Host: stamp.

  finalize_tokens.py --write TOKENS_MD [--progress PROGRESS_MD]
                     [--host SLUG] [--transcript T.jsonl] [--session ID] [--cwd DIR]

Reads Host: from progress.md (sibling of TOKENS_MD, or --progress / --host). Routes:

  claude / claude-code  -> token_report.py --write (transcript auto-detect unchanged)
  grok / grok-build     -> grok_token_report.py --write (SystemExit on missing session)
  cursor, copilot, codex, missing Host, unknown slug
                        -> Orchestrator: unavailable for this run + Duration from
                           progress.md spans. Never imports or runs token_report.py.

Stdlib only. Ledger rule: exact figure or unavailable; never a substitute, estimate,
invented number, or dashboard scrape.
"""
import argparse
import sys
from pathlib import Path

import _ledger

CLAUDE_HOSTS = frozenset({"claude", "claude-code"})
GROK_HOSTS = frozenset({"grok", "grok-build"})


def run_unavailable_write(token_path, progress=None, host_id=None):
    """Cursor/Copilot/Codex/unstamped/unknown: sentinel + duration fill. No token_report."""
    p = Path(token_path)
    if not p.is_file():
        print("finalize_tokens: {} does not exist - run check_tokens.py --init first".format(
            token_path), file=sys.stderr)
        return 1
    text = p.read_text(encoding="utf-8", errors="replace")
    tokens_sum = _ledger.sum_data_rows(text)
    compute, n_rows = _ledger.sum_row_durations(text)
    label = host_id or "unstamped"
    body = "\n".join([
        _ledger.UNAVAILABLE,
        "",
        "- host: {}".format(label),
        "- NOTE: this host exposes no local orchestrator usage field; Duration totals "
        "come from progress.md Log stamps. Never a dashboard scrape.",
    ])
    text = _ledger.replace_tail(text, body)
    text = _ledger.set_subagents_sum(text, tokens_sum)
    ppath = Path(progress) if progress else p.parent / "progress.md"
    span1 = span2 = None
    if ppath.is_file():
        span1, span2 = _ledger.parse_progress_spans(
            ppath.read_text(encoding="utf-8", errors="replace"))
    spans = [s for s in (span1, span2) if s is not None]
    wall = sum(spans) if spans else None
    text = _ledger.set_compute_totals(text, compute, n_rows, wall)
    p.write_text(text, encoding="utf-8")
    print(_ledger.UNAVAILABLE)
    print("timing: research+plan={} build+ship={} autonomous-total={} | sum-compute={} across {} dispatches".format(
        _ledger.format_duration(span1), _ledger.format_duration(span2),
        _ledger.format_duration(wall), _ledger.format_duration(compute), n_rows))
    return 0


def run_claude(token_path, transcript, progress):
    import token_report
    return token_report.run_write(token_path, transcript, progress)


def run_grok(token_path, progress, session_id=None, cwd=None):
    import grok_token_report
    argv = ["--write", str(token_path)]
    if progress:
        argv.extend(["--progress", str(progress)])
    if session_id:
        argv.extend(["--session", str(session_id)])
    if cwd:
        argv.extend(["--cwd", str(cwd)])
    return grok_token_report.main(argv)


def resolve_host(host_opt, progress_path, token_path):
    if host_opt:
        return host_opt.strip().casefold()
    ppath = Path(progress_path) if progress_path else Path(token_path).parent / "progress.md"
    if not ppath.is_file():
        return None
    return _ledger.parse_host(ppath.read_text(encoding="utf-8", errors="replace"))


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Ship:6 token dispatcher. Route by Host: in progress.md.")
    ap.add_argument("--write", metavar="TOKENS_MD", required=True,
                    help="existing tokens.md to finalize (never created here)")
    ap.add_argument("--progress", dest="progress_opt", metavar="PROGRESS_MD",
                    help="progress.md for Host: and wall-clock spans (default: sibling of TOKENS_MD)")
    ap.add_argument("--host", dest="host_opt",
                    help="override Host: slug (tests / recovery; default: parse progress.md)")
    ap.add_argument("--transcript", dest="transcript_opt",
                    help="Claude transcript path (passed through to token_report.py)")
    ap.add_argument("--session", dest="session_id",
                    help="Grok session id (passed through to grok_token_report.py)")
    ap.add_argument("--cwd", dest="cwd_opt",
                    help="Grok cwd for session discovery (passed through to grok_token_report.py)")
    a = ap.parse_args(argv)
    host = resolve_host(a.host_opt, a.progress_opt, a.write)
    if host in CLAUDE_HOSTS:
        return run_claude(a.write, a.transcript_opt, a.progress_opt)
    if host in GROK_HOSTS:
        return run_grok(a.write, a.progress_opt, a.session_id, a.cwd_opt)
    return run_unavailable_write(a.write, a.progress_opt, host)


if __name__ == "__main__":
    sys.exit(main())
