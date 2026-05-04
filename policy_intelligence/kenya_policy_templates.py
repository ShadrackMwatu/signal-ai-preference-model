"""Kenya-focused policy wording templates."""

KEY_POLICY_MESSAGES = {
    "positive_growth": "The scenario supports aggregate activity, but distributional safeguards remain important.",
    "negative_growth": "The scenario weakens aggregate activity and should be redesigned or sequenced more gradually.",
    "revenue_gain": "Government revenue improves, creating fiscal space for targeted public investment.",
    "revenue_loss": "Government revenue weakens; identify offsetting measures before implementation.",
    "trade_gain": "Trade balance indicators improve under the prototype assumptions.",
    "trade_loss": "Trade balance pressure rises; import substitution or export support may be needed.",
}


def county_context_note() -> str:
    return (
        "For Kenya policy use, connect SAM accounts to county-level revealed demand "
        "evidence where possible, while keeping all behavioral data aggregated and privacy-safe."
    )
