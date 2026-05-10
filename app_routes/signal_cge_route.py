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

from Signal_CGE.signal_ai.conversation_engine.chat_orchestrator import run_chat_simulation
from Signal_CGE.signal_cge.diagnostics.model_readiness import get_model_readiness
from Signal_CGE.signal_cge.knowledge.document_loader import load_model_profile
from Signal_CGE.signal_cge.knowledge.reference_index import build_reference_index
from Signal_CGE.signal_cge.knowledge.scenario_context import get_scenario_context
from Signal_CGE.signal_cge.learning.adaptive_rules import apply_adaptive_prompt_rules
from Signal_CGE.signal_cge.learning.model_gap_detector import generate_model_gap_report
from Signal_CGE.signal_cge.learning.model_improvement_suggestions import (
    generate_model_improvement_suggestions,
)
from Signal_CGE.signal_cge.learning.recommendation_engine import recommend_adaptive_next_simulations
from Signal_CGE.signal_cge.learning.scenario_pattern_learning import find_similar_simulations
from Signal_CGE.signal_cge.learning.simulation_memory import record_simulation_learning_event
from Signal_CGE.signal_cge.learning.learning_registry import write_learning_summary
from Signal_CGE.signal_cge.full_cge.model_gap_report import generate_full_cge_gap_report
from Signal_CGE.signal_cge.experiments.experiment_runner import run_prototype_experiment
from Signal_CGE.signal_cge.solvers.equilibrium_solver import solve_static_equilibrium


FULL_CGE_FALLBACK_MESSAGE = (
    "Prototype result: full equilibrium CGE solver is not yet active. Signal is using the available "
    "SAM multiplier/prototype backend and canonical repo model profile."
)
EQUILIBRIUM_SOLVER_MESSAGE = (
    "Signal used the open-source prototype equilibrium CGE solver. Results reflect a simplified "
    "calibrated equilibrium system, not yet the full recursive-dynamic model."
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
    similar_simulations = find_similar_simulations(prompt, scenario)
    gap_report = generate_model_gap_report(write=True)
    full_cge_status = _full_cge_development_status()
    experiment_payload = run_prototype_experiment(prompt or "")
    diagnostics = {
        **result.get("diagnostics", {}),
        "model_profile_loaded": True,
        "reference_sections": reference_index.get("sections", []),
        "canonical_model_profile": "Signal_CGE/models/canonical/signal_cge_master/model_profile.yaml",
        "uploaded_sam": "provided" if sam_path else "not provided; using canonical profile and fallback SAM where needed",
        "fallback_explanation": FULL_CGE_FALLBACK_MESSAGE,
        "adaptive_rules": adaptive_hints,
        "knowledge_references_used": knowledge_context["reference_labels"],
        "similar_prior_simulations": len(similar_simulations),
        "model_gap_report": gap_report,
        "full_cge_development_status": full_cge_status,
        "experiment_payload": experiment_payload,
    }
    equilibrium_result = solve_static_equilibrium(None, scenario, {"closure": "base_closure"})
    if equilibrium_result.get("success"):
        structured_results = _equilibrium_structured_results(equilibrium_result, scenario)
        solver_used = "Open-source prototype equilibrium CGE solver"
        backend = "open_source_equilibrium_solver"
        result_type = "open_source_equilibrium_cge_prototype"
        fallback_message = EQUILIBRIUM_SOLVER_MESSAGE
    else:
        structured_results = _structured_results(result.get("results", {}), scenario)
        solver_used = "SAM multiplier fallback"
        backend = result.get("results", {}).get("backend") or result.get("backend") or "python_sam_multiplier"
        result_type = "prototype_directional_indicator"
        fallback_message = FULL_CGE_FALLBACK_MESSAGE
    diagnostics["solver_used"] = solver_used
    diagnostics["equilibrium_solver"] = equilibrium_result.get("diagnostics", {})
    diagnostics["solver_failure_reason"] = "" if equilibrium_result.get("success") else equilibrium_result.get("reason", "solver unavailable")
    diagnostics["fallback_explanation"] = fallback_message
    chart_data = _chart_data(structured_results)
    results_table = _results_table(structured_results)
    interpretation = _policy_interpretation(result, knowledge_context, adaptive_hints, similar_simulations)
    model_improvements = generate_model_improvement_suggestions()
    interpretation["recommended_next_simulations"] = _dedupe(
        interpretation.get("recommended_next_simulations", [])
        + recommend_adaptive_next_simulations(scenario)
    )[:5]
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
            "model_gap_report": gap_report,
        }
    )
    learning_summary = write_learning_summary(limit=100)
    learning_trace = _build_learning_trace(
        learning_event=learning_event,
        adaptive_hints=adaptive_hints,
        scenario=scenario,
        similar_simulations=similar_simulations,
        model_improvements=model_improvements,
    )
    downloads = _write_downloads(
        prompt=prompt,
        scenario=scenario,
        readiness=readiness,
        diagnostics=diagnostics,
        results=structured_results,
        results_table=results_table,
        interpretation=interpretation,
        model_profile=model_profile,
        knowledge_context=knowledge_context,
        learning_event_id=learning_event["event_id"],
        model_improvements=model_improvements,
        learning_trace=learning_trace,
        similar_simulations=similar_simulations,
        gap_report=gap_report,
        learning_summary=learning_summary,
        full_cge_status=full_cge_status,
        experiment_payload=experiment_payload,
    )
    return {
        "scenario": _interpreted_scenario(scenario, result.get("results", {})),
        "readiness": readiness,
        "diagnostics": diagnostics,
        "results": structured_results,
        "results_table": results_table,
        "chart_data": chart_data,
        "interpretation": interpretation,
        "learning_trace": learning_trace,
        "full_cge_development_status": full_cge_status,
        "experiment_payload": experiment_payload,
        "knowledge_context": knowledge_context,
        "model_improvement_suggestions": model_improvements,
        "model_gap_report": gap_report,
        "similar_prior_simulations": similar_simulations,
        "learning_summary": learning_summary,
        "learning_event_id": learning_event["event_id"],
        "result_type": result_type,
        "downloads": downloads,
        "backend_used": backend,
        "solver_used": solver_used,
        "fallback_message": fallback_message,
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
        "result_type": results.get("result_type", "prototype_directional_indicator"),
    }


