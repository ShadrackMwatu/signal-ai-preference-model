from pathlib import Path

from cge_workbench.equilibrium_solver.calibration import calibrate_static_cge, default_static_sam
from cge_workbench.equilibrium_solver.equations import build_variable_vector, equilibrium_residuals
from cge_workbench.equilibrium_solver.solver import solve_baseline, solve_static_cge


def test_baseline_residuals_are_near_zero():
    calibration = calibrate_static_cge(default_static_sam())
    residuals = equilibrium_residuals(build_variable_vector(calibration), calibration)
    assert max(abs(value) for value in residuals) < 1e-10


def test_static_solver_converges_on_default_sam():
    result = solve_static_cge(default_static_sam())
    assert result["success"] is True
    assert result["residual_norm"] < 1e-6
    assert result["max_abs_residual"] < 1e-6
    assert result["message"].startswith("Signal Static CGE Solver active")


def test_tariff_shock_changes_trade_and_fiscal_values():
    result = solve_static_cge(
        default_static_sam(),
        {"shock_type": "import_tariff_change", "target_account": "cmach", "shock_value": -10, "shock_unit": "percent"},
    )
    assert result["success"] is True
    changes = result["percentage_changes"]
    assert changes["imports"] > 0
    assert changes["government_revenue"] < 0


def test_comparison_and_diagnostics_outputs_are_created():
    result = solve_static_cge(default_static_sam())
    assert "percentage_changes" in result
    assert result["tables"]["percentage_change_table"]
    assert Path("cge_workbench/outputs/latest_diagnostics.json").exists()
    assert Path(result["downloads"]["results_json"]).exists()
    assert Path(result["downloads"]["percentage_changes_csv"]).exists()
    assert Path(result["downloads"]["policy_brief_md"]).exists()


def test_app_import_still_works():
    import app

    assert app.get_public_tab_labels() == ["Behavioral Signals AI", "Signal CGE"]
