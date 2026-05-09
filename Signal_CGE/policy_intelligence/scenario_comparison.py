"""Scenario comparison helpers."""

from __future__ import annotations


def compare_scenarios(results: list[dict[str, object]]) -> list[dict[str, object]]:
    """Compare scenarios by key macro impacts."""

    comparison: list[dict[str, object]] = []
    for result in results:
        metrics = result.get("metrics", {})
        comparison.append(
            {
                "run_id": result.get("run_id"),
                "status": result.get("status"),
                "backend": result.get("backend"),
                "gdp_impact": metrics.get("gdp_impact", 0.0),
                "welfare_impact": metrics.get("household_welfare_impact", 0.0),
                "government_revenue_impact": metrics.get("government_revenue_impact", 0.0),
                "trade_impact": metrics.get("trade_impact", 0.0),
            }
        )
    return sorted(comparison, key=lambda row: float(row["gdp_impact"]), reverse=True)
