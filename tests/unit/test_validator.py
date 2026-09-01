from pathlib import Path

from sdd_skill.output.validator import validate_spec


def test_validate_spec_warns_when_traceability_ids_missing(tmp_path: Path) -> None:
    spec = tmp_path / "IMPLEMENTATION_SPEC.md"
    spec.write_text("# Spec\n\nDraft\n", encoding="utf-8")

    result = validate_spec(spec)

    assert result.ok
    assert "No FR-* IDs found." in result.warnings


def test_validate_spec_fails_ready_with_blocking_question(tmp_path: Path) -> None:
    spec = tmp_path / "IMPLEMENTATION_SPEC.md"
    spec.write_text(
        "# Spec\n\nReady for Implementation\n\n- Q-001 Blocking: choose behavior\n",
        encoding="utf-8",
    )

    result = validate_spec(spec)

    assert not result.ok
