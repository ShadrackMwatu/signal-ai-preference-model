from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path

from cge_workbench.diagnostics.sam_balance_checks import validate_sam
from cge_workbench.interpreters.natural_language_to_scenario import parse_scenario_prompt
from cge_workbench.interpreters.policy_brief_generator import generate_policy_brief
from cge_workbench.interpreters.result_explainer import explain_results
from cge_workbench.runners.gams_runner import GAMS_UNAVAILABLE_MESSAGE, GAMSRunner
from cge_workbench.runners.python_runner import PythonSAMRunner
from cge_workbench.runners.runner_interface import RunnerConfig


TEST_OUTPUT = Path("cge_workbench/outputs/test_ai_cge_workbench")


def test_scenario_parsing_vat_reduction():
    scenario = parse_scenario_prompt("Simulate a 10% VAT reduction on manufacturing")

    assert scenario.shock_type == "tax"
    assert scenario.target_accounts == ["manufacturing"]
    assert scenario.shock_value == -10
    assert scenario.closure_rule == "government_savings_adjusts"


def test_scenario_parsing_care_formalization():
    scenario = parse_scenario_prompt("Convert 25% of unpaid care work into paid care work")

    assert scenario.shock_type == "care_formalization"
    assert "fcp" in scenario.target_accounts
    assert scenario.shock_value == 25


def test_sam_validation_flags_zero_column():
    sam = pd.DataFrame(
        [[0.0, 0.0], [2.0, 0.0]],
        index=["a", "b"],
        columns=["a", "b"],
    )

    result = validate_sam(sam)

    assert result["valid"] is True
    assert "b" in result["zero_columns"]
    assert result["warnings"]


def test_multiplier_computation_runs_with_expected_shape():
    output_dir = TEST_OUTPUT / "multiplier"
    output_dir.mkdir(parents=True, exist_ok=True)
    sam = pd.DataFrame(
        [[0.0, 2.0], [1.0, 0.0]],
        index=["care", "households"],
        columns=["care", "households"],
    )
    sam_path = output_dir / "sam.csv"
    sam.to_csv(sam_path)
    runner = PythonSAMRunner(RunnerConfig(output_dir=output_dir, sam_path=sam_path))

    result = runner.run(
        {
            "scenario_name": "Care shock",
            "shock_type": "demand",
            "target_accounts": ["care"],
            "shock_value": 10,
            "shock_unit": "percent",
            "closure_rule": "standard_sam_multiplier",
        }
    )

    assert result.success is True
    assert result.results["leontief_inverse_shape"] == [2, 2]
    assert np.isfinite(list(result.results["accounts"].values())).all()


def test_zero_column_handling_does_not_crash():
    output_dir = TEST_OUTPUT / "zero_column"
    output_dir.mkdir(parents=True, exist_ok=True)
    sam = pd.DataFrame(
        [[0.0, 0.0], [1.0, 0.0]],
        index=["care", "households"],
        columns=["care", "households"],
    )
    sam_path = output_dir / "sam.csv"
    sam.to_csv(sam_path)

    result = PythonSAMRunner(RunnerConfig(output_dir=output_dir, sam_path=sam_path)).run(
        {
            "scenario_name": "Zero column",
            "shock_type": "demand",
            "target_accounts": ["households"],
            "shock_value": 5,
            "shock_unit": "percent",
            "closure_rule": "standard_sam_multiplier",
        }
    )

    assert result.success is True
    assert "households" in result.results["zero_columns"]


def test_gams_availability_check_returns_message_when_missing(monkeypatch):
    output_dir = TEST_OUTPUT / "gams"
    output_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("cge_workbench.runners.gams_runner.find_gams_executable", lambda: None)

    result = GAMSRunner(RunnerConfig(output_dir=output_dir)).run({"scenario_name": "Baseline"})

    assert result.success is False
    assert result.message == GAMS_UNAVAILABLE_MESSAGE


def test_result_explanation_generation():
    explanation = explain_results(
        {
            "backend": "python_sam_multiplier",
            "scenario": {"scenario_name": "Care investment", "shock_type": "public_investment"},
            "results": {"accounts": {"paid_care_services": 1.2}, "factors": {}, "households": {}},
            "diagnostics": {},
        }
    )

    assert "executive_summary" in explanation
    assert "recommended_next_steps" in explanation


def test_policy_brief_generation_contains_required_sections():
    brief = generate_policy_brief(
        {
            "backend": "python_sam_multiplier",
            "scenario": {
                "scenario_name": "Care investment",
                "shock_type": "public_investment",
                "target_accounts": ["paid_care_services"],
                "shock_value": 20,
                "shock_unit": "percent",
                "closure_rule": "investment_driven_with_fixed_prices",
            },
            "results": {"accounts": {"paid_care_services": 1.2}, "factors": {}, "households": {}},
            "diagnostics": {},
        }
    )

    assert "# Signal CGE Policy Simulation Brief" in brief
    assert "## 7. Gender-care effects" in brief
    assert "## 10. Recommendations" in brief
