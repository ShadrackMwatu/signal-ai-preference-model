"""Post-run result validation for Signal workbench outputs."""

from __future__ import annotations

from typing import Any


def validate_results(results: dict[str, Any]) -> dict[str, Any]:
    warnings: list[str] = []
    accounts = results.get("accounts", {})
    if not accounts:
        warnings.append("No account-level results were produced.")
    large = [account for account, value in accounts.items() if abs(float(value)) > 1_000_000]
    if large:
        warnings.append(f"Very large multiplier effects detected for: {', '.join(large[:8])}.")
    if results.get("zero_columns"):
        warnings.append("Zero-column accounts were excluded from coefficient effects.")
    if not results.get("households"):
        warnings.append("No household accounts were identified; household welfare effects may be incomplete.")
    if not results.get("factors"):
        warnings.append("No factor accounts were identified; factor income effects may be incomplete.")
    ranking = sorted(accounts.items(), key=lambda item: abs(float(item[1])), reverse=True)
    return {
        "valid": True,
        "warnings": warnings,
        "sector_ranking": ranking[:10],
        "multiplier_size_check": "review" if large else "within_expected_screening_range",
    }
