"""SAM account classification for the Signal CGE calibration prototype."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import pandas as pd


CARE_FACTOR_SUFFIXES = {"fcp", "fcu", "fnp", "fnu", "mcp", "mcu", "mnp", "mnu"}


@dataclass(slots=True)
class AccountClassification:
    activities: list[str]
    commodities: list[str]
    factors: list[str]
    households: list[str]
    government: list[str]
    investment: list[str]
    taxes: list[str]
    imports: list[str]
    exports: list[str]
    rest_of_world: list[str]
    unclassified: list[str]
    kenya_gender_care_factors: list[str]

    def to_dict(self) -> dict[str, list[str]]:
        return asdict(self)


def classify_sam_accounts(sam: pd.DataFrame) -> AccountClassification:
    accounts = [str(account) for account in sam.index]
    classified: dict[str, list[str]] = {
        "activities": [],
        "commodities": [],
        "factors": [],
        "households": [],
        "government": [],
        "investment": [],
        "taxes": [],
        "imports": [],
        "exports": [],
        "rest_of_world": [],
    }
    for account in accounts:
        key = account.lower()
        if key in CARE_FACTOR_SUFFIXES or any(term in key for term in ["factor", "labour", "labor", "capital", "land"]):
            classified["factors"].append(account)
        elif any(term in key for term in ["household", "hh"]):
            classified["households"].append(account)
        elif any(term in key for term in ["government", "gov"]):
            classified["government"].append(account)
        elif any(term in key for term in ["investment", "capital_formation", "savings"]):
            classified["investment"].append(account)
        elif any(term in key for term in ["tax", "vat", "tariff"]):
            classified["taxes"].append(account)
        elif any(term in key for term in ["import", "m_"]):
            classified["imports"].append(account)
        elif any(term in key for term in ["export", "x_"]):
            classified["exports"].append(account)
        elif any(term in key for term in ["row", "rest_of_world", "foreign"]):
            classified["rest_of_world"].append(account)
        elif any(term in key for term in ["commodity", "com_", "goods", "services"]):
            classified["commodities"].append(account)
        elif any(term in key for term in ["activity", "act_", "prod", "sector", "care", "manufacturing", "transport"]):
            classified["activities"].append(account)
        else:
            classified["commodities"].append(account)

    used = {item for values in classified.values() for item in values}
    return AccountClassification(
        **classified,
        unclassified=[account for account in accounts if account not in used],
        kenya_gender_care_factors=[account for account in accounts if account.lower() in CARE_FACTOR_SUFFIXES],
    )
