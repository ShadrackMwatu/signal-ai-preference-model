from __future__ import annotations

from Signal_CGE.signal_cge.solvers.static_equilibrium_solver import (
    calibration_from_sam_path,
    solve_static_equilibrium,
)


def _tariff_scenario() -> dict[str, object]:
    return {
        "policy_instrument": "import_tariff",
        "shock_type": "import_tariff",
        "target_account": "cmach",
        "target_commodity": "cmach",
        "shock_direction": "decrease",
        "shock_magnitude_percent": 10.0,
        "shock_size": -10.0,
    }


def test_benchmark_calibration_solves_and_replication_passes() -> None:
    result = solve_static_equilibrium(calibration_from_sam_path(), _tariff_scenario())

    assert result["success"] is True
    assert result["result_type"] == "validated_static_equilibrium_cge_solver"
    assert result["validation"]["checks"]["base_year_replication"] is True
    assert result["diagnostics"]["benchmark_replication_check"]["passed"] is True


def test_tariff_shock_solves_with_low_residual() -> None:
    result = solve_static_equilibrium(calibration_from_sam_path(), _tariff_scenario())

    assert result["diagnostics"]["converged"] is True
    assert result["diagnostics"]["residual_norm"] < 1e-4
    assert result["percentage_changes"]["import_price_change_pct"] < 0
    assert result["percentage_changes"]["government_tariff_revenue_change_pct"] < 0


def test_validation_gate_prevents_false_validated_label() -> None:
    bad_calibration = {
        "account_classification": {"activities": ["a"], "commodities": [], "factors": []},
        "benchmark_flows": {},
        "share_parameters": {},
        "diagnostics": {
            "max_absolute_imbalance": 10.0,
            "negative_value_count": 0,
            "zero_column_accounts": [],
        },
    }

    result = solve_static_equilibrium(bad_calibration, _tariff_scenario())

    assert result["success"] is False
    assert result["result_type"] == "validation_failed"
    assert result["result_type"] != "validated_static_equilibrium_cge_solver"


def test_route_uses_validated_static_solver() -> None:
    from app_routes.signal_cge_route import run_signal_cge_prompt

    result = run_signal_cge_prompt("reduce import tariffs on cmach by 10%")

    assert result["solver_used"] == "Validated open-source static equilibrium CGE solver"
    assert result["backend_used"] == "validated_static_equilibrium_cge_solver"
    assert result["diagnostics"]["equilibrium_solver"]["benchmark_replication_check"]["passed"] is True


def test_route_falls_back_when_validation_fails(monkeypatch) -> None:
    import app_routes.signal_cge_route as route

    def failed_static_solver(*args, **kwargs):
        return {
            "success": False,
            "result_type": "validation_failed",
            "reason": "forced validation failure",
            "diagnostics": {"converged": False, "failed_equations": ["forced"]},
        }

    monkeypatch.setattr(route, "solve_static_equilibrium", failed_static_solver)
    result = route.run_signal_cge_prompt("reduce import tariffs on cmach by 10%")

    assert result["result_type"] in {"open_source_equilibrium_cge_prototype", "prototype_directional_indicator"}
    assert result["result_type"] != "validated_static_equilibrium_cge_solver"


def test_app_imports_with_validated_static_solver() -> None:
    import app

    assert app.get_public_tab_labels() == ["Behavioral Signals AI", "Signal CGE"]
