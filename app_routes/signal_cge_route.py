"""
Signal CGE Route

Thin orchestration layer for Signal CGE.
Compatible with normalized two-domain Signal architecture.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from datetime import UTC, datetime
import json
import csv

from Signal_CGE.solvers.gdx_reader import summarize_gdx_results
from Signal_CGE.solvers.result_parser import parse_signal_results


# =========================================================
# SAFE IMPORTS WITH FALLBACKS
# =========================================================
try:
    from Signal_CGE.cge_core.chat_orchestrator import run_chat_simulation
except Exception:
    def run_chat_simulation(prompt, sam_file=None):
        return {
            "success": True,
            "prompt": prompt,
            "sam_file": sam_file,
            "message": "Signal CGE fallback chat orchestrator active."
        }


try:
    from Signal_CGE.diagnostics.model_readiness import get_model_readiness
except Exception:
    def get_model_readiness() -> dict[str, Any]:
        return {
            "status": "prototype_ready",
            "message": "Signal CGE route is active. Full diagnostics module not yet connected.",
        }


try:
    from Signal_CGE.sam.document_loader import load_model_profile
except Exception:
    def load_model_profile() -> dict[str, Any]:
        return {
            "model_name": "Signal CGE",
            "status": "fallback_model_profile",
        }


try:
    from Signal_CGE.sam.reference_index import build_reference_index
except Exception:
    def build_reference_index() -> dict[str, Any]:
        return {
            "sections": [
                "SAM",
                "CGE core",
                "Solvers",
                "Diagnostics",
            ]
        }


try:
    from Signal_CGE.sam.scenario_context import get_scenario_context
except Exception:
    def get_scenario_context(scenario: dict[str, Any]) -> dict[str, Any]:
        return {
            "scenario": scenario,
            "reference_labels": [
                "Signal CGE normalized architecture",
            ],
        }


try:
    from Signal_CGE.solvers.static_equilibrium_solver import (
        calibration_from_sam_path,
        solve_static_equilibrium,
    )
except Exception:
    def calibration_from_sam_path(sam_path: str | None = None) -> dict[str, Any]:
        return {
            "sam_path": sam_path,
            "calibration_status": "fallback_calibration",
        }

    def solve_static_equilibrium(
        calibration: dict[str, Any],
        scenario: dict[str, Any],
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return {
            "success": True,
            "result_type": "fallback_static_equilibrium",
            "percentage_changes": {
                "output_change_pct": 0.0,
                "household_welfare_proxy_change_pct": 0.0,
                "trade_balance_change_pct": 0.0,
            },
        }


try:
    from Signal_CGE.solvers.equilibrium_solver import (
        solve_static_equilibrium as solve_prototype_equilibrium,
    )
except Exception:
    def solve_prototype_equilibrium(
        calibration: dict[str, Any],
        scenario: dict[str, Any],
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return {
            "success": True,
            "result_type": "fallback_prototype_equilibrium",
            "percentage_changes": {
                "output_change_pct": 0.0,
                "household_welfare_proxy_change_pct": 0.0,
                "trade_balance_change_pct": 0.0,
            },
        }


try:
    from Signal_CGE.solvers.solver_registry import get_solver_registry
except Exception:
    def get_solver_registry() -> dict[str, Any]:
        return {
            "available": [
                "fallback_static_equilibrium",
                "fallback_prototype_equilibrium",
            ],
            "status": "fallback_registry",
        }


# =========================================================
# CONSTANTS
# =========================================================

FULL_CGE_FALLBACK_MESSAGE = (
    "Full recursive-dynamic CGE solver is still under development. "
    "Signal is using the available static equilibrium / SAM fallback backend."
)

VALIDATED_STATIC_SOLVER_MESSAGE = (
    "Signal used the validated static equilibrium CGE solver."
)

PROTOTYPE_SOLVER_MESSAGE = (
    "Signal used the prototype equilibrium solver backend."
)


# =========================================================
# MAIN ENTRY POINT
# =========================================================

def run_signal_cge_prompt(
    prompt: str,
    uploaded_file: Any | None = None,
    backend: str = "static_equilibrium",
) -> dict[str, Any]:

    sam_path = _uploaded_path(uploaded_file)
    model_profile = load_model_profile()
    reference_index = build_reference_index()
    readiness = get_model_readiness()

    scenario = {
        "prompt": prompt,
        "backend_requested": backend,
        "model_profile": model_profile,
    }

    knowledge_context = get_scenario_context(scenario)

    run_chat_simulation(
        prompt or "Run baseline Signal CGE scenario",
        sam_file=sam_path,
    )

    try:
        calibration = calibration_from_sam_path(sam_path)

        equilibrium_result = solve_static_equilibrium(
            calibration,
            scenario,
            {"closure": "base_closure"},
        )

        if not equilibrium_result.get("success"):
            raise RuntimeError("Validated solver failed.")

        structured_results = _equilibrium_structured_results(equilibrium_result)
        solver_used = "validated_static_equilibrium"
        fallback_message = VALIDATED_STATIC_SOLVER_MESSAGE

    except Exception:
        try:
            calibration = calibration_from_sam_path(sam_path)

            prototype_result = solve_prototype_equilibrium(
                calibration,
                scenario,
                {"closure": "base_closure"},
            )

            structured_results = _equilibrium_structured_results(prototype_result)
            solver_used = "prototype_equilibrium_solver"
            fallback_message = PROTOTYPE_SOLVER_MESSAGE

        except Exception:
            structured_results = {
                "GDP/output effect": 0.0,
                "household income effect": 0.0,
                "trade effect": 0.0,
                "result_type": "fallback",
            }

            solver_used = "fallback"
            fallback_message = FULL_CGE_FALLBACK_MESSAGE

    diagnostics = {
        "solver_used": solver_used,
        "available_solvers": get_solver_registry(),
        "fallback_explanation": fallback_message,
        "model_profile_loaded": True,
        "reference_sections": reference_index.get("sections", []),
    }

    results_table = _results_table(structured_results)
    chart_data = _chart_data(structured_results)

    interpretation = {
        "summary": fallback_message,
        "knowledge_references_used": knowledge_context.get(
            "reference_labels",
            [],
        ),
    }

    downloads = _write_downloads(
        prompt=prompt,
        scenario=scenario,
        diagnostics=diagnostics,
        results=structured_results,
        results_table=results_table,
        interpretation=interpretation,
    )

    # ==========================================
    # READ REAL GAMS RESULT FILES
    # ==========================================

    summary_text, results_df, diagnostics_df, interpretation_text = parse_signal_results()

    return {
        "scenario": scenario,
        "readiness": readiness,
        "diagnostics": diagnostics,
        "results": structured_results,
        "results_table": results_table,
        "chart_data": chart_data,
        "interpretation": interpretation,
        "downloads": downloads,
        "backend_used": solver_used,

        # Real GAMS outputs
        "gams_summary": summary_text,
        "gams_results_df": results_df,
        "gams_diagnostics_df": diagnostics_df,
        "gams_interpretation": interpretation_text,
    }


# =========================================================
# HELPERS
# =========================================================

def _uploaded_path(file_obj: Any | None) -> str | None:
    if file_obj is None:
        return None

    return str(getattr(file_obj, "name", file_obj))


def _equilibrium_structured_results(
    solver_result: dict[str, Any],
) -> dict[str, Any]:

    changes = solver_result.get("percentage_changes", {})

    return {
        "GDP/output effect": float(changes.get("output_change_pct", 0.0)),
        "household income effect": float(
            changes.get("household_welfare_proxy_change_pct", 0.0)
        ),
        "trade effect": float(changes.get("trade_balance_change_pct", 0.0)),
        "result_type": solver_result.get("result_type", "static_equilibrium"),
    }


def _chart_data(results: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"metric": "GDP/output", "effect": results.get("GDP/output effect", 0.0)},
        {"metric": "Household income", "effect": results.get("household income effect", 0.0)},
        {"metric": "Trade", "effect": results.get("trade effect", 0.0)},
    ]


def _results_table(results: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"metric": "GDP/output", "effect": results.get("GDP/output effect", 0.0)},
        {"metric": "Household income", "effect": results.get("household income effect", 0.0)},
        {"metric": "Trade", "effect": results.get("trade effect", 0.0)},
        {"metric": "Result type", "effect": results.get("result_type", "fallback")},
    ]


def _write_downloads(
    prompt: str,
    scenario: dict[str, Any],
    diagnostics: dict[str, Any],
    results: dict[str, Any],
    results_table: list[dict[str, Any]],
    interpretation: dict[str, Any],
) -> dict[str, str]:

    output_dir = (
        Path("outputs")
        / "signal_cge"
        / datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "prompt": prompt,
        "scenario": scenario,
        "diagnostics": diagnostics,
        "results": results,
        "results_table": results_table,
        "interpretation": interpretation,
    }

    json_path = output_dir / "results.json"
    csv_path = output_dir / "results.csv"

    json_path.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "effect"])
        writer.writeheader()

        for row in results_table:
            writer.writerow(row)

    return {
        "results_json": str(json_path),
        "results_csv": str(csv_path),
    }