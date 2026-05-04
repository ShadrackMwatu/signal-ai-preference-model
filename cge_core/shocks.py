"""Shock utilities for Signal CGE models."""

from __future__ import annotations

from signal_modeling_language.schema import SMLModel


def shock_table(model: SMLModel) -> list[dict[str, float | str]]:
    return [
        {
            "name": shock.name,
            "target": shock.target,
            "operator": shock.operator,
            "value": shock.value,
        }
        for shock in model.shocks
    ]


def aggregate_shock_size(model: SMLModel) -> float:
    return round(sum(abs(shock.value) for shock in model.shocks), 6)
