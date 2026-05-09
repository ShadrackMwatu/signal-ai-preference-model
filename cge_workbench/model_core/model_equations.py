"""Equation registry for the formal Signal CGE model."""

from __future__ import annotations

from typing import Any

from .factor_market_block import build_factor_market_block
from .government_block import build_government_block
from .household_block import build_household_block
from .investment_savings_block import build_investment_savings_block
from .market_clearing_block import build_market_clearing_block
from .price_block import build_price_block
from .production_block import build_production_block
from .trade_block import build_trade_block


EXPECTED_BLOCKS = [
    "production",
    "household",
    "government",
    "investment_savings",
    "trade",
    "factor_market",
    "price",
    "market_clearing",
]


def get_equation_registry(parameters: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return the complete Signal CGE block and placeholder-equation registry."""

    payload = parameters or {}
    blocks = {
        "production": build_production_block(payload),
        "household": build_household_block(payload),
        "government": build_government_block(payload),
        "investment_savings": build_investment_savings_block(payload),
        "trade": build_trade_block(payload),
        "factor_market": build_factor_market_block(payload),
        "price": build_price_block(payload),
        "market_clearing": build_market_clearing_block(payload),
    }
    return {
        "model": "Signal CGE Model",
        "status": "formal_structure_placeholder",
        "blocks": blocks,
        "expected_blocks": EXPECTED_BLOCKS,
    }


def validate_equation_registry(registry: dict[str, Any]) -> dict[str, Any]:
    blocks = registry.get("blocks", {})
    missing = [block for block in EXPECTED_BLOCKS if block not in blocks]
    empty = [name for name, block in blocks.items() if not block.get("equations")]
    errors = [f"Missing block: {block}" for block in missing] + [f"Block has no equations: {block}" for block in empty]
    return {"valid": not errors, "errors": errors}
