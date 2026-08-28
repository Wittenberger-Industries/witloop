"""finalize_tokens.py: Host-keyed ship:6 dispatcher (unavailable path never binds Claude)."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT = REPO_ROOT / "plugins" / "wit"
SCRIPTS = ROOT / "skills" / "ship" / "scripts"
FINALIZE = SCRIPTS / "finalize_tokens.py"
CHECK = SCRIPTS / "check_tokens.py"

sys.path.insert(0, str(SCRIPTS))
import _ledger  # noqa: E402


# Same stamps as tests/test_timing_report.py (wall 1971+3012 = 4983s = 1h23m03s).
PROGRESS_STAMPS = """\
## Log
- 2026-07-05 **Created** feature, phase = brainstorm
- 2026-07-05T14:19:47+02:00 **Update** phase = research (handoff accepted)
- 2026-07-05T14:41:03+02:00 **Update** phase = plan
- 2026-07-05T14:52:38+02:00 **Update** design gate opened
- 2026-07-05T15:08:02+02:00 **Update** design gate approved, phase = build
- 2026-07-05T15:58:14+02:00 **Update** PR opened, phase = done
"""

GROK_PROGRESS = """\
## Log
- 2026-07-12T10:00:00+03:00 **Update** phase = research
- 2026-07-12T10:04:00+03:00 **Update** design gate opened
- 2026-07-12T10:05:00+03:00 **Update** design gate auto-approved
- 2026-07-12T10:25:00+03:00 **Update** PR opened
"""

PLANTED_OUT = 424242


def run(args, *, env=None, cwd=None):
    return subprocess.run(
        [sys.executable, "-X", "importtime", *map(str, args)],
        capture_output=True, text=True, env=env, cwd=cwd,
    )


def isolated_env(home, extra=None):
    env = os.environ.copy()
    home = str(Path(home).resolve())
    env["HOME"] = home
    env["USERPROFILE"] = home
    env["PYTHONNOUSERSITE"] = "1"
    drive = Path(home).drive
    if drive:
        env["HOMEDRIVE"] = drive
        env["HOMEPATH"] = home[len(drive):] or "\\"
    if extra:
        env.update(extra)
    return env


def encode_claude_project_path(path):
    s = str(Path(path).resolve())
    if len(s) >= 2 and s[1] == ":":
        s = s[0] + s[2:]
    return s.replace("\\", "-").replace("/", "-")


def plant_claude_leftover(home, cwd):
    """Distinctive same-cwd leftover plus a newer foreign project jsonl."""
    base = Path(home) / ".claude" / "projects"
    mine = base / encode_claude_project_path(cwd)
    mine.mkdir(parents=True)
    payload = {
        "message": {
            "usage": {
                "input_tokens": 1,
                "output_tokens": PLANTED_OUT,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
            },
            "model": "claude-opus-4-8",
        }
    }
    (mine / "session.jsonl").write_text(json.dumps(payload) + "\n", encoding="utf-8")
    foreign = base / "C--Users-other-repo"
    foreign.mkdir(parents=True)
    (foreign / "foreign.jsonl").write_text(json.dumps(payload) + "\n", encoding="utf-8")
    return mine / "session.jsonl"


def write_progress(path, host=None, stamps=PROGRESS_STAMPS):
    lines = ["---\ntype: Feature Progress\ntitle: fixture\n---\n\n# Feature: fixture\n\n"]
    if host is not None:
        lines.append("- **Host:** {}\n".format(host))
    lines.append("\n")
    lines.append(stamps)
    path.write_text("".join(lines), encoding="utf-8")


def init_ledger(feat, slug="fixture"):
    p = feat / "tokens.md"
    r = run([CHECK, "--init", p])
    if r.returncode != 0:
        raise RuntimeError("check_tokens --init failed: " + r.stderr)
    return p


def add_row(tokens_md, tokens=100, duration="1m00s"):
    text = tokens_md.read_text(encoding="utf-8").replace(
        "| orchestrator |",
        "| build W1 | task-runner: t1 | {} | {} | exact |\n| orchestrator |".format(
            tokens, duration),
    )
    tokens_md.write_text(text, encoding="utf-8")


def imported_token_report(stderr):
    for line in (stderr or "").splitlines():
        name = line.rstrip().rsplit("|", 1)[-1].strip()
        if name == "token_report":
            return True
    return False


def make_grok_session(sessions_root):
    session = Path(sessions_root) / "D%3A%5Cx%5Crepo" / "0199-test-session"
    (session / "subagents" / "a1").mkdir(parents=True)
    (session / "subagents" / "a2").mkdir(parents=True)
    (session / "subagents" / "a1" / "meta.json").write_text(json.dumps({
        "subagent_id": "a1", "description": "Task 1 schema",
        "subagent_type": "general-purpose", "effective_model_id": "grok-4.5",
    }), encoding="utf-8")
    (session / "subagents" / "a2" / "meta.json").write_text(json.dumps({
        "subagent_id": "a2", "description": "Task 2 ui",
        "subagent_type": "general-purpose", "effective_model_id": "grok-4.5",
    }), encoding="utf-8")
    events = [
        {"params": {"sessionUpdate": "subagent_finished", "subagent_id": "a1",
                    "tokens_used": 100, "duration_ms": 65000, "tool_calls": 5, "turns": 1}},
        {"params": {"sessionUpdate": "subagent_finished", "subagent_id": "a2",
                    "tokens_used": 200, "duration_ms": 130000, "tool_calls": 9, "turns": 1}},
        {"params": {"_meta": {"totalTokens": 55000}}},
    ]
    (session / "updates.jsonl").write_text(
        "\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")
    (session / "signals.json").write_text(json.dumps({
        "primaryModelId": "grok-4.5", "contextTokensUsed": 51000,
        "contextWindowTokens": 200000, "contextWindowUsage": 25,
        "turnCount": 7, "assistantMessageCount": 4, "toolCallCount": 30,
        "sessionDurationSeconds": 900,
    }), encoding="utf-8")
    (session / "summary.json").write_text(json.dumps({
        "info": {"id": "0199-test-session", "cwd": "D:\\x\\repo"},
        "generated_title": "test",
    }), encoding="utf-8")
    return session


def fixture_transcript(d):
    f = Path(d) / "t.jsonl"
    f.write_text(
        '{"message":{"usage":{"input_tokens":10,"output_tokens":20,'
        '"cache_creation_input_tokens":0,"cache_read_input_tokens":5},"model":"claude-opus-4-8"}}\n'
        '{"usage":{"input_tokens":1,"output_tokens":2,'
        '"cache_creation_input_tokens":0,"cache_read_input_tokens":0}}\n',
        encoding="utf-8",
    )
    return f


class CursorUnavailableTests(unittest.TestCase):
    def test_cursor_does_not_bind_planted_claude_session(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            home = d / "home"
            feat = d / "feat"
            feat.mkdir()
            home.mkdir()
            p = init_ledger(feat)
            add_row(p)
            write_progress(feat / "progress.md", host="cursor")
            plant_claude_leftover(home, feat)
            env = isolated_env(home)
            r = run([FINALIZE, "--write", p], env=env, cwd=feat)
            self.assertEqual(r.returncode, 0, r.stderr)
            out = p.read_text(encoding="utf-8")
            self.assertIn(_ledger.UNAVAILABLE, out)
            self.assertNotIn("_PENDING", out)
            self.assertNotIn(str(PLANTED_OUT), out)
            self.assertNotIn("424,242", out)
            self.assertNotIn("transcript:", out)
            self.assertFalse(imported_token_report(r.stderr), r.stderr)
            self.assertEqual(run([CHECK, p]).returncode, 0)

    def test_cursor_fills_duration_without_claude_tree(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            home = d / "home"
            feat = d / "feat"
            feat.mkdir()
            home.mkdir()
            p = init_ledger(feat)
            add_row(p, tokens=100, duration="1m00s")
            write_progress(feat / "progress.md", host="cursor")
            env = isolated_env(home)
            r = run([FINALIZE, "--write", p], env=env, cwd=feat)
            self.assertEqual(r.returncode, 0, r.stderr)
            out = p.read_text(encoding="utf-8")
            self.assertIn(_ledger.UNAVAILABLE, out)
            self.assertIn("**Σ compute: 1m00s across 1 dispatches.**", out)
            self.assertIn("**Autonomous wall-clock (excl. manual steps): 1h23m03s.**", out)
            self.assertFalse(imported_token_report(r.stderr), r.stderr)
            self.assertEqual(run([CHECK, p]).returncode, 0)

    def test_zero_row_all_unavailable_passes_gate(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            feat = d / "feat"
            feat.mkdir()
            p = init_ledger(feat)
            write_progress(feat / "progress.md", host="cursor")
            r = run([FINALIZE, "--write", p], env=isolated_env(d / "home"), cwd=feat)
            self.assertEqual(r.returncode, 0, r.stderr)
            out = p.read_text(encoding="utf-8")
            self.assertIn("**Subagents (exact): 0.**", out)
            self.assertIn(_ledger.UNAVAILABLE, out)
            self.assertEqual(run([CHECK, p]).returncode, 0)

    def test_missing_host_is_fail_safe_unavailable(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            home = d / "home"
            feat = d / "feat"
            feat.mkdir()
            home.mkdir()
            p = init_ledger(feat)
            add_row(p)
            write_progress(feat / "progress.md", host=None)
            plant_claude_leftover(home, feat)
            r = run([FINALIZE, "--write", p], env=isolated_env(home), cwd=feat)
            self.assertEqual(r.returncode, 0, r.stderr)
            out = p.read_text(encoding="utf-8")
            self.assertIn(_ledger.UNAVAILABLE, out)
            self.assertNotIn(str(PLANTED_OUT), out)
            self.assertNotIn("424,242", out)
            self.assertFalse(imported_token_report(r.stderr), r.stderr)

    def test_copilot_codex_unknown_write_unavailable(self):
        for host in ("copilot", "codex", "not-a-host"):
            with self.subTest(host=host):
                with tempfile.TemporaryDirectory() as d:
                    d = Path(d)
                    feat = d / "feat"
                    feat.mkdir()
                    p = init_ledger(feat)
                    add_row(p)
                    write_progress(feat / "progress.md", host=host)
                    r = run([FINALIZE, "--write", p], env=isolated_env(d / "home"), cwd=feat)
                    self.assertEqual(r.returncode, 0, r.stderr)
                    out = p.read_text(encoding="utf-8")
                    self.assertIn(_ledger.UNAVAILABLE, out)
                    self.assertFalse(imported_token_report(r.stderr), r.stderr)
                    self.assertEqual(run([CHECK, p]).returncode, 0)

    def test_missing_tokens_md_exits_1_creates_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            missing = d / "nope" / "tokens.md"
            r = run([FINALIZE, "--write", missing], env=isolated_env(d / "home"))
            self.assertNotEqual(r.returncode, 0)
            self.assertFalse(missing.exists())

    def test_write_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            feat = d / "feat"
            feat.mkdir()
            p = init_ledger(feat)
            add_row(p)
            write_progress(feat / "progress.md", host="cursor")
            env = isolated_env(d / "home")
            r1 = run([FINALIZE, "--write", p], env=env, cwd=feat)
            self.assertEqual(r1.returncode, 0, r1.stderr)
            first = p.read_text(encoding="utf-8")
            r2 = run([FINALIZE, "--write", p], env=env, cwd=feat)
            self.assertEqual(r2.returncode, 0, r2.stderr)
            self.assertEqual(p.read_text(encoding="utf-8"), first)


class ClaudeAndGrokRouteTests(unittest.TestCase):
    def test_host_claude_parses_transcript(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            feat = d / "feat"
            feat.mkdir()
            p = init_ledger(feat)
            add_row(p, tokens=100, duration="1m00s")
            add_row(p, tokens=50, duration="1m30s")
            write_progress(feat / "progress.md", host="claude")
            t = fixture_transcript(d)
            r = run(
                [FINALIZE, "--write", p, "--host", "claude", "--transcript", t],
                env=isolated_env(d / "home"), cwd=feat,
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            out = p.read_text(encoding="utf-8")
            self.assertIn("output tokens (generated): 22", out)
            self.assertIn("**Subagents (exact): 150.**", out)
            self.assertIn("**Σ compute: 2m30s across 2 dispatches.**", out)
            self.assertNotIn("_PENDING", out)
            self.assertEqual(run([CHECK, p]).returncode, 0)

    def test_host_grok_backfills_session_split(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            grok_home = d / "grokhome"
            feat = d / "feat"
            feat.mkdir()
            session = make_grok_session(grok_home / "sessions")
            p = init_ledger(feat)
            text = p.read_text(encoding="utf-8").replace(
                "| orchestrator |",
                "| build | Task 1 schema | 0 | 1m05s | Grok: tokens unobservable in-run |\n"
                "| build | Task 2 ui | 0 | 2m10s | Grok: tokens unobservable in-run |\n"
                "| orchestrator |",
            )
            p.write_text(text, encoding="utf-8")
            write_progress(feat / "progress.md", host="grok", stamps=GROK_PROGRESS)
            env = isolated_env(d / "home", extra={"GROK_HOME": str(grok_home)})
            r = run(
                [FINALIZE, "--write", p, "--host", "grok", "--session", session.name],
                env=env, cwd=feat,
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            out = p.read_text(encoding="utf-8")
            self.assertIn("**Subagents (exact): 300.**", out)
            self.assertIn(_ledger.UNAVAILABLE, out)
            self.assertIn("**Σ compute: 3m15s across 2 dispatches.**", out)
            self.assertIn("**Autonomous wall-clock (excl. manual steps): 24m00s.**", out)
            self.assertFalse(imported_token_report(r.stderr), r.stderr)
            self.assertIsNone(_ledger.verify(p))

    def test_host_grok_missing_session_exits(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            feat = d / "feat"
            feat.mkdir()
            p = init_ledger(feat)
            write_progress(feat / "progress.md", host="grok")
            grok_home = d / "empty-grok"
            grok_home.mkdir()
            env = isolated_env(d / "home", extra={"GROK_HOME": str(grok_home)})
            r = run([FINALIZE, "--write", p, "--host", "grok"], env=env, cwd=feat)
            self.assertNotEqual(r.returncode, 0)
            self.assertTrue(
                "session" in (r.stdout + r.stderr).lower(),
                r.stdout + r.stderr,
            )


class ProgressOverrideTests(unittest.TestCase):
    def test_progress_flag_not_sibling(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            feat = d / "feat"
            other = d / "other"
            feat.mkdir()
            other.mkdir()
            p = init_ledger(feat)
            add_row(p, duration="1m00s")
            write_progress(other / "progress.md", host="cursor")
            r = run(
                [FINALIZE, "--write", p, "--progress", other / "progress.md"],
                env=isolated_env(d / "home"), cwd=feat,
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            out = p.read_text(encoding="utf-8")
            self.assertIn("**Autonomous wall-clock (excl. manual steps): 1h23m03s.**", out)


if __name__ == "__main__":
    unittest.main()
