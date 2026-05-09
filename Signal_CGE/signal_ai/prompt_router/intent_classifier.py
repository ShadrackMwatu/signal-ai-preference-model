"""Deterministic intent classification for Signal policy prompts."""

from __future__ import annotations


def classify_intent(user_prompt: str) -> dict[str, str | float]:
    text = (user_prompt or "").lower()
    if "compare" in text:
        intent = "compare_scenarios"
    elif any(term in text for term in ["brief", "explain", "interpret"]):
        intent = "explain_results"
    elif any(term in text for term in ["run", "simulate", "increase", "double", "shock", "reduce"]):
        intent = "run_simulation"
    else:
        intent = "compile_scenario"

    domain = "care_economy" if "care" in text else "general_policy"
    if "vat" in text or "tax" in text:
        domain = "tax_policy"
    elif "trade" in text or "export" in text:
        domain = "trade_policy"
    elif "infrastructure" in text or "transport" in text:
        domain = "infrastructure"

    return {"intent": intent, "domain": domain, "confidence": 0.85}