def _equilibrium_structured_results(solver_result: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    changes = solver_result.get("percentage_changes", {})
    policy = solver_result.get("policy", {})
    return {
        "GDP/output effect": round(float(changes.get("output_change_pct", 0.0)), 6),
        "factor income effect": round(float(changes.get("activity_price_change_pct", 0.0)), 6),
        "household income effect": round(float(changes.get("household_welfare_proxy_change_pct", 0.0)), 6),
        "government balance effect": round(float(changes.get("government_revenue_change_pct", 0.0)), 6),
        "trade effect": round(float(changes.get("trade_balance_change_pct", 0.0)), 6),
        "welfare/proxy welfare effect": round(float(changes.get("household_welfare_proxy_change_pct", 0.0)), 6),
        "import price change": round(float(changes.get("import_price_change_pct", 0.0)), 6),
        "import demand change": round(float(changes.get("import_demand_change_pct", 0.0)), 6),
        "government tariff revenue change": round(float(changes.get("government_tariff_revenue_change_pct", 0.0)), 6),
        "output change": round(float(changes.get("output_change_pct", 0.0)), 6),
        "trade balance change": round(float(changes.get("trade_balance_change_pct", 0.0)), 6),
        "gender-care impact": "Not applicable to this scenario." if not _is_care_relevant(scenario) else round(float(changes.get("household_welfare_proxy_change_pct", 0.0)), 6),
        "account_effects": {
            "domestic_output": policy.get("domestic_output", 0.0),
            "imports": policy.get("imports", 0.0),
            "exports": policy.get("exports", 0.0),
            "government_revenue": policy.get("government_revenue", 0.0),
            "household_income": policy.get("household_income", 0.0),
        },
        "percentage_changes": changes,
        "backend": "open_source_equilibrium_solver",
        "result_type": "open_source_equilibrium_cge_prototype",
        "solver_label": solver_result.get("solver_label", "Open-source prototype equilibrium CGE solver"),
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


def _results_table(results: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"metric": "GDP/output", "effect": results.get("GDP/output effect", 0.0)},
        {"metric": "Factor income", "effect": results.get("factor income effect", 0.0)},
        {"metric": "Household income", "effect": results.get("household income effect", 0.0)},
        {"metric": "Government balance", "effect": results.get("government balance effect", 0.0)},
        {"metric": "Trade/import pressure", "effect": results.get("trade effect", 0.0)},
        {"metric": "Welfare/proxy welfare", "effect": results.get("welfare/proxy welfare effect", 0.0)},
        {"metric": "Gender-care impact", "effect": results.get("gender-care impact", "Not applicable to this scenario.")},
        {"metric": "Result type", "effect": results.get("result_type", "prototype_directional_indicator")},
    ]


def _account_effect(results: dict[str, Any], account_name: str) -> float:
    accounts = results.get("account_effects", {})
    return float(accounts.get(account_name, 0.0)) if isinstance(accounts, dict) else 0.0


def _policy_interpretation(
    result: dict[str, Any],
    knowledge_context: dict[str, Any],
    adaptive_hints: dict[str, Any],
    similar_simulations: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    summary = result.get("policy_summary", {})
    scenario = result.get("scenario", {})
    transmission = summary.get("expected_transmission_channel", "")
    if scenario.get("shock_type") == "import_tariff" or scenario.get("policy_instrument") == "import_tariff":
        target = scenario.get("target_account") or scenario.get("target_commodity") or scenario.get("shock_account", "target commodity")
        transmission = (
            f"`{target}` is treated as the target commodity/account. A tariff reduction affects the import tax wedge; "
            "lower import tariffs may reduce import prices, government tariff revenue may fall, import demand may increase, "
            "machinery-using sectors may benefit through lower input or investment costs, domestic substitutes may face "
            "competitive pressure, and trade-balance effects are ambiguous without full equilibrium solving."
        )
        likely_winners = [
            "machinery-using sectors",
            "investment-related activities",
            "consumers/users of machinery-linked goods",
            f"importers of {target}",
        ]
        likely_losers = [
            "government tariff revenue",
            "domestic substitutes",
            "trade balance if imports rise strongly",
        ]
        risks = [
            "Government tariff revenue may fall.",
            "Domestic substitutes may face stronger import competition.",
            "The trade balance may weaken if imports rise strongly.",
        ]
    else:
        likely_winners = summary.get("likely_winners", [])
        likely_losers = ["Accounts facing higher relative costs or reduced demand, subject to SAM mapping."]
        risks = summary.get("likely_risks", [])
    return {
        "transmission_mechanism": transmission,
        "winners_and_losers": {
            "likely_winners": likely_winners,
            "likely_losers": likely_losers,
        },
        "risks": risks,
        "caveats": [
            summary.get("interpretation_caveat", ""),
            FULL_CGE_FALLBACK_MESSAGE,
            "Full equilibrium effects require the future solver.",
        ],
        "recommended_next_simulations": _recommended_next_simulations(summary, adaptive_hints),
        "knowledge_references_used": knowledge_context["reference_labels"],
        "prior_learning_used": [
            {
                "event_id": event.get("event_id"),
                "scenario_type": event.get("scenario_type"),
                "target_account": event.get("target_account"),
            }
            for event in (similar_simulations or [])[:3]
        ],
        "full_cge_additional_capture": [
            "Endogenous price feedbacks across all markets.",
            "Government revenue, savings-investment, and external-balance closure responses.",
            "Factor-market reallocation and market-clearing effects.",
            "Trade-balance and welfare effects after economy-wide adjustment.",
        ],
    }


def _write_downloads(
    prompt: str,
    scenario: dict[str, Any],
    readiness: dict[str, Any],
    diagnostics: dict[str, Any],
    results: dict[str, Any],
    results_table: list[dict[str, Any]],
    interpretation: dict[str, Any],
    model_profile: dict[str, Any],
    knowledge_context: dict[str, Any],
    learning_event_id: str,
    model_improvements: dict[str, Any],
    learning_trace: dict[str, Any],
    similar_simulations: list[dict[str, Any]] | None = None,
    gap_report: dict[str, Any] | None = None,
    learning_summary: dict[str, Any] | None = None,
    full_cge_status: dict[str, Any] | None = None,
    experiment_payload: dict[str, Any] | None = None,
) -> dict[str, str]:
    output_dir = Path("outputs") / "signal_cge_public" / datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "prompt": prompt,
        "scenario": scenario,
        "readiness": readiness,
        "diagnostics": diagnostics,
        "validation_status": _validation_status(diagnostics),
        "results": results,
        "results_table": results_table,
        "interpretation": interpretation,
        "model_profile": model_profile,
        "knowledge_context": knowledge_context,
        "model_references_used": knowledge_context.get("reference_labels", []),
        "solver_backend_used": diagnostics.get("solver_used", results.get("backend", "not available")),
        "learning_event_id": learning_event_id,
        "learning_trace": learning_trace,
        "result_type": "prototype_directional_indicator",
        "model_improvement_suggestions": model_improvements,
        "similar_prior_simulations": similar_simulations or [],
        "model_gap_report": gap_report or {},
        "learning_summary": learning_summary or {},
        "full_cge_development_status": full_cge_status or {},
        "experiment_payload": experiment_payload or {},
    }
    md_path = output_dir / "signal_cge_policy_brief.md"
    json_path = output_dir / "signal_cge_results.json"
    csv_path = output_dir / "signal_cge_results.csv"
    md_path.write_text(_policy_brief_markdown(payload), encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "effect"])
        writer.writeheader()
        for row in results_table:
            writer.writerow({"metric": row["metric"], "effect": row["effect"]})
    return {"policy_brief_md": str(md_path), "results_json": str(json_path), "results_csv": str(csv_path)}


