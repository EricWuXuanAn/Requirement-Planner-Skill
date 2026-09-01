# Installation

```bash
python -m pip install -e .
python -m pip install -e '.[dev]'
requirement-planner install --project /path/to/repo --dry-run
requirement-planner install --project /path/to/repo --agent codex
```

The installer writes and updates the core skill at:

```text
<repo>/.agents/skills/requirement-planner/
```

It records created files in:

```text
<repo>/.requirement-planner/install-manifest.json
```

The installer does not require or manage source credentials.
