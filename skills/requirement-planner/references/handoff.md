# Handoff

Before implementation, the coding agent must:

1. Check git status.
2. Read repository instructions.
3. Read `IMPLEMENTATION_SPEC.md` and `TEST_REQUIREMENTS.md`.
4. Confirm evidence paths still exist.
5. Run `scripts/validate_spec.py` against `IMPLEMENTATION_SPEC.md` before
   handoff.
6. If validation reports errors, fix the specification and rerun the same
   validator until no errors remain. Do not hand off a failing specification.
7. Stop if repository changes make the spec stale.
8. Refuse to silently answer unresolved blocking questions.

Implementation verification must report against `AC-*` and `TR-*` IDs.
