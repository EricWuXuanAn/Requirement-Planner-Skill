# Requirement Source Access

Requirement URLs are acquired only through the executing agent's available,
user-authorized browser tools. First inspect existing tabs and reuse a matching
URL (for Jira, matching origin and issue key); otherwise open the supplied URL.
Verify the page identity before extraction. Follow the bounded recovery and
login handling in `skills/requirement-planner/SKILL.md`.

Do not use Jira REST APIs, legacy fetch scripts, HTTP clients, or issue-tracker
connectors for source acquisition. Do not inspect `.env`, local Jira credentials,
cookies, or CA settings. Local inspection and validation scripts remain supported.
If browser access is unavailable, ask for pasted or exported requirement content.
