"""Schemas for Signal execution learning memory."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime


@dataclass
class RunMemory:
    """Privacy-safe memory record derived from a model run."""

    run_id: str
    timestamp: str
    status: str
    requested_backend: str
    actual_backend: str
    model_name: str
    error_patterns: list[str] = field(default_factory=list)
    result_patterns: list[str] = field(default_factory=list)
    diagnostics: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
