from __future__ import annotations

import math

import pandas as pd
import pytest

from cge_workbench.calibration import (
    calibrate_share_parameters,
    calibrate_signal_cge,
    classify_sam_accounts,
    run_calibration_diagnostics,
    validate_sam_matrix,
)


def _sample_sam() -> pd.DataFrame:
    accounts = [
        "care_activity",
        "manufacturing_activity",
        "care_commodity",
        "manufacturing_commodity",
        "fcp",
        "mcp",
        "household_rural",
        "government",
        "investment",
        "rest_of_world",
        "vat_tax",
    ]
    data = pd.DataFrame(0.0, index=accounts, columns=accounts)
    data.loc["care_commodity", "care_activity"] = 20
    data.loc["manufacturing_commodity", "care_activity"] = 10
    data.loc["fcp", "care_activity"] = 30
    data.loc["mcp", "care_activity"] = 20
    data.loc["vat_tax", "care_activity"] = 3
    data.loc["care_commodity", "manufacturing_activity"] = 5
    data.loc["manufacturing_commodity", "manufacturing_activity"] = 30
    data.loc["fcp", "manufacturing_activity"] = 10
    data.loc["mcp", "manufacturing_activity"] = 25
    data.loc["vat_tax", "manufacturing_activity"] = 6
    data.loc["care_commodity", "household_rural"] = 40
    data.loc["manufacturing_commodity", "household_rural"] = 60
    data.loc["care_commodity", "government"] = 15
    data.loc["manufacturing_commodity", "government"] = 5
    data.loc["care_commodity", "investment"] = 12
    data.loc["manufacturing_commodity", "investment"] = 18
    data.loc["rest_of_world", "care_commodity"] = 8
    data.loc["rest_of_world", "manufacturing_commodity"] = 12
    data.loc["care_commodity", "rest_of_world"] = 7
    data.loc["manufacturing_commodity", "rest_of_world"] = 13
    return data


def test_square_sam_validation_rejects_non_square():
    bad = pd.DataFrame([[1, 2, 3], [4, 5, 6]], index=["a", "b"], columns=["a", "b", "c"])

    with pytest.raises(ValueError, match="square"):
        validate_sam_matrix(bad)


def test_square_sam_validation_rejects_mismatched_labels():
    bad = pd.DataFrame([[1, 2], [3, 4]], index=["a", "b"], columns=["a", "c"])

    with pytest.raises(ValueError, match="labels"):
        validate_sam_matrix(bad)


def test_account_classification_and_care_suffixes():
    classification = classify_sam_accounts(_sample_sam())

    assert "care_activity" in classification["activities"]
    assert "care_commodity" in classification["commodities"]
    assert "fcp" in classification["factors"]
    assert "mcp" in classification["factors"]
    assert classification["care_factors"] == ["fcp", "mcp"]
    assert "household_rural" in classification["households"]
    assert "government" in classification["government"]
    assert "investment" in classification["savings_investment"]
    assert "rest_of_world" in classification["rest_of_world"]
    assert "vat_tax" in classification["taxes"]


def test_share_parameters_sum_sensibly():
    sam = _sample_sam()
    classification = classify_sam_accounts(sam)
    shares = calibrate_share_parameters(sam, classification)

    production_care = shares["production_input_shares"]["care_activity"]
    household = shares["household_expenditure_shares"]["household_rural"]
    government = shares["government_demand_shares"]["government"]
    investment = shares["investment_demand_shares"]["investment"]
    imports = shares["import_shares"]["rest_of_world"]

    assert round(sum(production_care.values()), 8) == 1.0
    assert round(sum(household.values()), 8) == 1.0
    assert round(sum(government.values()), 8) == 1.0
    assert round(sum(investment.values()), 8) == 1.0
    assert round(sum(imports.values()), 8) == 1.0
    assert production_care["fcp"] == round(30 / 80, 8)


def test_zero_denominator_handling_returns_finite_zeroes():
    sam = _sample_sam()
    sam["government"] = 0.0
    classification = classify_sam_accounts(sam)
    shares = calibrate_share_parameters(sam, classification)

    gov_shares = shares["government_demand_shares"]["government"]
    assert gov_shares
    assert all(value == 0.0 for value in gov_shares.values())
    assert all(math.isfinite(value) for value in gov_shares.values())


def test_diagnostics_return_warnings_and_readiness():
    sam = _sample_sam()
    classification = classify_sam_accounts(sam)
    diagnostics = run_calibration_diagnostics(sam, classification, tolerance=1e-12)

    assert diagnostics["valid"] is True
    assert diagnostics["warnings"]
    assert "readiness" in diagnostics
    assert diagnostics["readiness"]["sam_multiplier_analysis"] == "ready"


def test_calibrate_signal_cge_returns_expected_keys():
    result = calibrate_signal_cge(_sample_sam())

    assert {
        "account_classification",
        "benchmark_flows",
        "share_parameters",
        "diagnostics",
        "warnings",
        "cge_readiness_status",
    } <= set(result)
    assert result["benchmark_flows"]["factor_payments"]["fcp"]["care_activity"] == 30


def test_model_core_calibration_delegates_to_pipeline():
    from cge_workbench.model_core.calibration import calibrate_from_sam

    result = calibrate_from_sam(_sample_sam())

    assert "calibration_dataset" in result
    assert result["calibration_dataset"]["cge_readiness_status"]


def test_app_import_still_works():
    import app

    assert app.demo is not None
