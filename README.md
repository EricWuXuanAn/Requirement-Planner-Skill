# Requirement Planner

[繁體中文版](README.zh-TW.md)

Requirement Planner is a portable AI-agent skill for turning Jira issues, ticket
URLs, or product requirements into implementation-ready specifications. It
reads the source requirement through a capability available to the executing
agent, inspects the current repository, asks only
implementation-relevant questions, and produces planning documents before
product code is changed.

Generated documents are written to:

```text
docs/requirements/<REQUIREMENT_KEY>/
├── SOURCE_SNAPSHOT.md
├── IMPLEMENTATION_SPEC.md
└── TEST_REQUIREMENTS.md
```

All generated specification documents are written in Traditional Chinese.

The repository includes two forms:

- `skills/requirement-planner/`: standalone skill folder for Codex and other
  skill-aware coding agents.
- `src/`: optional Python package and CLI used for local development.

## Requirement Source Access

For a Jira URL, the agent uses only an available, user-authorized browser.
It first reuses an existing matching tab; otherwise it opens the supplied URL.
It never uses legacy Jira API scripts or checks local credentials. This
project does not provide a browser implementation and does not require Jira
credentials, cookies, API tokens, or company CA paths.

If login is required, authenticate in the interface provided by the agent and
then let it reload and verify the original issue URL. Never paste credentials
into chat. If no suitable capability is available, provide the requirement as
pasted text, an export, screenshot, PDF, or document instead.

## Installation and Usage

After this repository is published, users can install only the skill folder from
GitHub without cloning the whole repository:

```text
$skill-installer install https://github.com/<owner>/<repo>/tree/main/skills/requirement-planner
```

Restart Codex so it reloads the skill.

Then use it inside the target project:

```text
$requirement-planner
Please plan implementation for this Jira requirement:
https://jira.example.com/browse/APP-1234
```

### Cursor

Cursor discovers user skills from `~/.cursor/skills/` and `~/.agents/skills/`.
Install the skill into Cursor's personal skills directory:

```bash
git clone https://github.com/<owner>/<repo>.git requirement-planner-repo
mkdir -p ~/.cursor/skills
cp -R requirement-planner-repo/skills/requirement-planner ~/.cursor/skills/
```

Restart Cursor and invoke it with `/requirement-planner`, or let Cursor select
it when the request matches the skill description.

### Claude Code

Claude Code discovers user skills from `~/.claude/skills/`:

```bash
git clone https://github.com/<owner>/<repo>.git requirement-planner-repo
mkdir -p ~/.claude/skills
cp -R requirement-planner-repo/skills/requirement-planner ~/.claude/skills/
```

Restart Claude Code and invoke it with `/requirement-planner`, or let it select
the skill based on the request.

### Gemini CLI

Gemini CLI can install the skill directly from the repository URL:

```bash
gemini skills install https://github.com/<owner>/<repo>.git --path skills/
```

After installation, reload Gemini CLI and verify that `requirement-planner`
appears in the available skills. Use the Gemini CLI's workspace or user scope
option if you want to control where it is installed.

### Other AI agents that support `SKILL.md`

Download or copy only `skills/requirement-planner/`; cloning the entire project
is not required. Keep its `SKILL.md`, `scripts/`, `references/`, `schemas/`,
and `templates/` directories together. Place the folder in the agent's skill
directory according to that agent's documentation, then restart the agent.

### AI agents without native skill support

Copy the skill into the target project, then add this to the agent's project
instructions:

```text
When planning a requirement, read .agents/skills/requirement-planner/SKILL.md and
follow it exactly. Use only the available user-authorized browser tools for URL
requirements, and use the Python scripts in that skill only for inspection,
validation, and clear docs operations.
```

Adapter notes for different agents are available at:

- `src/sdd_skill_skill/adapters/codex/README.md`
- `src/sdd_skill_skill/adapters/claude/README.md`
- `src/sdd_skill_skill/adapters/generic/README.md`

## Standalone Skill Layout

```text
skills/requirement-planner/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── validation_rules.py
│   ├── inspect_project.py
│   └── validate_spec.py
├── references/
├── schemas/
└── templates/
```

The inspection and validation scripts are self-contained Python scripts. They do
not require this repo to be cloned or installed as a Python package.

## Optional CLI

Using the skill does not require installing the Python package. The CLI below is
only for local development, debugging, or directly running the tools:

```bash
requirement-planner inspect --project /path/to/project --output project.json
requirement-planner validate docs/requirements/APP-1234/IMPLEMENTATION_SPEC.md
requirement-planner version
```

Legacy command alias:

```bash
sdd-skill version
```

## Planning Contract

The installed skill requires the agent to:

- acquire and snapshot source requirements first;
- inspect the actual repository before proposing implementation;
- separate source facts, project facts, user decisions, engineering inferences,
  unknowns, and risks;
- ask at most three blocking or important questions per batch;
- wait for user confirmation before marking a spec Ready for Implementation;
- stop after planning unless the user explicitly asks for implementation.

## Clearing Generated Specification Documents

After reviewing the specifications, or when starting over, invoke the skill with:

```text
$requirement-planner clear docs
```

This deletes the following Requirement Planner-generated files under every
`docs/requirements/<REQUIREMENT_KEY>/` directory:

- `SOURCE_SNAPSHOT.md`
- `IMPLEMENTATION_SPEC.md`
- `TEST_REQUIREMENTS.md`

It does not delete the `docs/requirements/` directory itself or any other files
under `docs/`. The agent reports each deleted file, or explicitly reports when
none were found.

## Development Notes

Jira URLs and other URL requirements are read by the executing agent's available
source capability. Unsupported or inaccessible sources should fall back to
pasted or exported requirement content.
