"""Detect model gaps from repo knowledge and simulation learning memory."""

from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

from ..knowledge.reference_index import build_reference_index
from .learning_registry import summarize_learning_memory


REPORT_DIR = Path("Signal_CGE") / "outputs" / "model_improvement_reports"


def generate_model_gap_report(write: bool = True) -> dict[str, Any]:
    """Generate a deterministic model gap report without modifying model code."""

    index = build_reference_index()
    learning = summarize_learning_memory(limit=100)
    categories = index.get("knowledge_categories", {})
    repeated_warnings = learning.get("repeated_warnings", [])
    backend_limits = learning.get("backend_limitations_observed", [])
    report = {
        "timestamp": datetime.now(UTC).isoformat(),
        "missing_account_mappings": _missing_account_mapping_notes(learning),
        "missing_calibration_parameters": _missing_category_note(categories, "calibration"),
        "unresolved_closures": _missing_category_note(categories, "closures"),
        "repeated_warnings": repeated_warnings,
        "unsupported_scenario_types": _unsupported_scenario_notes(learning),
        "weak_interpretation_areas": _weak_interpretation_notes(learning),
        "solver_limitations": backend_limits or [("python_sam_multiplier", 1)],
        "missing_equations": _missing_category_note(categories, "equations"),
        "repeated_fallback_usage": any(item[0] == "python_sam_multiplier" for item in backend_limits),
        "safe_next_steps": [
            "Review proposed gaps before changing equations, closures, calibration formulas, or solver core.",
            "Add account mappings and scenario templates before expanding solver behavior.",
            "Prioritize full equilibrium price, government revenue, and market-clearing feedbacks.",
        ],
    }
    if write:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        path = REPORT_DIR / f"model_gap_report_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        report["report_path"] = str(path)
    return report


def _missing_category_note(categories: dict[str, list[str]], key: str) -> list[str]:
    if categories.get(key):
        return []
    return [f"No indexed {key.replace('_', ' ')} references were found in repo knowledge sources."]


def _missing_account_mapping_notes(learning: dict[str, Any]) -> list[str]:
    notes = []
    for account, _count in learning.get("common_target_accounts", []):
        if account in {"unknown", ""}:
            notes.append("Repeated unknown target accounts indicate missing account mapping rules.")
        elif str(account).startswith("c"):
            notes.append(f"Verify commodity mapping for `{account}`.")
    return notes or ["No repeated missing account mapping pattern detected yet."]


def _unsupported_scenario_notes(learning: dict[str, Any]) -> list[str]:
    supported = {"import_tariff", "trade_policy", "tax_policy", "care_economy", "productivity", "government_spending"}
    unsupported = [item for item in learning.get("common_scenario_types", []) if item[0] not in supported]
    return [f"Review scenario type `{scenario}`." for scenario, _count in unsupported]


def _weak_interpretation_notes(learning: dict[str, Any]) -> list[str]:
    if not learning.get("common_interpretation_patterns"):
        return ["Collect more interpretation memory before diagnosing weak policy explanation areas."]
    return ["Review repeated interpretation patterns for missing price, revenue, or welfare caveats."]
