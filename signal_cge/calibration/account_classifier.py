"""SAM account classification for the Signal CGE calibration prototype."""

from __future__ import annotations

import pandas as pd


CARE_SUFFIXES = {"fcp", "fcu", "fnp", "fnu", "mcp", "mcu", "mnp", "mnu"}
ACCOUNT_GROUPS = [
    "activities",
    "commodities",
    "factors",
    "households",
    "government",
    "taxes",
    "savings_investment",
    "rest_of_world",
    "unknown",
]


def classify_sam_accounts(sam: pd.DataFrame, account_map: dict[str, str] | None = None) -> dict[str, list[str]]:
    """Classify SAM accounts into CGE account groups.

    `account_map` can override deterministic classification with entries such
    as `{"hh_rural": "households"}`. Unknown override groups are ignored and
    the account falls back to rule-based classification.
    """

    accounts = [str(account) for account in sam.index]
    groups = {group: [] for group in ACCOUNT_GROUPS}
    account_map = {str(k): str(v) for k, v in (account_map or {}).items()}

    for account in accounts:
        override = account_map.get(account)
        group = override if override in groups else _classify_account(account)
        groups[group].append(account)

    groups["care_factors"] = [account for account in accounts if account.lower() in CARE_SUFFIXES]
    return groups


def _classify_account(account: str) -> str:
    key = account.lower()
    if key in CARE_SUFFIXES or any(term in key for term in ["factor", "labour", "labor", "capital", "land"]):
        return "factors"
    if any(term in key for term in ["household", "hh"]):
        return "households"
    if any(term in key for term in ["government", "gov"]):
        return "government"
    if any(term in key for term in ["tax", "vat", "tariff", "duty"]):
        return "taxes"
    if any(term in key for term in ["saving", "investment", "capital_formation", "stock_change"]):
        return "savings_investment"
    if any(term in key for term in ["row", "rest_of_world", "foreign", "import", "export"]):
        return "rest_of_world"
    if any(term in key for term in ["commodity", "com_", "goods"]):
        return "commodities"
    if any(term in key for term in ["activity", "act_", "prod", "sector", "manufacturing", "transport", "care"]):
        return "activities"
    if any(term in key for term in ["service", "services"]):
        return "commodities"
    return "unknown"
