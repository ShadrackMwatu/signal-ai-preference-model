"""Variable registry for the future full Signal CGE system."""

from __future__ import annotations

from typing import Any


VARIABLE_GROUPS: dict[str, list[str]] = {
    "prices": ["producer_price", "commodity_price", "import_price", "export_price", "factor_price", "consumer_price_index"],
    "quantities": ["activity_output", "commodity_supply", "composite_demand", "domestic_sales"],
    "activity_output": ["QA"],
    "commodity_demand": ["household_demand", "government_demand", "investment_demand", "intermediate_demand"],
    "factor_demand": ["labor_demand", "capital_demand", "land_demand", "factor_supply"],
    "institution_income": ["household_income", "enterprise_income", "government_revenue"],
    "government_accounts": ["government_revenue", "government_expenditure", "government_savings", "direct_tax_rate"],
    "trade": ["imports", "exports", "exchange_rate", "foreign_savings"],
    "macro": ["savings", "investment", "absorption", "nominal_gdp", "real_gdp"],
    "welfare": ["equivalent_variation_proxy", "household_real_income", "consumption_index"],
}


def get_variable_registry() -> dict[str, Any]:
    return {
        "model": "Signal CGE",
        "status": "blueprint",
        "variable_groups": VARIABLE_GROUPS,
        "variables": sorted({item for values in VARIABLE_GROUPS.values() for item in values}),
    }
