from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ToolError(Exception):
    code: str
    message: str
    recovery: str
    exit_code: int

    def to_dict(self) -> dict[str, dict[str, str]]:
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "recovery": self.recovery,
            }
        }
