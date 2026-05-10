"""Scenario orchestration service for Signal CGE."""

from __future__ import annotations

from typing import Any

from Signal_CGE.signal_ai.conversation_engine.chat_orchestrator import run_chat_simulation
from Signal_CGE.signal_cge.knowledge.scenario_context import get_scenario_context
from Signal_CGE.signal_cge.learning.adaptive_rules import apply_adaptive_prompt_rules


def build_scenario(prompt: str, uploaded_sam: str | None = None) -> dict[str, Any]:
    """Build and enrich a Signal CGE scenario."""

    result = run_chat_simulation(prompt or "Run baseline Signal CGE scenario", sam_file=uploaded_sam)
    scenario = result.get("scenario", {})
    return {
        "prompt": prompt,
        "scenario": scenario,
        "adaptive_hints": apply_adaptive_prompt_rules(prompt, scenario),
        "knowledge_context": get_scenario_context(scenario),
        "raw_result": result,
    }
