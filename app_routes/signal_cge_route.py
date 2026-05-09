"""Signal CGE route.

This module intentionally depends on Signal CGE packages only. It does not
import behavioral-only packages.
"""

from __future__ import annotations

import csv
from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

from signal_ai.conversation_engine.chat_orchestrator import run_chat_simulation
from signal_cge.diagnostics.model_readiness import get_model_readiness
from signal_cge.knowledge.document_loader import load_model_profile
from signal_cge.knowledge.reference_index import build_reference_index
from signal_cge.knowledge.scenario_context import get_scenario_context
from signal_cge.learning.adaptive_rules import apply_adaptive_prompt_rules
from signal_cge.learning.model_improvement_suggestions import generate_model_improvement_suggestions
from signal_cge.learning.simulation_memory import record_simulation_learning_event


FULL_CGE_FALLBACK_MESSAGE = (
    "Prototype result: full equilibrium CGE solver is not yet active. Signal is using the available "
    "SAM multiplier/prototype backend and canonical repo model profile."
)


def run_signal_cge_prompt(prompt: str, uploaded_file: Any | None = None) -> dict[str, Any]:
    """Run Signal CGE from repo-stored canonical files by default."""

    sam_path = _uploaded_path(uploaded_file)
    model_profile = load_model_profile()
    reference_index = build_reference_index()
    result = run_chat_simulation(prompt or "Run baseline Signal CGE scenario", sam_file=sam_path)
    scenario = result.get("scenario", {})
    adaptive_hints = apply_adaptive_prompt_rules(prompt, scenario)
    readiness = get_model_readiness()
    knowledge_context = get_scenario_context(scenario)
    diagnostics = {
        **result.get("diagnostics", {}),
        "model_profile_loaded": True,
        "reference_sections": reference_index.get("sections", []),
        "canonical_model_profile": "models/canonical/signal_cge_master/model_profile.yaml",
        "uploaded_sam": "provided" if sam_path else "not provided; using canonical profile and fallback SAM where needed",
        "fallback_explanation": FULL_CGE_FALLBACK_MESSAGE,
        "adaptive_rules": adaptive_hints,
        "knowledge_references_used": knowledge_context["reference_labels"],
    }
    structured_results = _structured_results(result.get("results", {}), scenario)
    chart_data = _chart_data(structured_results)
    interpretation = _policy_interpretation(result, knowledge_context, adaptive_hints)
    model_improvements = generate_model_improvement_suggestions()
    learning_event = record_simulation_learning_event(
        {
            "prompt": prompt,
            "scenario": scenario,
            "backend_used": structured_results.get("backend"),
            "readiness_status": readiness,
            "diagnostics_summary": _diagnostics_summary(diagnostics),
            "result_summary": _result_summary(structured_results),
            "interpretation_summary": interpretation,
            "caveats": interpretation.get("caveats", []),
            "recommended_next_simulations": interpretation.get("recommended_next_simulations", []),
            "knowledge_references_used": knowledge_context["reference_labels"],
        }
    )
    downloads = _write_downloads(
        prompt=prompt,
        scenario=scenario,
        readiness=readiness,
        diagnostics=diagnostics,
        results=structured_results,
        interpretation=interpretation,
        model_profile=model_profile,
        knowledge_context=knowledge_context,
        learning_event_id=learning_event["event_id"],
        model_improvements=model_improvements,
    )
    backend = result.get("results", {}).get("backend") or result.get("backend") or "python_sam_multiplier"
    return {
        "scenario": _interpreted_scenario(scenario, result.get("results", {})),
        "readiness": readiness,
        "diagnostics": diagnostics,
        "results": structured_results,
        "chart_data": chart_data,
        "interpretation": interpretation,
        "knowledge_context": knowledge_context,
        "model_improvement_suggestions": model_improvements,
        "learning_event_id": learning_event["event_id"],
        "result_type": "prototype_directional_indicator",
        "downloads": downloads,
        "backend_used": backend,
        "fallback_message": FULL_CGE_FALLBACK_MESSAGE,
    }


def _uploaded_path(file_obj: Any | None) -> str | None:
    if file_obj is None:
        return None
    return str(getattr(file_obj, "name", file_obj))


