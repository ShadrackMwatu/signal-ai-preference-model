"""Hugging Face app entrypoint for Signal AI Dashboard."""

from __future__ import annotations

from Signal_CGE.dashboard.baseline_dashboard import baseline_dashboard_markdown
import json
import os
from datetime import UTC, datetime
from html import escape
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

for _mpl_candidate in [
    Path(os.environ.get("TEMP", "")) / f"signal_ai_matplotlib_{os.getpid()}",
    Path(os.environ.get("LOCALAPPDATA", "")) / "SignalAI" / "matplotlib",
    Path(__file__).resolve().parent / ".cache" / "matplotlib",
    Path(__file__).resolve().parent / "outputs" / "matplotlib",
]:
    try:
        if str(_mpl_candidate):
            _mpl_candidate.mkdir(parents=True, exist_ok=True)
            os.environ.setdefault("MPLCONFIGDIR", str(_mpl_candidate))
            break
    except OSError:
        continue

import gradio as gr

from app_routes.behavioral_route import run_behavioral_signal_prediction
from app_routes.signal_cge_route import (
    FULL_CGE_FALLBACK_MESSAGE,
    run_signal_cge_prompt as route_run_signal_cge_prompt,
)

from Behavioral_Signals_AI.explainability import generate_prediction_explanation

try:
    from Behavioral_Signals_AI.privacy import PRIVACY_NOTICE
except Exception:
    PRIVACY_NOTICE = "Signal uses aggregate behavioural signals only and does not track individuals."

try:
    from Behavioral_Signals_AI.live_trends.trend_intelligence import (
        analyze_trend_batch,
        summarize_trend_batch,
    )
except Exception:
    def analyze_trend_batch(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {
                **record,
                "demand_classification": "Emerging Signal",
                "confidence_score": 65.0,
                "aggregate_demand_score": 55.0,
                "opportunity_score": 60.0,
                "emerging_trend_probability": 0.6,
                "unmet_demand_probability": 0.35,
                "investment_policy_interpretation": "Monitor trend and validate demand.",
                "model_source_explanation": "Fallback live trend intelligence.",
            }
            for record in records
        ]

    def summarize_trend_batch(location: str, analyses: list[dict[str, Any]]) -> str:
        return f"Showing {len(analyses)} aggregate trend signals for {location}."

try:
    from Behavioral_Signals_AI.live_trends.x_trends import fetch_x_trends, get_demo_trends
except Exception:
    def get_demo_trends(location: str = "Kenya", limit: int = 5) -> list[dict[str, Any]]:
        topics = [
            "Cost of living",
            "Fuel prices",
            "Jobs and youth employment",
            "Healthcare access",
            "Agriculture prices",
            "School fees",
            "Electricity prices",
            "Trade facilitation",
        ]
        return [
            {
                "trend_name": topic,
                "rank": index + 1,
                "tweet_volume": 1000 + index * 250,
                "location": location,
                "fetched_at": datetime.now(UTC).isoformat(),
                "source": "Demo fallback",
            }
            for index, topic in enumerate(topics[: int(limit)])
        ]

    def fetch_x_trends(location: str = "Kenya", limit: int = 5) -> list[dict[str, Any]]:
        return get_demo_trends(location, limit)


ROOT_DIR = Path(__file__).resolve().parent
PRIMARY_MODEL_PATH = ROOT_DIR / "Behavioral_Signals_AI" / "models" / "model.pkl"
LEGACY_MODEL_PATH = ROOT_DIR / "model.pkl"
PRIMARY_MODEL_METADATA_PATH = ROOT_DIR / "Behavioral_Signals_AI" / "models" / "metadata.json"

PUBLIC_TABS = ["Behavioral Signals AI", "Signal CGE"]

SIGNAL_DASHBOARD_CSS = """
.signal-trend-shell {
    border: 1px solid #dbe3ef;
    border-radius: 10px;
    background: #ffffff;
    padding: 14px;
}
.signal-trend-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 12px;
}
.signal-trend-title {
    color: #0f172a;
    font-size: 20px;
    font-weight: 800;
}
.signal-trend-count {
    min-width: 132px;
    border: 1px solid #dbe3ef;
    border-radius: 8px;
    padding: 10px 12px;
    text-align: right;
    background: #f8fafc;
}
.signal-trend-count strong {
    display: block;
    color: #16a34a;
    font-size: 30px;
}
.signal-trend-viewport {
    height: 260px;
    overflow: hidden;
    border: 1px solid #dbe3ef;
    border-radius: 8px;
    background: #f8fafc;
}
.signal-trend-rail {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 12px;
    animation: signalTrendScroll 24s linear infinite;
}
.signal-trend-issue {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    border: 1px solid #dbe3ef;
    border-radius: 8px;
    background: #ffffff;
    padding: 14px 16px;
}
.signal-trend-issue-name {
    color: #0f172a;
    font-size: 16px;
    font-weight: 800;
}
.signal-trend-pill {
    border: 1px solid #dbe3ef;
    border-radius: 999px;
    color: #475569;
    background: #f8fafc;
    font-size: 12px;
    font-weight: 650;
    padding: 4px 8px;
}
@keyframes signalTrendScroll {
    0% { transform: translateY(35%); }
    100% { transform: translateY(-55%); }
}
"""

DISPLAY_LABELS = {
    "Validate Signal Quality": "Emerging Signal — Further Monitoring Recommended",
    "Monitor Further": "Emerging Signal — Further Monitoring Recommended",
    "Weak Signal": "Limited Market Momentum",
    "Possible Noise": "Signal Volatility Detected",
    "Investigate Anomaly / Possible Unmet Demand": "Potential Unmet Demand Opportunity",
    "Moderate Demand": "Developing Market Interest",
    "High Demand": "Strong Demand Momentum",
    "Low Demand": "Limited Demand Signal",
    "Emerging Demand": "Emerging Demand Signal",
    "Declining Demand": "Limited Market Momentum",
    "Unmet Demand": "Potential Unmet Demand Opportunity",
}


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def _display_label(label: str) -> str:
    return DISPLAY_LABELS.get(label, label)


def _map_demand_label(prediction: Any) -> str:
    text = str(prediction).strip().lower()
    if prediction == 2 or text in {"2", "high", "high demand"}:
        return "High Demand"
    if prediction == 1 or text in {"1", "moderate", "moderate demand"}:
        return "Moderate Demand"
    if text in {"emerging", "emerging demand"}:
        return "Emerging Demand"
    if text in {"declining", "declining demand"}:
        return "Declining Demand"
    if text in {"unmet", "unmet demand"}:
        return "Unmet Demand"
    return "Low Demand"


