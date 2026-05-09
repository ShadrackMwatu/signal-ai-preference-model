"""Behavioral Signals AI route.

This module intentionally depends on behavioral intelligence packages only. It
does not import Signal CGE packages.
"""

from __future__ import annotations

from typing import Any

import behavioral_ai  # noqa: F401
import live_trends  # noqa: F401
from adaptive_learning import aggregate_feedback_for_retraining  # noqa: F401
from explainability import generate_prediction_explanation


def run_behavioral_signal_prediction(
    likes: float,
    comments: float,
    shares: float,
    searches: float,
    engagement_intensity: float,
    purchase_intent_score: float,
    trend_growth: float,
) -> dict[str, Any]:
    """Return a deterministic behavioral-signal prediction payload."""

    features = {
        "likes": float(likes or 0),
        "comments": float(comments or 0),
        "shares": float(shares or 0),
        "searches": float(searches or 0),
        "engagement_intensity": float(engagement_intensity or 0),
        "purchase_intent_score": float(purchase_intent_score or 0),
        "trend_growth": float(trend_growth or 0),
    }
    aggregate = min(
        100.0,
        (
            features["likes"] * 0.16
            + features["comments"] * 0.28
            + features["shares"] * 0.42
            + features["searches"] * 0.14
        )
        / 2.0,
    )
    opportunity = min(
        1.0,
        0.35 * features["engagement_intensity"]
        + 0.45 * features["purchase_intent_score"]
        + 0.20 * features["trend_growth"],
    )
    confidence = min(1.0, 0.45 + opportunity * 0.4 + min(features["searches"], 250.0) / 1500.0)
    if aggregate >= 65 and opportunity >= 0.62:
        label = "High Demand"
    elif aggregate >= 35 or opportunity >= 0.45:
        label = "Moderate Demand"
    else:
        label = "Low Demand"
    prediction = {
        "demand_classification": label,
        "confidence_score": confidence,
        "aggregate_demand_score": aggregate,
        "opportunity_score": opportunity,
        "unmet_demand_flag": features["searches"] > features["likes"] * 1.2,
        "emerging_trend_flag": features["trend_growth"] >= 0.45,
        "investment_opportunity_interpretation": _interpret_opportunity(label, opportunity),
    }
    explanation = generate_prediction_explanation(features, prediction)
    return {
        **prediction,
        "features": features,
        "key_drivers": explanation["key_drivers"],
        "key_driver_summary": explanation["driver_summary"],
        "policy_note": explanation["policy_note"],
        "route_domain": "Behavioral Signals AI",
    }


def _interpret_opportunity(label: str, opportunity: float) -> str:
    if label == "High Demand":
        return "Strong Investment Opportunity"
    if opportunity >= 0.45:
        return "Emerging Opportunity"
    return "Limited Market Momentum"
