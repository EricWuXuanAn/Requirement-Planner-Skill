#!/usr/bin/env python3
"""Shared, dependency-free validation rules for Requirement Planner specs."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

ID_RE = re.compile(r"\b(SRC|CODE|DEC|FR|NFR|AC|IMP|TR|RISK|Q)-\d{3}\b")
TABLE_ID_DEFINITION_RE = re.compile(
    r"^\s*\|\s*((?:SRC|CODE|DEC|FR|NFR|AC|IMP|TR|RISK|Q)-\d{3})\s*\|"
)
QUESTION_DEFINITION_RE = re.compile(
    r"^\s*[-*]\s+(Q-\d{3})(?:\s+(?:Blocking|Important|Non-blocking)\b|[:：—-])",
    re.IGNORECASE,
)
READY_RE = re.compile(r"(?i)Ready for Implementation")
BLOCKING_RE = re.compile(r"\bQ-\d{3}\b.*\bBlocking\b|\bBlocking\b.*\bQ-\d{3}\b", re.I)


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "errors": self.errors,
            "warnings": self.warnings,
        }


def validate_spec(path: Path) -> ValidationResult:
    if not path.exists():
        raise FileNotFoundError(path)

    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []
    ids = ID_RE.findall(text)
    declared_ids = find_declared_ids(text)
    duplicates = sorted(
        item for item, count in Counter(declared_ids).items() if count > 1
    )
    if duplicates:
        errors.append(f"Duplicate IDs found: {', '.join(duplicates)}")

    for prefix in ("FR", "AC", "TR"):
        if prefix not in ids:
            warnings.append(f"No {prefix}-* IDs found.")

    if READY_RE.search(text) and BLOCKING_RE.search(text):
        errors.append("Spec is Ready for Implementation while blocking questions remain.")

    check_confirmed_paths(text, path.parent, errors)
    return ValidationResult(ok=not errors, errors=errors, warnings=warnings)


def find_declared_ids(text: str) -> list[str]:
    """Find IDs where a spec defines them, excluding later traceability references."""
    declared: list[str] = []
    for line in text.splitlines():
        match = TABLE_ID_DEFINITION_RE.match(line) or QUESTION_DEFINITION_RE.match(line)
        if match:
            declared.append(match.group(1))
    return declared


def check_confirmed_paths(text: str, spec_dir: Path, errors: list[str]) -> None:
    repo_root = find_repo_root(spec_dir)
    in_confirmed = False
    for line in text.splitlines():
        if re.match(r"^##+\s+Confirmed", line, re.I):
            in_confirmed = True
            continue
        if in_confirmed and line.startswith("#"):
            in_confirmed = False
        if not in_confirmed:
            continue
        for path_text in re.findall(r"`([^`]+)`", line):
            if path_text.startswith(("http://", "https://")):
                continue
            if not (repo_root / path_text).exists():
                errors.append(f"Confirmed modification path does not exist: {path_text}")


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    return start.resolve()
