from __future__ import annotations

from Signal_CGE.signal_cge.solvers.equilibrium_solver import solve_static_equilibrium


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


def test_equilibrium_solver_imports_and_solves_simple_benchmark() -> None:
    result = solve_static_equilibrium(None, _tariff_scenario(), "base_closure")

    assert result["success"] is True
    assert result["result_type"] == "open_source_equilibrium_cge_prototype"
    assert result["diagnostics"]["converged"] is True
    assert result["diagnostics"]["residual_norm"] < 1e-6


def test_tariff_shock_changes_import_related_indicators() -> None:
    result = solve_static_equilibrium(None, _tariff_scenario(), "base_closure")
    changes = result["percentage_changes"]

    assert changes["import_price_change_pct"] < 0
    assert changes["import_demand_change_pct"] != 0
    assert changes["government_tariff_revenue_change_pct"] < 0
    assert "trade_balance_change_pct" in changes


def test_solver_returns_convergence_diagnostics() -> None:
    result = solve_static_equilibrium(None, _tariff_scenario(), "base_closure")
    diagnostics = result["diagnostics"]

    assert diagnostics["function_evaluations"] > 0
    assert len(diagnostics["equations_solved"]) == 10
    assert len(diagnostics["variables_solved"]) == 10
    assert diagnostics["closure_used"] == "base_closure"
    assert diagnostics["benchmark_replication_check"]


def test_route_uses_equilibrium_solver_when_payload_is_sufficient() -> None:
    from app_routes.signal_cge_route import run_signal_cge_prompt

    result = run_signal_cge_prompt("reduce import tariffs on cmach by 10%")

    assert result["backend_used"] == "validated_static_equilibrium_cge_solver"
    assert result["solver_used"] == "Validated open-source static equilibrium CGE solver"
    assert result["result_type"] == "validated_static_equilibrium_cge_solver"
    assert result["diagnostics"]["equilibrium_solver"]["converged"] is True


def test_route_falls_back_when_equilibrium_solver_fails(monkeypatch) -> None:
    import app_routes.signal_cge_route as route

    def failed_solver(*args, **kwargs):
        return {
            "success": False,
            "reason": "forced test failure",
            "diagnostics": {
                "converged": False,
                "residual_norm": 1.0,
                "equations_solved": [],
                "variables_solved": [],
                "failed_equations": ["forced"],
            },
        }

    monkeypatch.setattr(route, "solve_static_equilibrium", failed_solver)
    result = route.run_signal_cge_prompt("reduce import tariffs on cmach by 10%")

    assert result["backend_used"] in {"open_source_equilibrium_solver", "python_sam_multiplier"}
    assert result["result_type"] in {"open_source_equilibrium_cge_prototype", "prototype_directional_indicator"}


def test_app_imports_with_equilibrium_solver() -> None:
    import app

    assert app.get_public_tab_labels() == ["Behavioral Signals AI", "Signal CGE"]
