"""Account classification helpers for CGE calibration."""

from __future__ import annotations

import pandas as pd


INSTITUTION_KEYWORDS = {
    "households": {"household", "households", "rural", "urban"},
    "government": {"government", "tax", "public"},
    "investment": {"investment", "savings", "capital_account"},
    "rest_of_world": {"row", "rest_of_world", "foreign", "external"},
}


def classify_accounts(matrix: pd.DataFrame) -> dict[str, list[str]]:
    """Classify accounts into sectors and institutions using transparent heuristics."""

    accounts = [str(account) for account in matrix.index]
    institutions: dict[str, list[str]] = {key: [] for key in INSTITUTION_KEYWORDS}
    sectors: list[str] = []
    for account in accounts:
        matched = False
        for group, keywords in INSTITUTION_KEYWORDS.items():
            if any(keyword in account for keyword in keywords):
                institutions[group].append(account)
                matched = True
                break
        if not matched:
            sectors.append(account)
    return {"sectors": sectors, **institutions}
