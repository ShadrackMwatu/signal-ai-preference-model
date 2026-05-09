"""Deterministic chat orchestration for the Signal AI CGE Chat Studio."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cge_workbench.interpreters.natural_language_to_scenario import parse_scenario_prompt
from cge_workbench.workbench import run_chat_scenario
from policy_ai.policy_brief_service import generate_policy_summary
from signal_ai.memory.simulation_memory import save_simulation
from signal_ai.prompt_router.intent_classifier import classify_intent
from signal_ai.reasoning.economic_reasoner import (
    explain_transmission_channels,
    flag_possible_inconsistencies,
    validate_policy_shock,
)


def run_chat_simulation(
    user_prompt: str,
    sam_file: str | Path | None = None,
    previous_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    intent = classify_intent(user_prompt)
    scenario = parse_scenario_prompt(user_prompt).to_dict()
    if previous_context:
        scenario["previous_context_note"] = "Previous context was supplied and preserved for future memory-aware routing."
    validation = validate_policy_shock(scenario)

    fallback_warnings: list[str] = []
    try:
        run_result = run_chat_scenario(
            prompt=user_prompt,
            model_type="SAM multiplier",
            sam_path=str(sam_file) if sam_file else None,
        )
    except Exception as exc:
        if not sam_file:
            raise
        fallback_warnings.append(
            "Uploaded SAM could not be read or validated. Signal used the built-in demonstration SAM fallback."
        )
        run_result = run_chat_scenario(prompt=user_prompt, model_type="SAM multiplier")
        run_result.setdefault("diagnostics", {})
        run_result["diagnostics"]["uploaded_sam_fallback"] = {
            "valid": False,
            "warnings": fallback_warnings,
            "error": str(exc),
        }

    warnings = validation["warnings"] + fallback_warnings + flag_possible_inconsistencies(run_result)
    diagnostics = {"intent": intent, "validation": validation, **run_result.get("diagnostics", {})}
    policy_summary = generate_policy_summary(scenario, run_result.get("results", {}), diagnostics)
    explanation = {
        "transmission_channels": explain_transmission_channels(scenario),
        "workbench_explanation": run_result.get("explanation", {}),
    }
    response = {
        "scenario": scenario,
        "diagnostics": diagnostics,
        "results": run_result.get("results", {}),
        "explanation": explanation,
        "policy_summary": policy_summary,
        "warnings": list(dict.fromkeys(warnings)),
    }
    save_simulation({"scenario": scenario, "backend": run_result.get("backend"), "warnings": response["warnings"]})
    return response
