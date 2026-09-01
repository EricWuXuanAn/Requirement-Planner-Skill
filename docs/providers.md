# Requirement Source Access

Requirement Planner does not implement source providers or Jira REST API
access. URL requirements are read by the executing agent through an available,
user-authorized browser, issue tracker connector, or other source capability.

The agent must pause for user authentication when necessary, reload and verify
the original URL afterward, and never request or handle passwords, API tokens,
cookies, or CA bundle paths. If no source capability is available, use pasted or
exported requirement content instead.
