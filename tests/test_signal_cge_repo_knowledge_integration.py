"""Tests for Signal CGE repository knowledge integration."""

from __future__ import annotations

from pathlib import Path

from app_routes.signal_cge_route import run_signal_cge_prompt
from signal_cge.knowledge.document_loader import load_knowledge_base, load_model_profile, load_reference_bundle
from signal_cge.knowledge.scenario_context import get_scenario_context
from signal_cge.scenarios.scenario_schema import parse_scenario_prompt


def test_knowledge_loader_reads_repo_docs() -> None:
    profile = load_model_profile()
    knowledge_base = load_knowledge_base()
    bundle = load_reference_bundle()

    assert profile["model_identity"] == "Signal CGE"
    assert "Signal CGE Philosophy" in knowledge_base
    assert "equations/TRADE_BLOCK.md" in bundle
    assert "calibration/CALIBRATION_PIPELINE.md" in bundle


def test_scenario_context_returns_trade_references_for_tariff_shock() -> None:
    scenario = parse_scenario_prompt("reduce import tariffs on cmach by 10%").to_dict()
    context = get_scenario_context(scenario)
    paths = [item["path"] for item in context["references"]]

    assert any("TRADE_BLOCK.md" in path for path in paths)
    assert any("GOVERNMENT_BLOCK.md" in path for path in paths)
    assert any("PRICE_BLOCK.md" in path for path in paths)
    assert any("EXPERIMENT_WORKFLOW.md" in path for path in paths)


def test_run_signal_cge_prompt_includes_knowledge_context_and_trace() -> None:
    result = run_signal_cge_prompt("reduce import tariffs on cmach by 10%")

    assert "knowledge_context" in result
    assert "Trade Block" in result["knowledge_context"]["reference_labels"]
    assert "Model Reference Used" not in result["knowledge_context"]["reference_labels"]
    assert result["diagnostics"]["knowledge_references_used"]


def test_tariff_prompt_returns_improved_interpretation() -> None:
    result = run_signal_cge_prompt("reduce import tariffs on cmach by 10%")
    interpretation = result["interpretation"]["transmission_mechanism"]

    assert "cmach" in interpretation
    assert "import tax wedge" in interpretation
    assert "government tariff revenue may fall" in interpretation
    assert "trade-balance effects are ambiguous" in interpretation
    assert "future solver" in " ".join(result["interpretation"]["caveats"])


def test_fallback_results_are_prototype_directional_indicators() -> None:
    result = run_signal_cge_prompt("reduce import tariffs on cmach by 10%")

    assert result["result_type"] == "prototype_directional_indicator"
    assert result["results"]["result_type"] == "prototype_directional_indicator"
    assert "Prototype result" in result["fallback_message"]


def test_gender_care_impact_hidden_for_cmach_tariff() -> None:
    result = run_signal_cge_prompt("reduce import tariffs on cmach by 10%")

    assert result["results"]["gender-care impact"] == "Not applicable to this scenario."


def test_ui_output_includes_model_reference_used() -> None:
    import app

    outputs = app.signal_cge_prompt_ui("reduce import tariffs on cmach by 10%", None)

    assert "Trade Block loaded" in outputs[3]
    assert "Solver limitation note loaded" in outputs[3]


def test_downloadable_report_includes_knowledge_trace() -> None:
    result = run_signal_cge_prompt("reduce import tariffs on cmach by 10%")
    report = Path(result["downloads"]["policy_brief_md"]).read_text(encoding="utf-8")
    json_text = Path(result["downloads"]["results_json"]).read_text(encoding="utf-8")

    assert "Knowledge Trace" in report
    assert "Suggested Model Improvements" in report
    assert "knowledge_context" in json_text
    assert "learning_event_id" in json_text
