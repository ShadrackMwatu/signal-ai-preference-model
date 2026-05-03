"""Synthetic anonymized Kenya behavioral-signal data generation."""

from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import Sequence

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
SAMPLE_BEHAVIORAL_PATH = DATA_DIR / "sample_behavioral_signals.csv"
SAMPLE_COMPETITOR_PATH = DATA_DIR / "sample_competitors.csv"
SAMPLE_FEEDBACK_PATH = DATA_DIR / "sample_feedback.csv"

KENYA_COUNTIES = ("Nairobi", "Mombasa", "Kisumu", "Nakuru", "Machakos", "Kiambu", "Turkana")
CATEGORIES = ("agri_inputs", "clean_energy", "digital_services", "retail", "transport")
TIME_PERIODS = ("2026-Q1", "2026-Q2", "2026-Q3", "2026-Q4")
CONSUMER_SEGMENTS = ("budget_seekers", "growth_smes", "urban_youth", "rural_producers")
DEMAND_CLASSES = (
    "High demand",
    "Moderate demand",
    "Low demand",
    "Emerging demand",
    "Declining demand",
    "Unmet demand",
)


def generate_synthetic_behavioral_data(seed: int = 2026) -> pd.DataFrame:
    """Create anonymized aggregate behavioral signals with supervised labels."""

    rng = random.Random(seed)
    rows: list[dict[str, object]] = []
    category_base = {
        "agri_inputs": 0.62,
        "clean_energy": 0.66,
        "digital_services": 0.76,
        "retail": 0.58,
        "transport": 0.61,
    }
    county_factor = {
        "Nairobi": 1.22,
        "Mombasa": 1.08,
        "Kisumu": 1.0,
        "Nakuru": 1.04,
        "Machakos": 0.91,
        "Kiambu": 1.16,
        "Turkana": 0.72,
    }
    segment_factor = {
        "budget_seekers": 0.86,
        "growth_smes": 1.18,
        "urban_youth": 1.11,
        "rural_producers": 0.95,
    }

    signal_number = 1
    for time_index, time_period in enumerate(TIME_PERIODS):
        trend_factor = 1 + (time_index * 0.08)
        for county in KENYA_COUNTIES:
            for category in CATEGORIES:
                for consumer_segment in CONSUMER_SEGMENTS:
                    latent_demand = (
                        category_base[category]
                        * county_factor[county]
                        * segment_factor[consumer_segment]
                        * trend_factor
                        * rng.uniform(0.84, 1.16)
                    )
                    observation_count = 50 + rng.randint(0, 280)
                    views = int(observation_count * rng.uniform(5.0, 16.0) * latent_demand)
                    clicks = int(views * rng.uniform(0.05, 0.18) * latent_demand)
                    likes = int(clicks * rng.uniform(0.18, 0.55))
                    comments = int(clicks * rng.uniform(0.04, 0.18))
                    shares = int(clicks * rng.uniform(0.03, 0.15))
                    saves = int(clicks * rng.uniform(0.04, 0.22))
                    searches = int(observation_count * rng.uniform(0.18, 0.75) * latent_demand)
                    hashtags = int(searches * rng.uniform(0.05, 0.22))
                    mentions = int(searches * rng.uniform(0.07, 0.28))
                    complaints = int(comments * rng.uniform(0.04, 0.32) * (1.45 - latent_demand))
                    purchase_intent = int(searches * rng.uniform(0.06, 0.27) * latent_demand)
                    repeated = int(clicks * rng.uniform(0.1, 0.42) * latent_demand)
                    ignored = int(views * rng.uniform(0.03, 0.18) * (1.35 - min(latent_demand, 1.2)))
                    delayed = int(comments * rng.uniform(0.03, 0.2) * (1.3 - min(latent_demand, 1.1)))

                    dissatisfaction = complaints + delayed + ignored
                    unmet_ratio = dissatisfaction / max(1, comments + clicks)
                    market_gap = min(1.0, (unmet_ratio * 1.4) + (0.25 if county == "Turkana" else 0.0))
                    behavioral_score = min(
                        1.0,
                        (
                            clicks
                            + likes
                            + (1.25 * comments)
                            + (1.55 * shares)
                            + (1.4 * saves)
                            + searches
                            + purchase_intent
                            + repeated
                        )
                        / max(1, views + observation_count),
                    )
                    aggregate_score = min(1.0, (0.58 * latent_demand) + (0.42 * behavioral_score))
                    opportunity_score = min(
                        1.0,
                        (0.48 * aggregate_score)
                        + (0.34 * market_gap)
                        + (0.18 * min(1.0, searches / max(observation_count, 1))),
                    )
                    emerging_probability = min(1.0, opportunity_score + (time_index * 0.05))
                    unmet_probability = market_gap

                    rows.append(
                        {
                            "signal_id": f"agg-{signal_number:05d}",
                            "country": "Kenya",
                            "county": county,
                            "category": category,
                            "consumer_segment": consumer_segment,
                            "time_period": time_period,
                            "observation_count": observation_count,
                            "text": _synthetic_text(category, county, consumer_segment, market_gap, purchase_intent, rng),
                            "clicks": clicks,
                            "likes": likes,
                            "comments": comments,
                            "shares": shares,
                            "saves": saves,
                            "views": views,
                            "searches": searches,
                            "hashtags": hashtags,
                            "mentions": mentions,
                            "complaints": complaints,
                            "purchase_intent_phrases": purchase_intent,
                            "repeated_engagement": repeated,
                            "ignored_content": ignored,
                            "delayed_responses": delayed,
                            "demand_classification": _demand_classification(
                                aggregate_score,
                                opportunity_score,
                                market_gap,
                                time_index,
                            ),
                            "aggregate_demand_score": round(aggregate_score, 4),
                            "opportunity_score": round(opportunity_score, 4),
                            "emerging_trend_probability": round(emerging_probability, 4),
                            "unmet_demand_probability": round(unmet_probability, 4),
                            "market_gap": round(market_gap, 4),
                            "supply_shortage": round(min(1.0, market_gap + rng.uniform(-0.08, 0.12)), 4),
                            "scalability": round(min(1.0, 0.35 + latent_demand + rng.uniform(-0.18, 0.08)), 4),
                            "competition_intensity": round(min(1.0, 0.25 + county_factor[county] * rng.uniform(0.12, 0.34)), 4),
                            "trend_direction": _trend_direction(latent_demand, time_index),
                        }
                    )
                    signal_number += 1

    return pd.DataFrame(rows)


