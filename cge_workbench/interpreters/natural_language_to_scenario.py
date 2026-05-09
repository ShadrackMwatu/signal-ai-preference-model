"""Natural-language scenario parsing for the Signal CGE Workbench."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import re
from typing import Any


CARE_FACTOR_SUFFIXES = ["fcp", "fcu", "fnp", "fnu", "mcp", "mcu", "mnp", "mnu"]


@dataclass(slots=True)
class ScenarioSpec:
    """Structured scenario object passed to model runners."""

    scenario_name: str
    shock_type: str
    target_accounts: list[str]
    shock_value: float
    shock_unit: str = "percent"
    closure_rule: str = "standard_sam_multiplier"
    expected_outputs: list[str] = field(
        default_factory=lambda: [
            "macro_results",
            "sectoral_output",
            "factor_income",
            "household_income",
            "gender_care_effects",
            "diagnostics",
        ]
    )
    prompt: str = ""
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def parse_scenario_prompt(prompt: str) -> ScenarioSpec:
    """Parse a policy prompt into a transparent scenario specification."""

    text = (prompt or "").strip()
    lowered = text.lower()
    value = _extract_value(lowered)
    shock_type = "demand"
    accounts = ["all"]
    name = _scenario_name(text)
    notes: list[str] = []

    if any(term in lowered for term in ["vat", "tax"]):
        shock_type = "tax"
        accounts = _target_from_terms(lowered, {"manufacturing": ["manufacturing"]}, ["tax_accounts"])
        if "reduction" in lowered or "reduce" in lowered or "cut" in lowered:
            value = -abs(value)
    elif "productivity" in lowered:
        shock_type = "productivity"
        accounts = _target_from_terms(lowered, {"transport": ["transport"], "exports": ["exports"]}, ["all_activities"])
    elif "trade" in lowered or "export" in lowered:
        shock_type = "trade_facilitation"
        accounts = ["exports"]
    elif "unpaid care" in lowered and "paid care" in lowered:
        shock_type = "care_formalization"
        accounts = ["unpaid_care", "paid_care"] + CARE_FACTOR_SUFFIXES
    elif "double" in lowered and "care" in lowered:
        shock_type = "care_services_expansion"
        accounts = ["paid_care_services"] + CARE_FACTOR_SUFFIXES
        value = 100.0
    elif "care infrastructure" in lowered or ("care" in lowered and "investment" in lowered):
        shock_type = "public_investment"
        accounts = ["care_infrastructure", "paid_care_services"] + CARE_FACTOR_SUFFIXES
    elif any(term in lowered for term in ["health", "education", "water", "social services"]):
        shock_type = "public_investment"
        accounts = ["health", "education", "water", "social_services"]
    elif "infrastructure" in lowered:
        shock_type = "public_investment"
        accounts = ["infrastructure"]

    if not text:
        notes.append("No prompt supplied; using baseline scenario.")
        name = "Baseline"
        shock_type = "baseline"
        accounts = ["all"]
        value = 0.0

    return ScenarioSpec(
        scenario_name=name,
        shock_type=shock_type,
        target_accounts=accounts,
        shock_value=value,
        shock_unit="percent",
        closure_rule=_closure_for(shock_type),
        prompt=text,
        notes=notes,
    )


def _extract_value(text: str) -> float:
    if "double" in text:
        return 100.0
    match = re.search(r"(-?\d+(?:\.\d+)?)\s*(%|percent|percentage)?", text)
    return float(match.group(1)) if match else 0.0


def _scenario_name(prompt: str) -> str:
    cleaned = re.sub(r"\s+", " ", prompt).strip(" .")
    if not cleaned:
        return "Baseline"
    return cleaned[:80].capitalize()


def _target_from_terms(text: str, mapping: dict[str, list[str]], default: list[str]) -> list[str]:
    for term, accounts in mapping.items():
        if term in text:
            return accounts
    return default


def _closure_for(shock_type: str) -> str:
    if shock_type == "tax":
        return "government_savings_adjusts"
    if shock_type in {"public_investment", "care_services_expansion", "care_formalization"}:
        return "investment_driven_with_fixed_prices"
    if shock_type == "trade_facilitation":
        return "external_account_adjusts"
    return "standard_sam_multiplier"
