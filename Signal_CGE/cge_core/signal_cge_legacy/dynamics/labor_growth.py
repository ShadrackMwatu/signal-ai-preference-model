"""Labour growth helper."""


def update_labor_supply(previous_labor: float, growth_rate: float) -> float:
    return float(previous_labor * (1 + growth_rate))