def _normalize_demand_band(label: str) -> str:
    if label in {"High Demand"}:
        return "High Demand"
    if label in {"Moderate Demand", "Emerging Demand"}:
        return "Moderate Demand"
    return "Low Demand"


def _build_signal_features(
    likes: float,
    comments: float,
    shares: float,
    searches: float,
    engagement_intensity: float,
    purchase_intent_score: float,
    trend_growth: float,
) -> dict[str, float]:
    likes = _safe_float(likes)
    comments = _safe_float(comments)
    shares = _safe_float(shares)
    searches = _safe_float(searches)
    engagement_intensity = np.clip(_safe_float(engagement_intensity), 0, 1)
    purchase_intent_score = np.clip(_safe_float(purchase_intent_score), 0, 1)
    trend_growth = np.clip(_safe_float(trend_growth), -1, 1)

    total_engagement = likes + comments + shares + searches
    mentions_count = comments + shares * 0.5
    sentiment_score = np.clip((purchase_intent_score * 0.75) - 0.15 + trend_growth * 0.2, -1, 1)
    urgency_score = np.clip((searches / max(total_engagement, 1)) * 1.5 + trend_growth * 0.45, 0, 1)
    repetition_score = np.clip(searches / max(likes + comments + 1, 1), 0, 1)
    price_sensitivity = np.clip(0.65 - purchase_intent_score * 0.35 + (1 - engagement_intensity) * 0.15, 0, 1)
    noise_score = np.clip(1 - min((comments + shares + 1) / max(likes + searches + 1, 1), 1), 0, 1)
    engagement_rate = np.clip(total_engagement / max(total_engagement + 100, 1), 0, 1)
    weighted_engagement_score = np.clip(
        (likes + comments * 1.8 + shares * 2.4 + searches * 1.6 + mentions_count) / 100,
        0,
        10,
    )
    trend_momentum = np.clip(trend_growth * 0.6 + urgency_score * 0.4, 0, 1)
    unmet_need_signal = np.clip(urgency_score * 0.45 + price_sensitivity * 0.25 + (1 - sentiment_score) * 0.1, 0, 1)
    opportunity_index = np.clip(
        engagement_intensity * 0.22
        + purchase_intent_score * 0.22
        + trend_growth * 0.18
        + urgency_score * 0.14
        + repetition_score * 0.08
        + unmet_need_signal * 0.12
        + 0.55 * 0.06
        - noise_score * 0.08,
        0,
        1,
    )

    return {
        "likes": round(float(likes), 4),
        "comments": round(float(comments), 4),
        "shares": round(float(shares), 4),
        "searches": round(float(searches), 4),
        "likes_count": round(float(likes), 4),
        "comments_count": round(float(comments), 4),
        "shares_count": round(float(shares), 4),
        "searches_count": round(float(searches), 4),
        "mentions_count": round(float(mentions_count), 4),
        "engagement_intensity": round(float(engagement_intensity), 4),
        "purchase_intent_score": round(float(purchase_intent_score), 4),
        "sentiment_score": round(float(sentiment_score), 4),
        "urgency_score": round(float(urgency_score), 4),
        "trend_growth": round(float(trend_growth), 4),
        "repetition_score": round(float(repetition_score), 4),
        "price_sensitivity": round(float(price_sensitivity), 4),
        "noise_score": round(float(noise_score), 4),
        "engagement_rate": round(float(engagement_rate), 4),
        "weighted_engagement_score": round(float(weighted_engagement_score), 4),
        "trend_momentum": round(float(trend_momentum), 4),
        "unmet_need_signal": round(float(unmet_need_signal), 4),
        "opportunity_index": round(float(opportunity_index), 4),
    }


def _load_prediction_artifact() -> dict[str, Any] | None:
    for candidate in (PRIMARY_MODEL_PATH, LEGACY_MODEL_PATH):
        if candidate.exists():
            artifact = joblib.load(candidate)
            if isinstance(artifact, dict):
                return artifact
            return {"model": artifact, "feature_columns": ["likes", "comments", "shares", "searches"]}
    return None


def _metadata_value(key: str, default: str) -> str:
    if not PRIMARY_MODEL_METADATA_PATH.exists():
        return default
    try:
        payload = json.loads(PRIMARY_MODEL_METADATA_PATH.read_text(encoding="utf-8"))
        return str(payload.get(key, default))
    except Exception:
        return default


def _positive_probability(model: Any | None, vector: pd.DataFrame) -> float:
    if model is None or not hasattr(model, "predict_proba"):
        return 0.0
    probabilities = model.predict_proba(vector)[0]
    return float(probabilities[-1]) if len(probabilities) > 1 else float(probabilities[0])


def _predict_with_fallback(features: dict[str, float]) -> dict[str, Any]:
    latent = np.clip(
        features["engagement_intensity"] * 0.28
        + features["purchase_intent_score"] * 0.18
        + features["trend_growth"] * 0.2
        + features["urgency_score"] * 0.16
        + features["repetition_score"] * 0.1
        + features["opportunity_index"] * 0.26,
        0,
        1,
    )

    if features["searches"] >= 160 and features["engagement_intensity"] < 0.45 and features["purchase_intent_score"] >= 0.6:
        raw_demand = "Unmet Demand"
    elif features["trend_growth"] <= -0.08 and features["engagement_intensity"] < 0.5:
        raw_demand = "Declining Demand"
    elif features["trend_growth"] >= 0.48 and features["engagement_intensity"] >= 0.46:
        raw_demand = "Emerging Demand"
    elif latent >= 0.68:
        raw_demand = "High Demand"
    elif latent >= 0.42:
        raw_demand = "Moderate Demand"
    else:
        raw_demand = "Low Demand"

    unmet_probability = float(np.clip(features["unmet_need_signal"], 0, 1))
    emerging_probability = float(np.clip(features["trend_momentum"], 0, 1))
    confidence_score = float(np.clip(0.52 + abs(latent - 0.5) * 0.4, 0, 0.95))
    aggregate_demand_score = float(np.clip(latent * 100, 0, 100))
    opportunity_score = float(
        np.clip(
            aggregate_demand_score * 0.58
            + unmet_probability * 100 * 0.22
            + emerging_probability * 100 * 0.2,
            0,
            100,
        )
    )

    return {
        "raw_demand_classification": raw_demand,
        "demand_classification": _display_label(raw_demand),
        "demand_band": _normalize_demand_band(raw_demand),
        "confidence_score": round(confidence_score, 4),
        "aggregate_demand_score": round(aggregate_demand_score, 2),
        "opportunity_score": round(opportunity_score, 2),
        "unmet_demand_probability": round(unmet_probability, 4),
        "emerging_trend_probability": round(emerging_probability, 4),
        "prediction_source": "Fallback Logic — trained model not available.",
        "model_source_components": ["Fallback Logic"],
        "model_source_label": "Fallback Logic — trained model not available.",
        "explanation_note": "Fallback scoring used because the trained model artifact was unavailable.",
        "model_version": "unavailable",
    }


