---
type: Architecture
title: Architecture - Witloop
description: Mermaid module/dependency diagram of the real architecture.
timestamp: 2026-08-25
---

# Architecture - Witloop
_Diagrammed 2026-08-19; updated for the capability table (ADR-0001), work-type routing (1.15.0), and generic PLUGIN_ROOT (1.16.0)._

```mermaid
flowchart TD
  subgraph hosts["Host adapters"]
    claude_mf[".claude-plugin manifests"]
    codex_mf[".codex-plugin manifests"]
    caps["capabilities.md"]
    toolmaps["references tool maps"]
    keepalive["keep-alive.md templates"]
  end
  subgraph entry["Entry skills"]
    scan_sk["scan"]
    dev_sk["dev"]
    rpa_sk["rpa"]
    addissues["add-issues"]
  end
  subgraph phases["Phase skills"]
    brainstorm_sk["brainstorm"]
    research_sk["research"]
    plan_sk["plan"]
    build_sk["build"]
    ship_sk["ship"]
  end
  subgraph named["Named agent charters"]
    researcher["wit-researcher"]
    runner["wit-task-runner"]
    checker["wit-code-checker"]
  end
  subgraph py["Python gates"]
    validate_py["scripts/validate.py"]
    token_py["finalize_tokens.py"]
    posix_py["ensure_logdir and strip_frontmatter"]
    discover_py["discover_skills.py"]
  end
  subgraph onrepo["On-repo .wit state"]
    constitution["constitution / repo-map"]
    featuredir["features slug dossier"]
  end
  subgraph ondemand["On-demand from dev"]
    worktypes_md["work-types.md"]
    investigation_md["investigation.md"]
    bugfix_md["bug-fix.md"]
  end
  scan_sk --> constitution
  dev_sk --> worktypes_md
  dev_sk -.-> investigation_md
  dev_sk -.-> bugfix_md
  dev_sk --> brainstorm_sk
  brainstorm_sk --> research_sk
  research_sk --> plan_sk
  plan_sk --> build_sk
  build_sk --> ship_sk
  research_sk --> researcher
  build_sk --> runner
  ship_sk --> checker
  ship_sk --> token_py
  ship_sk --> posix_py
  research_sk --> discover_py
  caps -.-> entry
  caps -.-> keepalive
  toolmaps -.-> entry
  keepalive -.-> dev_sk
  claude_mf --> validate_py
  codex_mf --> validate_py
  constitution --> featuredir
```

Legend: solid arrows are the `/wit:dev` sequence and script calls; dashed arrows are host-adapter lookups the skills read rather than own. `dev` loads `work-types.md` on every run; `investigation.md` and `bug-fix.md` are on-demand (investigation exits read-only; bug-fix overlays phases). Four entry skills; one named review agent (`wit-code-checker`). `capabilities.md` is the capability x host matrix; `cursor-tools.md` is one of the tool maps. Entry skills stamp cells into `progress.md`; later phases read that stamp.
