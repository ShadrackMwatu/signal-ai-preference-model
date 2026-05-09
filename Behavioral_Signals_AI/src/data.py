"""Data loading helpers for Signal preference examples."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from .schemas import PreferenceExample


REQUIRED_COLUMNS = {
    "user_id",
    "item_id",
    "category",
    "price",
    "rating",
    "popularity",
    "label",
}


def load_examples(path: str | Path) -> list[PreferenceExample]:
    """Load labeled preference examples from a CSV file."""

    csv_path = Path(path)
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS.difference(reader.fieldnames or [])
        if missing:
            missing_columns = ", ".join(sorted(missing))
            raise ValueError(f"missing required columns: {missing_columns}")

        return [_row_to_example(row) for row in reader]


def save_examples(path: str | Path, examples: Iterable[PreferenceExample]) -> None:
    """Write labeled preference examples to a CSV file."""

    csv_path = Path(path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=sorted(REQUIRED_COLUMNS))
        writer.writeheader()
        for example in examples:
            writer.writerow(
                {
                    "user_id": example.user_id,
                    "item_id": example.item_id,
                    "category": example.category,
                    "price": example.price,
                    "rating": example.rating,
                    "popularity": example.popularity,
                    "label": example.label,
                }
            )


def _row_to_example(row: dict[str, str]) -> PreferenceExample:
    return PreferenceExample(
        user_id=row["user_id"],
        item_id=row["item_id"],
        category=row["category"],
        price=float(row["price"]),
        rating=float(row["rating"]),
        popularity=float(row["popularity"]),
        label=int(row["label"]),
    )
