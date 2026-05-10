"""Generate realistic synthetic training data for the Signal AI engine."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
OUTPUT_PATH = ROOT_DIR / "data" / "training" / "signal_training_data.csv"
DEMAND_CLASSES = [
    "High Demand",
    "Moderate Demand",
    "Low Demand",
    "Emerging Demand",
    "Declining Demand",
    "Unmet Demand",
]
COUNTIES = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Machakos", "Kiambu", "Turkana"]
TOPICS = ["retail", "food", "finance", "health", "mobility", "agriculture", "education"]
TIME_PERIODS = [f"2026-Q{quarter}" for quarter in range(1, 5)]


def generate_synthetic_signal_data(
    output_path: str | Path = OUTPUT_PATH,
    n_rows: int = 1800,
    random_state: int = 42,
) -> pd.DataFrame:
    """Create a balanced synthetic dataset with realistic demand-signal patterns."""

    rng = np.random.default_rng(random_state)
    class_counts = _balanced_class_counts(n_rows, len(DEMAND_CLASSES))
    records: list[dict[str, Any]] = []

    for demand_class, class_rows in zip(DEMAND_CLASSES, class_counts):
        for _ in range(class_rows):
            records.append(_generate_record(rng, demand_class))

    frame = pd.DataFrame(records)
    frame = frame.sample(frac=1.0, random_state=random_state).reset_index(drop=True)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(destination, index=False)
    return frame


def _generate_record(rng: np.random.Generator, demand_class: str) -> dict[str, Any]:
    county = str(rng.choice(COUNTIES))
    topic = str(rng.choice(TOPICS))
    time_period = str(rng.choice(TIME_PERIODS))
    county_boost = 1.08 if county in {"Nairobi", "Kiambu", "Mombasa"} else 0.96

    regime = {
        "High Demand": {
            "likes": (160, 32),
            "comments": (62, 12),
            "shares": (38, 8),
            "searches": (210, 26),
            "engagement_intensity": (0.82, 0.05),
            "purchase_intent_score": (0.84, 0.06),
            "trend_growth": (0.58, 0.08),
            "sentiment_score": (0.68, 0.12),
            "urgency_score": (0.73, 0.08),
            "repetition_score": (0.64, 0.08),
            "location_relevance": (0.74, 0.08),
            "price_sensitivity": (0.36, 0.08),
            "noise_score": (0.2, 0.07),
            "opportunity_label": "Strong Investment Opportunity",
            "unmet_demand_flag": 0,
            "emerging_trend_flag": 1,
        },
        "Moderate Demand": {
            "likes": (105, 24),
            "comments": (34, 8),
            "shares": (18, 5),
            "searches": (128, 20),
            "engagement_intensity": (0.63, 0.06),
            "purchase_intent_score": (0.58, 0.07),
            "trend_growth": (0.31, 0.09),
            "sentiment_score": (0.34, 0.15),
            "urgency_score": (0.49, 0.08),
            "repetition_score": (0.46, 0.08),
            "location_relevance": (0.63, 0.09),
            "price_sensitivity": (0.5, 0.09),
            "noise_score": (0.28, 0.08),
            "opportunity_label": "Emerging Opportunity",
            "unmet_demand_flag": 0,
            "emerging_trend_flag": 0,
        },
        "Low Demand": {
            "likes": (42, 12),
            "comments": (11, 4),
            "shares": (5, 2),
            "searches": (54, 12),
            "engagement_intensity": (0.34, 0.07),
            "purchase_intent_score": (0.28, 0.08),
            "trend_growth": (0.05, 0.07),
            "sentiment_score": (0.08, 0.12),
            "urgency_score": (0.22, 0.07),
            "repetition_score": (0.24, 0.08),
            "location_relevance": (0.45, 0.1),
            "price_sensitivity": (0.62, 0.1),
            "noise_score": (0.38, 0.09),
            "opportunity_label": "Weak Signal",
            "unmet_demand_flag": 0,
            "emerging_trend_flag": 0,
        },
        "Emerging Demand": {
            "likes": (92, 18),
            "comments": (28, 7),
            "shares": (19, 4),
            "searches": (152, 24),
            "engagement_intensity": (0.57, 0.06),
            "purchase_intent_score": (0.62, 0.07),
            "trend_growth": (0.66, 0.09),
            "sentiment_score": (0.44, 0.15),
            "urgency_score": (0.61, 0.08),
            "repetition_score": (0.54, 0.08),
            "location_relevance": (0.58, 0.1),
            "price_sensitivity": (0.47, 0.08),
            "noise_score": (0.26, 0.08),
            "opportunity_label": "Emerging Opportunity",
            "unmet_demand_flag": 0,
            "emerging_trend_flag": 1,
        },
        "Declining Demand": {
            "likes": (58, 16),
            "comments": (16, 5),
            "shares": (7, 3),
            "searches": (72, 15),
            "engagement_intensity": (0.41, 0.06),
            "purchase_intent_score": (0.36, 0.08),
            "trend_growth": (-0.18, 0.08),
            "sentiment_score": (-0.08, 0.14),
            "urgency_score": (0.26, 0.08),
            "repetition_score": (0.33, 0.08),
            "location_relevance": (0.52, 0.1),
            "price_sensitivity": (0.58, 0.08),
            "noise_score": (0.35, 0.09),
            "opportunity_label": "Monitor Further",
            "unmet_demand_flag": 0,
            "emerging_trend_flag": 0,
        },
        "Unmet Demand": {
            "likes": (74, 18),
            "comments": (18, 5),
            "shares": (9, 3),
            "searches": (196, 28),
            "engagement_intensity": (0.38, 0.07),
            "purchase_intent_score": (0.71, 0.07),
            "trend_growth": (0.27, 0.08),
            "sentiment_score": (0.22, 0.16),
            "urgency_score": (0.78, 0.08),
            "repetition_score": (0.7, 0.08),
            "location_relevance": (0.59, 0.1),
            "price_sensitivity": (0.69, 0.09),
            "noise_score": (0.24, 0.08),
            "opportunity_label": "Investigate Anomaly / Possible Unmet Demand",
            "unmet_demand_flag": 1,
            "emerging_trend_flag": 0,
        },
    }[demand_class]

    likes = max(0, int(rng.normal(*regime["likes"]) * county_boost))
    comments = max(0, int(rng.normal(*regime["comments"]) * county_boost))
    shares = max(0, int(rng.normal(*regime["shares"]) * county_boost))
    searches = max(0, int(rng.normal(*regime["searches"]) * county_boost))

    engagement_intensity = _bounded_normal(rng, *regime["engagement_intensity"])
    purchase_intent_score = _bounded_normal(rng, *regime["purchase_intent_score"])
    trend_growth = float(np.clip(rng.normal(*regime["trend_growth"]), -1, 1))
    sentiment_score = float(np.clip(rng.normal(*regime["sentiment_score"]), -1, 1))
    urgency_score = _bounded_normal(rng, *regime["urgency_score"])
    repetition_score = _bounded_normal(rng, *regime["repetition_score"])
    location_relevance = _bounded_normal(rng, *regime["location_relevance"])
    price_sensitivity = _bounded_normal(rng, *regime["price_sensitivity"])
    noise_score = _bounded_normal(rng, *regime["noise_score"])

    return {
        "topic": topic,
        "county": county,
        "time_period": time_period,
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "searches": searches,
        "engagement_intensity": round(engagement_intensity, 4),
        "purchase_intent_score": round(purchase_intent_score, 4),
        "trend_growth": round(trend_growth, 4),
        "sentiment_score": round(sentiment_score, 4),
        "urgency_score": round(urgency_score, 4),
        "repetition_score": round(repetition_score, 4),
        "location_relevance": round(location_relevance, 4),
        "price_sensitivity": round(price_sensitivity, 4),
        "noise_score": round(noise_score, 4),
        "demand_class": demand_class,
        "opportunity_label": regime["opportunity_label"],
        "unmet_demand_flag": int(regime["unmet_demand_flag"]),
        "emerging_trend_flag": int(regime["emerging_trend_flag"]),
    }


def _balanced_class_counts(total_rows: int, n_classes: int) -> list[int]:
    base = total_rows // n_classes
    counts = [base for _ in range(n_classes)]
    for index in range(total_rows - sum(counts)):
        counts[index % n_classes] += 1
    return counts


def _bounded_normal(rng: np.random.Generator, mean: float, std: float, lower: float = 0, upper: float = 1) -> float:
    return float(np.clip(rng.normal(mean, std), lower, upper))


def main() -> None:
    frame = generate_synthetic_signal_data()
    print(
        f"Generated {len(frame)} rows at {OUTPUT_PATH} "
        f"with demand classes: {', '.join(sorted(frame['demand_class'].unique()))}"
    )


if __name__ == "__main__":
    main()
