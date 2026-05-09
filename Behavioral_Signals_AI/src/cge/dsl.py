"""Compact policy-scenario language for Signal CGE runs."""

from __future__ import annotations

import re

from .schema import CGEScenario, CGEShock


SHOCK_PATTERN = re.compile(
    r"^shock\s+(?P<type>demand|productivity|tax|export|import_price|transfer)\s+"
    r"(?P<target>[a-zA-Z0-9 _-]+?)\s+by\s+(?P<change>[-+]?\d+(?:\.\d+)?)%?$",
    re.IGNORECASE,
)


def parse_scenario(text: str, default_name: str = "Signal CGE scenario") -> CGEScenario:
    """Parse the Signal CGE mini-language into a structured scenario."""

    name = default_name
    closure = "savings_driven"
    numeraire = "consumer_price_index"
    description = ""
    shocks: list[CGEShock] = []

    for raw_line in str(text).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition(":")
        if separator and key.lower() in {"name", "closure", "numeraire", "description"}:
            normalized_key = key.lower()
            if normalized_key == "name":
                name = value.strip() or name
            elif normalized_key == "closure":
                closure = _slug(value)
            elif normalized_key == "numeraire":
                numeraire = _slug(value)
            else:
                description = value.strip()
            continue

        match = SHOCK_PATTERN.match(line)
        if not match:
            raise ValueError(f"Could not parse CGE scenario line: {line}")
        shocks.append(
            CGEShock(
                shock_type=match.group("type").lower(),
                target=_slug(match.group("target")),
                change_percent=float(match.group("change")),
            )
        )

    if not shocks:
        raise ValueError("CGE scenario must include at least one shock")

    return CGEScenario(
        name=name,
        closure=closure,
        numeraire=numeraire,
        description=description,
        shocks=tuple(shocks),
    )


def scenario_from_behavioral_signal(
    county: str,
    category: str,
    demand_classification: str,
    opportunity_score: float,
) -> CGEScenario:
    """Convert aggregate revealed-demand output into a CGE demand-shock scenario."""

    category_to_sector = {
        "agri_inputs": "agriculture",
        "clean_energy": "manufacturing",
        "digital_services": "services",
        "retail": "services",
        "transport": "transport",
    }
    sector = category_to_sector.get(_slug(category), "services")
    class_multiplier = {"high": 1.0, "moderate": 0.55, "low": 0.2}.get(_slug(demand_classification), 0.35)
    shock = round(max(0.0, min(12.0, float(opportunity_score) * class_multiplier / 10)), 2)
    return CGEScenario(
        name=f"{county} revealed demand shock",
        description="Generated from anonymized aggregate behavioral-signal output.",
        shocks=(CGEShock("demand", sector, shock),),
    )


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", str(value).strip().lower()).strip("_")
