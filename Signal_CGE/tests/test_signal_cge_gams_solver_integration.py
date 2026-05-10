from __future__ import annotations

from pathlib import Path


def test_app_imports_when_gams_is_unavailable() -> None:
    import app

    assert app.get_public_tab_labels() == ["Behavioral Signals AI", "Signal CGE"]


def test_gams_runner_detects_status_gracefully(monkeypatch) -> None:
    from Signal_CGE.signal_cge.solvers import gams_runner

    monkeypatch.delenv("GAMS_PATH", raising=False)
    monkeypatch.setattr(gams_runner.shutil, "which", lambda _name: None)
    status = gams_runner.get_gams_status()

    assert status["backend"] == "gams_optional_solver"
    assert status["status"] == "unavailable"
    assert status["available"] is False


def test_solver_registry_includes_gams_optional_backend() -> None:
    from Signal_CGE.signal_cge.solvers.solver_registry import get_solver_registry

    registry = get_solver_registry()

    assert "validated_static_equilibrium_solver" in registry
    assert "open_source_equilibrium_solver" in registry
    assert "python_sam_multiplier" in registry
    assert "gams_optional_solver" in registry


def test_model_registry_reports_gams_status() -> None:
    from Signal_CGE.signal_cge.model_registry import get_model_registry

    registry = get_model_registry()

    assert "gams_optional_solver" in registry["solver_registry"]
    assert "gams_optional_solver" in registry["current_solver_options"]


def test_signal_cge_fallback_works_when_gams_unavailable(monkeypatch) -> None:
    from Signal_CGE.signal_cge.solvers import gams_runner
    from app_routes.signal_cge_route import run_signal_cge_prompt

    monkeypatch.delenv("GAMS_PATH", raising=False)
    monkeypatch.setattr(gams_runner.shutil, "which", lambda _name: None)
    result = run_signal_cge_prompt("reduce import tariffs on cmach by 10%")

    assert result["backend_used"] in {
        "validated_static_equilibrium_cge_solver",
        "open_source_equilibrium_solver",
        "python_sam_multiplier",
    }
    assert result["diagnostics"]["available_solvers"]["gams_optional_solver"]["status"] in {"available", "unavailable"}


def test_no_gams_license_files_are_required() -> None:
    sensitive = ["gamslice.txt", "gamslice.dat"]

    for name in sensitive:
        assert not Path(name).exists()
