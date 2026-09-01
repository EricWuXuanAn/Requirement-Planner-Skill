from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from importlib.resources.abc import Traversable
from importlib.resources import files
from pathlib import Path

from sdd_skill import __version__
from sdd_skill.errors import ToolError

MANIFEST_PATH = ".requirement-planner/install-manifest.json"
SKILL_TARGET = ".agents/skills/requirement-planner"


@dataclass
class InstallResult:
    action: str
    project: str
    dry_run: bool
    created: list[str]
    skipped: list[str]
    removed: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "action": self.action,
            "project": self.project,
            "dry_run": self.dry_run,
            "created": self.created,
            "skipped": self.skipped,
            "removed": self.removed,
        }


def install(project: Path, agent: str | None = None, *, dry_run: bool = False) -> InstallResult:
    root = _require_project(project)
    created: list[str] = []
    skipped: list[str] = []

    skill_source = files("sdd_skill_skill").joinpath("skill/requirement-planner")
    skill_target = root / SKILL_TARGET
    _copy_tree(
        skill_source,
        skill_target,
        root,
        created,
        skipped,
        dry_run=dry_run,
        overwrite=True,
    )

    # The package copy contains thin CLI wrappers. Replace the helper scripts
    # with standalone versions so the installed skill does not
    # require sdd_skill to be importable in the target project.
    standalone_scripts = files("sdd_skill_skill").joinpath("standalone_scripts")
    if not standalone_scripts.is_dir():
        # Development/editable installs do not materialize Hatch's
        # force-included directory inside the package. Fall back to the
        # canonical standalone scripts in the repository checkout.
        checkout_scripts = (
            Path(__file__).resolve().parents[2]
            / "skills"
            / "requirement-planner"
            / "scripts"
        )
        if checkout_scripts.is_dir():
            standalone_scripts = checkout_scripts
    if standalone_scripts.is_dir():
        _copy_tree(
            standalone_scripts,
            skill_target / "scripts",
            root,
            created,
            skipped,
            dry_run=dry_run,
            overwrite=True,
        )

    adapter_names = _adapter_names(agent)
    for adapter_name in adapter_names:
        adapter_source = files("sdd_skill_skill").joinpath(f"adapters/{adapter_name}")
        if adapter_source.is_dir():
            adapter_target = root / ".requirement-planner" / "adapters" / adapter_name
            _copy_tree(adapter_source, adapter_target, root, created, skipped, dry_run=dry_run)

    manifest = root / MANIFEST_PATH
    if not dry_run:
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(
            json.dumps(
                {
                    "tool": "Requirement Planner",
                    "version": __version__,
                    "installed_at": datetime.now(UTC).isoformat(),
                    "created": created,
                    "adapters": adapter_names,
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
    created.append(MANIFEST_PATH)
    return InstallResult("install", str(root), dry_run, created, skipped, [])


def uninstall(project: Path, *, dry_run: bool = False) -> InstallResult:
    root = _require_project(project)
    manifest = root / MANIFEST_PATH
    if not manifest.exists():
        raise ToolError(
            code="manifest_not_found",
            message="No Requirement Planner install manifest was found.",
            recovery="Run install first, or remove files manually after checking ownership.",
            exit_code=2,
        )

    data = json.loads(manifest.read_text(encoding="utf-8"))
    created = [str(item) for item in data.get("created", [])]
    removed: list[str] = []
    skipped: list[str] = []
    for relative in sorted(created, key=len, reverse=True):
        path = root / relative
        if not path.exists():
            skipped.append(relative)
            continue
        if not dry_run:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
        removed.append(relative)
    if manifest.exists() and str(MANIFEST_PATH) not in removed:
        if not dry_run:
            manifest.unlink()
        removed.append(MANIFEST_PATH)
    return InstallResult("uninstall", str(root), dry_run, [], skipped, removed)


def _require_project(project: Path) -> Path:
    root = project.resolve()
    if not root.exists() or not root.is_dir():
        raise ToolError(
            code="invalid_project",
            message="Project path is not a directory.",
            recovery="Pass --project with an existing repository path.",
            exit_code=8,
        )
    return root


def _copy_tree(
    source: Traversable,
    target: Path,
    root: Path,
    created: list[str],
    skipped: list[str],
    *,
    dry_run: bool,
    overwrite: bool = False,
) -> None:
    for item in source.iterdir():
        destination = target / item.name
        relative = str(destination.relative_to(root))
        if item.is_dir():
            _copy_tree(
                item,
                destination,
                root,
                created,
                skipped,
                dry_run=dry_run,
                overwrite=overwrite,
            )
            continue
        existed = destination.exists()
        if existed and not overwrite:
            skipped.append(relative)
            continue
        if not dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(item.read_bytes())
        if not existed:
            created.append(relative)


def _adapter_names(agent: str | None) -> list[str]:
    if agent:
        return [agent.lower()]
    return ["codex", "claude", "generic"]
