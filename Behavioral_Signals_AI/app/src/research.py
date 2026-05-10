"""Research-oriented outputs for policy, CGE/SAM, and publication workflows."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from .schemas import PreferencePrediction, PreferenceRequest


DEFAULT_CATEGORY_TO_SAM_ACCOUNT = {
    "analytics": "DIGITAL_SERVICES",
    "automation": "BUSINESS_SERVICES",
    "forecasting": "FINANCIAL_SERVICES",
    "research": "KNOWLEDGE_SERVICES",
}

PUBLICATION_NOTES = (
    "Score is a logistic regression preference probability.",
    "Drivers are coefficient-weighted transformed feature contributions.",
    "Validate synthetic prototype data against study data before policy inference.",
)

CGE_SAM_COLUMNS = [
    "scenario_id",
    "user_id",
    "item_id",
    "category",
    "sam_account",
    "preference_score",
    "preferred",
    "shock_value",
    "shock_direction",
    "top_driver",
]


def sam_account_for_category(category: str) -> str:
    """Map model categories to stable CGE/SAM account labels."""

    return DEFAULT_CATEGORY_TO_SAM_ACCOUNT.get(category.lower(), "UNMAPPED")


def policy_signal(score: float, preferred: bool) -> str:
    """Translate a probability score into an interpretable policy signal."""

    if preferred and score >= 0.7:
        return "strong_positive_preference"
    if preferred:
        return "moderate_positive_preference"
    if score <= 0.3:
        return "strong_negative_preference"
    return "moderate_negative_preference"


def cge_sam_shock(score: float) -> float:
    """Represent preference as a centered shock value for scenario models."""

    return round(score - 0.5, 4)


def cge_sam_row(
    request: PreferenceRequest,
    prediction: PreferencePrediction,
    scenario_id: str = "baseline",
) -> dict[str, str | float | bool]:
    """Create one CGE/SAM-ready export row."""

    top_driver = prediction.drivers[0].feature if prediction.drivers else ""
    shock = prediction.cge_sam_shock
    return {
        "scenario_id": scenario_id,
        "user_id": request.user_id,
        "item_id": request.item_id,
        "category": request.category,
        "sam_account": prediction.cge_sam_account,
        "preference_score": prediction.score,
        "preferred": prediction.preferred,
        "shock_value": shock,
        "shock_direction": "positive" if shock >= 0 else "negative",
        "top_driver": top_driver,
    }


def export_cge_sam_csv(
    path: str | Path,
    rows: Iterable[dict[str, str | float | bool]],
) -> None:
    """Write CGE/SAM integration rows to CSV."""

    export_path = Path(path)
    export_path.parent.mkdir(parents=True, exist_ok=True)
    with export_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CGE_SAM_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
