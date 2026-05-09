"""Capital accumulation helper."""


def update_capital_stock(previous_capital: float, investment: float, depreciation_rate: float) -> float:
    return float(previous_capital * (1 - depreciation_rate) + investment)
