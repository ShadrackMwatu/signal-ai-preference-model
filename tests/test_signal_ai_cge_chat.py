from __future__ import annotations

from cge_workbench.interpreters.natural_language_to_scenario import parse_scenario_prompt
from policy_ai.policy_brief_service import generate_policy_summary
from signal_ai.conversation_engine.chat_orchestrator import run_chat_simulation
from signal_ai.prompt_router.intent_classifier import classify_intent
from signal_ai.reasoning.economic_reasoner import validate_policy_shock


def test_intent_classification_for_simulation_prompt():
    intent = classify_intent("run infrastructure investment shock")

    assert intent["intent"] == "run_simulation"
    assert intent["domain"] == "infrastructure"


def test_natural_language_scenario_compiler_new_fields():
    scenario = parse_scenario_prompt("double care infrastructure").to_dict()

    assert scenario["model"] == "Signal CGE Workbench"
    assert scenario["shock_type"] == "care_infrastructure"
    assert scenario["shock_size"] == 100
    assert scenario["shock_account"] == "care_infrastructure"
    assert "target_outputs" in scenario


def test_government_spending_care_prompt():
    scenario = parse_scenario_prompt("increase government spending on care services by 10 percent").to_dict()

    assert scenario["shock_type"] == "government_spending"
    assert scenario["shock_size"] == 10
    assert "fcp" in scenario["target_accounts"]


def test_economic_reasoning_warnings_include_fallback_caveat():
    scenario = parse_scenario_prompt("simulate VAT increase").to_dict()

    validation = validate_policy_shock(scenario)

    assert validation["valid"] is True
    assert any("SAM multiplier" in warning for warning in validation["warnings"])


def test_chat_orchestrator_returns_expected_keys():
    result = run_chat_simulation("increase government spending on care services by 10 percent")

    assert {"scenario", "diagnostics", "results", "explanation", "policy_summary", "warnings"} <= set(result)
    assert result["scenario"]["shock_type"] == "government_spending"


def test_policy_brief_generation():
    scenario = parse_scenario_prompt("run infrastructure investment shock").to_dict()
    summary = generate_policy_summary(
        scenario,
        {"accounts": {"infrastructure": 12.0}},
        {"validation": {"warnings": ["screening warning"]}},
    )

    assert "executive_summary" in summary
    assert summary["likely_winners"] == ["infrastructure"]
    assert summary["suggested_next_simulations"]


def test_app_import_still_works():
    import app

    assert app.demo is not None
