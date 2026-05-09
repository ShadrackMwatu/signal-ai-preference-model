"""Module 1: deterministic synthetic data ingestion for Signal."""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .data import load_examples, save_examples
from .schemas import PreferenceExample


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SYNTHETIC_DATA_PATH = ROOT_DIR / "data" / "synthetic_preferences.csv"

CATEGORIES = ("analytics", "automation", "forecasting", "research")
USER_SEGMENTS = ("policy", "operations", "research", "planning")

CATEGORY_PRICE_BANDS = {
    "analytics": (12.0, 80.0),
    "automation": (18.0, 140.0),
    "forecasting": (25.0, 160.0),
    "research": (5.0, 60.0),
}

SEGMENT_CATEGORY_PREFERENCES = {
    "policy": {"analytics": 0.65, "automation": 0.45, "forecasting": 0.7, "research": 0.85},
    "operations": {"analytics": 0.7, "automation": 0.9, "forecasting": 0.45, "research": 0.4},
    "research": {"analytics": 0.55, "automation": 0.35, "forecasting": 0.7, "research": 0.95},
    "planning": {"analytics": 0.75, "automation": 0.55, "forecasting": 0.9, "research": 0.65},
}


@dataclass(frozen=True)
class SyntheticDataConfig:
    """Configuration for deterministic synthetic preference data."""

    users_per_segment: int = 3
    items_per_category: int = 4
    seed: int = 42

    def __post_init__(self) -> None:
        if self.users_per_segment < 1:
            raise ValueError("users_per_segment must be at least 1")
        if self.items_per_category < 1:
            raise ValueError("items_per_category must be at least 1")


def generate_synthetic_examples(
    config: SyntheticDataConfig | None = None,
) -> list[PreferenceExample]:
    """Generate labeled synthetic preference examples for policy experiments."""

    config = config or SyntheticDataConfig()
    rng = random.Random(config.seed)
    examples: list[PreferenceExample] = []

    for segment in USER_SEGMENTS:
        for user_number in range(1, config.users_per_segment + 1):
            user_id = f"{segment}_{user_number:03d}"
            price_sensitivity = 0.08 + (0.03 * rng.random())
            for category in CATEGORIES:
                category_preference = SEGMENT_CATEGORY_PREFERENCES[segment][category]
                for item_number in range(1, config.items_per_category + 1):
                    price = _draw_price(rng, category)
                    rating = round(2.4 + (2.5 * rng.random()), 2)
                    popularity = round(0.15 + (0.8 * rng.random()), 3)
                    label = _label_preference(
                        category=category,
                        category_preference=category_preference,
                        price=price,
                        price_sensitivity=price_sensitivity,
                        rating=rating,
                        popularity=popularity,
                    )
                    examples.append(
                        PreferenceExample(
                            user_id=user_id,
                            item_id=f"{category}_{item_number:02d}",
                            category=category,
                            price=price,
                            rating=rating,
                            popularity=popularity,
                            label=label,
                        )
                    )

    validate_examples(examples)
    return examples


def ingest_preferences(
    path: str | Path = DEFAULT_SYNTHETIC_DATA_PATH,
    *,
    generate_if_missing: bool = True,
    config: SyntheticDataConfig | None = None,
) -> list[PreferenceExample]:
    """Load a dataset, optionally generating synthetic data if the file is missing."""

    data_path = Path(path)
    if not data_path.exists():
        if not generate_if_missing:
            raise FileNotFoundError(f"dataset not found: {data_path}")
        write_synthetic_dataset(data_path, config=config)

    examples = load_examples(data_path)
    validate_examples(examples)
    return examples


def write_synthetic_dataset(
    path: str | Path = DEFAULT_SYNTHETIC_DATA_PATH,
    *,
    config: SyntheticDataConfig | None = None,
) -> list[PreferenceExample]:
    """Generate and persist a deterministic synthetic preference dataset."""

    examples = generate_synthetic_examples(config)
    save_examples(path, examples)
    return examples


def validate_examples(examples: Sequence[PreferenceExample]) -> None:
    """Validate that ingested examples are usable for model training."""

    if not examples:
        raise ValueError("dataset must contain at least one example")

    labels = {example.label for example in examples}
    if labels != {0, 1}:
        raise ValueError("dataset must contain both positive and negative labels")

    categories = {example.category for example in examples}
    missing_categories = set(CATEGORIES).difference(categories)
    if missing_categories:
        missing = ", ".join(sorted(missing_categories))
        raise ValueError(f"dataset is missing required categories: {missing}")


def summarize_examples(examples: Sequence[PreferenceExample]) -> dict[str, float | int]:
    """Return compact summary statistics for ingestion logs and tests."""

    validate_examples(examples)
    positive_count = sum(example.label for example in examples)
    return {
        "examples": len(examples),
        "users": len({example.user_id for example in examples}),
        "items": len({example.item_id for example in examples}),
        "categories": len({example.category for example in examples}),
        "positive_rate": round(positive_count / len(examples), 4),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Signal synthetic preference data.")
    parser.add_argument("--output", default=str(DEFAULT_SYNTHETIC_DATA_PATH))
    parser.add_argument("--users-per-segment", type=int, default=3)
    parser.add_argument("--items-per-category", type=int, default=4)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args(argv)

    config = SyntheticDataConfig(
        users_per_segment=args.users_per_segment,
        items_per_category=args.items_per_category,
        seed=args.seed,
    )
    examples = write_synthetic_dataset(args.output, config=config)
    print(json.dumps(summarize_examples(examples), sort_keys=True))
    return 0


def _draw_price(rng: random.Random, category: str) -> float:
    low, high = CATEGORY_PRICE_BANDS[category]
    return round(low + ((high - low) * rng.random()), 2)


def _label_preference(
    *,
    category: str,
    category_preference: float,
    price: float,
    price_sensitivity: float,
    rating: float,
    popularity: float,
) -> int:
    low, high = CATEGORY_PRICE_BANDS[category]
    normalized_price = (price - low) / (high - low)
    utility = (
        (0.4 * category_preference)
        + (0.3 * (rating / 5))
        + (0.25 * popularity)
        - (price_sensitivity * normalized_price)
    )
    return int(utility >= 0.58)


if __name__ == "__main__":
    raise SystemExit(main())
