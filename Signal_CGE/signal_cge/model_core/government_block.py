"""Government revenue, expenditure, and balance block."""

from __future__ import annotations

from typing import Any


BLOCK_NAME = "government"


def equation_placeholders() -> list[dict[str, str]]:
    return [
        {
            "name": "government_revenue",
            "equation": "YG = sum(tax_instruments, tax_rate * tax_base) + transfers_to_government",
            "role": "Government revenue aggregates tax and transfer receipts.",
        },
        {
            "name": "government_balance",
            "equation": "GOVSAV = YG - GEXP - transfers_from_government",
            "role": "Government savings adjusts under selected fiscal closures.",
        },
    ]


def validate_government_data(data: dict[str, Any]) -> dict[str, Any]:
    warnings = []
    if "government" not in {str(account).lower() for account in data.get("accounts", [])}:
        warnings.append("No explicit government account was identified.")
    return {"valid": True, "errors": [], "warnings": warnings}


def build_government_block(parameters: dict[str, Any]) -> dict[str, Any]:
    return {"block": BLOCK_NAME, "equations": equation_placeholders(), "validation": validate_government_data(parameters)}
