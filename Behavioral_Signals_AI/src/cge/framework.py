"""High-level orchestration for the Signal CGE modelling framework."""

from __future__ import annotations

from pathlib import Path

from .dsl import parse_scenario
from .gams import export_gams_model
from .policy import generate_policy_intelligence
from .sam import load_sam
from .simulation import run_cge_simulation


ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_SAMPLE_SAM = ROOT_DIR / "data" / "sample_sam.csv"
DEFAULT_SCENARIO = """name: Kenya aggregate demand and logistics scenario
closure: savings_driven
numeraire: consumer_price_index
shock demand agriculture by 6%
shock productivity transport by 3%
shock tax manufacturing by -1%
"""


def run_policy_scenario(
    scenario_text: str = DEFAULT_SCENARIO,
    sam_path: str | Path = DEFAULT_SAMPLE_SAM,
) -> dict[str, object]:
    """Run the full CGE workflow: parse, simulate, explain, and export GAMS."""

    sam = load_sam(sam_path)
    scenario = parse_scenario(scenario_text)
    result = run_cge_simulation(sam, scenario)
    intelligence = generate_policy_intelligence(result)
    return {
        "scenario": {
            "name": scenario.name,
            "closure": scenario.closure,
            "numeraire": scenario.numeraire,
            "description": scenario.description,
            "shocks": [
                {
                    "shock_type": shock.shock_type,
                    "target": shock.target,
                    "change_percent": shock.change_percent,
                }
                for shock in scenario.shocks
            ],
        },
        "macro_results": {
            "baseline_gdp": result.baseline_gdp,
            "simulated_gdp": result.simulated_gdp,
            "gdp_change_percent": result.gdp_change_percent,
            "household_welfare_change_percent": result.household_welfare_change_percent,
            "price_index_change_percent": result.price_index_change_percent,
            "fiscal_balance_change": result.fiscal_balance_change,
            "external_balance_change": result.external_balance_change,
        },
        "sector_impacts": result.sector_impacts,
        "diagnostics": result.diagnostics,
        "policy_intelligence": intelligence,
        "gams_model": export_gams_model(sam, scenario),
    }
