from __future__ import annotations

import pandas as pd

from cge_workbench.calibration import (
    build_calibration_dataset,
    calibrate_share_parameters,
    classify_sam_accounts,
    extract_benchmark_flows,
    run_calibration_diagnostics,
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
        "imports",
        "exports",
        "vat_tax",
    ]
    data = pd.DataFrame(0.0, index=accounts, columns=accounts)
    data.loc["care_commodity", "care_activity"] = 20
    data.loc["manufacturing_commodity", "care_activity"] = 10
    data.loc["fcp", "care_activity"] = 30
    data.loc["mcp", "care_activity"] = 20
    data.loc["care_commodity", "manufacturing_activity"] = 5
    data.loc["manufacturing_commodity", "manufacturing_activity"] = 30
    data.loc["fcp", "manufacturing_activity"] = 10
    data.loc["mcp", "manufacturing_activity"] = 25
    data.loc["care_commodity", "household_rural"] = 40
    data.loc["manufacturing_commodity", "household_rural"] = 60
    data.loc["care_commodity", "government"] = 15
    data.loc["manufacturing_commodity", "government"] = 5
    data.loc["care_commodity", "investment"] = 12
    data.loc["manufacturing_commodity", "investment"] = 18
    data.loc["imports", "care_commodity"] = 8
    data.loc["imports", "manufacturing_commodity"] = 12
    data.loc["care_commodity", "exports"] = 7
    data.loc["manufacturing_commodity", "exports"] = 13
    data.loc["vat_tax", "care_activity"] = 3
    data.loc["vat_tax", "manufacturing_activity"] = 6
    return data


def test_account_classification_identifies_major_account_groups():
    classification = classify_sam_accounts(_sample_sam())

    assert "care_activity" in classification.activities
    assert "care_commodity" in classification.commodities
    assert "fcp" in classification.factors
    assert "household_rural" in classification.households
    assert "government" in classification.government
    assert "investment" in classification.investment
    assert "imports" in classification.imports
    assert "exports" in classification.exports
    assert "vat_tax" in classification.taxes


def test_benchmark_flow_extraction_returns_expected_slices():
    sam = _sample_sam()
    classification = classify_sam_accounts(sam)
    flows = extract_benchmark_flows(sam, classification)

    assert flows["factor_payments"]["fcp"]["care_activity"] == 30
    assert flows["household_consumption"]["care_commodity"]["household_rural"] == 40
    assert flows["government_demand"]["care_commodity"]["government"] == 15
    assert flows["investment_demand"]["manufacturing_commodity"]["investment"] == 18
    assert flows["tax_payments"]["vat_tax"]["manufacturing_activity"] == 6


def test_share_parameter_calibration_for_main_blocks():
    sam = _sample_sam()
    classification = classify_sam_accounts(sam)
    shares = calibrate_share_parameters(sam, classification)

    assert round(shares["production"]["care_activity"]["fcp"], 6) == round(30 / 80, 6)
    assert round(shares["household_demand"]["household_rural"]["care_commodity"], 6) == 0.4
    assert round(shares["government_demand"]["government"]["care_commodity"], 6) == 0.75
    assert round(shares["investment_demand"]["investment"]["manufacturing_commodity"], 6) == 0.6
    assert shares["trade_imports"]["imports"]["manufacturing_commodity"] == 0.6
    assert round(shares["factor_payments"]["care_activity"]["mcp"], 6) == round(20 / 50, 6)


def test_calibration_diagnostics_include_placeholder_warning():
    sam = _sample_sam()
    classification = classify_sam_accounts(sam)
    diagnostics = run_calibration_diagnostics(sam, classification)

    assert diagnostics["valid"] is True
    assert any("placeholders" in warning for warning in diagnostics["warnings"])
    assert diagnostics["max_absolute_imbalance"] >= 0


def test_build_calibration_dataset_integrates_all_outputs():
    dataset = build_calibration_dataset(_sample_sam())

    assert dataset["model"] == "Signal CGE Model"
    assert dataset["status"] == "calibration_prototype"
    assert "classification" in dataset
    assert "benchmark_flows" in dataset
    assert "share_parameters" in dataset
    assert "diagnostics" in dataset
    assert "model_core_summary" in dataset
