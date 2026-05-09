"""Investment-savings balance block."""

from __future__ import annotations

from typing import Any


BLOCK_NAME = "investment_savings"


def equation_placeholders() -> list[dict[str, str]]:
    return [
        {
            "name": "total_savings",
            "equation": "SAV = household_savings + government_savings + foreign_savings",
            "role": "Aggregate savings pools domestic and foreign savings sources.",
        },
        {
            "name": "investment_demand",
            "equation": "QINV[c] = investment_share[c] * real_investment",
            "role": "Investment demand allocates total investment across commodities.",
        },
    ]


def validate_investment_savings_data(data: dict[str, Any]) -> dict[str, Any]:
    errors = []
    savings_rate = data.get("savings_rate")
    if savings_rate is not None and float(savings_rate) < 0:
        errors.append("Savings rate must be non-negative.")
    return {"valid": not errors, "errors": errors}


def build_investment_savings_block(parameters: dict[str, Any]) -> dict[str, Any]:
    return {"block": BLOCK_NAME, "equations": equation_placeholders(), "validation": validate_investment_savings_data(parameters)}
