"""Price normalization and price-linkage block."""

from __future__ import annotations

from typing import Any


BLOCK_NAME = "price"


def equation_placeholders() -> list[dict[str, str]]:
    return [
        {
            "name": "consumer_price_index",
            "equation": "CPI = sum(c, cpi_weight[c] * PQ[c])",
            "role": "The consumer price index aggregates commodity prices.",
        },
        {
            "name": "numeraire",
            "equation": "NUMERAIRE_PRICE = 1",
            "role": "One price index or reference price anchors the price system.",
        },
    ]


def validate_price_data(data: dict[str, Any]) -> dict[str, Any]:
    numeraire = data.get("numeraire", "consumer_price_index")
    supported = {"consumer_price_index", "exchange_rate", "producer_price_index"}
    errors = [] if numeraire in supported else [f"Unsupported numeraire: {numeraire}"]
    return {"valid": not errors, "errors": errors}


def build_price_block(parameters: dict[str, Any]) -> dict[str, Any]:
    return {"block": BLOCK_NAME, "equations": equation_placeholders(), "validation": validate_price_data(parameters)}
