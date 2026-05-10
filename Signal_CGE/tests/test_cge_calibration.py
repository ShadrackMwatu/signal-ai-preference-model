import numpy as np
import pandas as pd

from cge_workbench.equilibrium_solver.calibration import (
    calibrate_static_cge,
    default_static_sam,
    identify_accounts,
    validate_sam_balance,
)


def test_sam_balance_validation_works():
    sam = default_static_sam()
    validation = validate_sam_balance(sam)
    assert validation["balanced"] is True
    assert validation["max_absolute_imbalance"] == 0.0


def test_account_identification_and_calibration_are_finite():
    sam = default_static_sam()
    groups = identify_accounts(sam)
    assert groups["activities"]
    assert groups["commodities"]
    assert groups["factors"]
    calibration = calibrate_static_cge(sam)
    numeric_values = []
    for section in ["benchmark", "tax_rates", "elasticities"]:
        numeric_values.extend(float(value) for value in calibration[section].values())
    assert all(np.isfinite(value) for value in numeric_values)
    assert calibration["benchmark"]["commodity_price"] == 1.0


def test_non_square_sam_validation_fails():
    bad_sam = pd.DataFrame([[1, 2, 3], [4, 5, 6]], index=["a", "b"], columns=["a", "b", "c"])
    try:
        calibrate_static_cge(bad_sam)
    except ValueError as exc:
        assert "square" in str(exc)
    else:
        raise AssertionError("Expected non-square SAM to fail")
