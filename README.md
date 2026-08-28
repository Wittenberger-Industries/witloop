# Witloop marketplace

This repository is the **witloop** plugin marketplace. The installable plugin
lives in [`plugins/wit`](plugins/wit) so hosts copy that directory instead of
the git repo root (Copilot CLI on Windows fails with `os error 5` / access
denied when `source` is `./` and the copy includes `.git`).

## Install

**Claude Code**
```
/plugin marketplace add Wittenberger-Industries/witloop
/plugin install wit@witloop
```

**GitHub Copilot CLI**
```
copilot plugin marketplace add Wittenberger-Industries/witloop
copilot plugin install wit@witloop
```

**Grok Build**
```
grok plugin marketplace add Wittenberger-Industries/witloop
grok plugin install wit --trust
```

**Cursor**
```
/plugin marketplace add https://github.com/Wittenberger-Industries/witloop
/plugin install wit@witloop
```

Plugin docs, skills, and agents: [`plugins/wit/README.md`](plugins/wit/README.md).

Validate from this repo root:

```
python plugins/wit/scripts/validate.py
python -m unittest discover -s tests
```
