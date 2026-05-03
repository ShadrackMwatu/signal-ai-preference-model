"""Shared data schemas for training examples and predictions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PreferenceExample:
    """A labeled preference training example."""

    user_id: str
    item_id: str
    category: str
    price: float
    rating: float
    popularity: float
    label: int

    def __post_init__(self) -> None:
        if self.label not in (0, 1):
            raise ValueError("label must be 0 or 1")
        if self.price < 0:
            raise ValueError("price must be non-negative")
        if not 0 <= self.rating <= 5:
            raise ValueError("rating must be between 0 and 5")
        if not 0 <= self.popularity <= 1:
            raise ValueError("popularity must be between 0 and 1")


@dataclass(frozen=True)
class PreferenceRequest:
    """Unlabeled item context used for prediction."""

    user_id: str
    item_id: str
    category: str
    price: float
    rating: float
    popularity: float


@dataclass(frozen=True)
class PreferencePrediction:
    """Preference score returned by the model."""

    item_id: str
    score: float
    preferred: bool
