"""Kenya economic and social context mapping for aggregate signals."""

from __future__ import annotations

from typing import Any

CONTEXT_MAP = {
    "food and agriculture": ["cost of living", "agriculture cycles", "climate vulnerability", "informal food markets"],
    "cost of living": ["inflation pressure", "household purchasing power", "urban affordability"],
    "energy": ["energy access", "logistics costs", "inflation pressure"],
    "transport": ["trade/logistics", "urban mobility", "household transport budgets"],
    "jobs and labour market": ["youth unemployment", "urbanization", "informal economy livelihoods"],
    "housing": ["housing affordability", "urbanization", "rental pressure"],
    "technology and digital economy": ["digital adoption", "youth consumer demand", "mobile commerce"],
    "water and sanitation": ["water access", "climate vulnerability", "public service pressure"],
    "health": ["public service demand", "household welfare", "county service pressure"],
    "finance and credit": ["liquidity pressure", "small business finance", "household credit"],
}


def map_kenya_context(signal: dict[str, Any]) -> dict[str, Any]:
    category = str(signal.get("signal_category", "other")).lower()
    scope = str(signal.get("geographic_scope", "Kenya-wide"))
    topic = str(signal.get("signal_topic", "Kenya signal"))
    tags = CONTEXT_MAP.get(category, ["aggregate demand", "market pressure", "public concern"])
    sector = _sector_phrase(category)
    county_phrase = "Kenya-wide pressure" if scope == "Kenya-wide" else f"county-specific pressure in {scope}"
    return {
        "kenya_context_tags": tags,
        "macro_implications": _macro_implication(category, topic),
        "sector_implications": f"This signal is most relevant to {sector} and adjacent supply chains.",
        "county_implications": f"Current evidence points to {county_phrase}; county intelligence should be validated with additional aggregate data.",
        "business_opportunity": _business_opportunity(category),
        "policy_opportunity": _policy_opportunity(category),
        "risk_outlook": _risk_outlook(category, signal),
        "monitoring_recommendation": _monitoring_recommendation(category),
    }


def _macro_implication(category: str, topic: str) -> str:
    if category in {"food and agriculture", "cost of living", "energy", "transport"}:
        return f"{topic} may indicate household affordability pressure and possible pass-through into broader demand conditions."
    if category == "jobs and labour market":
        return f"{topic} may reflect livelihood pressure, labour-market search intensity, or income uncertainty."
    if category == "technology and digital economy":
        return f"{topic} may reflect consumer technology adoption, affordability constraints, or digital-service demand."
    return f"{topic} may signal an emerging Kenya aggregate demand or service-pressure pattern."


def _sector_phrase(category: str) -> str:
    return {
        "food and agriculture": "food retailers, processors, logistics firms, farmers, and market monitors",
        "cost of living": "retailers, household-goods suppliers, social protection teams, and price monitors",
        "energy": "fuel distributors, transport operators, manufacturers, and household energy providers",
        "transport": "transport operators, logistics providers, commuters, and urban planning teams",
        "jobs and labour market": "employers, training providers, recruitment platforms, and youth programmes",
        "technology and digital economy": "device retailers, fintech providers, telcos, and digital platforms",
        "water and sanitation": "water service providers, county agencies, and household resilience services",
    }.get(category, "business operators, county teams, and policy monitoring units")


def _business_opportunity(category: str) -> str:
    return {
        "food and agriculture": "Improve affordable supply, smaller pack sizes, stock planning, and price-sensitive distribution.",
        "technology and digital economy": "Position affordable devices, repair services, financing, and bundled digital access.",
        "jobs and labour market": "Expand matching, training, credentialing, and youth-focused employment services.",
        "transport": "Monitor logistics costs and explore efficient routing or lower-cost mobility options.",
        "energy": "Prepare for demand shifts toward efficiency, alternative fuels, or lower-cost energy access.",
    }.get(category, "Monitor demand pockets and test targeted offers using aggregate market evidence.")


def _policy_opportunity(category: str) -> str:
    return {
        "food and agriculture": "Strengthen market price monitoring, food distribution visibility, and affordability responses.",
        "cost of living": "Track household pressure signals alongside official price indicators and safety-net needs.",
        "water and sanitation": "Prioritize service continuity, drought monitoring, and county response planning.",
        "jobs and labour market": "Target labour-market programmes where search pressure and livelihood signals persist.",
        "health": "Monitor service access pressure and validate with facility-level aggregate indicators.",
    }.get(category, "Use this as an early aggregate signal for policy monitoring and follow-up validation.")


def _risk_outlook(category: str, signal: dict[str, Any]) -> str:
    direction = signal.get("predicted_direction", "stable")
    spread = signal.get("spread_risk", "Low")
    return f"Risk outlook is {direction} with {spread.lower()} spread risk based on current aggregate evidence."


def _monitoring_recommendation(category: str) -> str:
    if category in {"food and agriculture", "cost of living", "energy"}:
        return "Monitor search/news recurrence, price indicators, and related transport or household affordability signals."
    if category in {"water and sanitation", "health", "public services"}:
        return "Monitor county mentions, official service bulletins, and recurring public concern signals."
    return "Monitor persistence, source agreement, and related topics over the next refresh cycles."