def _predict_with_model(features: dict[str, float]) -> dict[str, Any]:
    artifact = _load_prediction_artifact()
    if artifact is None:
        return _predict_with_fallback(features)

    model = artifact.get("model", artifact)
    feature_columns = artifact.get("feature_columns") or list(features.keys())
    frame = pd.DataFrame([{col: float(features.get(col, 0.0)) for col in feature_columns}])

    raw_prediction = _map_demand_label(model.predict(frame)[0])
    probabilities = model.predict_proba(frame)[0] if hasattr(model, "predict_proba") else np.array([1.0])
    classes = [_map_demand_label(label) for label in getattr(model, "classes_", ["Low Demand", "Moderate Demand", "High Demand"])]
    class_probabilities = {label: float(prob) for label, prob in zip(classes, probabilities)}
    confidence_score = float(max(class_probabilities.values(), default=1.0))

    demand_weights = {
        "High Demand": 1.0,
        "Moderate Demand": 0.62,
        "Low Demand": 0.2,
        "Emerging Demand": 0.58,
        "Declining Demand": 0.16,
        "Unmet Demand": 0.52,
    }
    aggregate_demand_score = float(
        np.clip(sum(class_probabilities.get(label, 0.0) * weight for label, weight in demand_weights.items()) * 100, 0, 100)
    )

    unmet_probability = _positive_probability(artifact.get("unmet_model"), frame)
    emerging_probability = _positive_probability(artifact.get("emerging_model"), frame)
    opportunity_score = float(
        np.clip(
            aggregate_demand_score * 0.5
            + features["opportunity_index"] * 100 * 0.25
            + unmet_probability * 100 * 0.15
            + emerging_probability * 100 * 0.1,
            0,
            100,
        )
    )

    return {
        "raw_demand_classification": raw_prediction,
        "demand_classification": _display_label(raw_prediction),
        "demand_band": _normalize_demand_band(raw_prediction),
        "confidence_score": round(confidence_score, 4),
        "aggregate_demand_score": round(aggregate_demand_score, 2),
        "opportunity_score": round(opportunity_score, 2),
        "unmet_demand_probability": round(unmet_probability, 4),
        "emerging_trend_probability": round(emerging_probability, 4),
        "prediction_source": "Trained ML Model",
        "model_source_components": ["Trained ML Model"],
        "model_source_label": "Trained ML Model",
        "explanation_note": "Primary prediction produced by the trained local Signal model.",
        "model_version": str(artifact.get("model_version", _metadata_value("model_version", "legacy"))),
    }


def _apply_guardrails(result: dict[str, Any], features: dict[str, float]) -> dict[str, Any]:
    raw_demand = str(result.get("raw_demand_classification", result["demand_classification"]))
    demand_band = str(result.get("demand_band", _normalize_demand_band(raw_demand)))
    opportunity = float(result["opportunity_score"])
    confidence = float(result["confidence_score"])
    unmet_probability = float(result["unmet_demand_probability"])
    emerging_probability = float(result["emerging_trend_probability"])
    notes = [str(result["explanation_note"])]
    source_components = list(result.get("model_source_components", []))

    if demand_band == "High Demand" and opportunity >= 70:
        raw_interpretation = "Strong Investment Opportunity"
    elif demand_band == "Moderate Demand" and opportunity >= 55:
        raw_interpretation = "Emerging Opportunity"
    elif demand_band == "Low Demand" and opportunity >= 55:
        raw_interpretation = "Investigate Anomaly / Possible Unmet Demand"
        unmet_probability = max(unmet_probability, float(np.clip(features["unmet_need_signal"], 0, 1)))
        notes.append("Guardrail flagged a contradiction between low demand and elevated opportunity.")
    else:
        raw_interpretation = "Weak Signal"

    if demand_band == "High Demand" and confidence < 0.62:
        raw_interpretation = "Monitor Further"
        notes.append("High-demand classification arrived with low confidence and should be monitored further.")

    if features.get("searches", 0) >= 160 and features.get("engagement_intensity", 0) < 0.45:
        unmet_probability = max(unmet_probability, 0.72)
        notes.append("High searches with low engagement suggest a possible unmet demand pocket.")
        source_components.append("Anomaly / Unmet Demand Detection")

    if features.get("noise_score", 0) >= 0.75:
        raw_interpretation = "Validate Signal Quality" if opportunity >= 45 else raw_interpretation
        notes.append("High noise score suggests more data quality review before acting.")

    if len(notes) > 1:
        source_components.append("Guardrail Adjustment")

    result = dict(result)
    result["raw_demand_classification"] = raw_demand
    result["demand_classification"] = _display_label(raw_demand)
    result["raw_investment_opportunity_interpretation"] = raw_interpretation
    result["investment_opportunity_interpretation"] = _display_label(raw_interpretation)
    result["unmet_demand_flag"] = bool(unmet_probability >= 0.6)
    result["emerging_trend_flag"] = bool(emerging_probability >= 0.55)
    result["explanation_note"] = " ".join(notes)
    result["demand_band"] = demand_band
    result["unmet_demand_probability"] = round(unmet_probability, 4)
    result["model_source_components"] = list(dict.fromkeys(source_components))
    result["prediction_source"] = " | ".join(result["model_source_components"])
    result["model_source_label"] = result["prediction_source"].replace("â€”", "—")
    return result


