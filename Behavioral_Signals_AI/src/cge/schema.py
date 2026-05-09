"""Shared dataclasses for Signal CGE modelling."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CGEShock:
    """A policy or market shock expressed in percentage points."""

    shock_type: str
    target: str
    change_percent: float

    @property
    def change_decimal(self) -> float:
        return self.change_percent / 100


@dataclass(frozen=True)
class CGEScenario:
    """Parsed CGE scenario specification."""

    name: str
    shocks: tuple[CGEShock, ...]
    closure: str = "savings_driven"
    numeraire: str = "consumer_price_index"
    description: str = ""


@dataclass
class CGEResult:
    """Simulation output for a CGE scenario."""

    scenario: CGEScenario
    baseline_gdp: float
    simulated_gdp: float
    gdp_change_percent: float
    household_welfare_change_percent: float
    price_index_change_percent: float
    fiscal_balance_change: float
    external_balance_change: float
    sector_impacts: list[dict[str, float | str]]
    diagnostics: list[str] = field(default_factory=list)
