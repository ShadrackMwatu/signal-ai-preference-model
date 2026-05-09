"""Policy intelligence layer for Signal CGE outputs."""

from __future__ import annotations

from .schema import CGEResult


def generate_policy_intelligence(result: CGEResult) -> dict[str, object]:
    """Translate CGE simulation outputs into policy-facing recommendations."""

    ranked_sectors = sorted(
        result.sector_impacts,
        key=lambda sector: float(sector["output_change_percent"]),
        reverse=True,
    )
    leading_sector = str(ranked_sectors[0]["sector"]) if ranked_sectors else "services"
    risks: list[str] = []
    if result.price_index_change_percent > 2:
        risks.append("Inflation pressure may offset part of the welfare gain.")
    if result.external_balance_change < 0:
        risks.append("External balance may weaken if import pressure rises.")
    if result.gdp_change_percent < 0:
        risks.append("Scenario reduces aggregate output under current closure.")
    if not risks:
        risks.append("No major macro risk flag was triggered by this prototype run.")

    return {
        "summary": (
            f"{result.scenario.name} changes GDP by {result.gdp_change_percent}% "
            f"and household welfare by {result.household_welfare_change_percent}%."
        ),
        "priority_sectors": [str(sector["sector"]) for sector in ranked_sectors[:3]],
        "recommended_policy_actions": [
            f"Prioritize productivity and market-access support for {leading_sector}.",
            "Sequence fiscal measures with household welfare safeguards.",
            "Use SAM balancing diagnostics before publication-grade calibration.",
        ],
        "risks": risks,
        "gams_compatibility": "Export includes sets, SAM parameters, shocks, equations, model, and solve block.",
        "publication_note": (
            "Prototype comparative-static outputs are transparent and reproducible; "
            "publication use should document closure, elasticities, SAM source, and balancing method."
        ),
    }
