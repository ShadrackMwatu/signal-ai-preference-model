"""Collect feedback from runs, user edits, GAMS logs, solvers, and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from backends.gams.lst_parser import parse_lst

from .memory_schema import EvidenceLink, FeedbackEntry, utc_now


def user_feedback(
    run_id: str,
    issue_type: str,
    original_value: str,
    corrected_value: str,
    lesson_learned: str,
    confidence_score: float = 0.75,
    source: str = "user_correction",
) -> FeedbackEntry:
    """Create evidence-linked user correction feedback."""

    return FeedbackEntry(
        run_id=run_id,
        timestamp=utc_now(),
        issue_type=issue_type,
        source=source,
        original_value=original_value,
        corrected_value=corrected_value,
        lesson_learned=lesson_learned,
        confidence_score=confidence_score,
        evidence=EvidenceLink(
            source_run=run_id,
            observed_error_or_result=original_value,
            correction_made=corrected_value,
            validation_status="user_reviewed",
        ),
    )


def collect_run_feedback(run_result: dict[str, Any]) -> list[FeedbackEntry]:
    """Collect structured feedback entries from an execution result."""

    entries: list[FeedbackEntry] = []
    run_id = str(run_result.get("run_id", "unknown"))
    validation = run_result.get("validation", {}) or {}
    message = str(run_result.get("message", ""))

    for error in validation.get("errors", []):
        entries.append(_entry(run_id, "validation_error", "validator", str(error), "", "Fix validation error before solving.", 0.9))
    for warning in validation.get("warnings", []):
        entries.append(_entry(run_id, "validation_warning", "validator", str(warning), "", "Review warning before publication-grade runs.", 0.65))
    if validation.get("sam_balanced") is False:
        entries.append(_entry(run_id, "sam_imbalance", "balance_check", "row-column imbalance", "", "Review accounts with large percentage imbalance.", 0.85))
    if "GAMS backend unavailable" in message:
        entries.append(_entry(run_id, "gams_unavailable", "solver_message", message, "Use python_nlp fallback for validation only.", "Install GAMS or explicitly select experimental backend.", 0.95))
    if "not production-grade" in message:
        entries.append(_entry(run_id, "experimental_solver", "solver_message", message, "Require GAMS solver confirmation.", "Do not treat experimental backend as production evidence.", 0.9))
    if str(run_result.get("status", "")).lower() == "ok":
        entries.append(_entry(run_id, "successful_model_run", "scenario_result", "run completed", "retain template pattern", "This model structure produced a successful prototype run.", 0.7))
    return entries


def collect_lst_feedback(run_id: str, lst_path: str | Path) -> list[FeedbackEntry]:
    parsed = parse_lst(lst_path)
    entries: list[FeedbackEntry] = []
    for error in parsed.get("errors", []):
        entries.append(_entry(run_id, "gams_error", "gams_lst", str(error), "", _lesson_for_gams_error(str(error)), 0.85))
    return entries


def build_run_snapshot(run_result: dict[str, Any]) -> dict[str, Any]:
    calibration = run_result.get("calibration", {}) or {}
    validation = run_result.get("validation", {}) or {}
    return {
        "run_id": run_result.get("run_id"),
        "model_name": run_result.get("model_name"),
        "sam_structure": {
            "accounts": list((calibration.get("row_totals") or {}).keys()),
            "balance_status": validation.get("sam_balanced"),
        },
        "account_classifications": calibration.get("account_classification", {}),
        "calibration_patterns": {
            "has_output_shares": bool(calibration.get("output_shares")),
            "total_activity_positive": float(calibration.get("total_activity", 0.0)) > 0,
        },
        "model_equations": run_result.get("equations", []),
        "closure_rules": run_result.get("closure_rules", {}),
        "shock_definitions": run_result.get("shocks", []),
        "gams_errors": run_result.get("solver_result", {}).get("gams", {}).get("lst", {}).get("errors", []),
        "solver_failures": [] if str(run_result.get("status")) == "ok" else [run_result.get("message", "")],
        "successful_model_run": str(run_result.get("status")) == "ok",
        "final_report": run_result.get("report_path", ""),
        "validation_status": "valid" if validation.get("valid") else "invalid",
    }


def _entry(
    run_id: str,
    issue_type: str,
    source: str,
    original_value: str,
    corrected_value: str,
    lesson_learned: str,
    confidence_score: float,
) -> FeedbackEntry:
    return FeedbackEntry(
        run_id=run_id,
        timestamp=utc_now(),
        issue_type=issue_type,
        source=source,
        original_value=original_value,
        corrected_value=corrected_value,
        lesson_learned=lesson_learned,
        confidence_score=confidence_score,
        evidence=EvidenceLink(
            source_run=run_id,
            observed_error_or_result=original_value,
            correction_made=corrected_value,
            validation_status="captured",
        ),
    )


def _lesson_for_gams_error(error: str) -> str:
    lowered = error.lower()
    if "uncontrolled set" in lowered:
        return "Check equation indexing; every indexed symbol must be controlled by a declared set domain."
    if "infeasible" in lowered:
        return "Review closure assumptions, bounds, calibration, and shock magnitudes."
    return "Review generated GAMS code near the reported error marker."
