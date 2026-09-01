#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class ProjectInspection:
    root: str
    is_git_repository: bool
    instructions: list[str]
    docs: list[str]
    build_files: list[str]
    source_roots: list[str]
    detected_stacks: list[str]
    optional_tools: list[str]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def main() -> int:
    parser = argparse.ArgumentParser(prog="inspect_project.py")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    payload = inspect_project(args.project).to_dict()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
        payload = {"output": str(args.output)}
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def inspect_project(project: Path) -> ProjectInspection:
    root = project.resolve()
    files = {path.name: path for path in root.iterdir()} if root.exists() else {}
    build_candidates = [
        "build.gradle",
        "build.gradle.kts",
        "settings.gradle",
        "settings.gradle.kts",
        "pom.xml",
        "package.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "requirements.txt",
        "pyproject.toml",
        "go.mod",
        "Cargo.toml",
        "Package.swift",
        "*.xcodeproj",
        "*.csproj",
        "Dockerfile",
        "docker-compose.yml",
        "terraform.tf",
    ]
    return ProjectInspection(
        root=str(root),
        is_git_repository=(root / ".git").exists(),
        instructions=existing(root, ["AGENTS.md", "CLAUDE.md", ".cursorrules", ".cursor/rules", ".agents"]),
        docs=existing(root, ["README.md", "CONTRIBUTING.md", "docs"]),
        build_files=glob_existing(root, build_candidates),
        source_roots=existing(root, ["src", "app", "lib", "packages", "modules", "Sources", "tests"]),
        detected_stacks=detect_stacks(root, files),
        optional_tools=existing_tools(root),
    )


def existing(root: Path, names: list[str]) -> list[str]:
    return [str((root / name).relative_to(root)) for name in names if (root / name).exists()]


def glob_existing(root: Path, patterns: list[str]) -> list[str]:
    matches: list[str] = []
    for pattern in patterns:
        for path in root.glob(pattern):
            matches.append(str(path.relative_to(root)))
    return sorted(set(matches))


def detect_stacks(root: Path, files: dict[str, Path]) -> list[str]:
    stacks: list[str] = []
    if "build.gradle" in files or "build.gradle.kts" in files:
        stacks.append("gradle")
    if "pom.xml" in files:
        stacks.append("maven")
    if "package.json" in files:
        stacks.append("node")
    if "pyproject.toml" in files or "requirements.txt" in files:
        stacks.append("python")
    if "go.mod" in files:
        stacks.append("go")
    if "Cargo.toml" in files:
        stacks.append("rust")
    if "Package.swift" in files:
        stacks.append("swift")
    if any(root.glob("*.xcodeproj")):
        stacks.append("xcode")
    if any(root.glob("*.csproj")):
        stacks.append("dotnet")
    if "Dockerfile" in files or "docker-compose.yml" in files:
        stacks.append("docker")
    if any(root.glob("*.tf")):
        stacks.append("terraform")
    return stacks or ["unknown"]


def existing_tools(root: Path) -> list[str]:
    tools: list[str] = []
    if (root / ".codegraph").exists():
        tools.append("codegraph")
    return tools


if __name__ == "__main__":
    raise SystemExit(main())
