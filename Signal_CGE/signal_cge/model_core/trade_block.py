"""Trade block for imports, exports, and external balance."""

from __future__ import annotations

from typing import Any


BLOCK_NAME = "trade"


def equation_placeholders() -> list[dict[str, str]]:
    return [
        {
            "name": "import_price",
            "equation": "PM[c] = exchange_rate * world_import_price[c] * (1 + import_tariff[c])",
            "role": "Import prices combine world prices, tariffs, and exchange-rate assumptions.",
        },
        {
            "name": "export_supply",
            "equation": "QE[c] = EXPORT_FUNCTION(domestic_price[c], export_price[c], transform_elasticity[c])",
            "role": "Export supply responds to relative domestic and export prices.",
        },
    ]


def validate_trade_data(data: dict[str, Any]) -> dict[str, Any]:
    warnings = []
    accounts = {str(account).lower() for account in data.get("accounts", [])}
    if not any("export" in account for account in accounts):
        warnings.append("No export account was identified.")
    if not any("import" in account for account in accounts):
        warnings.append("No import account was identified.")
    return {"valid": True, "errors": [], "warnings": warnings}


def build_trade_block(parameters: dict[str, Any]) -> dict[str, Any]:
    return {"block": BLOCK_NAME, "equations": equation_placeholders(), "validation": validate_trade_data(parameters)}
