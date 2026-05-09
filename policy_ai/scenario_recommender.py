"""Scenario recommendations for iterative Signal policy analysis."""

from __future__ import annotations

from typing import Any


def recommend_next_scenarios(current_scenario: dict[str, Any]) -> list[str]:
    shock_type = current_scenario.get("shock_type", "")
    if "care" in shock_type:
        return [
            "Compare unpaid care and paid care formalization at 10%, 25%, and 50%.",
            "Increase care infrastructure investment by 20%.",
            "Test gender-disaggregated labour income effects for care-sector expansion.",
            "Run household welfare sensitivity by income group.",
        ]
    if shock_type == "tax":
        return [
            "Compare VAT increase and VAT reduction scenarios.",
            "Test compensating household transfer assumptions.",
            "Run the same tax shock with government savings adjusting.",
        ]
    return [
        "Run a lower shock-size sensitivity case.",
        "Run a higher shock-size sensitivity case.",
        "Compare household and factor income effects across target sectors.",
    ]
