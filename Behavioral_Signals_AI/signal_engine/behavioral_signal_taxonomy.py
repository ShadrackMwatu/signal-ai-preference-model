"""Behavioral signal taxonomy for aggregate demand intelligence."""

from __future__ import annotations

from typing import Any

SIGNAL_FAMILIES = {
    "Demand": {
        "description": "Revealed aggregate interest or intent for goods, services, access, or availability.",
        "indicators": [
            "repeated searches", "rising trend frequency", "comparison", "compare", "best", "where to buy",
            "near me", "delivery", "available", "availability", "buy", "purchase", "shop", "order",
            "increasing demand", "rising engagement", "location-specific purchase interest",
        ],
    },
    "Affordability": {
        "description": "Price sensitivity, purchasing-power pressure, or financing constraint.",
        "indicators": [
            "cheap", "affordable", "low cost", "discount", "wholesale", "second hand", "installment",
            "instalment", "financing", "loan", "pay later", "price", "prices", "cost", "high cost",
        ],
    },
    "Stress": {
        "description": "Household, service, livelihood, or supply stress signaled by aggregate behavior.",
        "indicators": [
            "jobs", "hospital near me", "water shortage", "fuel prices", "unga prices", "school fees",
            "rent", "electricity tokens", "drought", "shortage", "urgent", "crisis", "scarcity",
            "pressure", "stress", "unemployment", "clinic", "medicine",
        ],
    },
    "Opportunity": {
        "description": "Potential market, service-delivery, or policy opportunity from unmet or rising need.",
        "indicators": [
            "rapidly growing", "persistent unmet", "county-specific shortage", "rising service demand",
            "market gap", "supply gap", "increasing demand", "underserved", "available", "delivery",
            "new market", "opportunity", "expansion", "shortage",
        ],
    },
}

FAMILY_BADGES = {
    "Demand": "Demand signal",
    "Affordability": "Affordability pressure",
    "Stress": "Stress signal",
    "Opportunity": "Opportunity signal",
}


def classify_behavioral_families(signal: dict[str, Any], source_topics: list[str] | None = None) -> list[str]:
    text = _signal_text(signal, source_topics)
    families: list[str] = []
    for family, meta in SIGNAL_FAMILIES.items():
        if any(indicator.lower() in text for indicator in meta["indicators"]):
            families.append(family)
    category = str(signal.get("signal_category", "")).lower()
    if category in {"food and agriculture", "cost of living", "energy", "housing", "transport", "finance and credit"} and "Affordability" not in families:
        families.append("Affordability")
    if category in {"jobs and labour market", "health", "water and sanitation", "public services", "security and governance"} and "Stress" not in families:
        families.append("Stress")
    if signal.get("unmet_demand_likelihood") in {"High", "Medium"} and "Opportunity" not in families:
        families.append("Opportunity")
    if signal.get("demand_level") in {"High", "Moderate"} and "Demand" not in families:
        families.append("Demand")
    return _dedupe(families) or ["Demand"]


def interpret_family_combination(families: list[str], signal: dict[str, Any]) -> str:
    family_set = set(families)
    if {"Demand", "Affordability"}.issubset(family_set):
        return "Demand is visible, but affordability language suggests purchasing power may be constrained."
    if {"Demand", "Opportunity"}.issubset(family_set):
        return "Demand and unmet-need signals together suggest market expansion potential."
    if {"Stress", "Affordability"}.issubset(family_set):
        return "Stress and affordability signals together point to household welfare or cost-of-living pressure."
    if {"Stress", "Opportunity"}.issubset(family_set):
        return "Stress and opportunity signals together suggest a service delivery gap or policy intervention need."
    if "Demand" in family_set and str(signal.get("geographic_scope", "Kenya-wide")) == "Kenya-wide":
        return "Kenya-wide demand language suggests the signal may scale beyond one location if it persists."
    if "Stress" in family_set and signal.get("historical_pattern_match") not in {None, "No close historical pattern yet"}:
        return "Recurring stress signals may indicate a structural issue requiring policy attention."
    return "Behavioral family evidence is developing and should be monitored through persistence and source confirmation."


def family_badges(families: list[str]) -> list[str]:
    return [FAMILY_BADGES.get(family, family) for family in families]


def _signal_text(signal: dict[str, Any], source_topics: list[str] | None) -> str:
    parts = [
        signal.get("signal_topic"),
        signal.get("semantic_cluster"),
        signal.get("signal_category"),
        signal.get("source_summary"),
        signal.get("interpretation"),
        signal.get("recommended_action"),
    ]
    parts.extend(source_topics or signal.get("source_topics") or [])
    return " ".join(str(part).lower() for part in parts if part)


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            output.append(value)
    return output
