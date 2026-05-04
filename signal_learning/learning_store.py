"""Structured JSON learning database for Signal."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .memory_schema import AdaptationProposal, FeedbackEntry, ImplementationResult, LearningPattern


DEFAULT_LEARNING_STORE = Path("outputs") / "signal_learning_store.json"


class LearningStore:
    """Small JSON learning store that can later be replaced by SQLite."""

    def __init__(self, path: str | Path = DEFAULT_LEARNING_STORE) -> None:
        self.path = Path(path)

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return _empty_store()
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, data: dict[str, Any]) -> str:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
        return str(self.path)

    def add_feedback(self, feedback: FeedbackEntry) -> str:
        data = self.load()
        data["feedback"].append(feedback.to_dict())
        return self.save(data)

    def add_run_snapshot(self, snapshot: dict[str, Any]) -> str:
        data = self.load()
        data["run_snapshots"].append(_safe_snapshot(snapshot))
        return self.save(data)

    def add_patterns(self, patterns: list[LearningPattern]) -> str:
        data = self.load()
        existing = {pattern["pattern_id"]: pattern for pattern in data["patterns"]}
        for pattern in patterns:
            existing[pattern.pattern_id] = pattern.to_dict()
        data["patterns"] = list(existing.values())
        return self.save(data)

    def add_adaptation(self, proposal: AdaptationProposal) -> str:
        data = self.load()
        data["adaptations"].append(proposal.to_dict())
        return self.save(data)

    def add_implementation(self, result: ImplementationResult) -> str:
        data = self.load()
        data["implementations"].append(result.to_dict())
        return self.save(data)

    def add_report(self, run_id: str, report_path: str, report_summary: dict[str, Any]) -> str:
        data = self.load()
        data["reports"].append(
            {
                "run_id": run_id,
                "report_path": report_path,
                "summary": report_summary,
            }
        )
        return self.save(data)

    def lessons(self) -> list[dict[str, Any]]:
        data = self.load()
        return data["feedback"] + data["patterns"] + data["adaptations"]


def _empty_store() -> dict[str, Any]:
    return {
        "run_snapshots": [],
        "feedback": [],
        "patterns": [],
        "adaptations": [],
        "implementations": [],
        "reports": [],
    }


def _safe_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Keep structural learning evidence without storing raw SAM cells or PII."""

    allowed = {
        "run_id",
        "model_name",
        "sam_structure",
        "account_classifications",
        "calibration_patterns",
        "model_equations",
        "closure_rules",
        "shock_definitions",
        "gams_errors",
        "solver_failures",
        "successful_model_run",
        "final_report",
        "validation_status",
    }
    return {key: value for key, value in snapshot.items() if key in allowed}
