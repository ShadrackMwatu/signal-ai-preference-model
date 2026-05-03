"""Privacy-safe behavioral data pipeline for revealed demand intelligence."""

from __future__ import annotations

import argparse
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_BEHAVIORAL_DATA_PATH = ROOT_DIR / "data" / "behavioral_signals.csv"

KENYA_COUNTIES = ("Nairobi", "Mombasa", "Kisumu", "Nakuru", "Machakos", "Kiambu", "Turkana")
CATEGORIES = ("agri_inputs", "clean_energy", "digital_services", "retail", "transport")
TIME_PERIODS = ("2026-Q1", "2026-Q2", "2026-Q3", "2026-Q4")
ANONYMIZED_SEGMENTS = ("budget_seekers", "growth_smes", "urban_youth", "rural_producers")
COUNTRY = "Kenya"

BEHAVIOR_COLUMNS = (
    "clicks",
    "likes",
    "comments",
    "shares",
    "saves",
    "views",
    "searches",
    "hashtags",
    "mentions",
    "complaints",
    "purchase_intent_phrases",
    "repeated_engagement",
    "ignored_content",
    "delayed_responses",
)

CONTEXT_COLUMNS = ("country", "county", "category", "time_period", "anonymized_segment", "segment_size")
TEXT_COLUMNS = ("text",)

NLP_LABEL_COLUMNS = (
    "sentiment_label",
    "purchase_intent_label",
    "urgency_label",
    "dissatisfaction_label",
    "topic_label",
)

TARGET_COLUMNS = (
    "demand_classification",
    "behavioral_signal_score_target",
    "aggregate_demand_score_target",
    "opportunity_score_target",
    "emerging_trend_target",
    "unmet_demand_target",
    "market_gap_target",
    "trend_direction_label",
    "value_proposition_label",
    "product_service_label",
    "revenue_model_label",
    "supplier_recommendation_label",
    "logistics_recommendation_label",
    "payment_recommendation_label",
    "market_entry_strategy_label",
    "competitor_gap_label",
    "price_gap_label",
    "service_gap_label",
    "delivery_gap_label",
    "customer_dissatisfaction_label",
    "pricing_power_target",
    "customer_reach_target",
    "inventory_planning_target",
    "sales_forecast_target",
)

REQUIRED_COLUMNS = CONTEXT_COLUMNS + BEHAVIOR_COLUMNS + TEXT_COLUMNS + NLP_LABEL_COLUMNS + TARGET_COLUMNS

PII_COLUMNS = {
    "name",
    "email",
    "phone",
    "phone_number",
    "user_id",
    "username",
    "handle",
    "profile_url",
    "ip_address",
    "device_id",
    "national_id",
    "passport",
    "gps",
    "gps_coordinates",
    "latitude",
    "longitude",
    "lat",
    "lon",
    "psychological_profile",
    "psychographic_segment",
    "personality_score",
    "personality_type",
    "microtargeting_score",
}

PII_PATTERNS = (
    re.compile(r"[\w\.-]+@[\w\.-]+\.\w+"),
    re.compile(r"(?:\+?254|0)\d{9}\b"),
)


@dataclass(frozen=True)
class BehavioralDataConfig:
    """Configuration for synthetic anonymized behavioral data."""

    periods: Sequence[str] = TIME_PERIODS
    counties: Sequence[str] = KENYA_COUNTIES
    categories: Sequence[str] = CATEGORIES
    segments: Sequence[str] = ANONYMIZED_SEGMENTS
    seed: int = 77
    minimum_segment_size: int = 60


