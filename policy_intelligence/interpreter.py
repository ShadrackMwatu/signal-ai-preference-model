"""Convert CGE result metrics into policy language."""

from __future__ import annotations

from .kenya_policy_templates import KEY_POLICY_MESSAGES, county_context_note


def interpret_results(result: dict[str, object]) -> dict[str, object]:
    metrics = result.get("metrics", {})
    gdp = float(metrics.get("gdp_impact", 0.0))
    revenue = float(metrics.get("government_revenue_impact", 0.0))
    trade = float(metrics.get("trade_impact", 0.0))
    messages = [
        KEY_POLICY_MESSAGES["positive_growth" if gdp >= 0 else "negative_growth"],
        KEY_POLICY_MESSAGES["revenue_gain" if revenue >= 0 else "revenue_loss"],
        KEY_POLICY_MESSAGES["trade_gain" if trade >= 0 else "trade_loss"],
        county_context_note(),
    ]
    return {
        "gdp_impact": gdp,
        "household_welfare_impact": float(metrics.get("household_welfare_impact", 0.0)),
        "sectoral_output_impact": float(metrics.get("sectoral_output_impact", 0.0)),
        "employment_factor_income_impact": float(metrics.get("employment_factor_income_impact", 0.0)),
        "government_revenue_impact": revenue,
        "trade_impact": trade,
        "distributional_impact": float(metrics.get("distributional_impact", 0.0)),
        "key_policy_messages": messages,
        "solver_note": result.get("message", ""),
    }
