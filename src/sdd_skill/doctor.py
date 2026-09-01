from __future__ import annotations

import sys
from pathlib import Path
from sdd_skill.installer import MANIFEST_PATH, SKILL_TARGET


def run_doctor(project: Path) -> dict[str, object]:
    root = project.resolve()
    return {
        "python": {
            "version": sys.version.split()[0],
            "supported": sys.version_info >= (3, 11),
        },
        "project": {
            "path": str(root),
            "exists": root.exists(),
            "is_directory": root.is_dir(),
            "is_git_repository": (root / ".git").exists(),
        },
        "skill": {
            "installed": (root / SKILL_TARGET / "SKILL.md").exists(),
            "manifest": (root / MANIFEST_PATH).exists(),
        },
        "optional_tools": {
            "codegraph_index": (root / ".codegraph").exists(),
        },
    }
