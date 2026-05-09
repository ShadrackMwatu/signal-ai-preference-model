from __future__ import annotations

import importlib

import pandas as pd

from signal_cge.calibration import calibrate_signal_cge
from signal_cge.diagnostics.model_readiness import get_model_readiness
from signal_cge.model_registry import get_model_registry


def _sample_sam() -> pd.DataFrame:
    accounts = ["care_activity", "care_commodity", "fcp", "household", "government", "investment", "rest_of_world"]
    sam = pd.DataFrame(0.0, index=accounts, columns=accounts)
    sam.loc["care_commodity", "care_activity"] = 10
    sam.loc["fcp", "care_activity"] = 15
    sam.loc["care_commodity", "household"] = 8
    sam.loc["care_commodity", "government"] = 4
    sam.loc["care_commodity", "investment"] = 3
    sam.loc["rest_of_world", "care_commodity"] = 2
    sam.loc["care_commodity", "rest_of_world"] = 1
    return sam


def test_signal_cge_imports():
    modules = [
        "signal_cge",
        "signal_cge.data.sam_loader",
        "signal_cge.calibration.calibration_pipeline",
        "signal_cge.model_core.model_equations",
        "signal_cge.solvers.sam_multiplier_solver",
        "signal_cge.scenarios.scenario_schema",
        "signal_cge.dynamics.recursive_baseline",
        "signal_cge.diagnostics.model_readiness",
        "signal_cge.reporting.result_explainer",
    ]

    for module in modules:
        assert importlib.import_module(module)


def test_old_cge_workbench_imports_still_work():
    old_calibration = importlib.import_module("cge_workbench.calibration.calibration_pipeline")
    old_model_core = importlib.import_module("cge_workbench.model_core.model_equations")
    old_runner = importlib.import_module("cge_workbench.runners.python_runner")

    assert old_calibration.calibrate_signal_cge
    assert old_model_core.get_equation_registry
    assert old_runner.PythonSAMRunner


def test_calibration_pipeline_still_works():
    result = calibrate_signal_cge(_sample_sam())

    assert "account_classification" in result
    assert "share_parameters" in result
    assert result["cge_readiness_status"]["sam_multiplier_analysis"] == "ready"


def test_model_registry_returns_expected_fields():
    registry = get_model_registry()

    assert registry["model_identity"] == "Signal CGE Model"
    assert "current_solver_options" in registry
    assert "supported_scenario_types" in registry
    assert "supported_account_suffixes" in registry
    assert registry["active_backend_status"] == "python_sam_multiplier_ready"


def test_model_readiness_returns_expected_statuses():
    readiness = get_model_readiness(calibrate_signal_cge(_sample_sam()))

    assert readiness["sam_multiplier_readiness"] == "ready"
    assert readiness["calibration_readiness"] in {"ready", "partial"}
    assert readiness["full_cge_solver_readiness"] == "placeholder"
    assert readiness["recursive_dynamic_readiness"] == "placeholder"


def test_app_imports():
    import app

    assert app.demo is not None


def test_ai_cge_chat_studio_still_works():
    from signal_ai.conversation_engine.chat_orchestrator import run_chat_simulation

    result = run_chat_simulation("increase government spending on care services by 10 percent")

    assert result["scenario"]["shock_type"] == "government_spending"
    assert "policy_summary" in result
    assert result["warnings"]
