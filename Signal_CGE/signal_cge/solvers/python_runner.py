"""Open-source Python SAM multiplier fallback for Signal."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from signal_cge.diagnostics.result_validation import validate_results
from signal_cge.diagnostics.sam_balance_checks import validate_sam
from .runner_interface import ModelRunResult, RunnerConfig


DEFAULT_SAM = pd.DataFrame(
    [
        [0, 25, 12, 8, 10, 5],
        [20, 0, 15, 5, 8, 4],
        [14, 18, 0, 6, 10, 7],
        [8, 6, 4, 0, 5, 3],
        [9, 7, 8, 4, 0, 6],
        [6, 5, 7, 3, 6, 0],
    ],
    index=["paid_care_services", "manufacturing", "transport", "health", "households", "government"],
    columns=["paid_care_services", "manufacturing", "transport", "health", "households", "government"],
    dtype=float,
)


class PythonSAMRunner:
    """Run SAM multiplier simulations with transparent matrix algebra."""

    def __init__(self, config: RunnerConfig | None = None) -> None:
        self.config = config or RunnerConfig(model_type="SAM multiplier")

    def run(self, scenario: dict[str, Any]) -> ModelRunResult:
        output_dir = self.config.output_dir
        logs_dir = output_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = logs_dir / f"python_sam_{timestamp}.log"

        sam = load_sam(self.config.sam_path) if self.config.sam_path else DEFAULT_SAM.copy()
        pre = validate_sam(sam)
        endogenous = self.config.endogenous_accounts or list(sam.columns)
        exogenous = self.config.exogenous_accounts or []
        accounts = [account for account in endogenous if account in sam.index and account in sam.columns]

        if not accounts:
            raise ValueError("No valid endogenous accounts were found in the SAM.")

        sub_sam = sam.loc[accounts, accounts].astype(float)
        column_totals = sub_sam.sum(axis=0)
        zero_columns = column_totals[column_totals == 0].index.tolist()
        safe_totals = column_totals.replace(0, np.nan)
        coefficients = sub_sam.divide(safe_totals, axis=1).fillna(0.0)
        identity_minus_a = np.eye(len(accounts)) - coefficients.to_numpy()
        inverse = np.linalg.pinv(identity_minus_a)
        shock_vector = build_shock_vector(accounts, scenario, column_totals)
        result_vector = inverse @ shock_vector
        effects = pd.Series(result_vector, index=accounts, name="effect")

        results = {
            "accounts": effects.round(6).to_dict(),
            "activities": _summarize_group(effects, ["activity", "manufacturing", "transport", "care", "health", "education", "water"]),
            "commodities": _summarize_group(effects, ["commodity", "goods", "services"]),
            "factors": _summarize_group(effects, ["labour", "labor", "capital", "fcp", "fcu", "fnp", "fnu", "mcp", "mcu", "mnp", "mnu"]),
            "households": _summarize_group(effects, ["household", "households"]),
            "shock_vector": pd.Series(shock_vector, index=accounts).round(6).to_dict(),
            "leontief_inverse_shape": list(inverse.shape),
            "exogenous_accounts": exogenous,
            "zero_columns": zero_columns,
        }
        post = validate_results(results)
        diagnostics = {"pre_run": pre, "post_run": post}
        log_path.write_text(_log_text(scenario, diagnostics, results), encoding="utf-8")
        return ModelRunResult(
            success=True,
            backend="python_sam_multiplier",
            scenario=scenario,
            diagnostics=diagnostics,
            results=results,
            logs=["Python SAM multiplier run completed."],
            artifacts={"log": str(log_path)},
            message="Python-based SAM multiplier simulation completed.",
        )


def load_sam(path: str | Path) -> pd.DataFrame:
    source = Path(path)
    if source.suffix.lower() in {".xlsx", ".xls"}:
        frame = pd.read_excel(source, index_col=0)
    else:
        frame = pd.read_csv(source, index_col=0)
    frame.index = [str(item).strip() for item in frame.index]
    frame.columns = [str(item).strip() for item in frame.columns]
    return frame.apply(pd.to_numeric, errors="raise").astype(float)


def build_shock_vector(accounts: list[str], scenario: dict[str, Any], column_totals: pd.Series) -> np.ndarray:
    vector = np.zeros(len(accounts), dtype=float)
    targets = [str(target).lower() for target in scenario.get("target_accounts", [])]
    value = float(scenario.get("shock_value", 0.0))
    unit = str(scenario.get("shock_unit", "percent")).lower()
    if not targets or targets == ["all"]:
        target_indices = list(range(len(accounts)))
    else:
        target_indices = [
            index for index, account in enumerate(accounts)
            if any(target in account.lower() or account.lower() in target for target in targets)
        ]
    if not target_indices:
        target_indices = [0]
    for index in target_indices:
        base = float(column_totals.iloc[index])
        vector[index] = base * value / 100.0 if unit.startswith("percent") else value
    return vector


def _summarize_group(effects: pd.Series, terms: list[str]) -> dict[str, float]:
    selected = effects[[any(term in account.lower() for term in terms) for account in effects.index]]
    return selected.round(6).to_dict()


def _log_text(scenario: dict[str, Any], diagnostics: dict[str, Any], results: dict[str, Any]) -> str:
    return "\n".join(
        [
            "Signal Python SAM Multiplier Run",
            f"Scenario: {scenario}",
            f"Diagnostics: {diagnostics}",
            f"Results: {results}",
        ]
    )
