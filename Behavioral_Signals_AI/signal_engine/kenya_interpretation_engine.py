"""Kenya-specific interpretation layer for fused aggregate signals."""

from __future__ import annotations

from typing import Any


def interpret_kenya_signal(signal: dict[str, Any]) -> dict[str, str]:
    topic = str(signal.get("signal_topic", "this signal"))
    category = str(signal.get("signal_category", "other"))
    urgency = str(signal.get("urgency", "Medium"))
    pressure = _pressure_for_category(category)
    groups = _affected_groups(category)
    opportunity = _business_opportunity(category)
    policy = _policy_implication(category, urgency)
    monitoring = f"Monitor whether {topic} persists across search, news, official statistics, and public discussion signals over the next few update cycles."
    probable = f"Attention around {topic} may indicate {pressure}."
    interpretation = (
        f"{probable} This is relevant to {groups}. Business opportunity: {opportunity} "
        f"Policy implication: {policy} Near-term monitoring: {monitoring}"
    )
    return {
        "probable_meaning": probable,
        "economic_or_social_pressure": pressure,
        "affected_groups_or_sectors": groups,
        "business_opportunity": opportunity,
        "policy_implication": policy,
        "near_term_monitoring_recommendation": monitoring,
        "interpretation": interpretation,
    }


def _pressure_for_category(category: str) -> str:
    c = category.lower()
    if "food" in c or "cost" in c:
        return "household cost-of-living pressure and affordability concern"
    if "jobs" in c:
        return "labour-market pressure and income-seeking behavior"
    if "health" in c:
        return "service access pressure and possible unmet healthcare need"
    if "water" in c:
        return "basic-service stress and household welfare pressure"
    if "energy" in c or "transport" in c:
        return "input-cost pressure affecting household budgets and business operating costs"
    if "technology" in c or "finance" in c:
        return "emerging consumption shift and digital-service demand"
    return "emerging aggregate demand or public concern"


def _affected_groups(category: str) -> str:
    c = category.lower()
    if "food" in c:
        return "households, retailers, millers, farmers, food processors, and market monitoring teams"
    if "jobs" in c:
        return "job seekers, employers, training providers, labour agencies, and youth programmes"
    if "health" in c:
        return "patients, clinics, pharmacies, hospitals, insurers, and public health agencies"
    if "water" in c:
        return "households, water service providers, county governments, and sanitation programmes"
    if "energy" in c:
        return "transport operators, households, manufacturers, retailers, and energy suppliers"
    if "technology" in c:
        return "retailers, device importers, repair services, fintechs, and digital platforms"
    return "businesses, public agencies, investors, and local service providers"


def _business_opportunity(category: str) -> str:
    c = category.lower()
    if "food" in c:
        return "improve affordable supply, pack sizes, distribution, and price monitoring."
    if "jobs" in c:
        return "offer skills matching, recruitment services, short courses, and job-market information."
    if "health" in c:
        return "expand accessible clinics, telehealth, pharmacy availability, and appointment coordination."
    if "water" in c:
        return "support water delivery, storage, treatment, repair services, and county-level response."
    if "energy" in c:
        return "offer efficiency products, alternative energy, price alerts, and logistics planning."
    if "technology" in c:
        return "position affordable devices, repair, financing, and bundled digital services."
    return "validate the demand pocket and test a targeted product, service, or information response."


def _policy_implication(category: str, urgency: str) -> str:
    prefix = "High urgency suggests rapid coordination and monitoring. " if urgency.lower() == "high" else ""
    c = category.lower()
    if "food" in c or "cost" in c:
        return prefix + "Strengthen price surveillance, food security monitoring, and social protection targeting."
    if "jobs" in c:
        return prefix + "Improve labour-market information, youth employment support, and skills pathways."
    if "health" in c:
        return prefix + "Track access gaps and coordinate public health service availability."
    if "water" in c:
        return prefix + "Prioritize county water-service response and infrastructure maintenance."
    return prefix + "Use aggregate signal monitoring to prioritize further data validation and policy response."