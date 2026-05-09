"""Policy-friendly mechanism explanations for Signal simulations."""

from __future__ import annotations

from typing import Any


def explain_mechanism(scenario: dict[str, Any]) -> str:
    shock_type = scenario.get("shock_type", "")
    if shock_type == "government_spending":
        main = "A government spending shock raises public demand for the targeted account and spreads through supplier, labour, and household income linkages."
    elif shock_type in {"public_investment", "care_infrastructure", "infrastructure_investment"}:
        main = "An investment shock increases demand for construction, services, and linked inputs, then transmits to factors and households through SAM multipliers."
    elif shock_type == "tax":
        main = "A tax shock changes prices or disposable income while also affecting government revenue and savings assumptions."
    elif shock_type == "trade_facilitation":
        main = "A trade shock improves external demand or lowers trade costs, raising activity in export-linked accounts and their suppliers."
    elif "care" in shock_type:
        main = "A care-economy shock affects paid care services, unpaid-care substitution, gendered labour income, and household welfare channels."
    elif "infrastructure" in shock_type:
        main = "An infrastructure shock works through productivity, transport costs, and demand for infrastructure-linked activities."
    else:
        main = "The scenario works through fixed-price SAM multiplier linkages between accounts."
    return main + " The current Python pathway is a SAM multiplier fallback, not a full CGE equilibrium solver."
