"""Regression tests for the two-domain Signal repository layout."""

from __future__ import annotations

from pathlib import Path


def test_app_imports_with_two_public_tabs() -> None:
    import app

    assert hasattr(app, "demo")
    assert app.get_public_tab_labels() == ["Behavioral Signals AI", "Signal CGE"]


def test_behavioral_route_uses_behavioral_domain() -> None:
    from app_routes.behavioral_route import run_behavioral_signal_prediction

    result = run_behavioral_signal_prediction(100, 25, 15, 80, 0.4, 0.5, 0.3)
    source = Path("app_routes/behavioral_route.py").read_text(encoding="utf-8")

    assert result["route_domain"] == "Behavioral Signals AI"
    assert "Behavioral_Signals_AI" in source


def test_signal_cge_route_uses_signal_cge_domain() -> None:
    from app_routes.signal_cge_route import run_signal_cge_prompt

    result = run_signal_cge_prompt("reduce import tariffs on cmach by 10%")
    source = Path("app_routes/signal_cge_route.py").read_text(encoding="utf-8")

    assert result["scenario"]["target_account"] == "cmach"
    assert "Signal_CGE" in source


def test_signal_cge_canonical_model_profile_loads() -> None:
    from Signal_CGE.signal_cge.knowledge.document_loader import MODEL_PROFILE_PATH, load_model_profile

    profile = load_model_profile()

    assert MODEL_PROFILE_PATH.exists()
    assert "model_type" in profile
    assert "Signal_CGE/models/canonical" in str(MODEL_PROFILE_PATH).replace("\\", "/")


def test_compatibility_imports_still_work() -> None:
    import adaptive_learning
    import cge_core.calibration
    import cge_workbench
    import explainability
    import policy_ai.policy_brief_service
    import signal_ai.conversation_engine.chat_orchestrator
    import signal_cge.knowledge.document_loader
    import sml_workbench.parser.sml_parser
    import solvers.solver_registry

    assert adaptive_learning
    assert explainability
    assert cge_workbench


def test_domain_folders_exist() -> None:
    assert Path("Behavioral_Signals_AI/behavioral_ai").exists()
    assert Path("Behavioral_Signals_AI/live_trends").exists()
    assert Path("Signal_CGE/signal_cge").exists()
    assert Path("Signal_CGE/signal_ai").exists()
    assert Path("Signal_CGE/models/canonical/signal_cge_master/model_profile.yaml").exists()
