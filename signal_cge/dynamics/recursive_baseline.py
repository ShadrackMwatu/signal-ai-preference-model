"""Recursive baseline projection placeholder."""


def project_baseline(years: int, initial_index: float = 100.0, annual_growth: float = 0.0) -> list[float]:
    return [round(initial_index * ((1 + annual_growth) ** year), 6) for year in range(years)]
