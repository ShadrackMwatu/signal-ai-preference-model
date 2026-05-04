"""Result summaries for CGE executions."""

from __future__ import annotations


def summarize_results(result: dict[str, object]) -> dict[str, object]:
    """Create a compact, policy-facing result summary."""

    metrics = result.get("metrics", {})
    return {
        "run_id": result.get("run_id"),
        "status": result.get("status"),
        "backend": result.get("backend"),
        "message": result.get("message", ""),
        "gdp_impact": metrics.get("gdp_impact", 0.0),
        "household_welfare_impact": metrics.get("household_welfare_impact", 0.0),
        "government_revenue_impact": metrics.get("government_revenue_impact", 0.0),
        "trade_impact": metrics.get("trade_impact", 0.0),
    }