def _interpreted_scenario(scenario: dict[str, Any], results: dict[str, Any]) -> dict[str, Any]:
    return {
        "policy_shock": str(scenario.get("policy_instrument") or scenario.get("shock_type", "policy shock")).replace("_", " "),
        "policy_instrument": scenario.get("policy_instrument", scenario.get("shock_type", "")),
        "target_account": scenario.get("target_account", scenario.get("target_commodity", scenario.get("shock_account", ""))),
        "target_account_sector": scenario.get("target_account", scenario.get("target_commodity", scenario.get("shock_account", ""))),
        "shock_direction": scenario.get("shock_direction", "increase" if float(scenario.get("shock_size", 0) or 0) >= 0 else "decrease"),
        "shock_magnitude_percent": abs(float(scenario.get("shock_size", scenario.get("shock_value", 0)) or 0)),
        "shock_magnitude": f"{scenario.get('shock_size', scenario.get('shock_value', 0))} {scenario.get('shock_unit', 'percent')}",
        "simulation_type": scenario.get("simulation_type", "sam_multiplier"),
        "closure_assumption": scenario.get("closure", scenario.get("closure_rule", "standard_sam_multiplier")),
        "model_backend_used": results.get("backend", "python_sam_multiplier"),
        "raw_scenario": scenario,
    }


def _structured_results(results: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    accounts = results.get("accounts", {}) if isinstance(results, dict) else {}
    account_total = sum(float(value) for value in accounts.values()) if accounts else 0.0
    household_effect = sum(float(value) for account, value in accounts.items() if "household" in account.lower())
    trade_effect = sum(float(value) for account, value in accounts.items() if account.lower() in {"imports", "exports", "cmach"})
    government_effect = sum(float(value) for account, value in accounts.items() if "government" in account.lower())
    factor_effect = sum(
        float(value)
        for account, value in accounts.items()
        if any(term in account.lower() for term in ["labour", "labor", "capital", "fcp", "fcu", "fnp", "fnu", "mcp", "mcu", "mnp", "mnu"])
    )
    care_effect = sum(float(value) for account, value in accounts.items() if "care" in account.lower())
    return {
        "GDP/output effect": round(account_total, 6),
        "factor income effect": round(factor_effect, 6),
        "household income effect": round(household_effect, 6),
        "government balance effect": round(government_effect, 6),
        "trade effect": round(trade_effect, 6),
        "welfare/proxy welfare effect": round(household_effect or account_total, 6),
        "gender-care impact": round(care_effect, 6) if _is_care_relevant(scenario) else "Not applicable to this scenario.",
        "account_effects": accounts,
        "backend": results.get("backend", "python_sam_multiplier") if isinstance(results, dict) else "python_sam_multiplier",
        "result_type": "prototype_directional_indicator",
    }


def _chart_data(results: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"metric": "GDP/output", "effect": float(results.get("GDP/output effect", 0.0))},
        {"metric": "Household income", "effect": float(results.get("household income effect", 0.0))},
        {"metric": "Government balance", "effect": float(results.get("government balance effect", 0.0))},
        {"metric": "Imports", "effect": _account_effect(results, "imports")},
        {"metric": "Exports", "effect": _account_effect(results, "exports")},
        {"metric": "Welfare/proxy welfare", "effect": float(results.get("welfare/proxy welfare effect", 0.0))},
    ]


def _account_effect(results: dict[str, Any], account_name: str) -> float:
    accounts = results.get("account_effects", {})
    return float(accounts.get(account_name, 0.0)) if isinstance(accounts, dict) else 0.0


def _policy_interpretation(
    result: dict[str, Any],
    knowledge_context: dict[str, Any],
    adaptive_hints: dict[str, Any],
) -> dict[str, Any]:
    summary = result.get("policy_summary", {})
    scenario = result.get("scenario", {})
    transmission = summary.get("expected_transmission_channel", "")
    if scenario.get("shock_type") == "import_tariff":
        target = scenario.get("target_account") or scenario.get("target_commodity") or scenario.get("shock_account", "target commodity")
        transmission = (
            f"`{target}` is treated as the target commodity/account. A tariff reduction affects the import tax wedge; "
            "lower import tariffs may reduce import prices, government tariff revenue may fall, import demand may increase, "
            "machinery-using sectors may benefit through lower input or investment costs, domestic substitutes may face "
            "competitive pressure, and trade-balance effects are ambiguous without full equilibrium solving."
        )
    return {
        "transmission_mechanism": transmission,
        "winners_and_losers": {
            "likely_winners": summary.get("likely_winners", []),
            "likely_losers": ["Accounts facing higher relative costs or reduced demand, subject to SAM mapping."],
        },
        "risks": summary.get("likely_risks", []),
        "caveats": [
            summary.get("interpretation_caveat", ""),
            FULL_CGE_FALLBACK_MESSAGE,
            "Full equilibrium effects require the future solver.",
        ],
        "recommended_next_simulations": _recommended_next_simulations(summary, adaptive_hints),
        "knowledge_references_used": knowledge_context["reference_labels"],
    }


