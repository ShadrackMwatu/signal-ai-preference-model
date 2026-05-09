"""Market-clearing equations for commodities, factors, and macro balances."""

from __future__ import annotations

from typing import Any


BLOCK_NAME = "market_clearing"


def equation_placeholders() -> list[dict[str, str]]:
    return [
        {
            "name": "commodity_market_clearing",
            "equation": "QQ[c] = QINT[c] + QH[c] + QG[c] + QINV[c] + QE[c]",
            "role": "Composite commodity supply equals intermediate, household, government, investment, and export demand.",
        },
        {
            "name": "macro_balance",
            "equation": "savings = investment",
            "role": "Macro balance closes the model under the selected investment-savings closure.",
        },
    ]


def validate_market_clearing_data(data: dict[str, Any]) -> dict[str, Any]:
    errors = []
    if not data.get("commodities"):
        errors.append("Missing commodity accounts for market clearing.")
    return {"valid": not errors, "errors": errors}


def build_market_clearing_block(parameters: dict[str, Any]) -> dict[str, Any]:
    return {"block": BLOCK_NAME, "equations": equation_placeholders(), "validation": validate_market_clearing_data(parameters)}
