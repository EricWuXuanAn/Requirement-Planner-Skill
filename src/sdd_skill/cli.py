from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, TextIO

from sdd_skill import __version__
from sdd_skill.doctor import run_doctor
from sdd_skill.installer import install, uninstall
from sdd_skill.errors import ToolError
from sdd_skill.output.validator import validate_spec
from sdd_skill.project.detector import inspect_project


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        payload = _dispatch(args)
    except ToolError as exc:
        _write_json(exc.to_dict(), stream=sys.stderr)
        return exc.exit_code
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        _write_json(
            {
                "error": {
                    "code": "unexpected_error",
                    "message": str(exc),
                    "recovery": "Retry with valid inputs. If the issue persists, run doctor.",
                }
            },
            stream=sys.stderr,
        )
        return 10

    if payload is not None:
        _write_json(payload)
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="requirement-planner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_parser = subparsers.add_parser("install")
    install_parser.add_argument("--project", type=Path, default=Path.cwd())
    install_parser.add_argument("--agent")
    install_parser.add_argument("--dry-run", action="store_true")

    uninstall_parser = subparsers.add_parser("uninstall")
    uninstall_parser.add_argument("--project", type=Path, default=Path.cwd())
    uninstall_parser.add_argument("--dry-run", action="store_true")

    inspect_parser = subparsers.add_parser("inspect")
    inspect_parser.add_argument("--project", type=Path, default=Path.cwd())
    inspect_parser.add_argument("--output", type=Path)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("spec_path", type=Path)

    doctor_parser = subparsers.add_parser("doctor")
    doctor_parser.add_argument("--project", type=Path, default=Path.cwd())

    subparsers.add_parser("version")
    return parser


def _dispatch(args: argparse.Namespace) -> dict[str, Any] | None:
    if args.command == "install":
        return install(args.project, args.agent, dry_run=args.dry_run).to_dict()
    if args.command == "uninstall":
        return uninstall(args.project, dry_run=args.dry_run).to_dict()
    if args.command == "inspect":
        payload = inspect_project(args.project).to_dict()
        _write_output(args.output, payload)
        return payload if args.output is None else {"output": str(args.output)}
    if args.command == "validate":
        result = validate_spec(args.spec_path).to_dict()
        if not result["ok"]:
            raise ToolError(
                code="spec_validation_failed",
                message=json.dumps(result, ensure_ascii=False),
                recovery="Fix the reported traceability or readiness issues.",
                exit_code=9,
            )
        return result
    if args.command == "doctor":
        return run_doctor(args.project)
    if args.command == "version":
        return {"version": __version__}
    return None


def _write_json(payload: dict[str, Any], *, stream: TextIO = sys.stdout) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), file=stream)


def _write_output(path: Path | None, payload: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
