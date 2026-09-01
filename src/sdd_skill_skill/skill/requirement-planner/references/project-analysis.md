# Project Analysis

The agent must discover the project instead of assuming a language or framework.

Read or inspect:

- repository agent instructions;
- README, CONTRIBUTING, architecture, and docs;
- build, dependency, workspace, package, and module configuration;
- source roots and tests;
- requirement-related code, resources, schemas, migrations, routes, feature
  flags, and generated artifacts;
- git status and branch as baseline only.

Optional tools such as CodeGraph, language servers, and MCP connectors may speed
up inspection, but native file search and reading are valid fallbacks.

Evidence rows use:

| ID | Type | Path/Symbol | Relationship | Confidence |
| --- | --- | --- | --- | --- |

Modification scope must be one of Confirmed, Probable, Out of scope, or Unknown.
Confirmed file paths must exist.