def generate_behavioral_dataset(config: BehavioralDataConfig | None = None) -> pd.DataFrame:
    """Generate anonymized county/category/segment behavioral training data."""

    config = config or BehavioralDataConfig()
    rng = random.Random(config.seed)
    rows: list[dict[str, object]] = []
    category_base = {
        "agri_inputs": 0.63,
        "clean_energy": 0.68,
        "digital_services": 0.76,
        "retail": 0.58,
        "transport": 0.61,
    }
    county_multiplier = {
        "Nairobi": 1.22,
        "Mombasa": 1.08,
        "Kisumu": 1.0,
        "Nakuru": 1.04,
        "Machakos": 0.9,
        "Kiambu": 1.16,
        "Turkana": 0.72,
    }
    segment_multiplier = {
        "budget_seekers": 0.84,
        "growth_smes": 1.18,
        "urban_youth": 1.1,
        "rural_producers": 0.94,
    }

    for period_index, time_period in enumerate(config.periods):
        seasonal_growth = 1.0 + (period_index * 0.08)
        for county in config.counties:
            for category in config.categories:
                for segment in config.segments:
                    latent_demand = (
                        category_base[category]
                        * county_multiplier[county]
                        * segment_multiplier[segment]
                        * seasonal_growth
                        * rng.uniform(0.82, 1.18)
                    )
                    segment_size = config.minimum_segment_size + rng.randint(0, 260)
                    views = int(segment_size * rng.uniform(5.0, 16.0) * latent_demand)
                    clicks = int(views * rng.uniform(0.05, 0.18) * latent_demand)
                    likes = int(clicks * rng.uniform(0.18, 0.55))
                    comments = int(clicks * rng.uniform(0.04, 0.18))
                    shares = int(clicks * rng.uniform(0.03, 0.15))
                    saves = int(clicks * rng.uniform(0.04, 0.2))
                    searches = int(segment_size * rng.uniform(0.18, 0.75) * latent_demand)
                    hashtags = int(searches * rng.uniform(0.05, 0.22))
                    mentions = int(searches * rng.uniform(0.07, 0.28))
                    complaints = int(comments * rng.uniform(0.04, 0.3) * (1.45 - latent_demand))
                    intent_count = int(searches * rng.uniform(0.06, 0.26) * latent_demand)
                    repeated = int(clicks * rng.uniform(0.1, 0.42) * latent_demand)
                    ignored = int(views * rng.uniform(0.03, 0.18) * (1.35 - min(latent_demand, 1.2)))
                    delayed = int(comments * rng.uniform(0.03, 0.2) * (1.3 - min(latent_demand, 1.1)))

                    dissatisfaction = complaints + delayed + ignored
                    unmet_ratio = dissatisfaction / max(1, comments + clicks)
                    market_gap = min(1.0, (unmet_ratio * 1.4) + (0.25 if county == "Turkana" else 0.0))
                    behavior_signal = min(
                        1.0,
                        (
                            clicks
                            + likes
                            + (1.3 * comments)
                            + (1.6 * shares)
                            + (1.4 * saves)
                            + searches
                            + intent_count
                            + repeated
                        )
                        / max(1, views + segment_size),
                    )
                    aggregate_demand = min(1.0, (0.58 * latent_demand) + (0.42 * behavior_signal))
                    opportunity = min(
                        1.0,
                        (0.5 * aggregate_demand) + (0.32 * market_gap) + (0.18 * min(1.0, searches / max(segment_size, 1))),
                    )

                    rows.append(
                        {
                            "county": county,
                            "country": COUNTRY,
                            "category": category,
                            "time_period": time_period,
                            "anonymized_segment": segment,
                            "segment_size": segment_size,
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
                            "purchase_intent_phrases": intent_count,
                            "repeated_engagement": repeated,
                            "ignored_content": ignored,
                            "delayed_responses": delayed,
                            "text": _synthetic_text(category, county, segment, market_gap, intent_count, rng),
                            "sentiment_label": int(complaints < max(1, comments * 0.16)),
                            "purchase_intent_label": int(intent_count > max(2, searches * 0.12)),
                            "urgency_label": int((intent_count + complaints + delayed) > max(5, comments + saves)),
                            "dissatisfaction_label": int(unmet_ratio > 0.2),
                            "topic_label": category,
                            "demand_classification": _demand_classification(
                                aggregate_demand,
                                opportunity,
                                market_gap,
                                period_index,
                            ),
                            "behavioral_signal_score_target": round(behavior_signal, 4),
                            "aggregate_demand_score_target": round(aggregate_demand, 4),
                            "opportunity_score_target": round(opportunity, 4),
                            "emerging_trend_target": round(min(1.0, opportunity + (period_index * 0.05)), 4),
                            "unmet_demand_target": round(market_gap, 4),
                            "market_gap_target": round(market_gap, 4),
                            "trend_direction_label": _trend_label(latent_demand, period_index),
                            "value_proposition_label": _value_proposition(category, market_gap),
                            "product_service_label": _product_service(category, market_gap),
                            "revenue_model_label": _revenue_model(category, opportunity),
                            "supplier_recommendation_label": _supplier_recommendation(category, county),
                            "logistics_recommendation_label": _logistics_recommendation(county),
                            "payment_recommendation_label": _payment_recommendation(segment),
                            "market_entry_strategy_label": _market_entry_strategy(county, category, opportunity, market_gap),
                            "competitor_gap_label": _competitor_gap(category, market_gap),
                            "price_gap_label": _price_gap(category, unmet_ratio),
                            "service_gap_label": _service_gap(category, market_gap),
                            "delivery_gap_label": _delivery_gap(county, delayed, complaints),
                            "customer_dissatisfaction_label": _dissatisfaction_label(unmet_ratio),
                            "pricing_power_target": round(min(1.0, aggregate_demand * (1 - market_gap * 0.45)), 4),
                            "customer_reach_target": round(min(1.0, clicks / max(1, segment_size)), 4),
                            "inventory_planning_target": round(min(1.0, (saves + searches + intent_count) / max(1, views)), 4),
                            "sales_forecast_target": round(min(1.0, opportunity * latent_demand), 4),
                        }
                    )

    frame = pd.DataFrame(rows)
    validate_behavioral_schema(frame)
    validate_privacy(frame)
    return frame


