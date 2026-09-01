from pathlib import Path

from sdd_skill.installer import install, uninstall


def test_install_dry_run_reports_files_without_writing(tmp_path: Path) -> None:
    result = install(tmp_path, "generic", dry_run=True)

    assert result.dry_run
    assert ".requirement-planner/install-manifest.json" in result.created
    assert not (tmp_path / ".requirement-planner").exists()


def test_install_and_uninstall_round_trip(tmp_path: Path) -> None:
    install_result = install(tmp_path, "generic", dry_run=False)

    assert (tmp_path / ".agents/skills/requirement-planner/SKILL.md").exists()
    assert (tmp_path / ".requirement-planner/install-manifest.json").exists()

    uninstall_result = uninstall(tmp_path, dry_run=False)

    assert uninstall_result.removed
    assert not (tmp_path / ".agents/skills/requirement-planner/SKILL.md").exists()
    assert not (tmp_path / ".requirement-planner/install-manifest.json").exists()


def test_install_updates_existing_skill_files(tmp_path: Path) -> None:
    skill = tmp_path / ".agents/skills/requirement-planner"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("old", encoding="utf-8")

    install(tmp_path, "generic", dry_run=False)

    assert (skill / "SKILL.md").read_text(encoding="utf-8") != "old"
    assert (skill / "scripts/validate_spec.py").exists()
    assert (skill / "scripts/validation_rules.py").exists()
