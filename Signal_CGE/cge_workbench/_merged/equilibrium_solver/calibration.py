"""SAM calibration for the Signal Static CGE Solver.

The calibration layer turns a balanced social accounting matrix into a compact
benchmark equilibrium. It keeps the benchmark general and transparent so the
solver can run from any balanced SAM with recognizable account groups.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ACCOUNT_GROUPS = [
    "activities",
    "commodities",
    "factors",
    "households",
    "government",
    "taxes",
    "investment",
    "rest_of_world",
    "unknown",
]


def load_sam(path_or_dataframe: str | Path | pd.DataFrame) -> pd.DataFrame:
    """Load a SAM from a DataFrame, CSV, or Excel workbook."""

    if isinstance(path_or_dataframe, pd.DataFrame):
        sam = path_or_dataframe.copy()
    else:
        path = Path(path_or_dataframe)
        if path.suffix.lower() in {".xlsx", ".xls"}:
            sam = pd.read_excel(path, index_col=0)
        elif path.suffix.lower() == ".csv":
            sam = pd.read_csv(path, index_col=0)
        else:
            raise ValueError(f"Unsupported SAM file type: {path.suffix}")
    sam.index = sam.index.map(str)
    sam.columns = sam.columns.map(str)
    sam = sam.apply(pd.to_numeric, errors="coerce").fillna(0.0)
    if sam.shape[0] != sam.shape[1]:
        raise ValueError("SAM must be square.")
    if list(sam.index) != list(sam.columns):
        raise ValueError("SAM row and column labels must match and be in the same order.")
    return sam.astype(float)


def default_static_sam() -> pd.DataFrame:
    """Return a small balanced repo-default SAM for no-upload public runs."""

    accounts = ["act", "cgood", "labor", "hh", "gov", "tax", "inv", "row"]
    values = [
        [0, 30, 20, 10, 5, 4, 6, 8],
        [30, 0, 10, 25, 8, 3, 12, 10],
        [20, 10, 0, 30, 2, 1, 3, 4],
        [10, 25, 30, 0, 6, 2, 5, 4],
        [5, 8, 2, 6, 0, 5, 4, 3],
        [4, 3, 1, 2, 5, 0, 1, 2],
        [6, 12, 3, 5, 4, 1, 0, 3],
        [8, 10, 4, 4, 3, 2, 3, 0],
    ]
    return pd.DataFrame(values, index=accounts, columns=accounts, dtype=float)


def validate_sam_balance(sam: pd.DataFrame, tolerance: float = 1e-6) -> dict[str, Any]:
    """Validate row-column balance and basic numeric health."""

    sam = load_sam(sam)
    row_totals = sam.sum(axis=1)
    column_totals = sam.sum(axis=0)
    imbalance = row_totals - column_totals
    return {
        "balanced": bool(float(imbalance.abs().max()) <= tolerance),
        "max_absolute_imbalance": float(imbalance.abs().max()),
        "row_totals": row_totals.to_dict(),
        "column_totals": column_totals.to_dict(),
        "zero_rows": row_totals[row_totals.abs() <= tolerance].index.tolist(),
        "zero_columns": column_totals[column_totals.abs() <= tolerance].index.tolist(),
        "negative_entries": int((sam < 0).sum().sum()),
        "tolerance": tolerance,
    }


def identify_accounts(sam: pd.DataFrame, account_mapping: dict[str, str] | None = None) -> dict[str, list[str]]:
    """Classify SAM accounts into the groups required by a static CGE model."""

    groups = {group: [] for group in ACCOUNT_GROUPS}
    account_mapping = {str(k): str(v) for k, v in (account_mapping or {}).items()}
    aliases = {
        "savings_investment": "investment",
        "saving_investment": "investment",
        "row": "rest_of_world",
        "foreign": "rest_of_world",
    }
    for account in map(str, sam.index):
        mapped = account_mapping.get(account)
        mapped = aliases.get(mapped, mapped)
        group = mapped if mapped in groups else _classify_account(account)
        groups[group].append(account)
    return groups


def calibrate_static_cge(sam: str | Path | pd.DataFrame, account_mapping: dict[str, str] | None = None) -> dict[str, Any]:
    """Calibrate benchmark flows, shares, rates, and initial values from a SAM."""

    sam_df = load_sam(sam)
    balance = validate_sam_balance(sam_df)
    accounts = identify_accounts(sam_df, account_mapping)
    benchmark = _benchmark_values(sam_df, accounts)
    shares = _share_parameters(sam_df, accounts, benchmark)
    tax_rates = _tax_rates(sam_df, accounts, benchmark)
    elasticities = {
        "import_elasticity": 1.5,
        "export_elasticity": 1.1,
        "output_supply_elasticity": 0.6,
        "household_price_elasticity": 0.8,
        "factor_supply_elasticity": 0.5,
    }
    calibration = {
        "sam": sam_df,
        "accounts": accounts,
        "balance": balance,
        "benchmark": benchmark,
        "shares": shares,
        "tax_rates": tax_rates,
        "elasticities": elasticities,
        "initial_values": {key: float(value) for key, value in benchmark.items() if key in _solver_variable_names()},
        "prices": {"commodity_price": 1.0, "activity_price": 1.0, "factor_return": 1.0, "exchange_rate": 1.0},
        "warnings": _calibration_warnings(balance, accounts, benchmark),
    }
    _assert_finite(calibration)
    return calibration


def _benchmark_values(sam: pd.DataFrame, accounts: dict[str, list[str]]) -> dict[str, float]:
    total = _positive(float(sam.values.sum()), 100.0)
    household_income = _positive(_row_total(sam, accounts["households"]), 0.35 * total)
    government_demand = _positive(_flow(sam, accounts["commodities"], accounts["government"]), 0.08 * total)
    investment_observed = _positive(_flow(sam, accounts["commodities"], accounts["investment"]), 0.12 * total)
    imports = _positive(_flow(sam, accounts["rest_of_world"], accounts["commodities"]), 0.10 * total)
    exports = _positive(_flow(sam, accounts["commodities"], accounts["rest_of_world"]), 0.08 * total)
    intermediate = _positive(_flow(sam, accounts["commodities"], accounts["activities"]), 0.18 * total)
    factor_payments = _positive(_flow(sam, accounts["factors"], accounts["activities"]), 0.30 * total)
    savings = _positive(_flow(sam, accounts["investment"], accounts["households"]), 0.16 * household_income)
    investment = savings if savings > 0 else investment_observed
    direct_tax = min(0.20 * household_income, _positive(_flow(sam, accounts["government"], accounts["households"]), 0.06 * household_income))
    household_demand = _positive(household_income - savings - direct_tax, 0.65 * household_income)
    composite_demand = _positive(household_demand + government_demand + investment + intermediate, 0.50 * total)
    domestic_output = _positive(composite_demand - imports + exports, _row_total(sam, accounts["activities"]) or 0.45 * total)
    tariff_rate = 0.10
    commodity_tax_rate = 0.04
    activity_tax_rate = 0.03
    direct_tax_rate = direct_tax / household_income
    government_revenue = (
        commodity_tax_rate * composite_demand
        + activity_tax_rate * domestic_output
        + tariff_rate * imports
        + direct_tax_rate * household_income
    )
    return {
        "domestic_output": float(domestic_output),
        "composite_demand": float(composite_demand),
        "imports": float(imports),
        "exports": float(exports),
        "commodity_price": 1.0,
        "activity_price": 1.0,
        "factor_return": 1.0,
        "household_income": float(household_income),
        "household_demand": float(household_demand),
        "government_revenue": float(government_revenue),
        "government_demand": float(government_demand),
        "government_balance": float(government_revenue - government_demand),
        "investment": float(investment),
        "exchange_rate": 1.0,
        "external_balance": float(imports - exports),
        "intermediate_demand": float(intermediate),
        "factor_payments": float(factor_payments),
        "savings": float(savings),
    }


def _share_parameters(sam: pd.DataFrame, accounts: dict[str, list[str]], benchmark: dict[str, float]) -> dict[str, Any]:
    intermediate_share = benchmark["intermediate_demand"] / benchmark["domestic_output"]
    value_added_share = max(1.0 - intermediate_share, 1e-9)
    return {
        "intermediate_input_coefficients": _column_shares(sam, accounts["commodities"], accounts["activities"]),
        "production_intermediate_share": _clamp(intermediate_share, 0.05, 0.90),
        "production_value_added_share": _clamp(value_added_share, 0.10, 0.95),
        "factor_income_shares": _row_shares(sam, accounts["factors"]),
        "household_income_shares": _row_shares(sam, accounts["households"]),
        "household_consumption_budget_shares": _column_shares(sam, accounts["commodities"], accounts["households"]),
        "government_demand_shares": _column_shares(sam, accounts["commodities"], accounts["government"]),
        "investment_demand_shares": _column_shares(sam, accounts["commodities"], accounts["investment"]),
        "import_shares": _row_shares(sam, accounts["rest_of_world"]),
        "export_shares": _column_shares(sam, accounts["commodities"], accounts["rest_of_world"]),
        "savings_rate": _safe_divide(benchmark["savings"], benchmark["household_income"]),
        "government_demand_share": _safe_divide(benchmark["government_demand"], benchmark["composite_demand"]),
        "investment_share": _safe_divide(benchmark["investment"], benchmark["composite_demand"]),
        "household_consumption_share": _safe_divide(benchmark["household_demand"], benchmark["household_income"]),
    }


def _tax_rates(sam: pd.DataFrame, accounts: dict[str, list[str]], benchmark: dict[str, float]) -> dict[str, float]:
    return {
        "indirect_tax_rate": 0.04,
        "tariff_rate": 0.10,
        "commodity_tax_rate": 0.04,
        "activity_tax_rate": 0.03,
        "direct_tax_rate": _clamp(_safe_divide(benchmark["household_income"] - benchmark["household_demand"] - benchmark["savings"], benchmark["household_income"]), 0.0, 0.25),
    }


def _calibration_warnings(balance: dict[str, Any], accounts: dict[str, list[str]], benchmark: dict[str, float]) -> list[str]:
    warnings: list[str] = []
    if not balance["balanced"]:
        warnings.append("SAM row-column balance does not pass tolerance.")
    for group in ["activities", "commodities", "factors", "households", "government", "investment", "rest_of_world"]:
        if not accounts[group]:
            warnings.append(f"No accounts classified as {group}; fallback benchmark values were used.")
    for key, value in benchmark.items():
        if float(value) <= 0 and key not in {"government_balance", "external_balance"}:
            warnings.append(f"Benchmark value for {key} is non-positive.")
    return warnings


def _classify_account(account: str) -> str:
    key = account.lower()
    if key.startswith("a") or "activity" in key or "sector" in key:
        return "activities"
    if key.startswith("c") or "commodity" in key or "goods" in key:
        return "commodities"
    if key in {"fcp", "fcu", "fnp", "fnu", "mcp", "mcu", "mnp", "mnu"} or any(term in key for term in ["factor", "labor", "labour", "capital", "land"]):
        return "factors"
    if "household" in key or key.startswith("hh"):
        return "households"
    if "gov" in key or "government" in key:
        return "government"
    if any(term in key for term in ["tax", "tariff", "vat", "duty"]):
        return "taxes"
    if any(term in key for term in ["invest", "saving", "capital_formation"]):
        return "investment"
    if key in {"row", "rest_of_world"} or any(term in key for term in ["foreign", "export", "import"]):
        return "rest_of_world"
    return "unknown"


def _solver_variable_names() -> list[str]:
    return [
        "domestic_output",
        "composite_demand",
        "imports",
        "exports",
        "commodity_price",
        "activity_price",
        "factor_return",
        "household_income",
        "household_demand",
        "government_revenue",
        "government_balance",
        "investment",
        "exchange_rate",
    ]


def _flow(sam: pd.DataFrame, rows: list[str], columns: list[str]) -> float:
    if not rows or not columns:
        return 0.0
    return float(sam.loc[rows, columns].sum().sum())


def _row_total(sam: pd.DataFrame, rows: list[str]) -> float:
    return float(sam.loc[rows, :].sum().sum()) if rows else 0.0


def _row_shares(sam: pd.DataFrame, rows: list[str]) -> dict[str, float]:
    values = sam.loc[rows, :].sum(axis=1).to_dict() if rows else {}
    total = sum(float(v) for v in values.values())
    return {str(k): _safe_divide(float(v), total) for k, v in values.items()}


def _column_shares(sam: pd.DataFrame, rows: list[str], columns: list[str]) -> dict[str, dict[str, float]]:
    if not rows or not columns:
        return {}
    block = sam.loc[rows, columns]
    shares: dict[str, dict[str, float]] = {}
    for column in block.columns:
        total = float(block[column].sum())
        shares[str(column)] = {str(index): _safe_divide(float(value), total) for index, value in block[column].items()}
    return shares


def _safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    if abs(float(denominator)) < 1e-12:
        return float(default)
    value = float(numerator) / float(denominator)
    return value if np.isfinite(value) else float(default)


def _positive(value: float, fallback: float) -> float:
    return float(value) if np.isfinite(value) and value > 1e-9 else float(max(fallback, 1.0))


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, float(value)))


def _assert_finite(payload: dict[str, Any]) -> None:
    def check(value: Any) -> bool:
        if isinstance(value, dict):
            return all(check(v) for v in value.values())
        if isinstance(value, list):
            return all(check(v) for v in value)
        if isinstance(value, (int, float, np.floating)):
            return bool(np.isfinite(float(value)))
        return True

    if not check({k: v for k, v in payload.items() if k != "sam"}):
        raise ValueError("Calibration produced NaN or infinite values.")
