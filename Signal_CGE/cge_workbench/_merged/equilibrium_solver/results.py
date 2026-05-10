"""Result formatting for the Signal Static CGE Solver."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import pandas as pd


OUTPUT_DIR = Path("cge_workbench") / "outputs"


def build_result_tables(result: dict[str, Any]) -> dict[str, Any]:
    """Build summary, baseline, counterfactual, and percent-change tables."""

    baseline = result.get("baseline", {}).get("values", {})
    counterfactual = result.get("counterfactual", {}).get("values", {})
    changes = result.get("percentage_changes", {})
    rows = []
    for key in sorted(set(baseline) | set(counterfactual)):
        rows.append(
            {
                "variable": key,
                "baseline": baseline.get(key),
                "counterfactual": counterfactual.get(key),
                "percentage_change": changes.get(key),
            }
        )
    summary = {
        "solver_name": result.get("solver_name"),
        "success": result.get("success"),
        "residual_norm": result.get("residual_norm"),
        "max_abs_residual": result.get("max_abs_residual"),
        "message": result.get("message"),
    }
    return {
        "summary": summary,
        "baseline_table": [{"variable": k, "value": v} for k, v in baseline.items()],
        "counterfactual_table": [{"variable": k, "value": v} for k, v in counterfactual.items()],
        "percentage_change_table": [{"variable": k, "percentage_change": v} for k, v in changes.items()],
        "comparison_table": rows,
        "sector_impacts": _pick(changes, ["domestic_output", "composite_demand"]),
        "household_impacts": _pick(changes, ["household_income", "household_demand"]),
        "factor_income_impacts": _pick(changes, ["factor_return"]),
        "government_revenue_impacts": _pick(changes, ["government_revenue", "government_balance"]),
        "trade_impacts": _pick(changes, ["imports", "exports", "exchange_rate"]),
    }


def generate_policy_brief(result: dict[str, Any]) -> str:
    """Generate a concise Markdown policy brief."""

    shock = result.get("shock", {})
    tables = build_result_tables(result)
    return "\n\n".join(
        [
            "# Signal CGE Static Equilibrium Simulation Brief",
            "## Scenario\n```json\n" + json.dumps(shock, indent=2) + "\n```",
            "## Solver\n"
            + (
                "Signal Static CGE Solver active: results are generated from the open-source equilibrium solver "
                "using calibrated benchmark equations and the selected macro closure."
                if result.get("success")
                else "Static equilibrium solve did not pass convergence diagnostics."
            ),
            "## Diagnostics\n```json\n" + json.dumps(result.get("diagnostics", {}), indent=2) + "\n```",
            "## Summary\n```json\n" + json.dumps(tables["summary"], indent=2) + "\n```",
            "## Percentage Changes\n```json\n" + json.dumps(tables["percentage_change_table"], indent=2) + "\n```",
            "## Interpretation\n"
            + "Policy effects are reported as counterfactual deviations from the calibrated benchmark. "
            + "Price, income, fiscal, and trade channels adjust simultaneously through the static equilibrium equations.",
        ]
    )


def save_outputs(result: dict[str, Any], output_dir: str | Path = OUTPUT_DIR) -> dict[str, str]:
    """Save JSON, CSV, and Markdown outputs."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    tables = build_result_tables(result)
    json_path = output_path / "static_cge_results.json"
    csv_path = output_path / "static_cge_percentage_changes.csv"
    md_path = output_path / "static_cge_policy_brief.md"
    json_path.write_text(json.dumps({"result": _json_ready(result), "tables": tables}, indent=2), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["variable", "percentage_change"])
        writer.writeheader()
        writer.writerows(tables["percentage_change_table"])
    md_path.write_text(generate_policy_brief(result), encoding="utf-8")
    return {"results_json": str(json_path), "percentage_changes_csv": str(csv_path), "policy_brief_md": str(md_path)}


def _pick(values: dict[str, float], keys: list[str]) -> dict[str, float]:
    return {key: values.get(key, 0.0) for key in keys}


def _json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _json_ready(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_ready(v) for v in value]
    if hasattr(value, "tolist"):
        return value.tolist()
    return value