def _calculate_intelligence_scores(features: dict[str, float], result: dict[str, Any]) -> dict[str, float]:
    weighted_engagement_normalized = float(np.clip(features["weighted_engagement_score"] / 10, 0, 1))
    signal_strength = np.clip(
        (
            features["engagement_intensity"] * 0.28
            + features["purchase_intent_score"] * 0.22
            + features["engagement_rate"] * 0.14
            + weighted_engagement_normalized * 0.14
            + max(features["sentiment_score"], 0) * 0.08
            + float(result["confidence_score"]) * 0.14
        )
        * 100,
        0,
        100,
    )
    momentum_score = np.clip(
        (
            features["trend_momentum"] * 0.48
            + max(features["trend_growth"], 0) * 0.24
            + float(result["emerging_trend_probability"]) * 0.18
            + features["urgency_score"] * 0.1
        )
        * 100,
        0,
        100,
    )
    volatility_noise_score = np.clip(
        (
            features["noise_score"] * 0.7
            + abs(features["trend_growth"] - features["engagement_intensity"]) * 0.2
            + max(-features["sentiment_score"], 0) * 0.1
        )
        * 100,
        0,
        100,
    )
    persistence_score = np.clip(
        (features["repetition_score"] * 0.65 + features["engagement_intensity"] * 0.2 + features["engagement_rate"] * 0.15) * 100,
        0,
        100,
    )
    adoption_probability = np.clip(
        signal_strength * 0.3
        + momentum_score * 0.18
        + features["purchase_intent_score"] * 100 * 0.2
        + float(result["aggregate_demand_score"]) * 0.16
        + float(result["confidence_score"]) * 100 * 0.16,
        0,
        100,
    )
    viral_probability = np.clip(
        (
            min(features["shares_count"] / max(features["likes_count"] + 1, 1), 1) * 0.26
            + min(features["comments_count"] / max(features["likes_count"] + 1, 1), 1) * 0.12
            + min(features["searches_count"] / max(features["likes_count"] + 1, 1), 1) * 0.16
            + max(features["trend_growth"], 0) * 0.24
            + features["engagement_intensity"] * 0.12
            + features["urgency_score"] * 0.1
        )
        * 100,
        0,
        100,
    )
    return {
        "signal_strength_score": round(float(signal_strength), 2),
        "momentum_score": round(float(momentum_score), 2),
        "volatility_noise_score": round(float(volatility_noise_score), 2),
        "persistence_score": round(float(persistence_score), 2),
        "adoption_probability": round(float(adoption_probability), 2),
        "viral_probability": round(float(viral_probability), 2),
    }


def _build_risk_signals(features: dict[str, float], result: dict[str, Any]) -> list[str]:
    risks = []
    if float(result["confidence_score"]) < 0.6:
        risks.append("Low confidence means this signal should be monitored before large commitments.")
    if features["noise_score"] >= 0.7:
        risks.append("Signal volatility detected: elevated noise suggests additional validation is needed.")
    if bool(result.get("unmet_demand_flag")):
        risks.append("Potential unmet demand may reflect access, delivery, or affordability gaps.")
    if features["sentiment_score"] < 0:
        risks.append("Soft sentiment may limit conversion even if attention remains elevated.")
    if features["price_sensitivity"] >= 0.68:
        risks.append("High price sensitivity suggests affordability could slow adoption.")
    return risks[:3] or ["No major validation risks were detected in the current aggregate signal."]


def _build_why_this_matters(features: dict[str, float], result: dict[str, Any]) -> str:
    classification = str(result["demand_classification"])
    confidence = float(result["confidence_score"]) * 100
    if result.get("unmet_demand_flag"):
        return (
            "Rising search activity and uneven engagement suggest latent demand that may not yet be fully served. "
            f"The current signal is classified as {classification.lower()} with {confidence:.1f}% confidence."
        )
    if features["trend_growth"] >= 0.45:
        return (
            "Momentum is building quickly, which can signal a near-term opening for investment, product positioning, or targeted outreach. "
            f"Signal currently reads as {classification.lower()}."
        )
    return (
        "Current activity shows the market is moving, but the strength and quality of participation still matter. "
        f"Signal currently reads as {classification.lower()}."
    )


def predict_demand_details(
    likes: float,
    comments: float,
    shares: float,
    searches: float,
    engagement_intensity: float,
    purchase_intent_score: float,
    trend_growth: float,
) -> dict[str, Any]:
    try:
        features = _build_signal_features(
            likes,
            comments,
            shares,
            searches,
            engagement_intensity,
            purchase_intent_score,
            trend_growth,
        )
        model_result = _predict_with_model(features)
        guarded = _apply_guardrails(model_result, features)
        explanation = generate_prediction_explanation(features, guarded)
        guarded["key_drivers"] = explanation.get("key_drivers", [])
        guarded["key_driver_summary"] = explanation.get("driver_summary", "")
        guarded["policy_note"] = explanation.get("policy_note", "")
        guarded["risk_signals"] = _build_risk_signals(features, guarded)
        guarded.update(_calculate_intelligence_scores(features, guarded))
        guarded["why_this_matters"] = _build_why_this_matters(features, guarded)
        guarded["product_domain_route"] = run_behavioral_signal_prediction(
            likes,
            comments,
            shares,
            searches,
            engagement_intensity,
            purchase_intent_score,
            trend_growth,
        ).get("route_domain", "Behavioral_Signals_AI")
        return guarded
    except Exception as exc:
        return {
            "demand_classification": f"Error: {exc}",
            "confidence_score": 0.0,
            "aggregate_demand_score": 0.0,
            "opportunity_score": 0.0,
            "investment_opportunity_interpretation": "Prediction failed",
            "unmet_demand_probability": 0.0,
            "emerging_trend_probability": 0.0,
            "unmet_demand_flag": False,
            "emerging_trend_flag": False,
            "demand_band": "Low Demand",
            "prediction_source": "Error",
            "model_source_label": "Error",
            "explanation_note": f"Prediction pipeline failed: {exc}",
            "key_drivers": ["prediction error"],
            "risk_signals": ["Prediction pipeline failed before validation could complete."],
            "policy_note": "Check model availability and input validity before interpreting this signal.",
            "why_this_matters": "Signal could not complete the assessment.",
            "signal_strength_score": 0.0,
            "momentum_score": 0.0,
            "volatility_noise_score": 0.0,
            "persistence_score": 0.0,
            "adoption_probability": 0.0,
            "viral_probability": 0.0,
            "model_version": "unavailable",
        }


def _format_panel_explanation(result: dict[str, Any]) -> str:
    lines = [
        "AI Intelligence Brief",
        "",
        "1. Classification",
        f"Demand classification: {result.get('demand_classification', '')}",
        f"Confidence level: {float(result.get('confidence_score', 0)) * 100:.1f}%",
        f"Aggregate demand score: {float(result.get('aggregate_demand_score', 0)):.2f}",
        f"Opportunity score: {float(result.get('opportunity_score', 0)):.2f}",
        "",
        "2. Key Drivers",
    ]
    lines.extend(f"- {driver}" for driver in result.get("key_drivers", [])[:3] or ["No dominant drivers identified."])
    lines.extend(["", "3. Risk / Validation Signals"])
    lines.extend(f"- {risk}" for risk in result.get("risk_signals", [])[:3] or ["No major validation risks were detected."])
    lines.extend(["", "4. Strategic Interpretation", str(result.get("why_this_matters", "")), "", "5. Model Source", str(result.get("model_source_label", ""))])
    return "\n".join(lines)