def _policy_brief_markdown(payload: dict[str, Any]) -> str:
    return "\n\n".join(
        [
            "# Signal CGE Policy Simulation Brief",
            "## Prompt Entered\n" + str(payload["prompt"]),
            "## Interpreted Scenario\n```json\n" + json.dumps(payload["scenario"], indent=2) + "\n```",
            "## Model References Used\n```json\n" + json.dumps(payload["model_references_used"], indent=2) + "\n```",
            "## Solver/Backend Used\n" + str(payload["solver_backend_used"]),
            "## Validation Status\n```json\n" + json.dumps(payload["validation_status"], indent=2) + "\n```",
            "## Prototype Directional Results\n```json\n" + json.dumps(payload["results_table"], indent=2) + "\n```",
            "## Policy Interpretation\n```json\n" + json.dumps(payload["interpretation"], indent=2) + "\n```",
            "## Caveats\n```json\n" + json.dumps(payload["interpretation"].get("caveats", []), indent=2) + "\n```",
            "## Next Recommended Simulations\n```json\n" + json.dumps(payload["interpretation"].get("recommended_next_simulations", []), indent=2) + "\n```",
            "## Adaptive Learning Trace\n```json\n" + json.dumps(payload["learning_trace"], indent=2) + "\n```",
            "## Full CGE Development Status\n```json\n" + json.dumps(payload["full_cge_development_status"], indent=2) + "\n```",
            "## Diagnostics\n```json\n" + json.dumps(payload["diagnostics"], indent=2) + "\n```",
            "## Model Readiness\n```json\n" + json.dumps(payload["readiness"], indent=2) + "\n```",
            "## Knowledge Trace\n```json\n" + json.dumps(payload["knowledge_context"], indent=2) + "\n```",
            "## Suggested Model Improvements\n```json\n" + json.dumps(payload["model_improvement_suggestions"], indent=2) + "\n```",
            "## Model Gap Report\n```json\n" + json.dumps(payload["model_gap_report"], indent=2) + "\n```",
            "## Limitations\n" + FULL_CGE_FALLBACK_MESSAGE,
        ]
    )


