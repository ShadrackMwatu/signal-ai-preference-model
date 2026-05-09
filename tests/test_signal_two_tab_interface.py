"""Tests for the simplified two-tab Signal public interface."""

from __future__ import annotations

from pathlib import Path
import uuid

import pandas as pd


def test_app_imports_successfully() -> None:
    import app

    assert hasattr(app, "demo")


def test_public_interface_exposes_two_tabs_only() -> None:
    import app

    assert app.get_public_tab_labels() == ["Behavioral Signals AI", "Signal CGE"]


def test_old_cge_tabs_are_not_publicly_exposed() -> None:
    import app

    public_tabs = app.get_public_tab_labels()
    for hidden_tab in app.HIDDEN_PUBLIC_TABS:
        assert hidden_tab not in public_tabs

    source = Path("app.py").read_text(encoding="utf-8")
    assert 'with gr.Tab("Signal CGE Framework")' not in source
    assert 'with gr.Tab("AI CGE Chat Studio")' not in source
    assert 'with gr.Tab("SML CGE Workbench")' not in source
    assert 'with gr.Tab("Learning")' not in source


def test_run_signal_cge_prompt_without_upload() -> None:
    import app

    result = app.run_signal_cge_prompt("Simulate a 10 percent increase in government spending on care infrastructure.")

    assert {"scenario", "readiness", "diagnostics", "results", "interpretation"}.issubset(result)
    assert result["readiness"]["sam_multiplier_readiness"] == "ready"
    assert app.FULL_CGE_FALLBACK_MESSAGE in result["fallback_message"]


def test_run_signal_cge_prompt_with_mock_sam() -> None:
    import app

    scratch = Path("tests/_tmp")
    scratch.mkdir(parents=True, exist_ok=True)
    sam_path = scratch / f"mock_sam_{uuid.uuid4().hex}.csv"
    sam = pd.DataFrame(
        [[0, 10, 5], [8, 0, 4], [6, 3, 0]],
        index=["cmach", "households", "government"],
        columns=["cmach", "households", "government"],
        dtype=float,
    )
    sam.to_csv(sam_path)

    result = app.run_signal_cge_prompt("reduce import tariffs on cmach by 10%", uploaded_file=str(sam_path))

    assert result["scenario"]["target_account_sector"] == "cmach"
    assert result["results"]["account_effects"]
    assert result["diagnostics"]["uploaded_sam"] == "provided"


def test_tariff_prompt_is_parsed_correctly() -> None:
    import app

    result = app.run_signal_cge_prompt("reduce import tariffs on cmach by 10%")
    scenario = result["scenario"]
    raw = scenario["raw_scenario"]

    assert scenario["policy_shock"] == "import tariff"
    assert scenario["target_account_sector"] == "cmach"
    assert scenario["shock_magnitude"] == "-10.0 percent"
    assert raw["policy_instrument"] == "import tariff"
    assert raw["target_commodity"] == "cmach"
    assert raw["shock_direction"] == "reduction"


def test_signal_cge_output_sections_and_fallback_message() -> None:
    import app

    result = app.run_signal_cge_prompt("reduce import tariffs on cmach by 10%")

    assert "scenario" in result
    assert "readiness" in result
    assert "diagnostics" in result
    assert "results" in result
    assert "interpretation" in result
    assert app.FULL_CGE_FALLBACK_MESSAGE in result["diagnostics"]["fallback_explanation"]
    assert result["backend_used"] == "python_sam_multiplier"