def predict_demand(
    likes: float,
    comments: float,
    shares: float,
    searches: float,
    engagement_intensity: float,
    purchase_intent_score: float,
    trend_growth: float,
) -> tuple[str, float, float, float, float, float, str, str]:
    result = predict_demand_details(
        likes,
        comments,
        shares,
        searches,
        engagement_intensity,
        purchase_intent_score,
        trend_growth,
    )
    return (
        str(result["demand_classification"]),
        round(float(result["confidence_score"]) * 100, 2),
        round(float(result["aggregate_demand_score"]), 2),
        round(float(result["opportunity_score"]), 2),
        round(float(result["emerging_trend_probability"]) * 100, 2),
        round(float(result["unmet_demand_probability"]) * 100, 2),
        str(result["investment_opportunity_interpretation"]),
        _format_panel_explanation(result),
    )


def signal_model(
    likes: float,
    comments: float,
    shares: float,
    searches: float,
    engagement_intensity: float,
    purchase_intent_score: float,
    trend_growth: float,
) -> tuple[str, float, float]:
    result = predict_demand_details(
        likes,
        comments,
        shares,
        searches,
        engagement_intensity,
        purchase_intent_score,
        trend_growth,
    )
    label = str(result["demand_band"])
    legacy_label = {"High Demand": "High", "Moderate Demand": "Moderate", "Low Demand": "Low"}.get(label, label)
    return (
        legacy_label,
        max(0.0, min(100.0, float(result["aggregate_demand_score"]))),
        max(0.0, min(100.0, float(result["opportunity_score"]))),
    )


def _render_gauge_card(title: str, value: float, color: str) -> str:
    safe_title = escape(title)
    width = max(0.0, min(float(value), 100.0))
    return (
        "<div style='border:1px solid #dbe3ef;border-radius:8px;padding:12px;background:#ffffff;'>"
        f"<div style='font-size:13px;font-weight:600;color:#1f2937;margin-bottom:8px;'>{safe_title}</div>"
        f"<div style='font-size:24px;font-weight:700;color:#111827;margin-bottom:8px;'>{width:.1f}</div>"
        "<div style='height:12px;background:#eef2f7;border-radius:999px;overflow:hidden;'>"
        f"<div style='height:12px;width:{width:.1f}%;background:{color};border-radius:999px;'></div>"
        "</div></div>"
    )


def _render_radar_chart(values: dict[str, float]) -> str:
    rows = "".join(
        f"<div><strong>{escape(label)}:</strong> {float(value):.1f}</div>"
        for label, value in values.items()
    )
    return (
        "<div style='border:1px solid #dbe3ef;border-radius:8px;padding:12px;background:#ffffff;'>"
        "<div style='font-size:13px;font-weight:600;color:#1f2937;margin-bottom:8px;'>Opportunity Radar</div>"
        f"{rows}</div>"
    )


def _render_key_driver_cards(drivers: list[str], risks: list[str]) -> str:
    driver_markup = "".join(f"<li>{escape(str(driver))}</li>" for driver in (drivers or [])[:3])
    risk_markup = "".join(f"<li>{escape(str(risk))}</li>" for risk in (risks or [])[:3])
    return (
        "<div style='border:1px solid #dbe3ef;border-radius:8px;padding:12px;background:#ffffff;'>"
        "<strong>Key drivers</strong><ul>" + driver_markup + "</ul>"
        "<strong>Validation signals</strong><ul>" + risk_markup + "</ul></div>"
    )


def _build_visual_components(result: dict[str, Any]) -> dict[str, str]:
    return {
        "confidence_gauge_html": _render_gauge_card("Confidence Gauge", float(result["confidence_score"]) * 100, "#2563eb"),
        "signal_strength_gauge_html": _render_gauge_card("Signal Strength Gauge", float(result["signal_strength_score"]), "#16a34a"),
        "momentum_indicator_html": _render_gauge_card("Trend Momentum Indicator", float(result["momentum_score"]), "#d97706"),
        "opportunity_radar_html": _render_radar_chart(
            {
                "Opportunity": float(result["opportunity_score"]),
                "Momentum": float(result["momentum_score"]),
                "Adoption": float(result["adoption_probability"]),
                "Persistence": float(result["persistence_score"]),
                "Viral": float(result["viral_probability"]),
            }
        ),
        "key_driver_cards_html": _render_key_driver_cards(result.get("key_drivers", []), result.get("risk_signals", [])),
    }


def update_behavioral_dashboard(
    likes: float,
    comments: float,
    shares: float,
    searches: float,
    engagement_intensity: float,
    purchase_intent_score: float,
    trend_growth: float,
) -> tuple[Any, ...]:
    result = predict_demand_details(
        likes,
        comments,
        shares,
        searches,
        engagement_intensity,
        purchase_intent_score,
        trend_growth,
    )
    visuals = _build_visual_components(result)
    return (
        str(result["demand_classification"]),
        round(float(result["confidence_score"]) * 100, 2),
        round(float(result["aggregate_demand_score"]), 2),
        round(float(result["opportunity_score"]), 2),
        round(float(result["emerging_trend_probability"]) * 100, 2),
        round(float(result["unmet_demand_probability"]) * 100, 2),
        str(result["investment_opportunity_interpretation"]),
        _format_panel_explanation(result),
        round(float(result["signal_strength_score"]), 2),
        round(float(result["momentum_score"]), 2),
        round(float(result["volatility_noise_score"]), 2),
        round(float(result["persistence_score"]), 2),
        round(float(result["adoption_probability"]), 2),
        round(float(result["viral_probability"]), 2),
        str(result["why_this_matters"]),
        visuals["confidence_gauge_html"],
        visuals["signal_strength_gauge_html"],
        visuals["momentum_indicator_html"],
        visuals["opportunity_radar_html"],
        visuals["key_driver_cards_html"],
    )


def _utc_timestamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")


def _build_hidden_trends_frame(raw_frame: pd.DataFrame, intelligence_frame: pd.DataFrame) -> pd.DataFrame:
    if raw_frame.empty:
        raw_frame = pd.DataFrame(get_demo_trends("Kenya", limit=5))
    if intelligence_frame.empty:
        intelligence_frame = pd.DataFrame(analyze_trend_batch(raw_frame.to_dict(orient="records")))

    available_columns = [
        column
        for column in [
            "trend_name",
            "demand_classification",
            "confidence_score",
            "aggregate_demand_score",
            "opportunity_score",
            "emerging_trend_probability",
            "unmet_demand_probability",
            "investment_policy_interpretation",
            "model_source_explanation",
        ]
        if column in intelligence_frame.columns
    ]

    if "trend_name" in intelligence_frame.columns:
        return raw_frame.merge(intelligence_frame[available_columns], on="trend_name", how="left")
    return raw_frame


def _active_trend_count(trends_df: pd.DataFrame) -> int:
    if trends_df.empty or "trend_name" not in trends_df.columns:
        return 0
    names = trends_df["trend_name"].fillna("").astype(str).str.strip()
    return int(((names != "") & (names.str.lower() != "unavailable")).sum())