def load_behavioral_data(path: str | Path = DEFAULT_BEHAVIORAL_DATA_PATH) -> pd.DataFrame:
    """Load and validate anonymized behavioral signals."""

    frame = pd.read_csv(path)
    validate_behavioral_schema(frame)
    validate_privacy(frame)
    return frame


def write_behavioral_dataset(
    path: str | Path = DEFAULT_BEHAVIORAL_DATA_PATH,
    config: BehavioralDataConfig | None = None,
) -> pd.DataFrame:
    """Generate and persist the sample Kenya behavioral dataset."""

    frame = generate_behavioral_dataset(config)
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output_path, index=False)
    return frame


def validate_behavioral_schema(frame: pd.DataFrame) -> None:
    """Ensure all fields needed by the ML pipeline are present."""

    missing = set(REQUIRED_COLUMNS).difference(frame.columns)
    if missing:
        raise ValueError(f"missing behavioral columns: {', '.join(sorted(missing))}")


def validate_privacy(frame: pd.DataFrame) -> None:
    """Reject PII and individual-level records."""

    lower_columns = {column.lower() for column in frame.columns}
    blocked = lower_columns.intersection(PII_COLUMNS)
    if blocked:
        raise ValueError(f"PII columns are not allowed: {', '.join(sorted(blocked))}")

    if "segment_size" in frame.columns and (frame["segment_size"] < 30).any():
        raise ValueError("segment_size must be at least 30 to preserve aggregation privacy")

    if "country" in frame.columns and set(frame["country"].dropna()) != {COUNTRY}:
        raise ValueError("only country-level aggregate Kenya records are supported")

    if "text" in frame.columns:
        text = " ".join(frame["text"].astype(str).tolist())
        for pattern in PII_PATTERNS:
            if pattern.search(text):
                raise ValueError("PII-like text pattern detected")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate anonymized Signal behavioral data.")
    parser.add_argument("--output", default=str(DEFAULT_BEHAVIORAL_DATA_PATH))
    args = parser.parse_args(argv)
    frame = write_behavioral_dataset(args.output)
    print(f"wrote {len(frame)} anonymized aggregate rows to {args.output}")
    return 0


def _synthetic_text(
    category: str,
    county: str,
    segment: str,
    market_gap: float,
    intent_count: int,
    rng: random.Random,
) -> str:
    needs = {
        "agri_inputs": "farm inputs, seed quality, fertilizer access, harvest timing",
        "clean_energy": "solar kits, reliable power, repair support, battery replacement",
        "digital_services": "online payments, analytics dashboards, mobile onboarding",
        "retail": "fair prices, product availability, delivery reliability",
        "transport": "route reliability, last mile access, parcel tracking",
    }
    intent = "ready to buy and compare suppliers" if intent_count > 8 else "researching options"
    gap = "complaints about unmet need and delays" if market_gap > 0.42 else "positive service discovery"
    phrase = rng.choice(("aggregate mentions show", "anonymous posts discuss", "county trend indicates"))
    return f"{phrase} {needs[category]} in {county}; {segment} are {intent}; {gap}"


