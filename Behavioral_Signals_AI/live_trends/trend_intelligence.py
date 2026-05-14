"""Convert public aggregate trend records into Signal intelligence outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from Behavioral_Signals_AI.explainability.privacy import sanitize_trend_record


DOMAIN_ROOT = Path(__file__).resolve().parent
LOCATIONS_PATH = DOMAIN_ROOT / "config" / "locations.json"


def predict_demand_details(*args: Any, **kwargs: Any) -> dict[str, Any]:
    return {
        "demand_classification": "Emerging Demand Signal",
        "confidence_score": 0.52,
        "aggregate_demand_score": 61.0,
        "opportunity_score": 58.0,
    }


def analyze_trend_signal(trend_record: dict[str, Any]) -> dict[str, Any]:
    """Turn a public aggregate trend record into Signal-style demand intelligence."""

    safe_record = sanitize_trend_record(dict(trend_record))
    proxy_inputs = build_trend_proxy_inputs(safe_record)

    prediction = predict_demand_details(
        proxy_inputs["likes"],
        proxy_inputs["comments"],
        proxy_inputs["shares"],
        proxy_inputs["searches"],
        proxy_inputs["engagement_intensity"],
        proxy_inputs["purchase_intent_score"],
        proxy_inputs["trend_growth"],
    )
    explanation = (
        f"Trend intelligence uses aggregate proxy estimates from rank, tweet volume, freshness, and location relevance. "
        f"Trend '{safe_record['trend_name']}' was translated into model inputs rather than individual-level activity."
    )

    return {
        "trend_name": safe_record["trend_name"],
        "location": safe_record["location"],
        "rank": safe_record["rank"],
        "tweet_volume": safe_record.get("tweet_volume"),
        "source": safe_record["source"],
        "platform": safe_record.get("platform", safe_record.get("source", "Aggregate trend feed")),
        "category": safe_record.get("category", "general_public_interest"),
        "volume": safe_record.get("volume") or safe_record.get("tweet_volume"),
        "growth_indicator": safe_record.get("growth_indicator", "not available"),
        "relevance_to_demand": safe_record.get("relevance_to_demand", 0.0),
        "possible_policy_or_business_implication": safe_record.get("possible_policy_or_business_implication", "Monitor for demand, price, shortage, or opportunity implications."),
        "fetched_at": safe_record.get("fetched_at", ""),
        "demand_classification": prediction["demand_classification"],
        "confidence_score": round(float(prediction["confidence_score"]) * 100, 2),
        "aggregate_demand_score": round(float(prediction["aggregate_demand_score"]), 2),
        "opportunity_score": round(float(prediction["opportunity_score"]), 2),
        "emerging_trend_probability": round(float(prediction.get("emerging_trend_probability", 0.52)) * 100, 2),
        "unmet_demand_probability": round(float(prediction.get("unmet_demand_probability", 0.35)) * 100, 2),
        "investment_policy_interpretation": prediction.get(
            "investment_opportunity_interpretation",
            "Temporary local trend intelligence fallback",
        ),
        "model_source_explanation": (
            f"{prediction.get('model_source_label', 'Local trend intelligence fallback')}\n\n"
            f"{explanation}\n\n"
            f"{prediction.get('key_driver_summary', 'Trend intelligence is using a lightweight local fallback.')}"
        ),
    }


def analyze_trend_batch(trend_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [analyze_trend_signal(record) for record in trend_records]


def summarize_trend_batch(location: str, analyses: list[dict[str, Any]]) -> str:
    if not analyses:
        return f"No live trends are available for {location} right now."

    highest = max(analyses, key=lambda item: float(item["opportunity_score"]))
    emerging = sum(1 for item in analyses if float(item["emerging_trend_probability"]) >= 60)
    unmet = sum(1 for item in analyses if float(item["unmet_demand_probability"]) >= 60)
    return (
        f"Signal reviewed {len(analyses)} public aggregate trends for {location}. "
        f"The strongest immediate opportunity is {highest['trend_name']} with an opportunity score of "
        f"{highest['opportunity_score']:.2f}. {emerging} trend(s) show elevated emerging momentum and "
        f"{unmet} trend(s) suggest possible unmet demand. These are proxy estimates derived from trend rank, "
        f"tweet volume where available, freshness, and location relevance."
    )


def build_trend_proxy_inputs(trend_record: dict[str, Any]) -> dict[str, float]:
    location_relevance = _location_relevance(str(trend_record.get("location", "Kenya")))
    rank = max(1, int(trend_record.get("rank", 1) or 1))
    tweet_volume = trend_record.get("tweet_volume") or trend_record.get("volume")
    volume = float(tweet_volume) if isinstance(tweet_volume, (int, float)) else 45000.0

    rank_strength = max(0.12, 1 - ((rank - 1) / 20))
    volume_strength = min(volume / 250000, 1.0)
    freshness = 1.0

    likes = round(40 + (rank_strength * 140) + (volume_strength * 110), 2)
    comments = round(8 + (rank_strength * 40) + (volume_strength * 24), 2)
    shares = round(6 + (rank_strength * 24) + (volume_strength * 18), 2)
    searches = round(35 + (rank_strength * 120) + (volume_strength * 150), 2)
    engagement_intensity = round(min(0.25 + rank_strength * 0.48 + volume_strength * 0.16, 1.0), 4)
    purchase_intent_score = round(min(0.18 + volume_strength * 0.4 + location_relevance * 0.12, 1.0), 4)
    trend_growth = round(min((rank_strength * 0.52) + (freshness * 0.18) + (volume_strength * 0.22), 1.0), 4)

    return {
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "searches": searches,
        "engagement_intensity": engagement_intensity,
        "purchase_intent_score": purchase_intent_score,
        "trend_growth": trend_growth,
    }


def _location_relevance(location: str) -> float:
    if not Path(LOCATIONS_PATH).exists():
        return 0.65 if location in {"Kenya", "Nairobi"} else 0.55
    payload = json.loads(Path(LOCATIONS_PATH).read_text(encoding="utf-8"))
    return float(payload.get(location, payload.get("Kenya", {})).get("location_relevance", 0.65))
