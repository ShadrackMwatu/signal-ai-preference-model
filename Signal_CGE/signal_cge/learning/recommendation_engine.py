"""Adaptive recommendations for follow-up Signal CGE simulations."""

from __future__ import annotations

from typing import Any

from .learning_registry import summarize_learning_memory


def recommend_adaptive_next_simulations(scenario: dict[str, Any]) -> list[str]:
    """Recommend next simulations using current scenario and learning memory."""

    summary = summarize_learning_memory(limit=100)
    scenario_type = str(scenario.get("shock_type") or scenario.get("simulation_type") or "")
    target = scenario.get("target_account") or scenario.get("target_commodity") or scenario.get("shock_account") or "same account"
    recommendations = []
    if "tariff" in scenario_type or scenario.get("policy_instrument") == "import_tariff":
        recommendations.extend(
            [
                f"Run a symmetric tariff increase on {target} for sensitivity.",
                f"Compare tariff reduction on {target} with an import productivity shock.",
                "Run a government revenue replacement scenario after tariff reduction.",
            ]
        )
    if "care" in scenario_type:
        recommendations.append("Compare paid-care expansion with unpaid-care conversion.")
    if summary.get("backend_limitations_observed"):
        recommendations.append("Re-run priority scenarios when the full equilibrium solver is activated.")
    return recommendations[:5] or ["Run a baseline comparison and a sensitivity test with half the shock size."]