def _validation_status(diagnostics: dict[str, Any]) -> dict[str, Any]:
    validation = diagnostics.get("validation", {})
    equilibrium = diagnostics.get("equilibrium_solver", {})
    return {
        "policy_shock_valid": validation.get("valid", "not available") if isinstance(validation, dict) else "not available",
        "validation_warnings": validation.get("warnings", []) if isinstance(validation, dict) else [],
        "solver_converged": equilibrium.get("converged", "not available") if isinstance(equilibrium, dict) else "not available",
        "residual_norm": equilibrium.get("residual_norm", "not available") if isinstance(equilibrium, dict) else "not available",
        "closure_used": equilibrium.get("closure_used", "not available") if isinstance(equilibrium, dict) else "not available",
    }


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


def _build_learning_trace(
    learning_event: dict[str, Any],
    adaptive_hints: dict[str, Any],
    scenario: dict[str, Any],
    similar_simulations: list[dict[str, Any]],
    model_improvements: dict[str, Any],
) -> dict[str, Any]:
    rules = adaptive_hints.get("rules_applied", [])
    return {
        "learning_event_recorded": "yes" if learning_event.get("event_id") else "no",
        "learning_event_id": learning_event.get("event_id", ""),
        "adaptive_rule_used": rules,
        "scenario_pattern_recognized": scenario.get("shock_type") or scenario.get("simulation_type", "not classified"),
        "prior_similar_simulations_found": len(similar_simulations),
        "model_improvement_suggestions": model_improvements,
    }


def _full_cge_development_status() -> dict[str, Any]:
    gap = generate_full_cge_gap_report()
    return {
        "calibration_bridge_status": "blueprint",
        "equation_registry_status": "active blueprint",
        "closure_manager_status": "active blueprint",
        "experiment_engine_status": "prototype directional engine",
        "solver_status": "open-source prototype static equilibrium solver active; full recursive-dynamic solver not active",
        "recursive_dynamics_status": "blueprint",
        "gap_summary": gap,
    }


def _dedupe(items: list[Any]) -> list[Any]:
    seen = set()
    output = []
    for item in items:
        key = json.dumps(item, sort_keys=True) if isinstance(item, (dict, list)) else str(item)
        if key not in seen:
            seen.add(key)
            output.append(item)
    return output
