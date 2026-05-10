"""Equilibrium equations for the Signal Static CGE Solver."""

from __future__ import annotations

from typing import Any

import numpy as np

from .closures import normalize_closure
from .shocks import apply_shock, normalize_shock


VARIABLES = [
    "domestic_output",
    "composite_demand",
    "imports",
    "exports",
    "commodity_price",
    "activity_price",
    "factor_return",
    "household_income",
    "household_demand",
    "government_revenue",
    "government_balance",
    "investment",
    "exchange_rate",
]

EQUATIONS = [
    "production_output_supply",
    "production_zero_profit",
    "household_income_balance",
    "household_demand",
    "government_revenue",
    "government_balance",
    "savings_investment_balance",
    "armington_import_demand",
    "cet_export_supply",
    "commodity_market_demand",
    "commodity_market_supply",
    "factor_market_clearing",
    "numeraire_price",
]


def build_variable_vector(calibration: dict[str, Any]) -> np.ndarray:
    """Build a positive log variable vector from calibrated benchmark values."""

    benchmark = calibration["benchmark"]
    return np.log(np.array([max(float(benchmark[name]), 1e-9) for name in VARIABLES], dtype=float))


def unpack_variables(x: np.ndarray, calibration: dict[str, Any] | None = None) -> dict[str, float]:
    """Unpack a log vector into named positive model variables."""

    values = np.exp(np.clip(np.array(x, dtype=float), -50.0, 50.0))
    return {name: float(value) for name, value in zip(VARIABLES, values, strict=False)}


def equilibrium_residuals(
    x: np.ndarray,
    calibration: dict[str, Any],
    shock: dict[str, Any] | None = None,
    closure: dict[str, Any] | None = None,
) -> np.ndarray:
    """Return the static CGE residual vector.

    The system includes production, price, institution, trade, market-clearing,
    and macro-closure equations. Values near zero indicate equilibrium.
    """

    closure = normalize_closure(closure)
    variables = unpack_variables(x, calibration)
    benchmark = calibration["benchmark"]
    params = _base_parameters(calibration)
    params = apply_shock(params, normalize_shock(shock))

    qx = variables["domestic_output"]
    qq = variables["composite_demand"]
    qm = variables["imports"]
    qe = variables["exports"]
    pc = variables["commodity_price"]
    pa = variables["activity_price"]
    wf = variables["factor_return"]
    yh = variables["household_income"]
    ch = variables["household_demand"]
    gr = variables["government_revenue"]
    gb = variables["government_balance"]
    inv = variables["investment"]
    exr = variables["exchange_rate"]

    import_price = exr * (1.0 + params["tariff_rate"])
    base_import_price = 1.0 + params["base_tariff_rate"]
    export_price = exr * params["world_export_price"]
    intermediate = params["intermediate_coefficient"] * qx
    government_demand = benchmark["government_demand"] * params["government_demand_multiplier"]
    investment_demand = inv * params["investment_demand_multiplier"]
    output_target = benchmark["domestic_output"] * params["productivity"] * (pa / max(pc, 1e-9)) ** params["output_supply_elasticity"]
    unit_cost = (
        params["production_intermediate_share"] * pc
        + params["production_value_added_share"] * wf
    ) * ((1.0 + params["activity_tax_rate"]) / (1.0 + params["base_activity_tax_rate"])) / params["productivity"]
    household_income_target = benchmark["household_income"] * (wf * qx / benchmark["domestic_output"]) + params["household_transfer"]
    household_demand_target = benchmark["household_demand"] * (yh / benchmark["household_income"]) * (pc / benchmark["commodity_price"]) ** (-params["household_price_elasticity"])
    government_revenue_target = (
        params["commodity_tax_rate"] * pc * qq
        + params["activity_tax_rate"] * pa * qx
        + params["tariff_rate"] * exr * qm
        + params["direct_tax_rate"] * yh
    )
    savings_target = params["savings_rate"] * yh
    import_target = benchmark["imports"] * (qq / benchmark["composite_demand"]) * ((import_price / pc) / base_import_price) ** (-params["import_elasticity"])
    export_target = benchmark["exports"] * (qx / benchmark["domestic_output"]) * ((export_price / pa) / 1.0) ** params["export_elasticity"]
    commodity_demand_target = ch + government_demand + investment_demand + intermediate
    commodity_supply_target = qx + qm - qe
    factor_return_target = (qx / (benchmark["domestic_output"] * params["factor_supply"])) ** params["factor_supply_elasticity"]

    residuals = [
        _scaled(qx - output_target, benchmark["domestic_output"]),
        _scaled(pa - unit_cost, benchmark["activity_price"]),
        _scaled(yh - household_income_target, benchmark["household_income"]),
        _scaled(ch - household_demand_target, benchmark["household_demand"]),
        _scaled(gr - government_revenue_target, benchmark["government_revenue"]),
        _scaled(gb - (gr - government_demand), max(abs(benchmark["government_balance"]), 1.0)),
        _scaled(inv - savings_target, benchmark["investment"]),
        _scaled(qm - import_target, benchmark["imports"]),
        _scaled(qe - export_target, benchmark["exports"]),
        _scaled(qq - commodity_demand_target, benchmark["composite_demand"]),
        _scaled(qq - commodity_supply_target, benchmark["composite_demand"]),
        _scaled(wf - factor_return_target, benchmark["factor_return"]),
        pc - 1.0 if closure["numeraire"] == "fixed_commodity_price" else _scaled(exr * (qm - qe) - benchmark["external_balance"], max(abs(benchmark["external_balance"]), 1.0)),
    ]
    return np.array(residuals, dtype=float)


def equation_names() -> list[str]:
    """Return equation names in residual order."""

    return list(EQUATIONS)


def variable_names() -> list[str]:
    """Return variable names in vector order."""

    return list(VARIABLES)


def _base_parameters(calibration: dict[str, Any]) -> dict[str, float]:
    benchmark = calibration["benchmark"]
    shares = calibration["shares"]
    rates = calibration["tax_rates"]
    elasticities = calibration["elasticities"]
    return {
        "base_tariff_rate": rates["tariff_rate"],
        "tariff_rate": rates["tariff_rate"],
        "commodity_tax_rate": rates["commodity_tax_rate"],
        "activity_tax_rate": rates["activity_tax_rate"],
        "base_activity_tax_rate": rates["activity_tax_rate"],
        "direct_tax_rate": rates["direct_tax_rate"],
        "savings_rate": shares["savings_rate"],
        "production_intermediate_share": shares["production_intermediate_share"],
        "production_value_added_share": shares["production_value_added_share"],
        "intermediate_coefficient": benchmark["intermediate_demand"] / benchmark["domestic_output"],
        "import_elasticity": elasticities["import_elasticity"],
        "export_elasticity": elasticities["export_elasticity"],
        "output_supply_elasticity": elasticities["output_supply_elasticity"],
        "household_price_elasticity": elasticities["household_price_elasticity"],
        "factor_supply_elasticity": elasticities["factor_supply_elasticity"],
        "productivity": 1.0,
        "government_demand_multiplier": 1.0,
        "investment_demand_multiplier": 1.0,
        "household_transfer": 0.0,
        "factor_supply": 1.0,
        "world_export_price": 1.0,
        "household_income": benchmark["household_income"],
    }


def _scaled(value: float, scale: float) -> float:
    return float(value) / max(abs(float(scale)), 1e-9)
