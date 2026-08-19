---
type: Architecture
title: Architecture - Witloop
description: Mermaid module/dependency diagram of the real architecture.
timestamp: 2026-08-19
---

# Architecture - Witloop
_Diagrammed 2026-08-19 by /wit:scan._

```mermaid
flowchart TD
  subgraph hosts["Host adapters"]
    claude_mf[".claude-plugin manifests"]
    codex_mf[".codex-plugin manifests"]
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
    token_py["ship token parsers"]
  end
  subgraph onrepo["On-repo .wit state"]
    constitution["constitution / repo-map"]
    featuredir["features slug dossier"]
  end
  scan_sk --> constitution
  dev_sk --> brainstorm_sk
  brainstorm_sk --> research_sk
  research_sk --> plan_sk
  plan_sk --> build_sk
  build_sk --> ship_sk
  research_sk --> researcher
  build_sk --> runner
  ship_sk --> checker
  ship_sk --> token_py
  toolmaps -.-> entry
  keepalive -.-> dev_sk
  claude_mf --> validate_py
  codex_mf --> validate_py
  constitution --> featuredir
```

Legend: solid arrows are the `/wit:dev` sequence and script calls; dashed arrows are host-adapter lookups the skills read rather than own.