def _write_downloads(
    prompt: str,
    scenario: dict[str, Any],
    readiness: dict[str, Any],
    diagnostics: dict[str, Any],
    results: dict[str, Any],
    interpretation: dict[str, Any],
    model_profile: dict[str, Any],
    knowledge_context: dict[str, Any],
    learning_event_id: str,
    model_improvements: dict[str, Any],
) -> dict[str, str]:
    output_dir = Path("outputs") / "signal_cge_public" / datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "prompt": prompt,
        "scenario": scenario,
        "readiness": readiness,
        "diagnostics": diagnostics,
        "results": results,
        "interpretation": interpretation,
        "model_profile": model_profile,
        "knowledge_context": knowledge_context,
        "learning_event_id": learning_event_id,
        "result_type": "prototype_directional_indicator",
        "model_improvement_suggestions": model_improvements,
    }
    md_path = output_dir / "signal_cge_policy_brief.md"
    json_path = output_dir / "signal_cge_results.json"
    csv_path = output_dir / "signal_cge_results.csv"
    md_path.write_text(_policy_brief_markdown(payload), encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["account", "effect"])
        writer.writeheader()
        for account, effect in results.get("account_effects", {}).items():
            writer.writerow({"account": account, "effect": effect})
    return {"policy_brief_md": str(md_path), "results_json": str(json_path), "results_csv": str(csv_path)}


def _policy_brief_markdown(payload: dict[str, Any]) -> str:
    return "\n\n".join(
        [
            "# Signal CGE Policy Simulation Brief",
            "## Interpreted Scenario\n```json\n" + json.dumps(payload["scenario"], indent=2) + "\n```",
            "## Model Readiness\n```json\n" + json.dumps(payload["readiness"], indent=2) + "\n```",
            "## Diagnostics\n```json\n" + json.dumps(payload["diagnostics"], indent=2) + "\n```",
            "## Simulation Results\n```json\n" + json.dumps(payload["results"], indent=2) + "\n```",
            "## Policy Interpretation\n```json\n" + json.dumps(payload["interpretation"], indent=2) + "\n```",
            "## Knowledge Trace\n```json\n" + json.dumps(payload["knowledge_context"], indent=2) + "\n```",
            "## Suggested Model Improvements\n```json\n" + json.dumps(payload["model_improvement_suggestions"], indent=2) + "\n```",
            "## Limitations\n" + FULL_CGE_FALLBACK_MESSAGE,
        ]
    )


def _is_care_relevant(scenario: dict[str, Any]) -> bool:
    focused = {
        "prompt": scenario.get("prompt", ""),
        "shock_type": scenario.get("shock_type", ""),
        "target_accounts": scenario.get("target_accounts", []),
        "shock_account": scenario.get("shock_account", ""),
        "target_account": scenario.get("target_account", ""),
        "target_commodity": scenario.get("target_commodity", ""),
    }
    text = json.dumps(focused).lower()
    return "care" in text or any(suffix in text for suffix in ["fcp", "fcu", "fnp", "fnu", "mcp", "mcu", "mnp", "mnu"])


def _diagnostics_summary(diagnostics: dict[str, Any]) -> dict[str, Any]:
    validation = diagnostics.get("validation", {})
    warnings = []
    if isinstance(validation, dict):
        warnings.extend(validation.get("warnings", []) or [])
    warnings.extend(diagnostics.get("knowledge_references_used", []))
    return {
        "warnings": warnings,
        "fallback_explanation": diagnostics.get("fallback_explanation"),
        "reference_count": len(diagnostics.get("knowledge_references_used", [])),
    }


def _result_summary(results: dict[str, Any]) -> dict[str, Any]:
    return {
        "result_type": results.get("result_type"),
        "GDP/output effect": results.get("GDP/output effect"),
        "household income effect": results.get("household income effect"),
        "trade effect": results.get("trade effect"),
    }


def _recommended_next_simulations(summary: dict[str, Any], adaptive_hints: dict[str, Any]) -> list[str]:
    recommendations = list(summary.get("suggested_next_simulations", []))
    if adaptive_hints.get("policy_instrument") == "import_tariff":
        recommendations.extend(
            [
                "Test an alternative tariff shock size for sensitivity.",
                "Compare tariff reduction with productivity support for machinery-using sectors.",
                "Run a government revenue replacement scenario.",
            ]
        )
    return list(dict.fromkeys(recommendations))