def _render_public_trend_issue(record: dict[str, Any]) -> str:
    trend_name = escape(str(record.get("trend_name", "Monitoring trend")))
    source = escape(str(record.get("source", "Aggregate trend feed")))
    location = escape(str(record.get("location", "Kenya")))
    confidence = _safe_float(record.get("confidence_score"), 0.0)
    confidence_label = f"Confidence {confidence:.1f}%" if confidence > 0 else "Confidence pending"
    return (
        "<div class='signal-trend-issue'>"
        f"<div class='signal-trend-issue-name'>{trend_name}</div>"
        "<div>"
        f"<span class='signal-trend-pill'>{location}</span> "
        f"<span class='signal-trend-pill'>{escape(confidence_label)}</span> "
        f"<span class='signal-trend-pill'>{source}</span>"
        "</div></div>"
    )


def build_live_trend_html(trends_df: pd.DataFrame) -> str:
    if trends_df.empty or "trend_name" not in trends_df.columns:
        trends_df = _build_hidden_trends_frame(pd.DataFrame(get_demo_trends("Kenya", limit=5)), pd.DataFrame())

    records = [
        record
        for record in trends_df.to_dict(orient="records")
        if str(record.get("trend_name", "")).strip().lower() not in {"", "unavailable"}
    ]
    if not records:
        records = get_demo_trends("Kenya", limit=5)

    active_count = len(records)
    location = records[0].get("location", "Kenya")
    cards = [_render_public_trend_issue(record) for record in records]
    return (
        "<div class='signal-trend-shell'>"
        "<div class='signal-trend-header'>"
        "<div><div class='signal-trend-title'>Live Trend Intelligence</div>"
        f"<span class='signal-trend-pill'>Location: {escape(str(location))}</span> "
        f"<span class='signal-trend-pill'>Updated: {escape(_utc_timestamp())}</span></div>"
        f"<div class='signal-trend-count'><strong>{active_count}</strong><span> active trends</span></div>"
        "</div>"
        "<div class='signal-trend-viewport'><div class='signal-trend-rail'>"
        + "".join(cards + cards)
        + "</div></div></div>"
    )


def refresh_live_trends(location: str, trend_limit: float) -> tuple[pd.DataFrame, pd.DataFrame, str]:
    try:
        records = fetch_x_trends(location=location, limit=int(trend_limit))
        fallback_note = ""
    except Exception as exc:
        records = get_demo_trends(location=location if location in {"Kenya", "Nairobi", "Global"} else "Kenya", limit=int(trend_limit))
        fallback_note = f"Live API unavailable — displaying demo aggregate trends. Details: {exc}"

    analyses = analyze_trend_batch(records)
    raw_frame = pd.DataFrame(records)
    intelligence_frame = pd.DataFrame(analyses)
    trends_frame = _build_hidden_trends_frame(raw_frame, intelligence_frame)
    summary = summarize_trend_batch(location, analyses)
    if fallback_note:
        summary = f"{summary}\n\n{fallback_note}"
    return trends_frame, intelligence_frame, summary


def refresh_live_trend_intelligence(location: str, trend_limit: float) -> tuple[pd.DataFrame, str, int, str, pd.DataFrame]:
    trends_frame, intelligence_frame, summary = refresh_live_trends(location, trend_limit)
    return trends_frame, build_live_trend_html(trends_frame), _active_trend_count(trends_frame), summary, intelligence_frame


def _dashboard_status_banner() -> str:
    mode = "Live API available" if os.getenv("X_BEARER_TOKEN", "").strip() else "Demo fallback"
    return (
        "<div style='border:1px solid #cbd5e1;border-radius:10px;padding:14px 16px;margin:0 0 12px 0;background:#f8fafc;color:#0f172a;'>"
        "<div style='font-size:22px;font-weight:800;margin-bottom:8px;'>Signal AI Dashboard</div>"
        "<span style='border:1px solid #bbf7d0;background:#ecfdf5;border-radius:999px;padding:5px 10px;font-weight:700;'>Status: Running</span> "
        f"<span style='border:1px solid #bfdbfe;background:#eff6ff;border-radius:999px;padding:5px 10px;font-weight:700;'>Mode: {escape(mode)}</span> "
        "<span style='border:1px solid #e2e8f0;background:#ffffff;border-radius:999px;padding:5px 10px;font-weight:700;'>Privacy: Aggregate signals only</span>"
        "</div>"
    )


def _behavioral_section_intro() -> str:
    return (
        "## Behavioral Signals AI\n"
        "Estimate demand, opportunity, confidence, unmet demand, and market signal strength from aggregate behavioural inputs."
    )


def _how_to_use_signal_markdown() -> str:
    return (
        "1. Adjust behavioural signal inputs.\n"
        "2. Click **Predict Demand**.\n"
        "3. Review demand classification and opportunity score.\n"
        "4. Use Live Trend Intelligence to compare current topical issues."
    )


def _model_interpretation_markdown() -> str:
    return (
        "- **Demand Classification:** Overall demand band inferred from aggregate signal quality.\n"
        "- **Confidence Score:** How strongly Signal trusts the current classification.\n"
        "- **Aggregate Demand Score:** Combined demand intensity from engagement and search proxies.\n"
        "- **Opportunity Score:** Estimated market or policy action potential.\n"
        "- **Unmet Demand Probability:** Likelihood of access, affordability, or delivery gaps.\n"
        "- **Emerging Trend Probability:** Likelihood that the signal is gaining early momentum."
    )


def _fallback_live_trend_html(message: str = "Live API unavailable — displaying demo aggregate trends.") -> str:
    return f"<div class='signal-trend-shell'><h3>Live Trend Intelligence</h3><p>{escape(message)}</p></div>"


def _uploaded_path(file_obj: Any | None) -> str | None:
    if file_obj is None:
        return None
    return str(getattr(file_obj, "name", file_obj))


def run_signal_cge_prompt(prompt: str, uploaded_file: Any | None = None, backend: str = "Static equilibrium CGE solver") -> dict[str, Any]:
    return route_run_signal_cge_prompt(prompt, uploaded_file, backend)


def _render_interpreted_scenario(result: dict[str, Any]) -> str:
    scenario = result.get("scenario", {})
    return "\n".join(
        [
            "## Interpreted Scenario",
            f"- Prompt: `{scenario.get('prompt', '')}`",
            f"- Backend requested: `{scenario.get('backend_requested', result.get('backend_used', ''))}`",
            f"- Backend used: `{result.get('backend_used', '')}`",
        ]
    )


