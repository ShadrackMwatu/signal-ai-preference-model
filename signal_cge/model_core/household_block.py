"""Household income, consumption, and savings block."""

from __future__ import annotations

from typing import Any


BLOCK_NAME = "household"


def equation_placeholders() -> list[dict[str, str]]:
    return [
        {
            "name": "household_income",
            "equation": "YH[h] = sum(f, factor_income[h, f]) + transfers[h]",
            "role": "Household income combines factor receipts and transfers.",
        },
        {
            "name": "household_consumption_demand",
            "equation": "QH[h, c] = beta[h, c] * disposable_income[h] / PQ[c]",
            "role": "Household commodity demand follows calibrated budget shares.",
        },
    ]


def validate_household_data(data: dict[str, Any]) -> dict[str, Any]:
    errors = []
    if not data.get("households"):
        errors.append("Missing household accounts.")
    if "consumption_shares" in data and any(float(v) < 0 for v in data["consumption_shares"].values()):
        errors.append("Household consumption shares must be non-negative.")
    return {"valid": not errors, "errors": errors}


def build_household_block(parameters: dict[str, Any]) -> dict[str, Any]:
    return {"block": BLOCK_NAME, "equations": equation_placeholders(), "validation": validate_household_data(parameters)}
