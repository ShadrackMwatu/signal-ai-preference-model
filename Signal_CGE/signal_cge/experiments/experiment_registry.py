"""Experiment registry for Signal CGE policy simulations."""

from __future__ import annotations

from typing import Any


EXPERIMENT_TYPES: dict[str, dict[str, Any]] = {
    "trade_policy": {"instruments": ["import_tariff", "export_demand", "trade_facilitation"], "requires": ["trade_block", "price_block", "government_balance"]},
    "tax_policy": {"instruments": ["vat_tax", "direct_tax", "production_tax"], "requires": ["government_balance", "household_demand", "price_equations"]},
    "care_economy": {"instruments": ["care_investment", "paid_care_shift"], "requires": ["household_demand", "factor_markets", "investment_demand"]},
    "infrastructure": {"instruments": ["public_investment", "transport_productivity"], "requires": ["production", "investment_demand"]},
    "productivity": {"instruments": ["total_factor_productivity", "sector_productivity"], "requires": ["production", "factor_markets"]},
}


def get_experiment_registry() -> dict[str, Any]:
    return {"status": "active_blueprint", "experiment_types": EXPERIMENT_TYPES}
