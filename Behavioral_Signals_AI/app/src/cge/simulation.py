"""Local CGE-style execution engine for policy scenario prototyping."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .sam import calibrate_sam, validate_sam
from .schema import CGEResult, CGEScenario


def run_cge_simulation(sam: pd.DataFrame, scenario: CGEScenario) -> CGEResult:
    """Run a transparent CGE-style comparative-static simulation."""

    validated_sam = validate_sam(sam)
    calibration = calibrate_sam(validated_sam)
    sectors: list[str] = list(calibration["sectors"])
    sector_output: dict[str, float] = dict(calibration["sector_output"])
    baseline_gdp = float(calibration["baseline_gdp"])

    sector_impacts: list[dict[str, float | str]] = []
    simulated_gdp = 0.0
    weighted_price_pressure = 0.0
    export_pressure = 0.0
    import_price_pressure = 0.0

    for sector in sectors:
        baseline_output = sector_output[sector]
        weight = baseline_output / baseline_gdp
        demand = _shock_sum(scenario, "demand", sector)
        productivity = _shock_sum(scenario, "productivity", sector)
        tax = _shock_sum(scenario, "tax", sector)
        export = _shock_sum(scenario, "export", sector)
        import_price = _shock_sum(scenario, "import_price", sector)

        output_change = 0.65 * demand + 0.5 * productivity + 0.25 * export - 0.2 * tax
        price_change = 0.35 * demand - 0.45 * productivity + 0.15 * tax + 0.25 * import_price
        simulated_output = baseline_output * (1 + output_change)
        simulated_gdp += simulated_output
        weighted_price_pressure += weight * price_change
        export_pressure += weight * export
        import_price_pressure += weight * import_price

        sector_impacts.append(
            {
                "sector": sector,
                "baseline_output": round(baseline_output, 2),
                "simulated_output": round(simulated_output, 2),
                "output_change_percent": round(output_change * 100, 3),
                "price_change_percent": round(price_change * 100, 3),
            }
        )

    gdp_change_percent = ((simulated_gdp - baseline_gdp) / baseline_gdp) * 100
    price_index_change_percent = weighted_price_pressure * 100
    household_welfare_change_percent = (0.55 * gdp_change_percent) - (0.4 * price_index_change_percent)
    fiscal_balance_change = float(calibration["government_revenue"]) * np.mean([_shock.change_decimal for _shock in scenario.shocks if _shock.shock_type == "tax"] or [0.0])
    external_balance_change = baseline_gdp * (0.15 * export_pressure - 0.1 * import_price_pressure)

    diagnostics = _diagnostics(calibration["account_totals"])
    return CGEResult(
        scenario=scenario,
        baseline_gdp=round(baseline_gdp, 2),
        simulated_gdp=round(simulated_gdp, 2),
        gdp_change_percent=round(gdp_change_percent, 3),
        household_welfare_change_percent=round(household_welfare_change_percent, 3),
        price_index_change_percent=round(price_index_change_percent, 3),
        fiscal_balance_change=round(fiscal_balance_change, 3),
        external_balance_change=round(external_balance_change, 3),
        sector_impacts=sector_impacts,
        diagnostics=diagnostics,
    )


def _shock_sum(scenario: CGEScenario, shock_type: str, sector: str) -> float:
    return sum(
        shock.change_decimal
        for shock in scenario.shocks
        if shock.shock_type == shock_type and shock.target == sector
    )


def _diagnostics(account_totals: list[dict[str, object]]) -> list[str]:
    diagnostics: list[str] = []
    for row in account_totals:
        if abs(float(row["imbalance_ratio"])) > 0.01:
            diagnostics.append(f"SAM imbalance above 1% for {row['account']}")
    if not diagnostics:
        diagnostics.append("SAM account balances are within the 1% tolerance.")
    return diagnostics
