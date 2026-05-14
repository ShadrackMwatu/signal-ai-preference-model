"""Deterministic recommendations from aggregate trend demand signals."""

from __future__ import annotations

from typing import Any


def generate_trend_recommendation(signal: dict[str, Any]) -> str:
    """Generate a business/policy recommendation from an aggregate trend signal."""

    category = str(signal.get("inferred_demand_category", "general demand")).lower()
    urgency = str(signal.get("urgency", "moderate")).lower()
    unmet = float(signal.get("unmet_demand_likelihood", 0.0) or 0.0)
    trend = str(signal.get("trend_name", "this trend"))

    if "transport" in category or "logistics" in category:
        action = "check transport cost, logistics capacity, and last-mile service gaps"
    elif "price" in category or "cost" in category:
        action = "monitor price pressure, affordability constraints, and lower-cost alternatives"
    elif "employment" in category or "jobs" in category:
        action = "assess labour-market demand, youth employment support, and skills matching"
    elif "health" in category:
        action = "review healthcare access, medicine availability, and service delivery bottlenecks"
    elif "food" in category or "agriculture" in category:
        action = "track food supply, farm-input costs, and market availability"
    elif "finance" in category or "credit" in category:
        action = "monitor credit demand, repayment stress, and household liquidity needs"
    elif "technology" in category or "digital" in category:
        action = "evaluate digital adoption, service readiness, and SME productivity use cases"
    else:
        action = "validate demand through additional aggregate indicators before committing resources"

    if urgency == "high" or unmet >= 70:
        return f"Prioritize {trend}: {action}; prepare a near-term response and monitor follow-up trend movement."
    if urgency == "medium":
        return f"Monitor {trend}: {action}; compare with search, price, and service-delivery indicators."
    return f"Track {trend}: {action}; keep as an early signal until stronger aggregate evidence appears."