def generate_competitor_data() -> pd.DataFrame:
    """Create synthetic county/category competitor coverage data."""

    rows = []
    for county in KENYA_COUNTIES:
        for category in CATEGORIES:
            underserved = county in {"Turkana", "Machakos"} or category in {"agri_inputs", "transport"}
            rows.append(
                {
                    "county": county,
                    "category": category,
                    "competitor_count": 1 if underserved else 4,
                    "average_price_index": 0.78 if underserved else 1.08,
                    "service_quality_index": 0.42 if underserved else 0.74,
                    "delivery_reliability_index": 0.36 if county == "Turkana" else 0.7,
                }
            )
    return pd.DataFrame(rows)


def generate_feedback_data(seed: int = 404) -> pd.DataFrame:
    """Create synthetic aggregate feedback outcomes for adaptation tests."""

    rng = random.Random(seed)
    rows = []
    for county in KENYA_COUNTIES:
        for category in CATEGORIES:
            rows.append(
                {
                    "county": county,
                    "category": category,
                    "time_period": "2027-Q1",
                    "observed_conversion_rate": round(rng.uniform(0.05, 0.38), 4),
                    "observed_complaint_rate": round(rng.uniform(0.01, 0.19), 4),
                    "observed_repeat_rate": round(rng.uniform(0.04, 0.32), 4),
                }
            )
    return pd.DataFrame(rows)


def write_sample_data(data_dir: str | Path = DATA_DIR) -> None:
    """Write all local sample CSV files used by the modular pipeline."""

    output_dir = Path(data_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    generate_synthetic_behavioral_data().to_csv(output_dir / "sample_behavioral_signals.csv", index=False)
    generate_competitor_data().to_csv(output_dir / "sample_competitors.csv", index=False)
    generate_feedback_data().to_csv(output_dir / "sample_feedback.csv", index=False)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Signal sample market intelligence data.")
    parser.add_argument("--data-dir", default=str(DATA_DIR))
    args = parser.parse_args(argv)
    write_sample_data(args.data_dir)
    print(f"wrote sample behavioral, competitor, and feedback data to {args.data_dir}")
    return 0


def _synthetic_text(
    category: str,
    county: str,
    consumer_segment: str,
    market_gap: float,
    purchase_intent: int,
    rng: random.Random,
) -> str:
    needs = {
        "agri_inputs": "seed quality fertilizer access harvest timing farm input supply",
        "clean_energy": "solar kits battery replacement repair support reliable power",
        "digital_services": "online payments analytics dashboard mobile onboarding",
        "retail": "fair prices product availability delivery reliability",
        "transport": "route reliability parcel tracking last mile access",
    }
    intent = "ready to buy comparing suppliers" if purchase_intent > 8 else "searching and evaluating options"
    complaint = "complaints delays and unmet need" if market_gap > 0.42 else "positive discovery and saves"
    lead = rng.choice(("aggregate posts mention", "county-level comments discuss", "anonymous hashtags show"))
    return f"{lead} {needs[category]} in {county}; {consumer_segment} are {intent}; {complaint}"


def _demand_classification(
    aggregate_score: float,
    opportunity_score: float,
    market_gap: float,
    time_index: int,
) -> str:
    if market_gap >= 0.62 and aggregate_score >= 0.45:
        return "Unmet demand"
    if opportunity_score >= 0.72 and time_index >= 2:
        return "Emerging demand"
    if aggregate_score >= 0.72:
        return "High demand"
    if aggregate_score >= 0.52:
        return "Moderate demand"
    if aggregate_score < 0.34:
        return "Declining demand"
    return "Low demand"


def _trend_direction(latent_demand: float, time_index: int) -> str:
    if time_index >= 2 and latent_demand >= 0.85:
        return "rising"
    if latent_demand < 0.48:
        return "falling"
    return "stable"


if __name__ == "__main__":
    raise SystemExit(main())
