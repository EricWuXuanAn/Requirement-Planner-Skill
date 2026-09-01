from __future__ import annotations

import re

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?token|token|password|cookie|secret|ssh[_-]?key)\s*[:=]\s*([^\s]+)"),
    re.compile(r"(?i)(authorization:\s*bearer\s+)([A-Za-z0-9._~+/=-]+)"),
]


def redact(value: str) -> str:
    redacted = value
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub(lambda match: f"{match.group(1)}=<redacted>", redacted)
    return redacted


def redact_mapping(values: dict[str, str | None]) -> dict[str, str | None]:
    redacted: dict[str, str | None] = {}
    for key, value in values.items():
        if value is None:
            redacted[key] = None
            continue
        if any(marker in key.lower() for marker in ("token", "password", "secret", "cookie")):
            redacted[key] = "<configured>"
        else:
            redacted[key] = redact(value)
    return redacted
