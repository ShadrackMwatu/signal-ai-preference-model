"""Social Accounting Matrix loading and calibration utilities."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_SAM_COLUMNS = {"row_account", "column_account", "value"}
PII_COLUMNS = {"name", "username", "email", "phone", "user_id", "gps", "latitude", "longitude"}
INSTITUTIONAL_ACCOUNTS = {"households", "government", "investment", "rest_of_world"}


def load_sam(path: str | Path) -> pd.DataFrame:
    """Load a long-format SAM CSV after structural and privacy validation."""

    frame = pd.read_csv(path)
    return validate_sam(frame)


def validate_sam(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate that a SAM is aggregate, square, non-negative, and PII-free."""

    columns = set(frame.columns)
    missing = REQUIRED_SAM_COLUMNS - columns
    if missing:
        raise ValueError(f"SAM is missing required column(s): {', '.join(sorted(missing))}")

    pii_hits = columns.intersection(PII_COLUMNS)
    if pii_hits:
        raise ValueError(f"SAM contains disallowed PII column(s): {', '.join(sorted(pii_hits))}")

    sam = frame[list(REQUIRED_SAM_COLUMNS)].copy()
    sam["row_account"] = sam["row_account"].astype(str).str.strip().str.lower()
    sam["column_account"] = sam["column_account"].astype(str).str.strip().str.lower()
    sam["value"] = pd.to_numeric(sam["value"], errors="raise").astype(float)

    if sam.empty:
        raise ValueError("SAM must contain at least one transaction")
    if (sam["value"] < 0).any():
        raise ValueError("SAM values must be non-negative")

    row_accounts = set(sam["row_account"])
    column_accounts = set(sam["column_account"])
    if row_accounts != column_accounts:
        raise ValueError("SAM row and column accounts must describe the same account set")

    return sam


def sam_matrix(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a square SAM matrix with missing cells filled as zero."""

    sam = validate_sam(frame)
    accounts = sorted(set(sam["row_account"]).union(sam["column_account"]))
    matrix = sam.pivot_table(
        index="row_account",
        columns="column_account",
        values="value",
        aggfunc="sum",
        fill_value=0.0,
    )
    return matrix.reindex(index=accounts, columns=accounts, fill_value=0.0)


def account_totals(frame: pd.DataFrame) -> pd.DataFrame:
    """Compute row and column totals with balance diagnostics."""

    matrix = sam_matrix(frame)
    totals = pd.DataFrame(
        {
            "account": matrix.index,
            "row_total": matrix.sum(axis=1).to_numpy(),
            "column_total": matrix.sum(axis=0).reindex(matrix.index).to_numpy(),
        }
    )
    totals["imbalance"] = totals["row_total"] - totals["column_total"]
    totals["imbalance_ratio"] = totals["imbalance"] / totals[["row_total", "column_total"]].max(axis=1).replace(0, 1)
    return totals.round(6)


def calibrate_sam(frame: pd.DataFrame) -> dict[str, object]:
    """Derive baseline CGE accounts and macro totals from a SAM."""

    matrix = sam_matrix(frame)
    accounts = list(matrix.index)
    sectors = [account for account in accounts if account not in INSTITUTIONAL_ACCOUNTS]
    row_totals = matrix.sum(axis=1)
    column_totals = matrix.sum(axis=0)
    sector_output = {sector: float(row_totals[sector]) for sector in sectors}
    baseline_gdp = float(sum(sector_output.values()))
    if baseline_gdp <= 0:
        raise ValueError("SAM must contain positive productive-sector output")

    return {
        "accounts": accounts,
        "sectors": sectors,
        "sector_output": sector_output,
        "baseline_gdp": baseline_gdp,
        "household_income": float(row_totals.get("households", 0.0)),
        "government_revenue": float(row_totals.get("government", 0.0)),
        "external_balance": float(row_totals.get("rest_of_world", 0.0) - column_totals.get("rest_of_world", 0.0)),
        "account_totals": account_totals(frame).to_dict(orient="records"),
    }
