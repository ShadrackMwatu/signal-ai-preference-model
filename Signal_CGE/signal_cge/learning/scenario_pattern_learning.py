"""Learn deterministic scenario patterns from lightweight simulation memory."""

from __future__ import annotations

from collections import Counter
import re
from typing import Any

from .simulation_memory import load_simulation_memory


STOPWORDS = {"a", "an", "and", "by", "for", "in", "of", "on", "run", "show", "simulate", "the", "to"}


def learn_prompt_patterns(limit: int = 100) -> dict[str, Any]:
    """Summarize repeated prompt terms, targets, and scenario mappings."""

    events = load_simulation_memory(limit=limit)
    terms: Counter[str] = Counter()
    transitions: Counter[str] = Counter()
    for event in events:
        prompt = str(event.get("prompt", "")).lower()
        for term in re.findall(r"[a-zA-Z_][a-zA-Z0-9_/-]*", prompt):
            if term not in STOPWORDS and len(term) > 2:
                terms[term] += 1
        scenario_type = str(event.get("scenario_type") or "unknown")
        target = str(event.get("target_account") or "unknown")
        transitions[f"{scenario_type}:{target}"] += 1
    return {
        "event_count": len(events),
        "common_prompt_terms": terms.most_common(10),
        "common_scenario_target_pairs": transitions.most_common(10),
    }


def find_similar_simulations(prompt: str, scenario: dict[str, Any], limit: int = 5) -> list[dict[str, Any]]:
    """Return prior events with matching scenario type, target, or prompt terms."""

    events = load_simulation_memory(limit=100)
    text_terms = set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_/-]*", (prompt or "").lower()))
    scenario_type = scenario.get("shock_type") or scenario.get("simulation_type")
    target = scenario.get("target_account") or scenario.get("target_commodity") or scenario.get("shock_account")
    scored = []
    for event in events:
        score = 0
        if scenario_type and event.get("scenario_type") == scenario_type:
            score += 2
        if target and event.get("target_account") == target:
            score += 2
        score += len(text_terms.intersection(set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_/-]*", str(event.get("prompt", "")).lower()))))
        if score:
            scored.append((score, event))
    return [event for _score, event in sorted(scored, key=lambda item: item[0], reverse=True)[:limit]]