def _demand_classification(
    aggregate_demand: float,
    opportunity: float,
    market_gap: float,
    period_index: int,
) -> str:
    if market_gap >= 0.62 and aggregate_demand >= 0.45:
        return "Unmet demand"
    if opportunity >= 0.72 and period_index >= 2:
        return "Emerging demand"
    if aggregate_demand >= 0.72:
        return "High demand"
    if aggregate_demand >= 0.52:
        return "Moderate demand"
    if aggregate_demand < 0.34:
        return "Declining demand"
    return "Low demand"


def _trend_label(latent_demand: float, period_index: int) -> str:
    if period_index >= 2 and latent_demand >= 0.85:
        return "rising"
    if latent_demand < 0.48:
        return "falling"
    return "stable"


def _value_proposition(category: str, market_gap: float) -> str:
    if market_gap > 0.52:
        return f"accessible {category.replace('_', ' ')} with faster fulfillment"
    return f"trusted {category.replace('_', ' ')} with transparent pricing"


def _product_service(category: str, market_gap: float) -> str:
    if category == "agri_inputs":
        return "bundled input ordering service" if market_gap > 0.5 else "verified input marketplace"
    if category == "clean_energy":
        return "solar maintenance network" if market_gap > 0.5 else "pay as you go solar kits"
    if category == "digital_services":
        return "SME analytics assistant" if market_gap > 0.5 else "mobile business dashboard"
    if category == "transport":
        return "last mile logistics coordination" if market_gap > 0.5 else "route tracking service"
    return "county retail availability platform"


def _revenue_model(category: str, opportunity: float) -> str:
    if category in {"digital_services", "clean_energy"} and opportunity > 0.55:
        return "subscription"
    if opportunity > 0.62:
        return "commission"
    return "transaction_fee"


def _supplier_recommendation(category: str, county: str) -> str:
    if county == "Turkana":
        return "regional supplier pooling"
    if category in {"agri_inputs", "retail"}:
        return "multi-supplier marketplace"
    return "certified specialist suppliers"


def _logistics_recommendation(county: str) -> str:
    if county in {"Turkana", "Machakos"}:
        return "hub and spoke delivery"
    if county in {"Nairobi", "Kiambu"}:
        return "same day courier"
    return "scheduled route delivery"


def _payment_recommendation(segment: str) -> str:
    if segment == "budget_seekers":
        return "pay in installments"
    if segment == "growth_smes":
        return "invoice and wallet rails"
    return "mobile money checkout"


def _market_entry_strategy(county: str, category: str, opportunity: float, market_gap: float) -> str:
    if market_gap > 0.58 and opportunity > 0.55:
        return f"partner-led entry for {category.replace('_', ' ')} in underserved {county}"
    if opportunity > 0.62:
        return f"digital-first launch for {category.replace('_', ' ')} in {county}"
    return f"pilot and validate {category.replace('_', ' ')} demand in {county}"


def _competitor_gap(category: str, market_gap: float) -> str:
    if market_gap > 0.58:
        return f"weak fulfillment in {category.replace('_', ' ')}"
    if market_gap > 0.36:
        return f"pricing transparency gap in {category.replace('_', ' ')}"
    return f"service differentiation needed in {category.replace('_', ' ')}"


def _price_gap(category: str, unmet_ratio: float) -> str:
    if unmet_ratio > 0.42:
        return f"high affordability gap in {category.replace('_', ' ')}"
    if unmet_ratio > 0.2:
        return f"moderate pricing transparency gap in {category.replace('_', ' ')}"
    return f"limited price gap in {category.replace('_', ' ')}"


def _service_gap(category: str, market_gap: float) -> str:
    if market_gap > 0.58:
        return f"major service availability gap in {category.replace('_', ' ')}"
    if market_gap > 0.36:
        return f"service quality gap in {category.replace('_', ' ')}"
    return f"low service gap in {category.replace('_', ' ')}"


def _delivery_gap(county: str, delayed: int, complaints: int) -> str:
    if county == "Turkana" or delayed > complaints:
        return f"last mile delivery gap in {county}"
    if county in {"Nairobi", "Kiambu"}:
        return f"speed and reliability gap in {county}"
    return f"moderate delivery coordination gap in {county}"


def _dissatisfaction_label(unmet_ratio: float) -> str:
    if unmet_ratio > 0.42:
        return "high_dissatisfaction"
    if unmet_ratio > 0.2:
        return "moderate_dissatisfaction"
    return "low_dissatisfaction"


if __name__ == "__main__":
    raise SystemExit(main())
