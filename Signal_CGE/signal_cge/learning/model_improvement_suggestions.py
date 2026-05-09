"""Generate safe model improvement suggestions from learning memory."""

from __future__ import annotations

from typing import Any

from .learning_registry import summarize_learning_memory


def generate_model_improvement_suggestions(limit: int = 50) -> dict[str, Any]:
    """Suggest reviewed improvements without modifying model code."""

    summary = summarize_learning_memory(limit=limit)
    suggestions = list(summary.get("suggested_model_improvements", []))
    if any(target[0] == "cmach" for target in summary.get("common_target_accounts", [])):
        suggestions.append("Add or verify `cmach` commodity mapping in the canonical account map.")
    return {
        "missing_account_mappings": ["Review high-frequency unknown or commodity-prefixed targets."],
        "missing_scenario_templates": ["Add templates for repeated tariff, VAT, care, and productivity prompts."],
        "missing_equations": ["Full price, trade, government revenue, and market-clearing feedbacks require future solver work."],
        "calibration_improvements": ["Improve benchmark replication and account classification diagnostics."],
        "solver_features_needed": ["Open-source full equilibrium solver and recursive dynamic pathway."],
        "knowledge_docs_to_expand": ["Trade-policy examples", "Tariff revenue caveats", "Scenario comparison guide"],
        "suggestions": suggestions,
    }
