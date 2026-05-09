"""Tests for Signal product-domain ownership and app routing."""

from __future__ import annotations

from pathlib import Path


def test_app_imports_and_public_tabs_are_two_domains() -> None:
    import app

    assert hasattr(app, "demo")
    assert app.get_public_tab_labels() == ["Behavioral Signals AI", "Signal CGE"]


def test_behavioral_route_imports_without_cge_dependencies() -> None:
    from app_routes.behavioral_route import run_behavioral_signal_prediction

    result = run_behavioral_signal_prediction(120, 35, 24, 160, 0.55, 0.7, 0.35)

    assert result["route_domain"] == "Behavioral Signals AI"
    assert "demand_classification" in result
    source = Path("app_routes/behavioral_route.py").read_text(encoding="utf-8")
    for cge_only in ["signal_cge", "signal_ai", "policy_ai", "cge_workbench"]:
        assert cge_only not in source


def test_signal_cge_route_imports_without_behavioral_dependencies() -> None:
    from app_routes.signal_cge_route import run_signal_cge_prompt

    result = run_signal_cge_prompt("reduce import tariffs on cmach by 10%")

    assert result["scenario"]["target_account"] == "cmach"
    assert result["backend_used"] == "python_sam_multiplier"
    source = Path("app_routes/signal_cge_route.py").read_text(encoding="utf-8")
    for behavioral_only in ["behavioral_ai", "adaptive_learning", "live_trends"]:
        assert behavioral_only not in source


def test_signal_cge_loads_canonical_model_profile_without_upload() -> None:
    from app_routes.signal_cge_route import run_signal_cge_prompt

    result = run_signal_cge_prompt("reduce import tariffs on cmach by 10%")

    assert result["diagnostics"]["model_profile_loaded"] is True
    assert (
        result["diagnostics"]["canonical_model_profile"]
        == "Signal_CGE/models/canonical/signal_cge_master/model_profile.yaml"
    )
    assert result["diagnostics"]["uploaded_sam"].startswith("not provided")
    assert result["results"]["account_effects"]


def test_domain_map_documents_expected_ownership() -> None:
    text = Path("Documentation/SIGNAL_PRODUCT_DOMAIN_MAP.md").read_text(encoding="utf-8")

    assert "Behavioral Signals AI" in text
    assert "Signal CGE" in text
    assert "Legacy / compatibility" in text
    assert "`Signal_CGE/`" in text
    assert "`Behavioral_Signals_AI/`" in text
