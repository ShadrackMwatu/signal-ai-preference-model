"""Structured schemas for Signal's adaptive learning layer."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any, Literal


LearningMode = Literal["observe_only", "recommend", "safe_apply"]


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


@dataclass
class EvidenceLink:
    """Evidence required before Signal can treat a lesson as learned."""

    source_run: str
    observed_error_or_result: str
    correction_made: str
    validation_status: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass
class FeedbackEntry:
    """Feedback from users, validators, solvers, GAMS logs, or scenario results."""

    run_id: str
    timestamp: str
    issue_type: str
    source: str
    original_value: str
    corrected_value: str
    lesson_learned: str
    confidence_score: float
    evidence: EvidenceLink

    def to_dict(self) -> dict[str, Any]:
        values = asdict(self)
        values["confidence_score"] = round(float(self.confidence_score), 4)
        return values


@dataclass
class LearningPattern:
    """Recurring issue/result pattern inferred from evidence-linked feedback."""

    pattern_id: str
    issue_type: str
    description: str
    evidence_run_ids: list[str]
    occurrences: int
    confidence_score: float
    recommended_action: str

    def to_dict(self) -> dict[str, Any]:
        values = asdict(self)
        values["confidence_score"] = round(float(self.confidence_score), 4)
        return values


@dataclass
class AdaptationProposal:
    """Versioned proposed update to rules, templates, or recommendations."""

    version_id: str
    change_summary: str
    reason_for_change: str
    affected_templates_or_rules: list[str]
    confidence_score: float
    risk_level: Literal["low", "medium", "high"]
    recommended_mode: LearningMode
    evidence_run_ids: list[str]
    rollback_instructions: str

    def to_dict(self) -> dict[str, Any]:
        values = asdict(self)
        values["confidence_score"] = round(float(self.confidence_score), 4)
        return values


@dataclass
class ImplementationResult:
    """Result of a proposed or applied learning implementation."""

    status: Literal["suggested", "applied", "blocked", "rolled_back"]
    mode: LearningMode
    version_id: str
    message: str
    validation_status: str
    applied_files: list[str] = field(default_factory=list)
    rollback_files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
