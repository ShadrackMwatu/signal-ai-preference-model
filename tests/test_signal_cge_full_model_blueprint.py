from __future__ import annotations

import pandas as pd

from Signal_CGE.signal_cge.calibration.calibration_pipeline import calibrate_signal_cge
from Signal_CGE.signal_cge.experiments.experiment_runner import run_prototype_experiment
from Signal_CGE.signal_cge.experiments.shock_container import parse_shock_prompt
from Signal_CGE.signal_cge.full_cge.calibration_to_equilibrium import build_solver_ready_payload
from Signal_CGE.signal_cge.full_cge.closure_manager import validate_closure
from Signal_CGE.signal_cge.full_cge.equation_registry import get_equation_registry
from Signal_CGE.signal_cge.full_cge.model_gap_report import generate_full_cge_gap_report
from Signal_CGE.signal_cge.full_cge.parameter_registry import get_parameter_registry
from Signal_CGE.signal_cge.full_cge.variable_registry import get_variable_registry


def _sample_sam() -> pd.DataFrame:
    accounts = ["aagri", "cmach", "labor", "households", "government", "savings", "row"]
    data = [
        [0, 20, 10, 0, 0, 0, 5],
        [25, 0, 0, 12, 5, 8, 10],
        [15, 0, 0, 20, 0, 0, 0],
        [0, 0, 25, 0, 3, 4, 0],
        [5, 2, 0, 4, 0, 0, 1],
        [0, 5, 0, 6, 1, 0, 0],
        [5, 10, 0, 0, 1, 0, 0],
    ]
    return pd.DataFrame(data, index=accounts, columns=accounts, dtype=float)


def test_equation_registry_loads_expected_blocks() -> None:
    registry = get_equation_registry()

    assert registry["status"] == "blueprint"
    assert "production" in registry["blocks"]
    assert "armington_aggregation" in registry["blocks"]
    assert "numeraire_condition" in registry["blocks"]


def test_variable_and_parameter_registries_load() -> None:
    variables = get_variable_registry()
    parameters = get_parameter_registry()

    assert "prices" in variables["variable_groups"]
    assert "exchange_rate" in variables["variables"]
    assert "elasticities" in parameters["parameter_groups"]
    assert "closure_settings" in parameters["required_for_full_solve"]


def test_closure_manager_validates_known_closures() -> None:
    valid = validate_closure("base_closure")
    invalid = validate_closure("unknown_closure")

    assert valid["valid"] is True
    assert valid["settings"]["investment"] == "savings_driven"
    assert invalid["valid"] is False


def test_tariff_shock_creates_structured_experiment() -> None:
    shock = parse_shock_prompt("reduce import tariffs on cmach by 10%")
    run = run_prototype_experiment("reduce import tariffs on cmach by 10%")

    assert shock["instrument"] == "import_tariff"
    assert shock["target_commodity"] == "cmach"
    assert shock["shock_value_percent"] == -10.0
    assert run["result_type"] == "prototype_directional_indicator"
    assert "government_revenue_pressure" in run["directional_indicators"]


def test_calibration_bridge_returns_solver_ready_dictionary() -> None:
    calibration = calibrate_signal_cge(_sample_sam())
    payload = build_solver_ready_payload(calibration)

    assert payload["status"] == "solver_ready_blueprint"
    assert "benchmark_variables" in payload
    assert "benchmark_parameters" in payload
    assert payload["closure_settings"]["validation"]["valid"] is True


def test_model_gap_report_returns_missing_components() -> None:
    report = generate_full_cge_gap_report()

    assert "missing_for_full_cge_solving" in report
    assert "Numerical nonlinear solver backend" in report["missing_for_full_cge_solving"]
    assert report["registry_status"]["equation_blocks"] >= 18


def test_app_imports_with_full_model_blueprint() -> None:
    import app

    result = app.run_signal_cge_prompt("reduce import tariffs on cmach by 10%")
    assert "full_cge_development_status" in result
    assert result["full_cge_development_status"]["solver_status"].startswith("open-source prototype")
