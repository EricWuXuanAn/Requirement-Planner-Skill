#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


def _load_validator():
    path = Path(__file__).resolve().with_name("validation_rules.py")
    spec = importlib.util.spec_from_file_location("validation_rules", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Shared validation rules are not available.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(prog="validate_spec.py")
    parser.add_argument("spec_path", type=Path)
    args = parser.parse_args()

    try:
        result = _load_validator().validate_spec(args.spec_path)
    except FileNotFoundError:
        print(json.dumps({
            "error": {
                "code": "spec_not_found",
                "message": "Specification file does not exist.",
                "recovery": "Pass a valid IMPLEMENTATION_SPEC.md path.",
            }
        }, ensure_ascii=False, indent=2, sort_keys=True), file=sys.stderr)
        return 2

    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.ok else 9


if __name__ == "__main__":
    raise SystemExit(main())
