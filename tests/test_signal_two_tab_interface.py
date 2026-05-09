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

    assert {"scenario", "readiness", "diagnostics", "results", "chart_data", "interpretation"}.issubset(result)
    assert result["readiness"]["sam_multiplier_readiness"] == "ready"
    assert app.FULL_CGE_FALLBACK_MESSAGE in result["fallback_message"]
    assert "canonical repo model profile" in result["fallback_message"]
    assert result["diagnostics"]["uploaded_sam"].startswith("not provided")


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
    assert scenario["policy_instrument"] == "import_tariff"
    assert scenario["target_account"] == "cmach"
    assert scenario["shock_direction"] == "decrease"
    assert scenario["shock_magnitude_percent"] == 10.0
    assert scenario["simulation_type"] == "trade_policy"
    assert raw["policy_instrument"] == "import_tariff"
    assert raw["target_account"] == "cmach"
    assert raw["target_commodity"] == "cmach"
    assert raw["shock_direction"] == "decrease"
    assert raw["shock_magnitude_percent"] == 10.0


def test_signal_cge_output_sections_and_fallback_message() -> None:
    import app

    result = app.run_signal_cge_prompt("reduce import tariffs on cmach by 10%")

    assert "scenario" in result
    assert "readiness" in result
    assert "diagnostics" in result
    assert "results" in result
    assert "results_table" in result
    assert "chart_data" in result
    assert "interpretation" in result
    assert "learning_trace" in result
    assert app.FULL_CGE_FALLBACK_MESSAGE in result["diagnostics"]["fallback_explanation"]
    assert result["backend_used"] == "python_sam_multiplier"
    assert result["learning_trace"]["learning_event_recorded"] == "yes"


def test_tariff_winners_do_not_include_government_when_revenue_falls() -> None:
    import app

    result = app.run_signal_cge_prompt("reduce import tariffs on cmach by 10%")
    winners = result["interpretation"]["winners_and_losers"]["likely_winners"]
    losers = result["interpretation"]["winners_and_losers"]["likely_losers"]

    assert "government tariff revenue" not in winners
    assert "government tariff revenue" in losers
    assert "machinery-using sectors" in winners


def test_chart_data_and_download_files_are_created() -> None:
    import app

    result = app.run_signal_cge_prompt("reduce import tariffs on cmach by 10%")

    assert result["chart_data"]
    assert result["results_table"]
    assert {row["metric"] for row in result["chart_data"]} >= {
        "GDP/output",
        "Household income",
        "Government balance",
        "Imports",
        "Exports",
        "Welfare/proxy welfare",
    }
    assert Path(result["downloads"]["results_json"]).name == "signal_cge_results.json"
    assert Path(result["downloads"]["results_csv"]).name == "signal_cge_results.csv"
    assert Path(result["downloads"]["policy_brief_md"]).name == "signal_cge_policy_brief.md"
    for file_path in result["downloads"].values():
        assert Path(file_path).exists()

    json_text = Path(result["downloads"]["results_json"]).read_text(encoding="utf-8")
    brief_text = Path(result["downloads"]["policy_brief_md"]).read_text(encoding="utf-8")
    csv_text = Path(result["downloads"]["results_csv"]).read_text(encoding="utf-8")
    assert "results_table" in json_text
    assert "model_references_used" in json_text
    assert "learning_trace" in json_text
    assert "prototype_directional_indicator" in json_text
    assert "Adaptive Learning Trace" in brief_text
    assert "Trade/import pressure" in csv_text
