"""Parameter registry for full Signal CGE calibration."""

from __future__ import annotations

from typing import Any


PARAMETER_GROUPS: dict[str, list[str]] = {
    "share_parameters": ["input_output_shares", "value_added_shares", "household_budget_shares", "government_demand_shares", "investment_demand_shares"],
    "tax_parameters": ["import_tariff_rates", "indirect_tax_rates", "direct_tax_rates", "production_tax_rates"],
    "trade_parameters": ["armington_shares", "cet_shares", "world_import_prices", "world_export_prices"],
    "elasticities": ["substitution_elasticity", "transformation_elasticity", "income_elasticity", "export_demand_elasticity"],
    "dynamic_parameters": ["depreciation_rate", "labor_growth_rate", "productivity_growth_rate", "investment_allocation_shares"],
    "closure_parameters": ["fixed_numeraire", "fixed_foreign_savings", "fixed_government_savings", "factor_supply"],
}

REQUIRED_FOR_SOLVE = [
    "input_output_shares",
    "value_added_shares",
    "household_budget_shares",
    "import_tariff_rates",
    "armington_shares",
    "armington_elasticities",
    "closure_settings",
]


def get_parameter_registry() -> dict[str, Any]:
    return {
        "model": "Signal CGE",
        "status": "blueprint",
        "parameter_groups": PARAMETER_GROUPS,
        "required_for_full_solve": REQUIRED_FOR_SOLVE,
    }
