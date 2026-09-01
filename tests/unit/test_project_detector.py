from pathlib import Path

from sdd_skill.project.detector import inspect_project


def test_inspect_project_detects_python_and_codegraph(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
    (tmp_path / ".codegraph").mkdir()
    (tmp_path / "src").mkdir()

    result = inspect_project(tmp_path)

    assert "python" in result.detected_stacks
    assert "codegraph" in result.optional_tools
    assert "src" in result.source_roots
