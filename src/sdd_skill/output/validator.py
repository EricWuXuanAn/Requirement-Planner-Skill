from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from sdd_skill.errors import ToolError


def _load_rules():
    candidates = [
        Path(__file__).resolve().parents[3]
        / "skills/requirement-planner/scripts/validation_rules.py",
    ]
    try:
        from importlib.resources import files

        resource = files("sdd_skill_skill").joinpath("standalone_scripts/validation_rules.py")
        source = resource.read_text(encoding="utf-8")
    except (FileNotFoundError, ModuleNotFoundError):
        source = None

    if source is None:
        for candidate in candidates:
            if candidate.exists():
                source = candidate.read_text(encoding="utf-8")
                break
    if source is None:
        raise RuntimeError("Shared standalone validation rules are not available.")

    module = importlib.util.module_from_spec(
        importlib.util.spec_from_loader("validation_rules", loader=None)
    )
    sys.modules["validation_rules"] = module
    exec(compile(source, "validation_rules.py", "exec"), module.__dict__)
    return module


def validate_spec(path: Path):
    rules = _load_rules()
    try:
        return rules.validate_spec(path)
    except FileNotFoundError:
        raise ToolError(
            code="spec_not_found",
            message="Specification file does not exist.",
            recovery="Pass a valid IMPLEMENTATION_SPEC.md path.",
            exit_code=2,
        )
