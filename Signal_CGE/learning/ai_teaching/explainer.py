"""Readable concept explanations for the Signal learning module."""

from __future__ import annotations


EXPLANATIONS = {
    "signal": (
        "Signal is an integrated AI platform for behavioral intelligence, revealed preference analysis, live trend monitoring, "
        "SML-based CGE and SAM modeling, and economics learning support."
    ),
    "revealed preference intelligence": (
        "Revealed preference intelligence studies what people show through aggregate behavior rather than what they merely say. "
        "In Signal, clicks, searches, shares, and trend signals are translated into structured demand and opportunity insights."
    ),
    "behavioral signals": (
        "Behavioral signals are observable aggregate actions such as likes, comments, shares, or searches. "
        "Signal interprets them as evidence of market interest, momentum, urgency, or unmet demand."
    ),
    "demand classification": (
        "Demand classification is Signal's way of organizing market signals into readable categories such as strong demand momentum, "
        "developing market interest, or limited demand signal."
    ),
    "opportunity scoring": (
        "Opportunity scoring combines demand strength, momentum, unmet-demand risk, and quality checks to estimate whether a market opening may be actionable."
    ),
    "unmet demand": (
        "Unmet demand appears when aggregate interest is visible but supply, access, affordability, or delivery conditions are not fully satisfying that interest."
    ),
    "emerging trends": (
        "Emerging trends are signals that show growing momentum but may still need monitoring before they become established market demand."
    ),
    "sams": (
        "A Social Accounting Matrix records flows between production sectors, institutions, factors, government, trade, and households. "
        "It provides the accounting foundation for many CGE models."
    ),
    "cge models": (
        "Computable General Equilibrium models simulate how shocks ripple across an economy. "
        "They can estimate effects on GDP, employment, sector output, prices, welfare, and public finance."
    ),
    "sml": (
        "Signal Modelling Language is a lightweight internal language for declaring sets, parameters, variables, equations, shocks, and solve instructions for future CGE workflows."
    ),
    "policy simulation": (
        "Policy simulation uses structured economic models to compare scenarios, interpret trade-offs, and communicate likely impacts in a policy-friendly way."
    ),
}


def explain_concept(concept: str) -> str:
    key = str(concept or "").strip().lower()
    if key in EXPLANATIONS:
        return EXPLANATIONS[key]
    return (
        f"Signal does not yet have a dedicated teaching note for '{concept}'. "
        "Try one of these topics: Signal, revealed preference intelligence, behavioral signals, demand classification, "
        "opportunity scoring, unmet demand, emerging trends, SAMs, CGE models, SML, or policy simulation."
    )
