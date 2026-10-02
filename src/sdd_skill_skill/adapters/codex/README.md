# Codex Adapter

Install target:

```text
<repo>/.agents/skills/requirement-planner/
```

Prompt:

```text
Use the requirement-planner skill for this requirement URL: <URL>
```

The agent uses only an available user-authorized browser for URL requirements.
Reuse an existing matching tab first; otherwise open the supplied URL. Never use
legacy Jira API scripts or check local credentials. No browser vendor is assumed.
