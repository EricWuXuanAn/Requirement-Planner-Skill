from __future__ import annotations

from dataclasses import dataclass
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
        return {
            "root": self.root,
            "is_git_repository": self.is_git_repository,
            "instructions": self.instructions,
            "docs": self.docs,
            "build_files": self.build_files,
            "source_roots": self.source_roots,
            "detected_stacks": self.detected_stacks,
            "optional_tools": self.optional_tools,
        }


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
        instructions=_existing(root, ["AGENTS.md", "CLAUDE.md", ".cursorrules", ".agents"]),
        docs=_existing(root, ["README.md", "CONTRIBUTING.md", "docs"]),
        build_files=_glob_existing(root, build_candidates),
        source_roots=_existing(root, ["src", "app", "lib", "packages", "modules", "Sources", "tests"]),
        detected_stacks=_detect_stacks(root, files),
        optional_tools=_existing_tools(root),
    )


def _existing(root: Path, names: list[str]) -> list[str]:
    return [str((root / name).relative_to(root)) for name in names if (root / name).exists()]


def _glob_existing(root: Path, patterns: list[str]) -> list[str]:
    matches: list[str] = []
    for pattern in patterns:
        for path in root.glob(pattern):
            matches.append(str(path.relative_to(root)))
    return sorted(set(matches))


def _detect_stacks(root: Path, files: dict[str, Path]) -> list[str]:
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


def _existing_tools(root: Path) -> list[str]:
    tools = []
    if (root / ".codegraph").exists():
        tools.append("codegraph")
    return tools
