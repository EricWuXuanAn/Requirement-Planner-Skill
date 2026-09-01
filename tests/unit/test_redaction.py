from sdd_skill.security.redaction import redact, redact_mapping


def test_redact_secret_values() -> None:
    assert "abc123" not in redact("API_TOKEN=abc123")


def test_redact_mapping_marks_sensitive_keys_configured() -> None:
    values = redact_mapping({"API_TOKEN": "abc123", "SOURCE_URL": "https://jira.example.com"})

    assert values["API_TOKEN"] == "<configured>"
    assert values["SOURCE_URL"] == "https://jira.example.com"