def _render_results_cards(result: dict[str, Any]) -> str:
    results = result.get("results", {})
    cards = [
        ("GDP/output effect", results.get("GDP/output effect", 0.0)),
        ("Household income effect", results.get("household income effect", 0.0)),
        ("Trade effect", results.get("trade effect", 0.0)),
        ("Solver used", result.get("backend_used", "fallback")),
    ]
    return "<div style='display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;'>" + "".join(
        "<div style='border:1px solid #dbe3ef;border-radius:8px;padding:12px;background:#fff;'>"
        f"<div style='font-size:12px;color:#64748b;font-weight:700;'>{escape(label)}</div>"
        f"<div style='font-size:20px;font-weight:800;color:#0f172a;margin-top:4px;'>{escape(str(value))}</div>"
        "</div>"
        for label, value in cards
    ) + "</div>"


def _results_table_dataframe(result: dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(result.get("results_table", []))


def _render_policy_interpretation(interpretation: dict[str, Any]) -> str:
    return "\n".join(
        [
            "## Policy Interpretation",
            str(interpretation.get("summary", "")),
            "",
            "### References Used",
            *[f"- {item}" for item in interpretation.get("knowledge_references_used", [])],
        ]
    )


def _render_model_reference_used(result: dict[str, Any]) -> str:
    refs = result.get("knowledge_context", {}).get("reference_labels", [])
    return "\n".join(["## Model Reference Used", *[f"- {ref}" for ref in refs or ["Canonical Signal CGE route"]]])


def _render_adaptive_learning_trace(trace: dict[str, Any]) -> str:
    return "## Adaptive Learning Trace\n- Learning trace will activate as Signal CGE learning modules are connected."


def _render_full_cge_status(status: dict[str, Any]) -> str:
    return "## Full CGE Development Status\n- Static/prototype route active.\n- Full recursive-dynamic CGE model remains under development."


def _render_diagnostics(diagnostics: dict[str, Any]) -> str:
    return "## Diagnostics\n```json\n" + json.dumps(diagnostics, indent=2) + "\n```"


def _render_readiness(readiness: dict[str, Any]) -> str:
    return "## Model Readiness\n```json\n" + json.dumps(readiness, indent=2) + "\n```"


def signal_cge_prompt_ui(prompt: str, backend: str, uploaded_file: Any | None = None) -> tuple[
    str,
    str,
    pd.DataFrame,
    pd.DataFrame,
    str,
    str,
    str,
    str,
    str,
    str,
    str | None,
    str | None,
    str | None,
]:
    try:
        result = run_signal_cge_prompt(prompt, uploaded_file, backend)
        downloads = result.get("downloads", {})

        return (
            _render_interpreted_scenario(result),
            _render_results_cards(result),
            _results_table_dataframe(result),
            pd.DataFrame(result.get("chart_data", [])),
            _render_policy_interpretation(result.get("interpretation", {})),
            _render_model_reference_used(result),
            _render_adaptive_learning_trace(result.get("learning_trace", {})),
            _render_full_cge_status(result.get("full_cge_development_status", {})),
            _render_diagnostics(result.get("diagnostics", {})),
            _render_readiness(result.get("readiness", {})),
            downloads.get("policy_brief_md"),
            downloads.get("results_json"),
            downloads.get("results_csv"),
        )

    except Exception as exc:
        error_message = f"## Signal CGE Runtime Error\n\n`{type(exc).__name__}: {exc}`"

        empty_table = pd.DataFrame(
            [
                {"metric": "Status", "effect": "Simulation failed"},
                {"metric": "Reason", "effect": str(exc)},
            ]
        )

        empty_chart = pd.DataFrame(
            [
                {"metric": "GDP/output", "effect": 0.0},
                {"metric": "Household income", "effect": 0.0},
                {"metric": "Trade", "effect": 0.0},
            ]
        )

        return (
            error_message,
            "<div style='color:#b91c1c;font-weight:700;'>Signal CGE simulation failed. Check diagnostics below.</div>",
            empty_table,
            empty_chart,
            error_message,
            "## Model Reference Used\n- Error occurred before model reference could be loaded.",
            "## Adaptive Learning Trace\n- Not available because simulation failed.",
            "## Full CGE Development Status\n- Error occurred during simulation execution.",
            error_message,
            "## Model Readiness\n- Simulation route needs debugging.",
            None,
            None,
            None,
        )

with gr.Blocks(title="Signal AI Dashboard", css=SIGNAL_DASHBOARD_CSS) as demo:
    gr.HTML(value=_dashboard_status_banner())
    gr.Markdown("Behavioral intelligence and AI-native CGE simulation for policy analysis.")

    with gr.Tab("Behavioral Signals AI"):
        gr.Markdown(_behavioral_section_intro())
        with gr.Accordion("How to Use Signal", open=False):
            gr.Markdown(_how_to_use_signal_markdown())
        with gr.Accordion("Model Interpretation Guide", open=False):
            gr.Markdown(_model_interpretation_markdown())

        live_trend_feed = gr.HTML(value=_fallback_live_trend_html())

        with gr.Row():
            with gr.Column():
                likes = gr.Number(label="Likes", value=120, precision=0)
                comments = gr.Number(label="Comments", value=35, precision=0)
                shares = gr.Number(label="Shares", value=24, precision=0)
                searches = gr.Number(label="Searches", value=160, precision=0)
                engagement_intensity = gr.Slider(0, 1, value=0.55, label="Engagement Intensity")
                purchase_intent_score = gr.Slider(0, 1, value=0.7, label="Purchase Intent Score")
                trend_growth = gr.Slider(0, 1, value=0.35, label="Trend Growth")
                predict_button = gr.Button("Predict Demand")

            with gr.Column():
                with gr.Row():
                    demand_output = gr.Textbox(label="Demand Classification", interactive=False)
                    confidence_output = gr.Number(label="Confidence Score (%)", interactive=False)
                with gr.Row():
                    aggregate_output = gr.Number(label="Aggregate Demand Score", interactive=False)
                    opportunity_output = gr.Number(label="Opportunity Score", interactive=False)
                with gr.Row():
                    emerging_output = gr.Number(label="Emerging Trend Probability (%)", interactive=False)
                    unmet_output = gr.Number(label="Unmet Demand Probability (%)", interactive=False)
                interpretation_output = gr.Textbox(label="Investment / Policy Interpretation", lines=2, interactive=False)
                with gr.Row():
                    signal_strength_output = gr.Number(label="Signal Strength Score", interactive=False)
                    momentum_score_output = gr.Number(label="Momentum Score", interactive=False)
                    volatility_output = gr.Number(label="Volatility / Noise Score", interactive=False)
                with gr.Row():
                    persistence_output = gr.Number(label="Persistence Score", interactive=False)
                    adoption_output = gr.Number(label="Adoption Probability", interactive=False)
                    viral_output = gr.Number(label="Viral Probability", interactive=False)
                why_matters_output = gr.Textbox(label="Why This Matters", lines=4, interactive=False)
                with gr.Accordion("Technical Model Source and Explanation", open=False):
                    source_output = gr.Textbox(label="Model Source and Explanation", lines=16, interactive=False)

        with gr.Row():
            confidence_gauge_output = gr.HTML(label="Confidence Gauge")
            signal_strength_gauge_output = gr.HTML(label="Signal Strength Gauge")
            momentum_indicator_output = gr.HTML(label="Trend Momentum Indicator")

        with gr.Row():
            opportunity_radar_output = gr.HTML(label="Opportunity Radar Chart")
            key_driver_cards_output = gr.HTML(label="Key Driver Summary Cards")

        with gr.Row():
            trends_location = gr.Dropdown(label="Trend Location", choices=["Kenya", "Nairobi", "Global"], value="Kenya")
            trends_limit = gr.Slider(label="Number of Trends", minimum=3, maximum=10, step=1, value=5)
            refresh_trends_button = gr.Button("Refresh Trends")

        active_trends_output = gr.Number(label="Active Trends", precision=0, interactive=False, visible=False)
        trends_table = gr.Dataframe(label="Hidden Trends Table", interactive=False, visible=False)
        trend_intelligence_table = gr.Dataframe(label="Hidden Signal Intelligence Table", interactive=False, visible=False)
        trends_summary = gr.Textbox(label="Interpretation Summary", lines=6, interactive=False, visible=False)

        trend_outputs = [
            trends_table,
            live_trend_feed,
            active_trends_output,
            trends_summary,
            trend_intelligence_table,
        ]

        refresh_trends_button.click(
            fn=refresh_live_trend_intelligence,
            inputs=[trends_location, trends_limit],
            outputs=trend_outputs,
            show_api=False,
        )
        demo.load(
            fn=refresh_live_trend_intelligence,
            inputs=[trends_location, trends_limit],
            outputs=trend_outputs,
            show_api=False,
        )

        live_inputs = [
            likes,
            comments,
            shares,
            searches,
            engagement_intensity,
            purchase_intent_score,
            trend_growth,
        ]
        live_outputs = [
            demand_output,
            confidence_output,
            aggregate_output,
            opportunity_output,
            emerging_output,
            unmet_output,
            interpretation_output,
            source_output,
            signal_strength_output,
            momentum_score_output,
            volatility_output,
            persistence_output,
            adoption_output,
            viral_output,
            why_matters_output,
            confidence_gauge_output,
            signal_strength_gauge_output,
            momentum_indicator_output,
            opportunity_radar_output,
            key_driver_cards_output,
        ]

        for input_component in live_inputs:
            input_component.change(
                fn=update_behavioral_dashboard,
                inputs=live_inputs,
                outputs=live_outputs,
                show_api=False,
            )
        predict_button.click(
            fn=update_behavioral_dashboard,
            inputs=live_inputs,
            outputs=live_outputs,
            show_api=False,
        )
        demo.load(
            fn=update_behavioral_dashboard,
            inputs=live_inputs,
            outputs=live_outputs,
            show_api=False,
        )

    with gr.Tab("Signal CGE"):
        gr.Markdown(
            "## Signal CGE\n"
            "AI-native CGE simulation engine for policy prompts, SAM calibration, scenario execution, diagnostics, and policy interpretation."
        )
        gr.Markdown(baseline_dashboard_markdown())
        with gr.Accordion("How to use Signal CGE", open=False):
            gr.Markdown(
                "1. Type a policy simulation prompt.\n"
                "2. Signal CGE reads repo-stored canonical model files.\n"
                "3. Upload is optional.\n"
                "4. Click **Run Signal CGE Simulation**.\n"
                "5. Review scenario, results, diagnostics, model references, and downloads."
            )

        signal_cge_prompt = gr.Textbox(
            label="Enter simulation prompt",
            placeholder="reduce import tariffs on cmach by 10%",
            value="reduce import tariffs on cmach by 10%",
            lines=6,
        )
        signal_cge_backend = gr.Dropdown(
            label="Simulation backend",
            choices=[
                "Static equilibrium CGE solver",
                "SAM multiplier backend",
                "Optional GAMS backend if available",
            ],
            value="Static equilibrium CGE solver",
        )
        with gr.Accordion("Optional: Upload custom SAM/workbook", open=False):
            gr.Markdown("No upload is required. Signal CGE uses the canonical model stored in the repository unless a custom file is uploaded.")
            signal_cge_upload = gr.File(label="Upload SAM or experiment workbook", file_types=[".xlsx", ".csv"])

        run_signal_cge_button = gr.Button("Run Signal CGE Simulation")
        signal_cge_scenario_output = gr.Markdown(label="Interpreted Scenario")
        signal_cge_summary_cards = gr.HTML(label="Results Summary")
        signal_cge_results_table = gr.Dataframe(label="Numeric Results Table", interactive=False)
        signal_cge_effect_chart = gr.BarPlot(
            label="Scenario effects",
            x="metric",
            y="effect",
            title="Signal CGE Scenario Effects",
            tooltip=["metric", "effect"],
            vertical=False,
        )
        signal_cge_interpretation_output = gr.Markdown(label="Policy Interpretation")
        signal_cge_reference_output = gr.Markdown(label="Model Reference Used")
        signal_cge_learning_trace_output = gr.Markdown(label="Adaptive Learning Trace")
        signal_cge_full_status_output = gr.Markdown(label="Full CGE Development Status")
        signal_cge_diagnostics_output = gr.Markdown(label="Diagnostics")
        signal_cge_readiness_output = gr.Markdown(label="Model Readiness")

        with gr.Row():
            signal_cge_json_download = gr.File(label="Download JSON results")
            signal_cge_csv_download = gr.File(label="Download CSV results")
            signal_cge_brief_download = gr.File(label="Download Markdown policy brief")

        run_signal_cge_button.click(
            fn=signal_cge_prompt_ui,
            inputs=[signal_cge_prompt, signal_cge_backend, signal_cge_upload],
            outputs=[
                signal_cge_scenario_output,
                signal_cge_summary_cards,
                signal_cge_results_table,
                signal_cge_effect_chart,
                signal_cge_interpretation_output,
                signal_cge_reference_output,
                signal_cge_learning_trace_output,
                signal_cge_full_status_output,
                signal_cge_diagnostics_output,
                signal_cge_readiness_output,
                signal_cge_brief_download,
                signal_cge_json_download,
                signal_cge_csv_download,
            ],
            show_api=False,
        )

    gr.Markdown(
        "Signal is a privacy-preserving AI dashboard for aggregate behavioural signal intelligence, "
        "policy insight, and market demand analysis."
    )


if __name__ == "__main__":
    demo.launch(show_api=False)