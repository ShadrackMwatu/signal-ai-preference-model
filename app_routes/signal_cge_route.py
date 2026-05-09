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
    readiness = get_model_readiness()
    diagnostics = {
        **result.get("diagnostics", {}),
        "model_profile_loaded": True,
        "reference_sections": reference_index.get("sections", []),
        "canonical_model_profile": "models/canonical/signal_cge_master/model_profile.yaml",
        "uploaded_sam": "provided" if sam_path else "not provided; using canonical profile and fallback SAM where needed",
        "fallback_explanation": FULL_CGE_FALLBACK_MESSAGE,
    }
    structured_results = _structured_results(result.get("results", {}), scenario)
    chart_data = _chart_data(structured_results)
    interpretation = _policy_interpretation(result)
    downloads = _write_downloads(
        scenario=scenario,
        readiness=readiness,
        diagnostics=diagnostics,
        results=structured_results,
        interpretation=interpretation,
        model_profile=model_profile,
    )
    backend = result.get("results", {}).get("backend") or result.get("backend") or "python_sam_multiplier"
    return {
        "scenario": _interpreted_scenario(scenario, result.get("results", {})),
        "readiness": readiness,
        "diagnostics": diagnostics,
        "results": structured_results,
        "chart_data": chart_data,
        "interpretation": interpretation,
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
        "gender-care impact": round(care_effect, 6) if "care" in json.dumps(scenario).lower() else "Not a care-focused scenario.",
        "account_effects": accounts,
        "backend": results.get("backend", "python_sam_multiplier") if isinstance(results, dict) else "python_sam_multiplier",
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


def _policy_interpretation(result: dict[str, Any]) -> dict[str, Any]:
    summary = result.get("policy_summary", {})
    return {
        "transmission_mechanism": summary.get("expected_transmission_channel", ""),
        "winners_and_losers": {
            "likely_winners": summary.get("likely_winners", []),
            "likely_losers": ["Accounts facing higher relative costs or reduced demand, subject to SAM mapping."],
        },
        "risks": summary.get("likely_risks", []),
        "caveats": [summary.get("interpretation_caveat", ""), FULL_CGE_FALLBACK_MESSAGE],
        "recommended_next_simulations": summary.get("suggested_next_simulations", []),
    }


def _write_downloads(
    scenario: dict[str, Any],
    readiness: dict[str, Any],
    diagnostics: dict[str, Any],
    results: dict[str, Any],
    interpretation: dict[str, Any],
    model_profile: dict[str, Any],
) -> dict[str, str]:
    output_dir = Path("outputs") / "signal_cge_public" / datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "scenario": scenario,
        "readiness": readiness,
        "diagnostics": diagnostics,
        "results": results,
        "interpretation": interpretation,
        "model_profile": model_profile,
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
        ]
    )
