from __future__ import annotations

import importlib

import pandas as pd

from cge_workbench.model_core import calibrate_from_sam, get_equation_registry, validate_closure_rules
from cge_workbench.model_core.model_equations import EXPECTED_BLOCKS, validate_equation_registry


MODULES = [
    "cge_workbench.model_core.production_block",
    "cge_workbench.model_core.household_block",
    "cge_workbench.model_core.government_block",
    "cge_workbench.model_core.investment_savings_block",
    "cge_workbench.model_core.trade_block",
    "cge_workbench.model_core.factor_market_block",
    "cge_workbench.model_core.price_block",
    "cge_workbench.model_core.market_clearing_block",
    "cge_workbench.model_core.closure_system",
    "cge_workbench.model_core.calibration",
    "cge_workbench.model_core.model_equations",
]


def test_all_model_core_modules_import():
    for module_name in MODULES:
        assert importlib.import_module(module_name)


def test_calibration_accepts_sam_like_dataframe():
    sam = pd.DataFrame(
        [
            [0.0, 10.0, 5.0, 2.0],
            [8.0, 0.0, 4.0, 1.0],
            [6.0, 3.0, 0.0, 2.0],
            [3.0, 0.0, 1.0, 0.0],
        ],
        index=["care_activity", "household", "government", "fcp"],
        columns=["care_activity", "household", "government", "fcp"],
    )

    calibration = calibrate_from_sam(sam)

    assert calibration["accounts"] == ["care_activity", "household", "government", "fcp"]
    assert "care_activity" in calibration["activities"]
    assert "household" in calibration["households"]
    assert calibration["total_flow"] > 0
    assert "share_parameters" in calibration


def test_closure_rules_validate():
    valid = validate_closure_rules({"government": "government_deficit_closure"})
    invalid = validate_closure_rules({"government": "unsupported_rule"})

    assert valid["valid"] is True
    assert invalid["valid"] is False
    assert invalid["errors"]


def test_model_equation_registry_returns_expected_blocks():
    registry = get_equation_registry(
        {
            "activities": ["care_activity"],
            "commodities": ["care_commodity"],
            "factors": ["fcp"],
            "households": ["household"],
            "accounts": ["care_activity", "household", "government", "imports", "exports"],
        }
    )

    assert registry["model"] == "Signal CGE Model"
    assert set(EXPECTED_BLOCKS).issubset(registry["blocks"])
    assert validate_equation_registry(registry)["valid"] is True
    for block in EXPECTED_BLOCKS:
        assert registry["blocks"][block]["equations"]
