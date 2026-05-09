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
    model: str = "Signal CGE Workbench"
    simulation_type: str = "sam_multiplier"
    validation_warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload.update(
            {
                "shock_account": payload["target_accounts"][0] if payload["target_accounts"] else "",
                "shock_size": payload["shock_value"],
                "target_outputs": payload["expected_outputs"],
                "closure": payload["closure_rule"],
            }
        )
        if payload["shock_type"] == "import_tariff":
            payload["policy_instrument"] = "import tariff"
            payload["target_commodity"] = payload["shock_account"]
            payload["shock_direction"] = "reduction" if payload["shock_value"] < 0 else "increase"
        return payload


def parse_scenario_prompt(prompt: str) -> ScenarioSpec:
    """Parse a policy prompt into a transparent scenario specification."""

    text = (prompt or "").strip()
    lowered = text.lower()
    value = _extract_value(lowered)
    shock_type = "demand"
    simulation_type = "sam_multiplier"
    accounts = ["all"]
    name = _scenario_name(text)
    notes: list[str] = []

    if "tariff" in lowered and "import" in lowered:
        shock_type = "import_tariff"
        accounts = [_extract_target_after_on(lowered) or _extract_known_account(lowered) or "imports"]
        if "reduction" in lowered or "reduce" in lowered or "cut" in lowered or "lower" in lowered:
            value = -abs(value)
        elif value == 0:
            value = 5.0
    elif "compare" in lowered and "unpaid care" in lowered and "paid care" in lowered:
        shock_type = "care_comparison"
        simulation_type = "scenario_comparison"
        accounts = ["unpaid_care", "paid_care"] + CARE_FACTOR_SUFFIXES
        if value == 0:
            value = 25.0
    elif any(term in lowered for term in ["vat", "tax"]):
        shock_type = "tax"
        accounts = _target_from_terms(lowered, {"manufacturing": ["manufacturing"]}, ["tax_accounts"])
        if "reduction" in lowered or "reduce" in lowered or "cut" in lowered:
            value = -abs(value)
        elif value == 0:
            value = 5.0
    elif "productivity" in lowered:
        shock_type = "productivity"
        accounts = _target_from_terms(lowered, {"transport": ["transport"], "exports": ["exports"]}, ["all_activities"])
    elif "trade" in lowered or "export" in lowered:
        shock_type = "trade_facilitation"
        accounts = ["exports"]
    elif "unpaid care" in lowered and "paid care" in lowered:
        shock_type = "care_formalization"
        accounts = ["unpaid_care", "paid_care"] + CARE_FACTOR_SUFFIXES
    elif "double" in lowered and "care" in lowered and "infrastructure" in lowered:
        shock_type = "care_infrastructure"
        accounts = ["care_infrastructure", "paid_care_services"] + CARE_FACTOR_SUFFIXES
        value = 100.0
    elif "double" in lowered and "care" in lowered:
        shock_type = "care_services_expansion"
        accounts = ["paid_care_services"] + CARE_FACTOR_SUFFIXES
        value = 100.0
    elif "government spending" in lowered and "care" in lowered:
        shock_type = "government_spending"
        accounts = ["paid_care_services"] + CARE_FACTOR_SUFFIXES
    elif "care infrastructure" in lowered or ("care" in lowered and "investment" in lowered):
        shock_type = "public_investment"
        accounts = ["care_infrastructure", "paid_care_services"] + CARE_FACTOR_SUFFIXES
    elif any(term in lowered for term in ["health", "education", "water", "social services"]):
        shock_type = "public_investment"
        accounts = ["health", "education", "water", "social_services"]
    elif "infrastructure" in lowered:
        shock_type = "infrastructure_investment"
        accounts = ["infrastructure"]
        if value == 0:
            value = 10.0

    if not text:
        notes.append("No prompt supplied; using baseline scenario.")
        name = "Baseline"
        shock_type = "baseline"
        simulation_type = "baseline"
        accounts = ["all"]
        value = 0.0

    warnings = _validation_warnings(shock_type, accounts, value)

    return ScenarioSpec(
        scenario_name=name,
        shock_type=shock_type,
        target_accounts=accounts,
        shock_value=value,
        shock_unit="percent",
        closure_rule=_closure_for(shock_type),
        prompt=text,
        notes=notes,
        simulation_type=simulation_type,
        validation_warnings=warnings,
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
    if shock_type in {
        "public_investment",
        "care_services_expansion",
        "care_formalization",
        "care_comparison",
        "care_infrastructure",
        "government_spending",
        "infrastructure_investment",
    }:
        return "investment_driven_with_fixed_prices"
    if shock_type in {"trade_facilitation", "import_tariff"}:
        return "external_account_adjusts"
    return "standard_sam_multiplier"


def _validation_warnings(shock_type: str, accounts: list[str], value: float) -> list[str]:
    warnings: list[str] = []
    if not accounts:
        warnings.append("No shock account was identified.")
    if value < 0 and shock_type not in {"tax", "import_tariff"}:
        warnings.append("Negative shock size detected; confirm that this is intended.")
    if shock_type in {"demand", "baseline"} and value == 0:
        warnings.append("No active policy shock was detected.")
    return warnings


def _extract_target_after_on(text: str) -> str | None:
    match = re.search(r"\bon\s+([a-zA-Z][a-zA-Z0-9_/-]*)", text)
    if not match:
        return None
    return match.group(1).strip(" .,/;:")


def _extract_known_account(text: str) -> str | None:
    for token in ["cmach", "manufacturing", "imports", "exports", "agriculture", "transport"]:
        if token in text:
            return token
    return None
