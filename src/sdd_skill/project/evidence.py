from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    id: str
    type: str
    path_or_symbol: str
    relationship: str
    confidence: str
