"""Productivity growth helper."""


def update_productivity(previous_productivity: float, growth_rate: float) -> float:
    return float(previous_productivity * (1 + growth_rate))
